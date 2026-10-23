



////////////////////////////////////////////////////////////////////////////////////////////////////
/// <category>	AD-Funktionen. </category>
/// <categoryE>	AD functions. </categoryE>
///
///
/// <filesummary>	zur Steuerung bzw. Messung der AD Kanäle stehen die folgenden Funktionen zur Verfügung:. </filesummary>
/// <filesummaryE>	for controlling and measuring AD Channels these functions are available: </filesummaryE>
////////////////////////////////////////////////////////////////////////////////////////////////////

MAIV2DLL_EXPORT		AD_ClearChannelList(uint nInstance);	
MAIV2DLL_EXPORT		AD_AddChannelToList(uint nInstance, uint nChannel, uint nOversampling, uint nGain, uint nBipolar);							
MAIV2DLL_EXPORT		AD_GetChannelListSize(uint nInstance, uint * nCLSize);																		
MAIV2DLL_EXPORT		AD_ReadSingleValue(uint nInstance, uint nChannel, uint nOversampling, uint nGain, uint nBipolar, int * nRawValue);		
MAIV2DLL_EXPORT		AD_ReadSingleValueExt(uint nInstance, uint nChannel, uint nOversampling, uint nGain, uint nBipolar, int * nRawValue, double * dVoltage, float * fVoltage);		
MAIV2DLL_EXPORT		AD_ReadSingleVoltage(uint nInstance, uint nChannel, uint nOversampling, uint nGain, uint nBipolar, double * bVoltage);
MAIV2DLL_EXPORT		AD_SetFrequency(uint nInstance, double fFrequency);
MAIV2DLL_EXPORT 	AD_GetFrequency(uint nInstance, double * fFrequency);
MAIV2DLL_EXPORT 	AD_ReadLastBurst(uint nInstance, int RawData[], double Value[], uint * nNumberOfValues);
MAIV2DLL_EXPORT 	AD_ReadData(uint nInstance, uint nChannelListEntry, int RawData[], double Value[], uint * nValuesPerChannel, uint bPartBlock, uint bSkipData);
MAIV2DLL_EXPORT     AD_ReadDataExt(uint nInstance, uint nChannelListEntry, int pRawData[], double pDoubleValues[], float pFloatValues[], uint * nValuesPerChannel, uint bPartBlock, __int64* AODateTimeT0, double* AODateTimeDeltaT);
MAIV2DLL_EXPORT 	AD_ReadBinaryData(uint nInstance, uchar BinaryData[], uint * nLength);
MAIV2DLL_EXPORT     AD_GetBinaryWordsizePerChannel(uint nInstance,  uint * nSingleADWordSize);
MAIV2DLL_EXPORT     AD_ConvertBinaryBurstToDoublePerChannel(uint nInstance, uchar BinaryData[], double* nConvertedBurst);
MAIV2DLL_EXPORT		AD_GetStreamPipeLevel(uint nInstance, double * fStreamPipeLevel);
MAIV2DLL_EXPORT 	AD_GetNumberOfValues(uint nInstance, uint * nNumberOfValues);
MAIV2DLL_EXPORT 	AD_StartMeasure(uint nInstance);
MAIV2DLL_EXPORT 	AD_StopMeasure(uint nInstance);
MAIV2DLL_EXPORT 	AD_SetIEPE(uint nInstance, uint nChannel,uint nIEPEMode, uint bGain);
MAIV2DLL_EXPORT 	AD_SetIEPEOnAudioModul(uint nInstance, uint nChannel,uint bIEPEOn, uint bDCOn, uint bCurrentSourceOn, uint bGainOn);
MAIV2DLL_EXPORT 	AD_SetEventToBeRaisedWhenNumberOfBurstsAvailable(uint nInstance, void* hEventHandle, uint nNumberOfBursts);
MAIV2DLL_EXPORT		AD_Audio_SetHPFilter(uint nInstance,uint nChannel, uint bFilterOn);
MAIV2DLL_EXPORT     AD_Audio_SetHPFilterResponse(uint nInstance,  uint nADCNr, uint bLowGroupDelayResponseOn);

MAIV2DLL_EXPORT 	AD_ResetIEPE(uint nInstance);
MAIV2DLL_EXPORT 	AD_GetIEPEType(uint nInstance);

MAIV2DLL_EXPORT 	AD_GetCorrectionValue(uint nInstance, uint nChannel, float* fValue);
MAIV2DLL_EXPORT 	AD_SetCorrectionValue(uint nInstance, uint nChannel, float  fValue);
MAIV2DLL_EXPORT 	AD_WriteCorrectionValuesToDevice(uint nInstance);

