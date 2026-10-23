#ifndef _MAIV2DLL_H_
#define _MAIV2DLL_H_


#ifdef ANDROID
#include <memory>
#endif



#ifdef __GCC_BUILD_

#ifdef __cplusplus
extern "C" {
#endif

#else 


#endif


#include <MAI_Types.h>

#include <AD_Functions.h>
#include <DA_Functions.h>
#include <CT_Functions.h>
#include <Realtime_Functions.h>
#include <PoolFunctions.h>
#include <PWM_Functions.h>
#include <SSI_Functions.h>
#include <TTL_Functions.h>
#include <General_Functions.h>
#include <UART_Functions.h>
#include <Misc_Functions.h>
#include <MeasurementChannel_Functions.h>


#ifdef __GCC_BUILD_

#ifdef __cplusplus
 }
#endif

#else 


#endif



#endif

