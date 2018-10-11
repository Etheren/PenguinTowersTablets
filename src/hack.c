/* replace this from the function inside sckt.def/.c which is inside
   the latest csn directory (I think)
*/

#include <unistd.h>
#include <fcntl.h>
#include <signal.h>


int hack_nonBlocking (int fd)
{
    return fcntl(fd, fcntl(fd, F_GETFL) | O_NONBLOCK);
}

int hack_ignoreSignals (void)
{
  signal(SIGPIPE, SIG_IGN);
}

void _M2_hack_init () {}
void _M2_hack_finish () {}
