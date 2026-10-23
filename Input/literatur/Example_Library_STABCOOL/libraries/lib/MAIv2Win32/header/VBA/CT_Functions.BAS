Option Explicit 
Public Declare Function CT_ClearChannelList LIB "maiv2dll.DLL" (ByVal nInstance As Long) As Long
Public Declare Function CT_AddChannelToList LIB "maiv2dll.DLL" (ByVal nInstance As Long, ByVal nChannel As Long, ByVal bToADChannellist As Boolean) As Long
Public Declare Function CT_GetChannelListSize LIB "maiv2dll.DLL" (ByVal nInstance As Long, ByRef nCLSize As Long) As Long
Public Declare Function CT_SetFrequency LIB "maiv2dll.DLL" (ByVal nInstance As Long, ByVal fFreqency As Double) As Long
Public Declare Function CT_GetFrequency LIB "maiv2dll.DLL" (ByVal nInstance As Long, ByRef fFrequency As Double) As Long
Public Declare Function CT_ScaleData LIB "maiv2dll.DLL" (ByVal nInstance As Long, ByVal nChannelListEntry As Long, ByRef pInBuffer As Long, ByRef pOutBuffer As Double, ByVal nNumberOfValues As Long, ByVal ARFirstLastValue As Long) As Long
Public Declare Function CT_ReadData LIB "maiv2dll.DLL" (ByVal nInstance As Long, ByVal nChannelListEntry As Long, ByRef pBuffer As Long, ByRef nNumberOfValues As Long, ByVal bPartBlock As Long, ByVal bSkipData As Long) As Long
Public Declare Function CT_ReadDataExt LIB "maiv2dll.DLL" (ByVal nInstance As Long, ByVal nChannelListEntry As Long, ByRef pBuffer As Long, ByRef nNumberOfValues As Long, ByVal bPartBlock As Long, ByRef AODateTimeT0 As LongLong, ByRef AODateTimeDeltaT As Double) As Long
Public Declare Function CT_ReadSingleValue LIB "maiv2dll.DLL" (ByVal nInstance As Long, ByVal nChannel As Long, ByRef SingleValue As Long) As Long
Public Declare Function CT_GetStreamPipeLevel LIB "maiv2dll.DLL" (ByVal nInstance As Long, ByRef fStreamPipeLevel As Double) As Long
Public Declare Function CT_GetNumberOfValues LIB "maiv2dll.DLL" (ByVal nInstance As Long, ByRef nNumberOfValues As Long) As Long
Public Declare Function CT_StartMeasure LIB "maiv2dll.DLL" (ByVal nInstance As Long) As Long
Public Declare Function CT_StopMeasure LIB "maiv2dll.DLL" (ByVal nInstance As Long) As Long
Public Declare Function CT_GetIncrementalCounterDirections LIB "maiv2dll.DLL" (ByVal nInstance As Long, ByRef nDirectionValue As Long) As Long
Public Declare Function CT_SetCounterParameter LIB "maiv2dll.DLL" (ByVal nInstance As Long, ByVal nChannelListEntry As Long, ByVal eCOUNTERPARAMETER As Long, ByVal nParameterValue As Long) As Long
Public Declare Function CT_GetCounterParameter LIB "maiv2dll.DLL" (ByVal nInstance As Long, ByVal nChannelListEntry As Long, ByVal eCOUNTERPARAMETER As Long, ByRef nParameterValue As Long) As Long
Public Declare Function CT_GetCounterParametersForMode LIB "maiv2dll.DLL" (ByVal nInstance As Long, ByVal eCOUNTERMODE As Long, ByRef AvailableCounterParameters As Long) As Long
Public Declare Function CT_GetCounterParameterBoundaries LIB "maiv2dll.DLL" (ByVal nInstance As Long, ByVal eCOUNTERPARAMETER As Long, ByRef nMinValue As Long, ByRef nMaxValue As Long) As Long
Public Declare Function CT_GetAvailableCounterModes LIB "maiv2dll.DLL" (ByVal nInstance As Long, ByVal nChannel As Long, ByRef eCOUNTERMODES As Long) As Long
Public Declare Function CT_SetCounterMode LIB "maiv2dll.DLL" (ByVal nInstance As Long, ByVal nChannelListEntry As Long, ByVal eCOUNTERMODE As Long) As Long
Public Declare Function CT_GetCounterMode LIB "maiv2dll.DLL" (ByVal nInstance As Long, ByVal nChannelListEntry As Long, ByRef eCOUNTERMODE As Long) As Long
Public Declare Function CT_ImpulseCounter LIB "maiv2dll.DLL" (ByVal nInstance As Long, ByVal nChannel As Long, ByVal nPresetValue As Long, ByVal nUpDown As Long, ByVal nEdge As Long) As Long
Public Declare Function CT_FrequencyCounter LIB "maiv2dll.DLL" (ByVal nInstance As Long, ByVal nChannel As Long, ByVal nResolution As Long, ByVal nEdge As Long, ByVal nEachPeriod As Long) As Long
Public Declare Function CT_PeriodCounter LIB "maiv2dll.DLL" (ByVal nInstance As Long, ByVal nChannel As Long, ByVal nResolution As Long, ByVal nEdge As Long, ByVal nEachPeriod As Long) As Long
Public Declare Function CT_PulswidthCounter LIB "maiv2dll.DLL" (ByVal nInstance As Long, ByVal nChannel As Long, ByVal nResolution As Long, ByVal nEdge As Long, ByVal nEachPeriod As Long) As Long
Public Declare Function CT_IncrementalCounter LIB "maiv2dll.DLL" (ByVal nInstance As Long, ByVal nChannel As Long, ByVal nResolution As Long, ByVal nEdge As Long, ByVal nSoftwareReset As Long, ByVal nHardwareReset As Long, ByVal nHWResetEdge As Long, ByVal nInterpolation As Long) As Long
Public Declare Function CT_IncrementalCounterExtensionTime LIB "maiv2dll.DLL" (ByVal nInstance As Long, ByVal nChannel As Long, ByVal nResolution As Long) As Long
Public Declare Function CT_IncrementalCounterExtensionFlow LIB "maiv2dll.DLL" (ByVal nInstance As Long, ByVal nChannel As Long) As Long
Public Declare Function CT_UpDownCounter LIB "maiv2dll.DLL" (ByVal nInstance As Long, ByVal nChannel As Long, ByVal nPresetValue As Long, ByVal nUpDown As Long, ByVal nEdge As Long, ByVal nSoftwareReset As Long) As Long
Public Declare Function CT_SetCounterParameter_SingleValueMode LIB "maiv2dll.DLL" (ByVal nInstance As Long, ByVal nChannelNumber As Long, ByVal eCOUNTERPARAMETER As Long, ByVal nParameterValue As Long) As Long
Public Declare Function CT_GetCounterParameter_SingleValueMode LIB "maiv2dll.DLL" (ByVal nInstance As Long, ByVal nChannelNumber As Long, ByVal eCOUNTERPARAMETER As Long, ByRef nParameterValue As Long) As Long
Public Declare Function CT_SetCounterMode_SingleValueMode LIB "maiv2dll.DLL" (ByVal nInstance As Long, ByVal nChannelNumber As Long, ByVal eCOUNTERMODE As Long) As Long
Public Declare Function CT_GetCounterMode_SingleValueMode LIB "maiv2dll.DLL" (ByVal nInstance As Long, ByVal nChannelNumber As Long, ByRef eCOUNTERMODE As Long) As Long
Public Declare Function CT_Reset LIB "maiv2dll.DLL" (ByVal nInstance As Long, ByVal nHardwareChannelNumber As Long) As Long
