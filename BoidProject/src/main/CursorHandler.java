package main;

import java.awt.event.MouseEvent;
import java.awt.event.MouseListener;

public class CursorHandler implements MouseListener{

    public boolean isRightClicked, isLeftClicked;
    public int cursorX, cursorY;

    
    @Override
    public void mouseClicked(MouseEvent e) {
        if(e.getButton() == MouseEvent.BUTTON1){
            cursorX = e.getX();
            cursorY = e.getY();
            isLeftClicked = true;
        }
        else if (e.getButton() == MouseEvent.BUTTON3) {
            cursorX = e.getX();
            cursorY = e.getY();
            isRightClicked = true;
        }
    }

    @Override
    public void mousePressed(MouseEvent e) {
    }

    @Override
    public void mouseReleased(MouseEvent e) {
    }

    @Override
    public void mouseEntered(MouseEvent e) {
    }

    @Override
    public void mouseExited(MouseEvent e) {
    }
}