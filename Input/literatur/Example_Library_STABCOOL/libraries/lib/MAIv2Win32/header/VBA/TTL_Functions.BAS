Option Explicit 
Public Declare Function TTL_ClearChannelList LIB "maiv2dll.DLL" (ByVal nInstance As Long) As Long
Public Declare Function TTL_AddChannelToList LIB "maiv2dll.DLL" (ByVal nInstance As Long, ByVal nChannel As Long, ByVal bToADList As Boolean, ByVal nDigitalType As Long) As Long
Public Declare Function TTL_GetChannelListSize LIB "maiv2dll.DLL" (ByVal nInstance As Long, ByRef nCLSize As Long) As Long
Public Declare Function TTL_SetFrequency LIB "maiv2dll.DLL" (ByVal nInstance As Long, ByVal fFrequency As Double) As Long
Public Declare Function TTL_SetChannelDirection LIB "maiv2dll.DLL" (ByVal nInstance As Long, ByVal nChannel As Long, ByVal nDirectionValue As Long) As Long
Public Declare Function TTL_GetChannelDirection LIB "maiv2dll.DLL" (ByVal nInstance As Long, ByVal nChannel As Long, ByRef nDirection As Long) As Long
Public Declare Function TTL_GetIsChannelDirectionFixed LIB "maiv2dll.DLL" (ByVal nInstance As Long, ByVal nChannel As Long, ByRef nDirectionFixed As Long) As Long
Public Declare Function TTL_ReadData LIB "maiv2dll.DLL" (ByVal nInstance As Long, ByRef pBuffer As Long, ByRef nNumberOfBursts As Long, ByVal bPartBlock As Long, ByVal bSkipData As Long) As Long
Public Declare Function TTL_ReadData8 LIB "maiv2dll.DLL" (ByVal nInstance As Long, ByRef pBuffer As Byte, ByRef nNUmberOfBursts As Long) As Long
Public Declare Function TTL_ReadData16 LIB "maiv2dll.DLL" (ByVal nInstance As Long, ByRef pBuffer As Long, ByRef nNUmberOfBursts As Long) As Long
Public Declare Function TTL_ReadData32 LIB "maiv2dll.DLL" (ByVal nInstance As Long, ByRef pBuffer As Long, ByRef nNUmberOfBursts As Long) As Long
Public Declare Function TTL_ReadData64 LIB "maiv2dll.DLL" (ByVal nInstance As Long, ByRef pBuffer As Long, ByRef nNUmberOfBursts As Long) As Long
Public Declare Function TTL_GetBurstSize LIB "maiv2dll.DLL" (ByVal nInstance As Long, ByRef nBurstSizeInBytes As Long) As Long
Public Declare Function TTL_ReadDataExt LIB "maiv2dll.DLL" (ByVal nInstance As Long, ByRef pBuffer As Byte, ByRef nNUmberOfBursts As Long, ByVal nBurstSizeInBytes As Long, ByRef AODateTimeT0 As LongLong, ByRef AODateTimeDeltaT As Double) As Long
Public Declare Function TTL_ReadPort LIB "maiv2dll.DLL" (ByVal nInstance As Long, ByVal nPort As Long, ByRef nPortValue As Long) As Long
Public Declare Function TTL_WritePort LIB "maiv2dll.DLL" (ByVal nInstance As Long, ByVal nPort As Long, ByVal nPortValue As Long) As Long
Public Declare Function TTL_ReadBit LIB "maiv2dll.DLL" (ByVal nInstance As Long, ByVal nChannel As Long, ByRef nBit As Long) As Long
Public Declare Function TTL_WriteBit LIB "maiv2dll.DLL" (ByVal nInstance As Long, ByVal nChannel As Long, ByVal nBit As Long) As Long
Public Declare Function TTL_GetStreamPipeLevel LIB "maiv2dll.DLL" (ByVal nInstance As Long, ByRef fStreamPipeLevel As Double) As Long
Public Declare Function TTL_GetNumberOfValues LIB "maiv2dll.DLL" (ByVal nInstance As Long, ByRef nNumberOfValues As Long) As Long
Public Declare Function TTL_InitializeTargetSettings LIB "maiv2dll.DLL" (ByVal nInstance As Long) As Long
Public Declare Function TTL_StartMeasure LIB "maiv2dll.DLL" (ByVal nInstance As Long) As Long
Public Declare Function TTL_StopMeasure LIB "maiv2dll.DLL" (ByVal nInstance As Long) As Long
Public Declare Function TTL_GetPortInfos LIB "maiv2dll.DLL" (ByVal nInstance As Long, ByRef NumberOfPorts As Long, ByRef PortWidth As Long, ByRef NumberOfDigIn As Long, ByRef NumberOfDigOut As Long) As Long
