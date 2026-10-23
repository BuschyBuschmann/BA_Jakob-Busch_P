Option Explicit 
Public Declare Function DA_SetRange LIB "maiv2dll.DLL" (ByVal nInstance As Long, ByVal nRange As Long) As Long
Public Declare Function DA_ClearChannelList LIB "maiv2dll.DLL" (ByVal nInstance As Long) As Long
Public Declare Function DA_AddChannelToList LIB "maiv2dll.DLL" (ByVal nInstance As Long, ByVal nChannel As Long) As Long
Public Declare Function DA_GetChannelListSize LIB "maiv2dll.DLL" (ByVal nInstance As Long, ByRef nCLSize As Long) As Long
Public Declare Function DA_SetFrequency LIB "maiv2dll.DLL" (ByVal nInstance As Long, ByVal fFrequency As Double) As Long
Public Declare Function DA_StartOutput LIB "maiv2dll.DLL" (ByVal nInstance As Long) As Long
Public Declare Function DA_StopOutput LIB "maiv2dll.DLL" (ByVal nInstance As Long) As Long
Public Declare Function DA_WriteChannelRaw LIB "maiv2dll.DLL" (ByVal nInstance As Long, ByVal nChannel As Long, ByVal RawValue As Long) As Long
Public Declare Function DA_WriteChannelVoltage LIB "maiv2dll.DLL" (ByVal nInstance As Long, ByVal nChannel As Long, ByVal VoltageValue As Double) As Long
Public Declare Function DA_WriteRawData LIB "maiv2dll.DLL" (ByVal nInstance As Long, ByVal nChannelListEntry As Long, ByRef pBuffer As Long, ByRef nLength As Long, ByVal bPartBlock As Long) As Long
Public Declare Function DA_WriteScaledData LIB "maiv2dll.DLL" (ByVal nInstance As Long, ByVal nChannelListEntry As Long, ByRef fScaledValues As Double, ByRef nLength As Long, ByVal bPartBlock As Long) As Long
Public Declare Function DA_GetFifoState LIB "maiv2dll.DLL" (ByVal nInstance As Long, ByVal nChannel As Long, ByRef nNumberOfValues As Long) As Long
Public Declare Function DA_Audio_SetMonauralMode LIB "maiv2dll.DLL" (ByVal nInstance As Long, ByVal bLoopbackModeOn As Long) As Long
Public Declare Function DA_Audio_SetADLoopbackMode LIB "maiv2dll.DLL" (ByVal nInstance As Long, ByVal bLoopbackModeOn As Long) As Long
