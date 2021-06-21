#include <iostream>
 
#include <fcntl.h>
#include <stdlib.h>
 
#include <sys/types.h>
#include <sys/uio.h>
#include <unistd.h>
#include <stdio.h>

using namespace std;

int main(int argc, char *argv[]) {
  int fd;

  for(int i=1;i<argc;i++)
  { 
    fd = open(argv[i], O_RDONLY);
    if (fd == -1) {
      cout << "wcat: cannot open file"<< endl;
      return 1;
    }
  char buffer[4096];
  int ret;
  while ((ret = read(fd,buffer, 100)) > 0) {
      write(STDOUT_FILENO,buffer,ret);
  }
  close(fd);
}
return 0;
}