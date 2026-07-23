package main;

import java.util.ArrayList;

import entity.Enemy;
import entity.Entity;

public class Spawn {

    KeyHandler keyH;
    CursorHandler cursorH;
    ArrayList<Entity> entityList;
    ArrayList<Obstacle> obstacleList;
    int timer = 0;
    int maxSize = 5;


    public Spawn(KeyHandler keyHandle, CursorHandler cursorHandle, ArrayList<Entity> entityListArg, ArrayList<Obstacle> obstacleListArg) {
        keyH = keyHandle;
        cursorH = cursorHandle;
        entityList = entityListArg;
        obstacleList = obstacleListArg;
    }

    public void update() {
        // timer++;
        checkUserInput();

        
    }

    // Check if the user has manually spawned in things
    public void checkUserInput() {
        if(cursorH.isLeftClicked == true) {
            cursorH.isLeftClicked = false;
            Enemy enemy = new Enemy(cursorH.cursorX, cursorH.cursorY);
            entityList.add(enemy);

        } else if (cursorH.isRightClicked == true) {
            Obstacle obstacle = new Obstacle(cursorH.cursorX, cursorH.cursorY);
            obstacleList.add(obstacle);
            cursorH.isRightClicked = false;
        }
    }
}
