package main;

import java.awt.Graphics2D;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Random;
import java.util.concurrent.ThreadLocalRandom;

// Class to generate and draw procedurally generated polygons
public class Voronoi {

    int xPoints = 10;
    int yPoints = 10;

    int xPoly = 500;
    int yPoly = 500;
    int maxLength = 500;
    int minLength = 100;

    int numGenerate = 5;

    int[] xFinalPos = new int[numGenerate];
    int[] yFinalPos = new int[numGenerate];

    public void generate(int screenWidth, int screenHeight) {

        ArrayList<Integer> xAllVec = new ArrayList<Integer>();
        ArrayList<Integer> yAllVec = new ArrayList<Integer>();
        ArrayList<Integer> xFinalVec = new ArrayList<Integer>();
        ArrayList<Integer> yFinalVec = new ArrayList<Integer>();
        ArrayList<Integer> xAllCoord = new ArrayList<Integer>();
        ArrayList<Integer> yAllCoord = new ArrayList<Integer>();
        ArrayList<Integer> xCoordPos = new ArrayList<Integer>();
        ArrayList<Integer> yCoordPos = new ArrayList<Integer>();
        ArrayList<Integer> xCoordNeg = new ArrayList<Integer>();
        ArrayList<Integer> yCoordNeg = new ArrayList<Integer>();

        int cellWidth = Math.round(screenWidth/xPoints);
        int cellHeight = Math.round(screenHeight/yPoints);

        // Get random coordinates
        while (xAllCoord.size() < numGenerate) {

            int xLocation = ThreadLocalRandom.current().nextInt(minLength, maxLength);
            int yLocation = ThreadLocalRandom.current().nextInt(minLength, maxLength);

            if (xAllCoord.contains(xLocation) == false && yAllCoord.contains(yLocation) == false) {
                xAllCoord.add(xLocation);
                yAllCoord.add(yLocation);
            }
        }

        Collections.sort(xAllCoord);
        Collections.sort(yAllCoord);

        Random random = new Random();

        // Split x and y coordinates into two. So 4 arraylist in total.
        for (int i = 0; i < xAllCoord.size(); i++) {
            
            int xCoord = xAllCoord.get(i);
            int yCoord = yAllCoord.get(i);

            if (i == 0 || i == numGenerate-1) {
                xCoordPos.add(xCoord);
                yCoordPos.add(yCoord);
                xCoordNeg.add(xCoord);
                yCoordNeg.add(yCoord);
            } else if (random.nextBoolean() == true) {
                xCoordPos.add(xCoord);
                yCoordPos.add(yCoord);
            } else {
                xCoordNeg.add(xCoord);
                yCoordNeg.add(yCoord);
            }
        }

        // Find vector components and combine all the x and y vectors
        xAllVec.addAll(getVector(xCoordPos, true));
        xAllVec.addAll(getVector(xCoordNeg, false));
        yAllVec.addAll(getVector(yCoordPos, true));
        yAllVec.addAll(getVector(yCoordNeg, false));

        // Sort vectors by the angle from the positive x axis
        // Create arraylist first and initialize
        ArrayList<Double> allAngle = new ArrayList<Double>();

        allAngle.add(0,0.0);
        System.out.println("check1");
        // Sort the vectors
        for (int i = 0; i < numGenerate; i++) {

            int xVec = xAllVec.get(i);
            int yVec = yAllVec.get(i);

            double angle = Math.acos(xVec / Math.hypot(xVec, yVec));

            if (Collections.max(allAngle) < angle) {
                xFinalVec.add(xVec);
                yFinalVec.add(yVec);
            } else {
                xFinalVec.add(0,xVec);
                yFinalVec.add(0,yVec);
            }
            allAngle.add(angle);

        }

        // Get the position of the polygon
        for (int i = 0; i < numGenerate; i++) {
            if (i == 0) {
                xFinalPos[i] = xFinalVec.get(i) + xPoly;
                yFinalPos[i] = yFinalVec.get(i) + yPoly;
            } else {
                xFinalPos[i] = xFinalPos[i-1] + xFinalVec.get(i);
                yFinalPos[i] = yFinalPos[i-1] + yFinalVec.get(i);
            }

        }

    }

    public static ArrayList <Integer> getVector(ArrayList<Integer> coord, boolean isPositive) {

        ArrayList<Integer> result = new ArrayList<Integer>();

        for (int i = 1;  i < coord.size(); i++) {

            int vec = (coord.get(i) - coord.get(i-1));

            if (isPositive == false) {
                result.add(-vec);
            } else {
                result.add(vec);
            }
        }
        return result;
    }

    // Draw the polygon
    public void draw(Graphics2D g2) {
        
        g2.drawPolygon(xFinalPos, yFinalPos, numGenerate);
        
    }
}
