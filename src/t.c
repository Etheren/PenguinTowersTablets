#include <stdio.h>
#include <sys/time.h>
#include <time.h>


main()
{
  struct timeval t;

  gettimeofday (&t, NULL);
  printf("secs = %d, microseconds = %d\n", t.tv_sec, t.tv_usec);
}
