

////////////////////////////////////////////////////////////////////////////////////////////////////
/// <category>	DA-Funktionen. </category>
/// <categoryE>	DA functions. </categoryE>
///
///
/// <filesummary>	zur Steuerung bzw. Messung der DA Kanäle stehen die folgenden Funktionne zur Verfügung:. </filesummary>
/// <filesummaryE>	for controlling and measuring DA Channels these functions are available: </filesummaryE>
////////////////////////////////////////////////////////////////////////////////////////////////////
MAIV2DLL_EXPORT DA_SetRange(uint nInstance, uint nRange);
MAIV2DLL_EXPORT DA_ClearChannelList(uint nInstance);
MAIV2DLL_EXPORT DA_AddChannelToList(uint nInstance, uint nChannel);
MAIV2DLL_EXPORT DA_GetChannelListSize(uint nInstance, uint * nCLSize);
MAIV2DLL_EXPORT DA_SetFrequency(uint nInstance, double fFrequency);
MAIV2DLL_EXPORT DA_StartOutput(uint nInstance);
MAIV2DLL_EXPORT DA_StopOutput(uint nInstance);
MAIV2DLL_EXPORT	DA_WriteChannelRaw(uint nInstance, uint nChannel, int RawValue);
MAIV2DLL_EXPORT	DA_WriteChannelVoltage(uint nInstance, uint nChannel, double VoltageValue);
MAIV2DLL_EXPORT DA_WriteRawData(uint nInstance, uint nChannelListEntry, int pBuffer[], uint * nLength, uint bPartBlock);
MAIV2DLL_EXPORT DA_WriteScaledData(uint nInstance, uint nChannelListEntry, double fScaledValues[], uint * nLength, uint bPartBlock);
MAIV2DLL_EXPORT DA_GetFifoState(uint nInstance, uint nChannel, uint * nNumberOfValues);
MAIV2DLL_EXPORT DA_Audio_SetMonauralMode(uint nInstance, uint bLoopbackModeOn);
MAIV2DLL_EXPORT DA_Audio_SetADLoopbackMode(uint nInstance, uint bLoopbackModeOn);


