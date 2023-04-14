#include <stdlib.h>

int main(int argn, char **argv) {
  system("gcc -o philos.e philos.c");
  int i;
  for(i=0; i<1000; i++){
    system("./philos.e");
  }
}