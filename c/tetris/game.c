#include "tetris.h"

#include "game.h"
#include "brick.h"
#include "screen.h"

void init_board(char board[BOARD_HEIGHT][BOARD_WIDTH])
{
	unsigned char i, n;
	for (i = 0; i < BOARD_HEIGHT; i++) {
		for (n = 0; n < BOARD_WIDTH; n++) {
			board[i][n] = 0;
		}
	}
}

static unsigned char get_rand(const unsigned char i)
{
	rseed = rseed * 1103515245 + 12345;                                         
	return (unsigned char)((rseed / 65536) % 32768) % i;
}

static void remove_this_row(WINDOW *win, char board[BOARD_HEIGHT][BOARD_WIDTH], unsigned char y)
{
	unsigned char x;
	show_remove_row(win, board, y);
	for (; y > 0; y--) {
		for (x = 0; x < BOARD_WIDTH; x++) {
			board[y][x] = board[y - 1][x];
		}
	}
}

static void remove_rows(WINDOW *win, char board[BOARD_HEIGHT][BOARD_WIDTH], unsigned int *score, const char level)
{
	char removed_rows = 0;
	unsigned char x, y;
	unsigned int sub_score = 0;
	for (y = 0; y < BOARD_HEIGHT; y++) {
		for (x = 0; x < BOARD_WIDTH; x++) {
			if (board[y][x] == 0) {
				break;
			}
		}
		if (x >= BOARD_WIDTH) {
			remove_this_row(win, board, y);
			removed_rows++;
			sub_score += BONUS_CONST * level * removed_rows;
		}
	}
	*score += sub_score;
	if (removed_rows > 0) {
		refresh_win(win);
		usleep(REMOVE_SPLASH_TIME);
	}
}

static void calc_level(const unsigned int score, char *level)
{
	while (SPEED_CONST_2 - (*level + 1) * SPEED_CONST_1 >= 0 && score / (LEVEL_CONST * (unsigned int)pow((double)*level, 2)) > 0) {
		*level += 1;
	}
}

unsigned int start_game()
{
	char brick_type, next_brick_type, cur_brick[4][4], board[BOARD_HEIGHT][BOARD_WIDTH], run, level = 1;
	unsigned int score = 0;
	unsigned char x, y;
	WINDOW *board_win, *preview_win, *score_win;
	board_win = (WINDOW *)create_board_win();
	preview_win = (WINDOW *)create_preview_win();
	score_win = (WINDOW *)create_score_win();
	init_board(board);
	show_score(score_win, score, level);
	next_brick_type = get_rand(7) + 1;
	quit = 2;
	wait_for_start(board_win);
	quit = 0;
	while (quit == 0) {
		brick_type = next_brick_type;
		next_brick_type = get_rand(7) + 1;
		show_brick_preview(preview_win, next_brick_type);
		memcpy(cur_brick, brick_digit[brick_type - 1], sizeof(char) * 4 * 4);
		x = BOARD_WIDTH / 2;
		y = 0;
		run = 1;
		while (quit == 0) {
			show_board_win(board_win, board, cur_brick, brick_type, x, y);
			switch (get_key(board_win)) {
				case KEY_DOWN:
					if (check_brick(board, cur_brick, x, y + 1) == 0) {
						y++;
					}
					break;
				case KEY_UP:
					change_direction(board, cur_brick, x, y, 1);
					break;
				case KEY_RIGHT:
					if (check_brick(board, cur_brick, x + 1, y) == 0) {
						x++;
					}
					break;
				case KEY_LEFT:
					if (x > 0 && check_brick(board, cur_brick, x - 1, y) == 0) {
						x--;
					}
					break;
				case ' ':
					while (check_brick(board, cur_brick, x, y + 1) == 0) {
						y++;
					}
					break;
				case 'q':
					quit = 2;
					break;
			}
			usleep(SPEED_CONST_2 - level * SPEED_CONST_1);
			if (run > 15) {
				if (check_brick(board, cur_brick, x, y + 1) == 0) {
					y++;
					run = 0;
				} else {
					if (y <= 1) {
						quit = 2;
						show_game_over(board_win);
						quit = 1;
					}
					draw_to_board(board, cur_brick, brick_type, x, y);
					show_board_win(board_win, board, cur_brick, brick_type, x, y);
					remove_rows(board_win, board, &score, level);
					calc_level(score, &level);
					show_score(score_win, score, level);
					break;
				}
			}
			run++;
		}

	}
	destroy_score_win(score_win);
	destroy_preview_win(preview_win);
	destroy_board_win(board_win);
	return score;
}

