Option Explicit 
Public Declare Function AD_ClearChannelList LIB "maiv2dll.DLL" (ByVal nInstance As Long) As Long
Public Declare Function AD_AddChannelToList LIB "maiv2dll.DLL" (ByVal nInstance As Long, ByVal nChannel As Long, ByVal nOversampling As Long, ByVal nGain As Long, ByVal nBipolar As Long) As Long
Public Declare Function AD_GetChannelListSize LIB "maiv2dll.DLL" (ByVal nInstance As Long, ByRef nCLSize As Long) As Long
Public Declare Function AD_ReadSingleValue LIB "maiv2dll.DLL" (ByVal nInstance As Long, ByVal nChannel As Long, ByVal nOversampling As Long, ByVal nGain As Long, ByVal nBipolar As Long, ByRef nRawValue As Long) As Long
Public Declare Function AD_ReadSingleValueExt LIB "maiv2dll.DLL" (ByVal nInstance As Long, ByVal nChannel As Long, ByVal nOversampling As Long, ByVal nGain As Long, ByVal nBipolar As Long, ByRef nRawValue As Long, ByRef dVoltage As Double, ByRef fVoltage As Single) As Long
Public Declare Function AD_ReadSingleVoltage LIB "maiv2dll.DLL" (ByVal nInstance As Long, ByVal nChannel As Long, ByVal nOversampling As Long, ByVal nGain As Long, ByVal nBipolar As Long, ByRef bVoltage As Double) As Long
Public Declare Function AD_SetFrequency LIB "maiv2dll.DLL" (ByVal nInstance As Long, ByVal fFrequency As Double) As Long
Public Declare Function AD_GetFrequency LIB "maiv2dll.DLL" (ByVal nInstance As Long, ByRef fFrequency As Double) As Long
Public Declare Function AD_ReadLastBurst LIB "maiv2dll.DLL" (ByVal nInstance As Long, ByRef RawData As Long, ByRef Value As Double, ByRef nNumberOfValues As Long) As Long
Public Declare Function AD_ReadData LIB "maiv2dll.DLL" (ByVal nInstance As Long, ByVal nChannelListEntry As Long, ByRef RawData As Long, ByRef Value As Double, ByRef nValuesPerChannel As Long, ByVal bPartBlock As Long, ByVal bSkipData As Long) As Long
Public Declare Function AD_ReadDataExt LIB "maiv2dll.DLL" (ByVal nInstance As Long, ByVal nChannelListEntry As Long, ByRef pRawData As Long, ByRef pDoubleValues As Double, ByRef pFloatValues As Single, ByRef nValuesPerChannel As Long, ByVal bPartBlock As Long, ByRef AODateTimeT0 As LongLong, ByRef AODateTimeDeltaT As Double) As Long
Public Declare Function AD_ReadBinaryData LIB "maiv2dll.DLL" (ByVal nInstance As Long, ByRef BinaryData As Byte, ByRef nLength As Long) As Long
Public Declare Function AD_GetBinaryWordsizePerChannel LIB "maiv2dll.DLL" (ByVal nInstance As Long, ByRef nSingleADWordSize As Long) As Long
Public Declare Function AD_ConvertBinaryBurstToDoublePerChannel LIB "maiv2dll.DLL" (ByVal nInstance As Long, ByRef BinaryData As Byte, ByRef nConvertedBurst As Double) As Long
Public Declare Function AD_GetStreamPipeLevel LIB "maiv2dll.DLL" (ByVal nInstance As Long, ByRef fStreamPipeLevel As Double) As Long
Public Declare Function AD_GetNumberOfValues LIB "maiv2dll.DLL" (ByVal nInstance As Long, ByRef nNumberOfValues As Long) As Long
Public Declare Function AD_StartMeasure LIB "maiv2dll.DLL" (ByVal nInstance As Long) As Long
Public Declare Function AD_StopMeasure LIB "maiv2dll.DLL" (ByVal nInstance As Long) As Long
Public Declare Function AD_SetIEPE LIB "maiv2dll.DLL" (ByVal nInstance As Long, ByVal nChannel As Long, ByVal nIEPEMode As Long, ByVal bGain As Long) As Long
Public Declare Function AD_SetIEPEOnAudioModul LIB "maiv2dll.DLL" (ByVal nInstance As Long, ByVal nChannel As Long, ByVal bIEPEOn As Long, ByVal bDCOn As Long, ByVal bCurrentSourceOn As Long, ByVal bGainOn As Long) As Long
Public Declare Function AD_SetEventToBeRaisedWhenNumberOfBurstsAvailable LIB "maiv2dll.DLL" (ByVal nInstance As Long, ByRef hEventHandle As Long, ByVal nNumberOfBursts As Long) As Long
Public Declare Function AD_Audio_SetHPFilter LIB "maiv2dll.DLL" (ByVal nInstance As Long, ByVal nChannel As Long, ByVal bFilterOn As Long) As Long
Public Declare Function AD_Audio_SetHPFilterResponse LIB "maiv2dll.DLL" (ByVal nInstance As Long, ByVal nADCNr As Long, ByVal bLowGroupDelayResponseOn As Long) As Long
Public Declare Function AD_ResetIEPE LIB "maiv2dll.DLL" (ByVal nInstance As Long) As Long
Public Declare Function AD_GetIEPEType LIB "maiv2dll.DLL" (ByVal nInstance As Long) As Long
Public Declare Function AD_GetCorrectionValue LIB "maiv2dll.DLL" (ByVal nInstance As Long, ByVal nChannel As Long, ByRef fValue As Single) As Long
Public Declare Function AD_SetCorrectionValue LIB "maiv2dll.DLL" (ByVal nInstance As Long, ByVal nChannel As Long, ByVal fValue As Single) As Long
Public Declare Function AD_WriteCorrectionValuesToDevice LIB "maiv2dll.DLL" (ByVal nInstance As Long) As Long
