
#include <stdio.h>
#include <string.h>
#include <ctype.h>

int main(void)
{
  char text[100];                

  printf("\nEnter the string to be searched(less than 100 characters):\n");
  fgets(text, sizeof(text), stdin);

  printf("%d\n", strlen(text));
  text[strlen(text)] = '\0';

  printf("%s",text);

}
