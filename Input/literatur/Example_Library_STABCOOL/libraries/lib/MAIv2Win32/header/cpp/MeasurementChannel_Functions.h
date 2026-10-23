#ifndef _MAI_MEASUREMENTCHANNEL_H_
#define _MAI_MEASUREMENTCHANNEL_H_

#include <MAI_Types.h>

MAIV2DLL_EXPORT MeasurementChannel_GetNumberOfValues(uint nInstance, eMeasurementChannelType eChannelType, uint nChannelListEntry, uint* nNumberOfValues);
MAIV2DLL_EXPORT MeasurementChannel_ReadDataAsUInt32(uint nInstance, eMeasurementChannelType ChannelType, int nChannelListEntry, uint pData[], uint * nNumberOfValues, uint bPartBlock, __int64* DateTimeT0, double* DateTimeDeltaT);
MAIV2DLL_EXPORT MeasurementChannel_ReadDataAsDouble(uint nInstance, eMeasurementChannelType ChannelType, int nChannelListEntry, double pData[], uint * nNumberOfValues, uint bPartBlock, __int64* DateTimeT0, double* DateTimeDeltaT);


#endif // _MAI_MEASUREMENTCHANNEL_H_