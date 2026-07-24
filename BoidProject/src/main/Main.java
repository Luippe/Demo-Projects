package main;

import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;

import javax.swing.JFrame;
import javax.swing.SwingUtilities;
import javax.swing.Timer;

public class Main {
    public static JFrame window;

    public static void main(String[] args) {
        boolean smokeTest = args.length > 0 && "--smoke-test".equals(args[0]);
        String smokeTestMarker = args.length > 1 ? args[1] : null;
        SwingUtilities.invokeLater(() -> createWindow(smokeTest, smokeTestMarker));
    }

    private static void createWindow(boolean smokeTest, String smokeTestMarker) {
        window = new JFrame();
        window.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        window.setTitle("Boids");

        ScreenSetting screenSetting = new ScreenSetting();
        window.addWindowListener(new WindowAdapter() {
            @Override
            public void windowClosing(WindowEvent event) {
                screenSetting.shutdown();
            }
        });
        window.add(screenSetting);
        window.pack();
        window.setExtendedState(JFrame.MAXIMIZED_BOTH);
        window.setLocationRelativeTo(null);
        window.setVisible(true);

        screenSetting.requestFocusInWindow();
        screenSetting.initialize();

        if (smokeTest) {
            Timer smokeTestTimer = new Timer(1_500, event -> {
                boolean passed = window.isShowing()
                    && screenSetting.isShowing()
                    && screenSetting.mainThread != null;

                if (passed && smokeTestMarker != null) {
                    try {
                        Files.writeString(Path.of(smokeTestMarker), "BOIDS_SMOKE_TEST_OK");
                    } catch (IOException error) {
                        error.printStackTrace();
                        passed = false;
                    }
                }

                screenSetting.shutdown();
                window.dispose();
                System.out.println(passed ? "BOIDS_SMOKE_TEST_OK" : "BOIDS_SMOKE_TEST_FAILED");
                System.exit(passed ? 0 : 1);
            });
            smokeTestTimer.setRepeats(false);
            smokeTestTimer.start();
        }
    }
}
