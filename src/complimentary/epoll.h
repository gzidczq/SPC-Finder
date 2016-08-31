/* fake */  
  
#ifndef _SYS_EPOLL_H  
#define _SYS_EPOLL_H    1  
  
#include <stdint.h>  
#include <sys/types.h>  
  
/* Get __sigset_t.  */  
#include <sigset.h>  
  
#ifndef __sigset_t_defined  
# define __sigset_t_defined  
typedef __sigset_t sigset_t;  
#endif  
  
/* Get the platform-dependent flags.  */  
#include <epoll.h>  
  
#ifndef __EPOLL_PACKED  
# define __EPOLL_PACKED  
#endif  
  
  
  
/* Valid opcodes ( "op" parameter ) to issue to epoll_ctl().  */  
#define EPOLL_CTL_ADD 1 /* Add a file descriptor to the interface.  */  
#define EPOLL_CTL_DEL 2 /* Remove a file descriptor from the interface.  */  
#define EPOLL_CTL_MOD 3 /* Change file descriptor epoll_event structure.  */  
  
  
typedef union epoll_data;
  

  
#endif /* sys/epoll.h */ 
