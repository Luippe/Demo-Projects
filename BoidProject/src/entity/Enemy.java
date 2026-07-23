package entity;

import java.awt.Color;
import java.awt.geom.Path2D;
import java.util.concurrent.ThreadLocalRandom;

public class Enemy extends Entity{
    
    int sizeBase = 12;
    int sizeHeight = 24;

    // Spawn enemy at mouse location and give random velocity in x and y direction between -1~1.
    public Enemy(int defaultX, int defaultY) {

        setValue(defaultX, defaultY);
        setShape();
        
    }

    // Set default values
    public void setValue(int defaultX, int defaultY) {

        x = defaultX;
        y = defaultY;

        // vx = ThreadLocalRandom.current().nextDouble(-1,1);
        // vy = ThreadLocalRandom.current().nextDouble(-1,1);
        vx = -3;
        vy = -3;

        type = ThreadLocalRandom.current().nextInt(0,2);

        if (type == 0) {
            blueType();
        } else if (type == 1) {
            redType();
        }
    }
    
    // Create triangle
    public void setShape() {

        shape = new Path2D.Double();
        shape.moveTo(sizeHeight /2, 0);
        shape.lineTo(-sizeHeight / 2, sizeBase/ 2);
        shape.lineTo(-sizeHeight / 2, -sizeBase/ 2);
        shape.closePath();

    }

    public void blueType() {
        level = 0;
        protectRange = 10;
        visibleRange = 150;
        avoidFactor = 0.05;  // How repulsive the boids will be towards each other
        matchingFactor = 0.05; // How much the boids will match each other's velocity
        centeringFactor = 0.0001; // How much the boids will move towards the center of mass
        collisionFactor = 1; // How much should boids repel from obstacles
        turnFactor = 1;
        magnetFactor = 300; // How much should boids stick to obstacle. Higher the number, the more it will stick.
        maxSpeed = 6;
        minSpeed = 3;
        color = Color.BLUE;
    }

    public void redType() {
        level = 1;
        protectRange = 20;
        visibleRange = 200;
        avoidFactor = 0.01;  // How repulsive the boids will be towards each other
        matchingFactor = 0.05; // How much the boids will match each other's velocity
        centeringFactor = 0.001; // How much the boids will move towards the center of mass
        collisionFactor = 1; // How much should boids repel from obstacles
        turnFactor = 1;
        magnetFactor = 300; // How much should boids stick to obstacle
        maxSpeed = 4;
        minSpeed = 1;
        color = Color.RED;
    }
}


