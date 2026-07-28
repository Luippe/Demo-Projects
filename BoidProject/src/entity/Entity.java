package entity;

import java.awt.Color;

import java.awt.Graphics2D;
import java.awt.geom.AffineTransform;
import java.awt.geom.Path2D;


public class Entity {
    
    public int x, y;
    public double vx, vy;
    public Path2D shape;
    public int type;
    public int level;

    public int protectRange;
    public int visibleRange;

    public double avoidFactor;  // How repulsive the boids will be towards each other
    public double matchingFactor; // How much the boids will match each other's velocity
    public double centeringFactor; // How much the boids will move towards the center of mass
    public double collisionFactor; // How much should boids repel from obstacles
    public double turnFactor;
    public int magnetFactor; // How much should boids stick to obstacle

    public int maxSpeed;
    public int minSpeed;

    public Color color;


    public void draw(Graphics2D g2) {
        // Get the current canvas and save it
        // transform the canvas, then draw the boid, then transform the canvas back to its original
        AffineTransform save = g2.getTransform();

        g2.setColor(color);
        g2.translate(x,y);
        g2.rotate(Math.atan2(vy,vx));
        g2.fill(shape);
        g2.draw(shape);
        g2.setTransform(save);
        g2.setColor(Color.BLACK);

    }

}
