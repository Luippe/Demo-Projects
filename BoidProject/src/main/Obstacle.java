package main;

import java.awt.Color;
import java.awt.Graphics2D;
import java.awt.Polygon;
import java.util.Arrays;
import java.util.concurrent.ThreadLocalRandom;

public class Obstacle {

    int numPoints = 4;
    int xMargin = 50;
    int yMargin = 50;
    int xCenter, yCenter;
    int halfBoxWidth = 50;
    int halfBoxHeight = 50;
    int radiusMargin = 100;
    int innerMargin = 0;
    double outerRadius;  // Outer circle radius where boids will try to avoid the obstacle
    double maxPointRadius;  // Circle radius where boids cannot get any closer
    int x,y;
    
    int[] xPoints = new int[numPoints];
    int[] yPoints = new int[numPoints];
    int[] xBounding = new int[numPoints];
    int[] yBounding = new int[numPoints];
    int[] xQuad = {1, -1, -1, 1};
    int[] yQuad = {1, 1, -1, -1};

    public Obstacle(int defaultX, int defaultY) {

        x = defaultX;
        y = defaultY;
        generate(defaultX, defaultY);
        getRadius();
        
    }

    // Generate a polygon with numPoints verticies
    public void generate(int defaultX, int defaultY) {

        // Generate a point at each quadrant which will be the vertex of the polygon
        for (int i = 0; i < numPoints; i++) {

            int xRandom = ThreadLocalRandom.current().nextInt(-halfBoxWidth, halfBoxWidth);
            int yRandom = ThreadLocalRandom.current().nextInt(-halfBoxHeight, halfBoxHeight);

            xPoints[i] = defaultX + xRandom + (xMargin + halfBoxWidth)*xQuad[i];
            yPoints[i] = defaultY + yRandom + (yMargin + halfBoxHeight)*yQuad[i];

            xCenter += xPoints[i];
            yCenter += yPoints[i];
        }

        // Calculate centroid of polygon
        xCenter = xCenter/numPoints;
        yCenter = yCenter/numPoints;
    }

    public void getRadius() {
        for (int i = 0; i < numPoints; i++) {
            double radius = Math.hypot(xCenter-xPoints[i], yCenter-yPoints[i]);
            // double radius = Math.hypot(x-xPoints[i], y-yPoints[i]);
            if (radius > maxPointRadius) {

                maxPointRadius = radius;
            }
        }
        maxPointRadius = maxPointRadius + innerMargin;
        outerRadius = maxPointRadius + radiusMargin;
    }

    // Draw bounding boxes and circles for debug purposes
    public void drawBoundingLines(Graphics2D g2) {

        g2.setColor(Color.red);
        g2.drawOval((int) (xCenter-maxPointRadius),(int) (yCenter-maxPointRadius), (int) (2*maxPointRadius), (int) (2*maxPointRadius));
        g2.drawOval((int) (xCenter-maxPointRadius-radiusMargin), (int) (yCenter-maxPointRadius-radiusMargin), (int) (2*(maxPointRadius + radiusMargin)), (int) (2*(maxPointRadius + radiusMargin)));
        // g2.fillRect(xCenter, yCenter, 3,3);
        // g2.setColor(Color.blue);
        // g2.fillRect(x,y, 3,3);
        g2.setColor(Color.LIGHT_GRAY);
        
    }

    // Draw the polygon
    public void draw(Graphics2D g2) {
        
        g2.setColor(Color.LIGHT_GRAY);
        g2.fillPolygon(xPoints, yPoints, numPoints);
    }

    // Move the obstacle by dx and dy
    public void moveObstacle(int dx, int dy) {
        xCenter += dx;
        yCenter += dy;
        for(int i = 0; i < numPoints; i++) {
            xPoints[i] += dx;
            yPoints[i] += dy;
        }
    }
}
