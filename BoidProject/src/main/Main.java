package main;

import javax.swing.JFrame;

public class Main {
    public static JFrame window;
    public static void main(String[] args) throws Exception {
        window = new JFrame();
        window.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        window.setTitle("Boids");
        ScreenSetting screenSetting = new ScreenSetting();
        window.add(screenSetting);
        window.pack();
        window.setVisible(true);
        window.setExtendedState(JFrame.MAXIMIZED_BOTH);
        screenSetting.initialize();

    }
}
