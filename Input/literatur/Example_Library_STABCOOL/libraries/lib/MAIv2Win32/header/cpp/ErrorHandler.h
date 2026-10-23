
#ifndef _ERRORHANDLER_H_
#define _ERRORHANDLER_H_


#ifdef ANDROID
#include <memory>
#endif

#include <Typedef.h>


long GetErrorDescription_intern(long ErrorNumber, char * ErrorDescription);


#endif
