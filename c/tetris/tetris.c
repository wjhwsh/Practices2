#include "tetris.h"

#include "screen.h"
#include "game.h"

char quit = 0;
unsigned long rseed = 1;

static void quit_sig_handler(const int code)
{
	if (quit > 1) {
		restore_screen();
		exit(0);
	}
	quit = 3;
}

int main(int argc, char *argv[])
{
	rseed = time(NULL);

	signal(SIGKILL, quit_sig_handler);
	signal(SIGWINCH, quit_sig_handler);
	signal(SIGTERM, quit_sig_handler);
	signal(SIGINT, quit_sig_handler);
	signal(SIGQUIT, quit_sig_handler);
	if (quit != 0) {
		return 0;
	}
	if (init_screen() != 0) {
		return 1;
	}
	do {
		start_game();
	} while(quit == 1);
	restore_screen();
	return 0;
}

