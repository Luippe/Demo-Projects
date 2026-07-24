package main;

import java.awt.Graphics2D;
import java.awt.event.KeyEvent;
import java.awt.image.BufferedImage;
import java.util.concurrent.atomic.AtomicReference;

import javax.swing.SwingUtilities;

import entity.Enemy;
import entity.Entity;

public final class BoidsSmokeTest {

    private BoidsSmokeTest() {
    }

    public static void main(String[] args) throws Exception {
        AtomicReference<Throwable> failure = new AtomicReference<>();

        SwingUtilities.invokeAndWait(() -> {
            try {
                exerciseSimulation();
            } catch (Throwable error) {
                failure.set(error);
            }
        });

        if (failure.get() != null) {
            throw new AssertionError("Boids smoke test failed", failure.get());
        }

        System.out.println("BOIDS_LOGIC_TEST_OK");
    }

    private static void exerciseSimulation() {
        ScreenSetting screen = new ScreenSetting();
        screen.setSize(800, 600);

        require(screen.bordersEnabled, "Borders should be enabled by default");
        pressSpace(screen);
        require(!screen.bordersEnabled, "Space did not disable borders");

        Enemy unboundedBoid = new Enemy(0, 300);
        unboundedBoid.vx = -3;
        unboundedBoid.vy = 0;
        screen.entityList.add(unboundedBoid);
        screen.update();
        require(unboundedBoid.x < screen.widthMargin && unboundedBoid.vx < 0,
            "Disabled borders still constrained a boid");

        screen.entityList.clear();
        pressSpace(screen);
        require(screen.bordersEnabled, "Space did not re-enable borders");

        // Borders now steer boids away from the screen edges smoothly. A boid
        // heading into the left edge should be nudged back gradually over
        // several frames -- not have its velocity flipped in a single step --
        // and it must never cross the edge out of the visible area.
        Enemy boundedBoid = new Enemy(30, 300);
        boundedBoid.vx = -3;
        boundedBoid.vy = 0;
        boundedBoid.minSpeed = 1;
        boundedBoid.maxSpeed = 6;
        boundedBoid.turnFactor = 1;
        screen.entityList.add(boundedBoid);

        double velocityBeforeTurn = boundedBoid.vx;
        screen.update();
        require(boundedBoid.vx > velocityBeforeTurn,
            "Enabled borders did not start steering the boid away from the edge");
        require(boundedBoid.vx <= 0,
            "Border turn was sudden instead of gradual");

        boolean turnedBack = false;
        for (int frame = 0; frame < 400; frame++) {
            screen.update();
            require(boundedBoid.x >= 0, "A boid escaped past the left screen edge");
            if (boundedBoid.vx > 0) {
                turnedBack = true;
                break;
            }
        }
        require(turnedBack, "Enabled borders never turned the boid back inward");

        screen.entityList.clear();
        screen.cursorH.cursorX = 200;
        screen.cursorH.cursorY = 200;
        screen.cursorH.isLeftClicked = true;
        screen.update();
        require(screen.entityList.size() == 1, "Left-click did not create a boid");

        screen.entityList.clear();
        screen.cursorH.cursorX = 400;
        screen.cursorH.cursorY = 300;
        screen.cursorH.isRightClicked = true;
        screen.update();
        require(screen.obstacleList.size() == 1, "Right-click did not create an obstacle");

        Obstacle centerObstacle = screen.obstacleList.get(0);
        Enemy centeredBoid = new Enemy(centerObstacle.xCenter, centerObstacle.yCenter);
        centeredBoid.vx = 0;
        centeredBoid.vy = 0;
        screen.entityList.add(centeredBoid);

        for (int row = 0; row < 5; row++) {
            for (int column = 0; column < 10; column++) {
                screen.entityList.add(new Enemy(80 + column * 45, 80 + row * 45));
            }
        }

        int oldObstacleX = centerObstacle.xCenter;
        screen.keyH.rightPressed = true;
        screen.update();
        screen.keyH.rightPressed = false;
        require(centerObstacle.xCenter == oldObstacleX - screen.cameraSpeed,
            "Keyboard camera movement did not update the world");

        for (int frame = 0; frame < 500; frame++) {
            screen.update();
        }

        for (Entity entity : screen.entityList) {
            require(Double.isFinite(entity.vx) && Double.isFinite(entity.vy),
                "Simulation produced a non-finite velocity");
            require(Math.hypot(entity.vx, entity.vy) <= entity.maxSpeed + 0.0001,
                "Simulation exceeded a boid's speed limit");
        }

        BufferedImage image = new BufferedImage(800, 600, BufferedImage.TYPE_INT_ARGB);
        Graphics2D graphics = image.createGraphics();
        try {
            screen.paint(graphics);
        } finally {
            graphics.dispose();
        }
    }

    private static void pressSpace(ScreenSetting screen) {
        long now = System.currentTimeMillis();
        KeyEvent pressed = new KeyEvent(
            screen,
            KeyEvent.KEY_PRESSED,
            now,
            0,
            KeyEvent.VK_SPACE,
            ' '
        );
        KeyEvent released = new KeyEvent(
            screen,
            KeyEvent.KEY_RELEASED,
            now,
            0,
            KeyEvent.VK_SPACE,
            ' '
        );

        screen.keyH.keyPressed(pressed);
        screen.keyH.keyPressed(pressed);
        screen.update();
        screen.keyH.keyReleased(released);
    }

    private static void require(boolean condition, String message) {
        if (!condition) {
            throw new IllegalStateException(message);
        }
    }
}
