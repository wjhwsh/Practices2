#include <stdio.h>
#include <sys/stat.h>
#include <string.h>
#include <errno.h>

int main(int argc, char **argv) 
{
	struct stat  file_stat;

	while(argc-- > 1) {

		if(lstat(argv[argc], &file_stat) == -1)
			fprintf(stderr, "%s\n", strerror(errno));
		else {
			fprintf(stdout, "Links\tUid\tGid\tSize\tName\n");
			fprintf(stdout, "%u\t%u\t%u\t%u\t%s\n", file_stat.st_nlink,
			        file_stat.st_uid, file_stat.st_gid, file_stat.st_size,
			        argv[argc]);
		}
	}
	return 0;
}
