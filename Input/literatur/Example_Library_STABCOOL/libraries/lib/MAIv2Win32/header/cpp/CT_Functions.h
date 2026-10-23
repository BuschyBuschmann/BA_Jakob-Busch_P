

////////////////////////////////////////////////////////////////////////////////////////////////////
/// <category>	CT-Funktionen. </category>
/// <categoryE>	CT functions. </categoryE>
///
///
/// <filesummary>	zur Steuerung bzw. Messung der CT Kanäle stehen die folgenden Funktionne zur Verfügung:. </filesummary>
/// <filesummaryE>	for controlling and measuring CT Channels these functions are available: </filesummaryE>
////////////////////////////////////////////////////////////////////////////////////////////////////
MAIV2DLL_EXPORT CT_ClearChannelList(uint nInstance);
MAIV2DLL_EXPORT CT_AddChannelToList(uint nInstance, uint nChannel, bool bToADChannellist);
MAIV2DLL_EXPORT CT_GetChannelListSize(uint nInstance, uint * nCLSize);
MAIV2DLL_EXPORT CT_SetFrequency(uint nInstance, double fFreqency);
MAIV2DLL_EXPORT CT_GetFrequency(uint nInstance, double * fFrequency);

MAIV2DLL_EXPORT CT_ScaleData(uint nInstance, uint nChannelListEntry, int pInBuffer[], double pOutBuffer[],uint nNumberOfValues, int& ARFirstLastValue);
MAIV2DLL_EXPORT CT_ReadData(uint nInstance, uint nChannelListEntry, uint pBuffer[], uint * nNumberOfValues, uint bPartBlock, uint bSkipData);
MAIV2DLL_EXPORT CT_ReadDataExt(uint nInstance, uint nChannelListEntry, uint pBuffer[], uint * nNumberOfValues, uint bPartBlock, __int64* AODateTimeT0, double* AODateTimeDeltaT);
MAIV2DLL_EXPORT CT_ReadSingleValue(uint nInstance, uint nChannel, uint * SingleValue);
MAIV2DLL_EXPORT CT_GetStreamPipeLevel(uint nInstance, double * fStreamPipeLevel);
MAIV2DLL_EXPORT CT_GetNumberOfValues(uint nInstance, uint * nNumberOfValues);
MAIV2DLL_EXPORT CT_StartMeasure(uint nInstance);
MAIV2DLL_EXPORT CT_StopMeasure(uint nInstance);

MAIV2DLL_EXPORT CT_GetIncrementalCounterDirections(uint nInstance, uint* nDirectionValue);

MAIV2DLL_EXPORT CT_SetCounterParameter(uint nInstance, uint nChannelListEntry, uint eCOUNTERPARAMETER, uint nParameterValue);
MAIV2DLL_EXPORT CT_GetCounterParameter(uint nInstance, uint nChannelListEntry, uint  eCOUNTERPARAMETER, uint*  nParameterValue);
MAIV2DLL_EXPORT CT_GetCounterParametersForMode(uint nInstance, uint  eCOUNTERMODE, uint* AvailableCounterParameters);
MAIV2DLL_EXPORT CT_GetCounterParameterBoundaries(uint nInstance, uint eCOUNTERPARAMETER, uint* nMinValue  , uint*  nMaxValue);

MAIV2DLL_EXPORT CT_GetAvailableCounterModes(uint nInstance, uint nChannel,  uint* eCOUNTERMODES);

MAIV2DLL_EXPORT CT_SetCounterMode(uint nInstance, uint nChannelListEntry,  uint  eCOUNTERMODE);
MAIV2DLL_EXPORT CT_GetCounterMode(uint nInstance, uint nChannelListEntry,  uint* eCOUNTERMODE);


// Deprecated ConterMode Functions (may be removed in future versions):
MAIV2DLL_EXPORT CT_ImpulseCounter(uint nInstance, uint nChannel, uint nPresetValue, uint nUpDown, uint nEdge);
MAIV2DLL_EXPORT CT_FrequencyCounter(uint nInstance, uint nChannel, uint nResolution, uint nEdge, uint nEachPeriod);
MAIV2DLL_EXPORT CT_PeriodCounter(uint nInstance, uint nChannel, uint nResolution, uint nEdge, uint nEachPeriod);
MAIV2DLL_EXPORT CT_PulswidthCounter(uint nInstance, uint nChannel, uint nResolution, uint nEdge, uint nEachPeriod);
MAIV2DLL_EXPORT CT_IncrementalCounter(uint nInstance, uint nChannel, uint nResolution, uint nEdge, uint nSoftwareReset, uint nHardwareReset, uint nHWResetEdge, uint nInterpolation);
MAIV2DLL_EXPORT CT_IncrementalCounterExtensionTime(uint nInstance, uint nChannel, uint nResolution);
MAIV2DLL_EXPORT CT_IncrementalCounterExtensionFlow(uint nInstance, uint nChannel);
MAIV2DLL_EXPORT CT_UpDownCounter(uint nInstance, uint nChannel, uint nPresetValue, uint nUpDown, uint nEdge, uint nSoftwareReset);


// new ConterMode Functions for Ethernet Device SingleValue Mode :
MAIV2DLL_EXPORT CT_SetCounterParameter_SingleValueMode(uint nInstance, uint nChannelNumber, uint eCOUNTERPARAMETER, int nParameterValue);
MAIV2DLL_EXPORT CT_GetCounterParameter_SingleValueMode(uint nInstance, uint nChannelNumber, uint  eCOUNTERPARAMETER, int*  nParameterValue);
MAIV2DLL_EXPORT CT_SetCounterMode_SingleValueMode(uint nInstance, uint nChannelNumber,  uint  eCOUNTERMODE);
MAIV2DLL_EXPORT CT_GetCounterMode_SingleValueMode(uint nInstance, uint nChannelNumber,  uint* eCOUNTERMODE);
MAIV2DLL_EXPORT CT_Reset(uint nInstance, uint nHardwareChannelNumber);
