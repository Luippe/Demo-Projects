import asyncio
import multiprocessing
import os
import subprocess
import sys

from menu import run_menu, show_error


GAME_PORT = 5555


def run_server_mode(ipv, port):
    from server import ServerNetwork

    network = ServerNetwork(ipv=ipv, port=port)
    asyncio.run(network.main())


def start_server_process(ipv, port):
    if getattr(sys, "frozen", False):
        command = [sys.executable, "--server", "--ip", ipv, "--port", str(port)]
    else:
        command = [
            sys.executable,
            os.path.abspath(__file__),
            "--server",
            "--ip",
            ipv,
            "--port",
            str(port),
        ]

    creation_flags = 0
    if os.name == "nt" and getattr(sys, "frozen", False):
        creation_flags = subprocess.CREATE_NO_WINDOW

    return subprocess.Popen(command, creationflags=creation_flags)


def stop_server_process(server_process):
    if server_process is None:
        return

    descendants = []
    try:
        import psutil
    except ImportError:
        psutil = None

    stopped_with_psutil = False
    if psutil is not None:
        try:
            parent = psutil.Process(server_process.pid)
            descendants = parent.children(recursive=True)
            for process in reversed(descendants):
                process.terminate()
            parent.terminate()
            _, remaining = psutil.wait_procs(descendants + [parent], timeout=3)
            for process in remaining:
                process.kill()
            stopped_with_psutil = True
        except psutil.Error:
            pass

    if not stopped_with_psutil:
        if server_process.poll() is None:
            server_process.terminate()

    try:
        server_process.wait(timeout=3)
    except subprocess.TimeoutExpired:
        server_process.kill()
        server_process.wait(timeout=3)


def argument_value(name, default):
    try:
        return sys.argv[sys.argv.index(name) + 1]
    except (ValueError, IndexError):
        return default


def main():
    multiprocessing.freeze_support()

    if "--server" in sys.argv:
        ipv = argument_value("--ip", "0.0.0.0")
        port = int(argument_value("--port", str(GAME_PORT)))
        run_server_mode(ipv, port)
        return

    choice, ipv = run_menu()
    if choice == "quit":
        return

    server_process = None
    try:
        if choice == "host":
            server_process = start_server_process(ipv, GAME_PORT)

        from network import Network

        attempts = 100 if choice == "host" else 5
        network = Network(
            ipv=ipv,
            port=GAME_PORT,
            connect_attempts=attempts,
            retry_delay=0.2,
        )
        asyncio.run(network.main())
    except Exception as error:
        show_error(str(error))
    finally:
        stop_server_process(server_process)


if __name__ == "__main__":
    main()
