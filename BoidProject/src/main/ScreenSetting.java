package main;

import java.awt.BasicStroke;
import java.awt.Color;
import java.awt.Dimension;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.Toolkit;
import java.util.ArrayList;

import javax.swing.JPanel;

import entity.Entity;


public class ScreenSetting extends JPanel implements Runnable {

    private static final long serialVersionUID = 1L;

    // Screen Settings
    Dimension screenSize = Toolkit.getDefaultToolkit().getScreenSize();
    final int screenWidth = (int) screenSize.getWidth();
    final int screenHeight = (int) screenSize.getHeight();
    // The border is drawn on the screen edges; boids start turning away once
    // they come within this many pixels of an edge.
    final int widthMargin = 120;
    final int heightMargin = 120;
    final Color backgroundColor = new Color(0, 171, 240);
    int dxCamera = 0;
    int dyCamera = 0;
    int cameraSpeed = 3;
    volatile boolean bordersEnabled = true;
    KeyHandler keyH = new KeyHandler();
    CursorHandler cursorH = new CursorHandler();
    
    
    ArrayList<Entity> entityList = new ArrayList<>();
    ArrayList<Obstacle> obstacleList = new ArrayList<>();
    Spawn spawn = new Spawn(keyH, cursorH, entityList, obstacleList);
    final Object stateLock = new Object();

    // FPS. Set fps
    int FPS = 60;

    // Create Thread for the screen
    volatile Thread mainThread;

    public ScreenSetting() {
        // this.setPreferredSize(new Dimension(800,800));
        this.setPreferredSize(new Dimension(screenWidth, screenHeight));
        this.setBackground(backgroundColor);
        this.setDoubleBuffered(true);
        this.addKeyListener(keyH);
        this.addMouseListener(cursorH);
        this.setFocusable(true);
    }

    // Call this method to start the thread
    public synchronized void initialize() {
        if (mainThread != null) {
            return;
        }

        mainThread = new Thread(this, "boids-simulation");
        mainThread.start();
    }

    public synchronized void shutdown() {
        Thread runningThread = mainThread;
        mainThread = null;
        if (runningThread != null) {
            runningThread.interrupt();
        }
    }

    @Override
    public void run() {

        Thread runningThread = Thread.currentThread();
        double drawInterval = 1_000_000_000.0 / FPS;
        int timer = 0;
        double nextDrawTime = System.nanoTime() + drawInterval;

        // While this thread exists, continue the while loop
        while (mainThread == runningThread) {
            
            update();
            repaint();

            try {
                double remainingTime = nextDrawTime - System.nanoTime();
                remainingTime = remainingTime/1000000;  // Convert to millisec since sleep only takes millisec

                timer++;
                if (timer > 3) {
                    // System.out.printf("Remaining Time: %.5s\n", remainingTime);
                    // System.out.printf("Memory Usage: %s\n", Runtime.getRuntime().totalMemory() - Runtime.getRuntime().freeMemory());
                    timer = 0;
                }
                
                // Run immediately if the program takes more than 1/60 of a sec to run. Rarely happens
                if (remainingTime < 0) {
                    remainingTime = 0;
                }

                Thread.sleep((long) remainingTime);
                nextDrawTime += drawInterval;

            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                break;
            }
        }

        synchronized (this) {
            if (mainThread == runningThread) {
                mainThread = null;
            }
        }
    }

    // Update stuff
    public void update() {
        synchronized (stateLock) {
            updateState();
        }
    }

    private void updateState() {
        // if(cursorH.isLeftClicked == true) {
        //     cursorH.isLeftClicked = false;
        //     Enemy enemy = new Enemy(cursorH.cursorX, cursorH.cursorY);
        //     entityList.add(enemy);

        // } else if (cursorH.isRightClicked == true) {
        //     Obstacle obstacle = new Obstacle(cursorH.cursorX, cursorH.cursorY);
        //     obstacleList.add(obstacle);
        //     cursorH.isRightClicked = false;
        // }
        
        
        spawn.update();
        updateKeys();

        if (dxCamera != 0 || dyCamera != 0) {
            for (Entity entity : entityList) {
                entity.x += dxCamera;
                entity.y += dyCamera;
            }
            for (Obstacle obstacle : obstacleList) {
                obstacle.moveObstacle(dxCamera, dyCamera);
            }
        }

        for(Entity boid: entityList) {

            double closedx = 0;
            double closedy = 0;
            double xvelAvg = 0;
            double yvelAvg = 0;
            double xposAvg = 0;
            double yposAvg = 0;
            double neighboringBoids = 0;

            for(Entity otherBoid: entityList) {
                if (boid != otherBoid && boid.type == otherBoid.type) {

                    double distance = Math.hypot(boid.x-otherBoid.x, boid.y-otherBoid.y);
                    if (distance <= boid.protectRange) {  // What boids are in the protectRange

                        closedx += boid.x - otherBoid.x;
                        closedy += boid.y - otherBoid.y;

                    }
                    else if (distance <= boid.visibleRange) {    // What boids are in the visibleRange? Get their average velocity and position

                        xvelAvg += otherBoid.vx;
                        yvelAvg += otherBoid.vy;
                        xposAvg += otherBoid.x;
                        yposAvg += otherBoid.y;

                        neighboringBoids += 1;
                    }
                }
            }
            if (neighboringBoids > 0) {  // Move boid towards center of mass of other boids

                xvelAvg = xvelAvg/neighboringBoids;
                yvelAvg = yvelAvg/neighboringBoids;
                xposAvg = xposAvg/neighboringBoids;
                yposAvg = yposAvg/neighboringBoids;
                boid.vx += (xvelAvg - boid.vx)*boid.matchingFactor;
                boid.vy += (yvelAvg - boid.vy)*boid.matchingFactor;
                boid.vx += (xposAvg - boid.x)*boid.centeringFactor;
                boid.vy += (yposAvg - boid.y)*boid.centeringFactor;

            }

            boid.vx = boid.vx + closedx*boid.avoidFactor;
            boid.vy = boid.vy + closedy*boid.avoidFactor;
            
            updateCollision(boid);
            updateBorders(boid);

            // Put speed limit on how fast boids can travel
            double speed = Math.hypot(boid.vx, boid.vy);
            if (!Double.isFinite(speed) || speed == 0) {
                boid.vx = boid.minSpeed;
                boid.vy = 0;
            }
            else if (speed > boid.maxSpeed) {

                boid.vx = (boid.vx/speed)*boid.maxSpeed;
                boid.vy = (boid.vy/speed)*boid.maxSpeed;

            }

            else if (speed < boid.minSpeed) {

                boid.vx = (boid.vx/speed)*boid.minSpeed;
                boid.vy = (boid.vy/speed)*boid.minSpeed;

            }

            boid.x = boid.x + (int) Math.round(boid.vx);
            boid.y = boid.y + (int) Math.round(boid.vy);
        }
    }

    // Update collision for each boid
    public void updateCollision(Entity boid) {
        for (Obstacle obstacle: obstacleList) {
            int xVec = boid.x - obstacle.xCenter;
            int yVec = boid.y - obstacle.yCenter;
            double dist = Math.hypot(xVec, yVec);
            // System.out.println(xVec*boid.vx + yVec*boid.vy);
            if (dist < obstacle.outerRadius && xVec*boid.vx + yVec*boid.vy < boid.magnetFactor) { // Is the boid inside the bounding radius and moving towards the obstacle?
                if (dist == 0) {
                    boid.vx += boid.collisionFactor;
                    continue;
                }

                // Get direction in which the boid is moving
                double xRecip = yVec/dist;
                double yRecip = -xVec/dist;
                double distanceFromEdge = dist - obstacle.maxPointRadius;
                if (Math.abs(distanceFromEdge) < 1.0) {
                    distanceFromEdge = Math.copySign(1.0, distanceFromEdge == 0 ? 1.0 : distanceFromEdge);
                }
                double inverseDist = (obstacle.outerRadius - dist)/distanceFromEdge;
                if (xRecip*boid.vx + yRecip*boid.vy > 0) { // If dot product is positive, move boid in that direction.
                    boid.vx = boid.vx + xRecip*inverseDist*boid.collisionFactor;
                    boid.vy = boid.vy + yRecip*inverseDist*boid.collisionFactor;
                } else {
                    boid.vx = boid.vx - xRecip*inverseDist*boid.collisionFactor;
                    boid.vy = boid.vy - yRecip*inverseDist*boid.collisionFactor;
                }
            }
        }
    }

    // Steer boids away from the screen edges. The border sits on the edges, and
    // boids curve away gradually as they enter the margin band next to it: the
    // nudge grows the closer a boid gets, so the turn is smooth rather than a
    // sudden bounce.
    public void updateBorders(Entity boid) {
        if (!bordersEnabled) {
            return;
        }

        int panelWidth = getWidth() > 0 ? getWidth() : screenWidth;
        int panelHeight = getHeight() > 0 ? getHeight() : screenHeight;
        int rightEdge = panelWidth - 1;
        int bottomEdge = panelHeight - 1;

        // Never let the turn band be wider than half the panel on small windows.
        int marginX = Math.min(widthMargin, Math.max(1, panelWidth / 2));
        int marginY = Math.min(heightMargin, Math.max(1, panelHeight / 2));

        if (boid.x < marginX) {
            double strength = (double) (marginX - boid.x) / marginX;
            boid.vx += boid.turnFactor * strength;
        }
        else if (boid.x > rightEdge - marginX) {
            double strength = (double) (boid.x - (rightEdge - marginX)) / marginX;
            boid.vx -= boid.turnFactor * strength;
        }

        if (boid.y < marginY) {
            double strength = (double) (marginY - boid.y) / marginY;
            boid.vy += boid.turnFactor * strength;
        }
        else if (boid.y > bottomEdge - marginY) {
            double strength = (double) (boid.y - (bottomEdge - marginY)) / marginY;
            boid.vy -= boid.turnFactor * strength;
        }

        // Safety net: if a boid still reaches an edge, stop it from crossing
        // instead of letting it leave the visible area.
        if (boid.x < 0) {
            boid.x = 0;
            if (boid.vx < 0) {
                boid.vx = 0;
            }
        }
        else if (boid.x > rightEdge) {
            boid.x = rightEdge;
            if (boid.vx > 0) {
                boid.vx = 0;
            }
        }

        if (boid.y < 0) {
            boid.y = 0;
            if (boid.vy < 0) {
                boid.vy = 0;
            }
        }
        else if (boid.y > bottomEdge) {
            boid.y = bottomEdge;
            if (boid.vy > 0) {
                boid.vy = 0;
            }
        }
    }


    // Update key strokes
    public void updateKeys() {
        if (keyH.consumeBorderToggleRequest()) {
            bordersEnabled = !bordersEnabled;
        }

        dxCamera = 0;
        dyCamera = 0;
        if (keyH.leftPressed == true) {
            dxCamera = cameraSpeed;
        }
        if (keyH.rightPressed == true) {
            dxCamera = -cameraSpeed;
        }
        if (keyH.upPressed == true) {
            dyCamera = cameraSpeed;
        }
        if (keyH.downPressed == true) {
            dyCamera = -cameraSpeed;
        }
    }

    // Draw the updated stuff onto screen. Use Java's Graphics class into this method
    @Override
    public void paintComponent(Graphics g) {

        super.paintComponent(g);

        Graphics2D g2 = (Graphics2D) g.create();
        try {
            synchronized (stateLock) {
                // Draw all entities
                for(Entity entity: entityList) {
                    entity.draw(g2);
                }
                for(Obstacle obstacle: obstacleList) {
                    obstacle.draw(g2);
                    // obstacle.drawBoundingLines(g2);
                }

                if (bordersEnabled) {
                    // Draw the border on the screen edges (inset by 1px so the
                    // 2px stroke stays fully visible).
                    int borderWidth = Math.max(0, getWidth() - 3);
                    int borderHeight = Math.max(0, getHeight() - 3);
                    g2.setColor(new Color(255, 255, 255, 180));
                    g2.setStroke(new BasicStroke(2f));
                    g2.drawRect(1, 1, borderWidth, borderHeight);
                }
            }
        } finally {
            g2.dispose();
        }
    }
}
