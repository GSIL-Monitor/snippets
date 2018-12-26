#ifndef _IPIPX_H_
#define _IPIPX_H_

int ipipx_init(const char* ipdb);
int ipipx_destroy();
int ipipx_find(const char *ip, char *result);

#endif //_IPIPX_H_
