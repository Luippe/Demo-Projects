package entity;

import java.awt.Color;
import java.awt.Graphics2D;

import main.KeyHandler;
import main.ScreenSetting;

public class Player extends Entity{

    ScreenSetting ss;
    KeyHandler keyH;

    public Player(ScreenSetting ss, KeyHandler keyH) {

        this.ss = ss;
        this.keyH = keyH;

        setDefaultValues();
    }

    public void setDefaultValues() {

        x = 100;
        y = 100;
        vx = 0;
        vy = 0;
    }

    public void update() {

        // if(keyH.upPressed == true) {
        //     y -= speed;
        // }
        // else if(keyH.downPressed == true) {
        //     y += speed;
        // }
        // else if(keyH.leftPressed == true) {
        //     x -= speed;
        // }
        // else if(keyH.rightPressed == true) {
        //     x += speed;
        // }

    }

    public void draw(Graphics2D g2) {

        g2.setColor(Color.white);
        g2.fillRect(x,y,100,100);

    }
}
