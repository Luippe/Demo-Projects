# Netgame

<p align="center">
  <a href="https://github.com/Luippe/Demo-Projects/releases/latest/download/Netgame.exe"><img src="https://img.shields.io/badge/DOWNLOAD%20FOR%20WINDOWS-.EXE-0078D4?style=for-the-badge&logo=windows&logoColor=white" height="68" alt="Download Netgame for Windows (.exe)"></a>
</p>

<p align="center">
<em>Prefer the code? <a href="https://download-directory.github.io/?url=https://github.com/Luippe/Demo-Projects/tree/main/netgame">Download the source folder</a>.</em></p>

A cooperative multiplayer dungeon prototype built with **Python** and **pygame**.
Host or join a game over a local network, explore procedurally generated rooms,
collect and equip items, and fight enemies together.

## Controls

| Input | Action |
|-------|--------|
| `W` / `A` / `S` / `D` | Move |
| `F` | Interact, pick up an item, or ready up at an entrance |
| `E` | Open or close the inventory |
| `P` | Open or close settings |
| Left `Ctrl` | Change facing direction without moving |
| Left `Shift` | Toggle attack-area highlighting |
| Right-click | Open the action menu |
| Left-click | Select menus, items, and actions |
| `Esc` | Quit |

Controls can be rebound from the in-game **Settings → Control** tab.

## Playing together

The simplest way to connect players who aren't on the same network is
[LogMeIn Hamachi](https://vpn.net/) — everyone joins the same Hamachi network,
then:

1. The host selects **Host Game** and enters their Hamachi IPv4 address.
2. Everyone else selects **Join Game** and enters that same address.
3. If Windows Firewall asks, allow `Netgame.exe` on private networks.

Netgame uses TCP port `5555`. Keep it on a trusted private network — the game
protocol isn't designed for exposure to the public internet.

## Run from source

Needs **Python 3.9+**. From inside the `netgame` folder:

```bash
pip install -r requirements.txt
python run.py
```

## Build the Windows executable

```bash
pip install -r requirements.txt
pip install pyinstaller
python -m PyInstaller --noconfirm --clean Netgame.spec
```

The self-contained executable lands at `dist/Netgame.exe`.
