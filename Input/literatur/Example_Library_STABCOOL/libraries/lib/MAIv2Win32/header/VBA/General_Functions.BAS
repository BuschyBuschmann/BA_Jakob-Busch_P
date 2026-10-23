Option Explicit 
Public Declare Function ClearAllChannelLists LIB "maiv2dll.DLL" (ByVal nInstance As Long) As Long
Public Declare Function ResetDevice LIB "maiv2dll.DLL" (ByVal nInstance As Long) As Long
Public Declare Function LoadFirmware LIB "maiv2dll.DLL" (ByVal nInstance As Long) As Long
Public Declare Function StartMeasure LIB "maiv2dll.DLL" (ByVal nInstance As Long) As Long
Public Declare Function StopMeasure LIB "maiv2dll.DLL" (ByVal nInstance As Long) As Long
Public Declare Function SetStreamingMode LIB "maiv2dll.DLL" (ByVal nInstance As Long, ByVal nStreamingMode As Long) As Long
Public Declare Function SetDataBufferModes LIB "maiv2dll.DLL" (ByVal nInstance As Long, ByVal bGetADDataInStreamBuffer As Long, ByVal bGetCTDataInStreamBuffer As Long, ByVal bGetTTLDataInStreamBuffer As Long) As Long
Public Declare Function SetRunningMode LIB "maiv2dll.DLL" (ByVal nInstance As Long, ByVal MasterSlave As Long) As Long
Public Declare Function SetRunningModeEx LIB "maiv2dll.DLL" (ByVal nInstance As Long, ByVal MasterSlave As Long, ByVal AIMultipleMastersAllowed As Boolean) As Long
Public Declare Function EnableSoftwareClock LIB "maiv2dll.DLL" (ByVal nInstance As Long, ByVal AIFetchADDataInUserMode As Long, ByVal =1 As Long) As Long
Public Declare Function ConfigCard LIB "maiv2dll.DLL" (ByVal nInstance As Long, ByVal TriggerExtern As Long, ByVal ExternEdge As Long, ByVal DifferenzMode As Long, ByVal p4 As Long) As Long
Public Declare Function SetGlobalTriggerValues LIB "maiv2dll.DLL" (ByVal nInstance As Long, ByVal nPreTrigger As Long, ByVal nPostTrigger As Long, ByVal nWaitForStartTrigger As Long) As Long
Public Declare Function ConfigMeasure LIB "maiv2dll.DLL" (ByVal nInstance As Long) As Long
Public Declare Function IdentifierDevice LIB "maiv2dll.DLL" (ByVal nInstance As Long) As Long
Public Declare Function IsUSBHighSpeed LIB "maiv2dll.DLL" (ByVal nInstance As Long, ByRef IsUSBHighSpeed As Long) As Long
Public Declare Function RemoteDeviceConnect LIB "maiv2dll.DLL" (ByRef nInstance As Long, ByRef sIPAdress As Byte, ByVal nUDPINPort As Long, ByVal bShowErrorMessage As Boolean, ByRef bIsNewInDevicelist As Boolean) As Long
Public Declare Function RemoteDeviceDisconnect LIB "maiv2dll.DLL" (ByVal nInstance As Long) As Long
Public Declare Function RemoteDevicesSearch LIB "maiv2dll.DLL" () As Long
Public Declare Function RemoteDevicesSearchAndConnectAll LIB "maiv2dll.DLL" () As Long
Public Declare Function RemoteDevicesGetIPFromSearchResult LIB "maiv2dll.DLL" (ByVal nIndex As Long, ByRef sIPv4Address As Byte, ByVal nBuffersize As Long) As Long
Public Declare Function RemoteDeviceGetIPFromPoolHandle LIB "maiv2dll.DLL" (ByVal nInstance As Long, ByRef sIPv4Address As Byte, ByVal nBuffersize As Long, ByRef nTCPPort As Long, ByRef nUDPPort As Long) As Long
Public Declare Function GetCardName LIB "maiv2dll.DLL" (ByVal nInstance As Long) As Long
Public Declare Function GetCardProducer LIB "maiv2dll.DLL" (ByVal nInstance As Long) As Long
Public Declare Function GetCardSeller LIB "maiv2dll.DLL" (ByVal nInstance As Long) As Long
Public Declare Function GetManufacture_Name LIB "maiv2dll.DLL" (ByVal nInstance As Long) As Long
Public Declare Function GetSerialNumber LIB "maiv2dll.DLL" (ByVal nInstance As Long) As Long
Public Declare Function GetCustomer_Name LIB "maiv2dll.DLL" (ByVal nInstance As Long) As Long
Public Declare Function GetCustomer_Number LIB "maiv2dll.DLL" (ByVal nInstance As Long) As Long
Public Declare Function GetCustomer_DateOfPurchase LIB "maiv2dll.DLL" (ByVal nInstance As Long) As Long
Public Declare Function GetADChannels LIB "maiv2dll.DLL" (ByVal nInstance As Long) As Long
Public Declare Function GetADChannelsNumberOfOversamplingModes LIB "maiv2dll.DLL" (ByVal nInstance As Long) As Long
Public Declare Function GetADChannelsNumberOfGainModes LIB "maiv2dll.DLL" (ByVal nInstance As Long) As Long
Public Declare Function GetADSampleWidth LIB "maiv2dll.DLL" (ByVal nInstance As Long) As Long
Public Declare Function GetADSampleRate LIB "maiv2dll.DLL" (ByVal nInstance As Long) As Long
Public Declare Function GetDAChannels LIB "maiv2dll.DLL" (ByVal nInstance As Long) As Long
Public Declare Function GetDASampleWidth LIB "maiv2dll.DLL" (ByVal nInstance As Long) As Long
Public Declare Function GetDASampleRate LIB "maiv2dll.DLL" (ByVal nInstance As Long) As Long
Public Declare Function GetTTLChannels LIB "maiv2dll.DLL" (ByVal nInstance As Long) As Long
Public Declare Function GetTTLSampleWidth LIB "maiv2dll.DLL" (ByVal nInstance As Long) As Long
Public Declare Function GetTTLSampleRate LIB "maiv2dll.DLL" (ByVal nInstance As Long) As Long
Public Declare Function GetCTChannels LIB "maiv2dll.DLL" (ByVal nInstance As Long) As Long
Public Declare Function GetCTSampleWidth LIB "maiv2dll.DLL" (ByVal nInstance As Long) As Long
Public Declare Function GetCTSampleRate LIB "maiv2dll.DLL" (ByVal nInstance As Long) As Long
Public Declare Function GetPWMChannels LIB "maiv2dll.DLL" (ByVal nInstance As Long) As Long
Public Declare Function GetPWMSampleWidth LIB "maiv2dll.DLL" (ByVal nInstance As Long) As Long
Public Declare Function GetPWMSampleRate LIB "maiv2dll.DLL" (ByVal nInstance As Long) As Long
Public Declare Function GetSoftwareExtension LIB "maiv2dll.DLL" (ByVal nInstance As Long, ByRef pSWExtension As Long) As Long
Public Declare Function GetHardwareExtension LIB "maiv2dll.DLL" (ByVal nInstance As Long, ByRef pHWExtension As Long) As Long
Public Declare Function GetDevicePropertyStringA LIB "maiv2dll.DLL" (ByVal nInstance As Long, ByRef pszPropertyName As Long, ByRef pData As Byte, ByRef pcbData As Long) As Long
Public Declare Function GetMeasurementProcessorVersion LIB "maiv2dll.DLL" (ByVal nInstance As Long) As Long
Public Declare Function GetControllerFirmwareVersion LIB "maiv2dll.DLL" (ByVal nInstance As Long) As Long
Public Declare Function GetSystemDriverVersion LIB "maiv2dll.DLL" (ByVal nInstance As Long, ByRef DLLVersion As Byte) As Long
Public Declare Function PrivateFlashDataRead LIB "maiv2dll.DLL" (ByVal nInstance As Long, ByRef PrivateData As Byte, ByVal nLength As Long) As Long
Public Declare Function PrivateFlashDataWrite LIB "maiv2dll.DLL" (ByVal nInstance As Long, ByRef PrivateData As Byte, ByVal nLength As Long) As Long
Public Declare Function PrivateFlashDataClear LIB "maiv2dll.DLL" (ByVal nInstance As Long) As Long
Public Declare Function SetLEDs LIB "maiv2dll.DLL" (ByVal nInstance As Long, ByVal AIRedOrFirstLEDOn As Boolean, ByVal AIGreenOrSecondLEDOn As Boolean, ByVal AIThirdLEDOn As Boolean) As Long
Public Declare Function GetDLLVersion LIB "maiv2dll.DLL" () As Long
Public Declare Function GetLIBVersion LIB "maiv2dll.DLL" () As Long
Public Declare Function GetCardIDBySerial LIB "maiv2dll.DLL" (ByRef Serial As Byte, ByRef nCardID As Long) As Long
Public Declare Function GetDeviceInfo LIB "maiv2dll.DLL" (ByVal nCardID As Long, ByRef nDeviceType As Long, ByRef Serial As Byte) As Long
Public Declare Function GetNumberOfBurstsOnADController LIB "maiv2dll.DLL" (ByVal nCardID As Long, ByRef nNumberOfBursts As Long) As Long
Public Declare Function GetNumberOfBurstsOnCTController LIB "maiv2dll.DLL" (ByVal nCardID As Long, ByRef nNumberOfBursts As Long) As Long
Public Declare Function AlteraRegisterRead LIB "maiv2dll.DLL" (ByVal nCardID As Long, ByVal nAdress As Long, ByRef nRegisterValue As Long) As Long
Public Declare Function AlteraRegisterWrite LIB "maiv2dll.DLL" (ByVal nCardID As Long, ByVal nAdress As Long, ByVal nRegisterValue As Long) As Long
