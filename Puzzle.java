/*
 *  * @(#)Puzzle.java   
 *   *
 *    * Copyright (c) 1996 Aaron Fuegi All Rights Reserved.
 *     *
 *      * Permission to use, copy, modify, and distribute this software
 *       * and its documentation for NON-COMMERCIAL or COMMERCIAL purposes and
 *        * without fee is hereby granted. 
 *
 *         * Acknowledgments:
 *          *    Thanks to Jason Heirtzler, previously of Boston University who wrote 
 *           *      this game as a script long ago.
 *            *    Thanks to Arthur van Hoff whose TicTacToe code formed a rough basis for
 *             *      this code.
 *              */

import java.awt.*;
import java.awt.event.*;
import java.awt.image.*;
import java.io.*;
import java.net.*;
import java.applet.*;

/**
 *  * A 9-piece Puzzle applet. A very simple, and mostly brain-dead
 *   * implementation of this dumb game! <p>
 *
 *    * @author Aaron Fuegi
 *     */
public
class Puzzle extends Applet implements MouseListener {
    Image offscreenImg;
    Graphics offscreenG;
    int curlocs[] = {-1,-1,-1,-1,-1,-1,-1,-1,-1};
    static final int WIN = 1;
    static final int DEBUG = 0;
    static final int height=180;
    static final int width=177;
    int xoff = width / 3;
    int yoff = height / 3;
    int numPieces=9;
    int piecesHigh=3;
    int piecesAcross=3;
    int openloc;
    int ininit=1;
    int firstMove=0;
    int done[];
    int alldone=0;

    /**
     *      * Figure what the status of the game is.
     *           */
    int status() {  
        for (int i=0;i<9;i++)
            if (curlocs[i]!=i) { return -1; }
        return WIN;
    }

    /**
     *      * The image for white.
     *           */
    Image squares[];
    Image victory;
    Image again;
    Image win;

    /**
     *      * Initialize the applet. Resize and load images.
     *           */
    public void init() {
        int i,j;
        int temp = -1;

        offscreenImg = createImage(this.getSize().width,this.getSize().height);
        offscreenG=offscreenImg.getGraphics();

        offscreenG.setColor(getBackground());
        offscreenG.fillRect(0,0,this.getSize().width,this.getSize().height);

        showStatus("Beginning Loading Pieces...");

        done=new int[numPieces];
        for(i=0;i<9;i++) done[i]=0;

        squares = new Image[numPieces];
        for (i=0;i<9;i++) { 
            squares[i] = getImage(getCodeBase(), "images/puzzle/p"+i+".gif");
            showStatus("Loaded piece "+i+"/"+numPieces);
        }

        showStatus("Loading other images for end game");
        victory = getImage(getCodeBase(), "images/puzzle/victory.gif");
        again = getImage(getCodeBase(), "images/puzzle/again.gif");
        if (DEBUG==1) win = getImage(getCodeBase(), "images/puzzle/win.gif");

        setBoard();

        addMouseListener(this);
    }

    public void setBoard() {
        int i,j;
        int movedir;
        int deformValue;

        /* Set board to winning position */
        for (i=0;i<9;i++) {
            curlocs[i]= i;
        }
        openloc=4;

        showStatus("Setting up Board");

        /* Make random number of moves to deform board position */
        deformValue = 150 + (int)Math.floor(Math.random()*100.00);

        for (i=0;i<deformValue;i++) {
            movedir = (int)Math.floor(Math.random()*4);
            while (((openloc<3)&&(movedir==0))||
                    (((openloc%3)==0)&&(movedir==1))||
                    ((openloc>5)&&(movedir==2))||
                    ((((openloc+1)%3)==0)&&(movedir==3)))
                movedir = (int)Math.floor(Math.random()*4);
            deformmove(movedir);
        }

        showStatus("Begin play");   

        firstMove=1;
    }


    public void deformmove(int dir) {
        int swapval = -1;
        int r,c;

        /* Check up,down,left,right */
        if (dir==0) { swapval=openloc-3; }
        if (dir==2) { swapval=openloc+3; }
        if (dir==1) { swapval=openloc-1; }
        if (dir==3) { swapval=openloc+1; }

        /* No need for dummy variable since black is always 4 */
        curlocs[openloc]=curlocs[swapval];
        curlocs[swapval]=4;
        openloc=swapval;
    }

    public void update(Graphics g) {
        paint(g);
    }

    /**
     *      * Paint it.
     *           */

    public void paint(Graphics g) {
        int i = 0;

        if (firstMove==1) {
            if (alldone==1) firstMove=0;
            for (int r = 0 ; r < 3 ; r++) {
                for (int c = 0 ; c < 3 ; c++) {
                    int loc=r*3+c;
                    int whichPiece=curlocs[loc];
                    offscreenG.drawImage(squares[whichPiece], c*xoff + 1, r*yoff + 1, this);
                }
            }
        }

        if (status()==WIN) {
            showStatus("Game Over: Victory");   
            offscreenG.drawImage(victory, 200, 1, this);
            offscreenG.drawImage(again, 300, 119, this);
        }
        else if (DEBUG==1)
            offscreenG.drawImage(win, 300, 119, this);
        else {
            offscreenG.fillRect(200,1,300,160);
        }
        g.drawImage(offscreenImg,0,0,this);
    }

    public boolean imageUpdate(Image img, int flags, int x, int y, int wid, int ht) {
        int i;
        int alldonehere=1;

        if (flags == ALLBITS) {
            for(i=0;i<9;i++) {
                if (img.equals(squares[i])) { 
                    done[i]=1; 
                }
            }

            for(i=0;i<9;i++) {
                if (done[i]!=1) alldonehere=0;
            }
            if (alldonehere==1) {
                alldone=1;
                repaint();
            }
        } 
        return true;
    }

    public int makemove(int row, int col) {
        int loc=row*3+col;
        int r,c,whichPiece;

        int swapval = -1;

        /* Check up,down,left,right */
        if ((row!=0)&&(curlocs[(loc-3)]==4)) { swapval=loc-3; }
        if ((row!=2)&&(curlocs[(loc+3)]==4)) { swapval=loc+3; }
        if ((col!=0)&&(curlocs[(loc-1)]==4)) { swapval=loc-1; }
        if ((col!=2)&&(curlocs[(loc+1)]==4)) { swapval=loc+1; }

        if (swapval != -1) {
            /* No need for dummy variable since black is always 4 */
            curlocs[swapval]=curlocs[loc];
            curlocs[loc]=4;
            r=swapval/3;
            c=swapval % 3;
            whichPiece=curlocs[swapval];
            offscreenG.drawImage(squares[whichPiece], c*xoff + 1, r*yoff + 1, this);
            r=loc/3;
            c=loc % 3;
            whichPiece=4;
            offscreenG.drawImage(squares[whichPiece], c*xoff + 1, r*yoff + 1, this);
            return 1;
        }
        else {
            return swapval;
        }
    }


    /**
     *      * The user has clicked in the applet. Figure out where
     *           * and see if a legal move is possible. If it is a legal
     *                * move, respond with a legal move (if possible).
     *                     */
    /*    public boolean mouseUp(Event evt, int x, int y) { */
    public void mouseReleased(MouseEvent e) {
        int x,y;
        x=e.getX();
        y=e.getY();

        if ((status()==WIN)&&(x>300)&&(x<400)&&(y>119)&&(y<159)) {
            System.out.println("Restart");
            setBoard(); 
            repaint(); 
        }

        // Figure out the row/colum
        int c = (x * 3) / width;
        int r = (y * 3) / height;
        if ((x>300)&&(x<400)&&(y>119)&&(y<159)&&(DEBUG==1)) {
            for(int i=0;i<9;i++)
                curlocs[i]=i;
            firstMove=1;
        }
        else if ((c>=0)&&(c<3)&&(r>=0)&&(r<3)) {
            if (DEBUG==1) System.out.println("Made move");
            makemove(r,c);
        }
        repaint();

        showStatus("Play in progress"); 
    }

    public void mousePressed(MouseEvent e) {
    }

    public void mouseClicked(MouseEvent e) {
    }

    public void mouseEntered(MouseEvent e) {
    }

    public void mouseExited(MouseEvent e) {
    }

    public String getAppletInfo() {
        return "9-Puzzle by Aaron Fuegi";
    }
}
