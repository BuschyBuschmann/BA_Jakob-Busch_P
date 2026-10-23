

////////////////////////////////////////////////////////////////////////////////////////////////////
/// <category>	TTL-Funktionen. </category>
/// <categoryE>	TTL functions. </categoryE>
///
///
/// <filesummary>	zur Steuerung bzw. Messung der TTL Kanäle stehen die folgenden Funktionne zur Verfügung:. </filesummary>
/// <filesummaryE>	for controlling and measuring TTL Channels these functions are available: </filesummaryE>
////////////////////////////////////////////////////////////////////////////////////////////////////
MAIV2DLL_EXPORT TTL_ClearChannelList(uint nInstance);
MAIV2DLL_EXPORT TTL_AddChannelToList(uint nInstance, uint nChannel, bool bToADList, uint nDigitalType);
MAIV2DLL_EXPORT TTL_GetChannelListSize(uint nInstance, uint * nCLSize);
MAIV2DLL_EXPORT TTL_SetFrequency(uint nInstance, double fFrequency);
MAIV2DLL_EXPORT TTL_SetChannelDirection(uint nInstance, uint nChannel, uint nDirectionValue);
MAIV2DLL_EXPORT TTL_GetChannelDirection(uint nInstance, uint nChannel, uint * nDirection);
MAIV2DLL_EXPORT TTL_GetIsChannelDirectionFixed(uint nInstance, uint nChannel, uint * nDirectionFixed);
MAIV2DLL_EXPORT TTL_ReadData(uint nInstance, uint pBuffer[], uint * nNumberOfBursts, uint bPartBlock, uint bSkipData);
MAIV2DLL_EXPORT TTL_ReadData8(uint nInstance, uchar* pBuffer, uint * nNUmberOfBursts);
MAIV2DLL_EXPORT TTL_ReadData16(uint nInstance, ushort* pBuffer, uint * nNUmberOfBursts);
MAIV2DLL_EXPORT TTL_ReadData32(uint nInstance, uint* pBuffer, uint * nNUmberOfBursts);
MAIV2DLL_EXPORT TTL_ReadData64(uint nInstance, u64* pBuffer, uint * nNUmberOfBursts);
MAIV2DLL_EXPORT TTL_GetBurstSize(uint nInstance, uint* nBurstSizeInBytes);
MAIV2DLL_EXPORT TTL_ReadDataExt(uint nInstance, uchar* pBuffer, uint * nNUmberOfBursts, uint nBurstSizeInBytes, __int64* AODateTimeT0, double* AODateTimeDeltaT);
MAIV2DLL_EXPORT TTL_ReadPort(uint nInstance, uint nPort, uint * nPortValue);
MAIV2DLL_EXPORT TTL_WritePort(uint nInstance, uint nPort, uint nPortValue);
MAIV2DLL_EXPORT TTL_ReadBit(uint nInstance, uint nChannel, uint * nBit);
MAIV2DLL_EXPORT TTL_WriteBit(uint nInstance, uint nChannel, uint nBit);
MAIV2DLL_EXPORT TTL_GetStreamPipeLevel(uint nInstance, double * fStreamPipeLevel);
MAIV2DLL_EXPORT TTL_GetNumberOfValues(uint nInstance, uint * nNumberOfValues);
MAIV2DLL_EXPORT TTL_InitializeTargetSettings(uint nInstance);
MAIV2DLL_EXPORT TTL_StartMeasure(uint nInstance);
MAIV2DLL_EXPORT TTL_StopMeasure(uint nInstance);
MAIV2DLL_EXPORT TTL_GetPortInfos(uint nInstance, uint * NumberOfPorts, uint * PortWidth, uint * NumberOfDigIn, uint * NumberOfDigOut);





