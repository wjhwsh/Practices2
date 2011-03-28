#ifndef _CTRIS_H
#define _CTRIS_H

#include <stdio.h>
#include <math.h>
#include <string.h>
#include <unistd.h>
#include <ncurses.h>
#include <stdlib.h>
#include <stdarg.h>
#include <fcntl.h>
#include <signal.h>
#include <limits.h>
#include <time.h>

#define HEIGHT 24 /* height of the screen */
#define WIDTH 80 /* width of the screen */
#define BOARD_HEIGHT (HEIGHT - 5) /* height of the board */
#define BOARD_WIDTH 15 /* width of the board */
#define YES 0
#define NO 1
#define REMOVE_SPLASH_TIME 500000 /* in microseconds */

/* with this variables you can change the average constancy of a game */
#define SPEED_CONST_1 500
#define SPEED_CONST_2 15000
#define BONUS_CONST 100
#define LEVEL_CONST 300

char quit;
unsigned long rseed;

#endif
