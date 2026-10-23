////////////////////////////////////////////////////////////////////////////////////////////////////
/// <category>	Device Funktionen. </category>
/// <categoryE>	device functions. </categoryE>
///
///
/// <filesummary>	zur Steuerung der nicht kanaltyp-spezifischen Kartenfunktionen stehen diese Funktionen zur Verfügung: </filesummary>
/// <filesummaryE>	for controlling the devices non channel dependent features these functions are available: </filesummaryE>
////////////////////////////////////////////////////////////////////////////////////////////////////

// general functions
MAIV2DLL_EXPORT		ClearAllChannelLists(uint nInstance);
MAIV2DLL_EXPORT     ResetDevice(uint nInstance);
MAIV2DLL_EXPORT		LoadFirmware(uint nInstance);
MAIV2DLL_EXPORT		StartMeasure(uint nInstance);
MAIV2DLL_EXPORT		StopMeasure(uint nInstance);
MAIV2DLL_EXPORT		SetStreamingMode(uint nInstance, uint nStreamingMode);
MAIV2DLL_EXPORT		SetDataBufferModes(uint nInstance, uint bGetADDataInStreamBuffer, uint bGetCTDataInStreamBuffer, uint bGetTTLDataInStreamBuffer);
MAIV2DLL_EXPORT		SetRunningMode(uint nInstance, uint MasterSlave);
MAIV2DLL_EXPORT		SetRunningModeEx(uint nInstance, uint MasterSlave, bool AIMultipleMastersAllowed);
MAIV2DLL_EXPORT		EnableSoftwareClock(uint nInstance, uint AIFetchADDataInUserMode, uint AISoftwareADBufferSizeInBursts =1);
MAIV2DLL_EXPORT		ConfigCard(uint nInstance, uint TriggerExtern, uint ExternEdge, uint DifferenzMode, uint p4);
MAIV2DLL_EXPORT		SetGlobalTriggerValues(uint nInstance, uint nPreTrigger, uint nPostTrigger, uint nWaitForStartTrigger);
MAIV2DLL_EXPORT		ConfigMeasure(uint nInstance);
MAIV2DLL_EXPORT		IdentifierDevice(uint nInstance);
MAIV2DLL_EXPORT		IsUSBHighSpeed(uint nInstance, uint* IsUSBHighSpeed);

// remoteDevice Funktionnen
MAIV2DLL_EXPORT		RemoteDeviceConnect(uint* nInstance, char* sIPAdress, int nUDPINPort, bool bShowErrorMessage , bool* bIsNewInDevicelist);
MAIV2DLL_EXPORT		RemoteDeviceDisconnect(uint nInstance);
MAIV2DLL_EXPORT		RemoteDevicesSearch();
MAIV2DLL_EXPORT		RemoteDevicesSearchAndConnectAll();
MAIV2DLL_EXPORT		RemoteDevicesGetIPFromSearchResult(int nIndex, char sIPv4Address[], int nBuffersize);
MAIV2DLL_EXPORT		RemoteDeviceGetIPFromPoolHandle(uint nInstance, char sIPv4Address[], int nBuffersize, uint* nTCPPort, int* nUDPPort);


// Eigenschaften der Karte
MAIV2DLL_EXPORT_CHAR	GetCardName(uint nInstance);
MAIV2DLL_EXPORT_CHAR	GetCardProducer(uint nInstance);
MAIV2DLL_EXPORT_CHAR	GetCardSeller(uint nInstance);
MAIV2DLL_EXPORT_CHAR	GetManufacture_Name(uint nInstance);
MAIV2DLL_EXPORT_CHAR	GetSerialNumber(uint nInstance);
MAIV2DLL_EXPORT_CHAR	GetCustomer_Name(uint nInstance);
MAIV2DLL_EXPORT_CHAR	GetCustomer_Number(uint nInstance);
MAIV2DLL_EXPORT_CHAR	GetCustomer_DateOfPurchase(uint nInstance);
MAIV2DLL_EXPORT		GetADChannels(uint nInstance);
MAIV2DLL_EXPORT		GetADChannelsNumberOfOversamplingModes(uint nInstance);
MAIV2DLL_EXPORT		GetADChannelsNumberOfGainModes(uint nInstance);
MAIV2DLL_EXPORT		GetADSampleWidth(uint nInstance);
MAIV2DLL_EXPORT		GetADSampleRate(uint nInstance);
MAIV2DLL_EXPORT		GetDAChannels(uint nInstance);
MAIV2DLL_EXPORT		GetDASampleWidth(uint nInstance);
MAIV2DLL_EXPORT		GetDASampleRate(uint nInstance);
MAIV2DLL_EXPORT		GetTTLChannels(uint nInstance);
MAIV2DLL_EXPORT		GetTTLSampleWidth(uint nInstance);
MAIV2DLL_EXPORT		GetTTLSampleRate(uint nInstance);
MAIV2DLL_EXPORT		GetCTChannels(uint nInstance);
MAIV2DLL_EXPORT		GetCTSampleWidth(uint nInstance);
MAIV2DLL_EXPORT		GetCTSampleRate(uint nInstance);
MAIV2DLL_EXPORT		GetPWMChannels(uint nInstance);
MAIV2DLL_EXPORT		GetPWMSampleWidth(uint nInstance);
MAIV2DLL_EXPORT		GetPWMSampleRate(uint nInstance);
MAIV2DLL_EXPORT		GetSoftwareExtension(uint nInstance, uint* pSWExtension);
MAIV2DLL_EXPORT		GetHardwareExtension(uint nInstance, uint* pHWExtension);
MAIV2DLL_EXPORT		GetDevicePropertyStringA(uint nInstance, const char* pszPropertyName, char* pData, uint* pcbData);

MAIV2DLL_EXPORT		GetMeasurementProcessorVersion(uint nInstance);
MAIV2DLL_EXPORT		GetControllerFirmwareVersion(uint nInstance);
MAIV2DLL_EXPORT		GetSystemDriverVersion(uint nInstance, char DLLVersion[]);
MAIV2DLL_EXPORT		PrivateFlashDataRead(uint nInstance, uchar PrivateData[], uint nLength);
MAIV2DLL_EXPORT		PrivateFlashDataWrite(uint nInstance, uchar PrivateData[], uint nLength);
MAIV2DLL_EXPORT		PrivateFlashDataClear(uint nInstance);

MAIV2DLL_EXPORT		SetLEDs(uint nInstance,bool AIRedOrFirstLEDOn,bool AIGreenOrSecondLEDOn,bool AIThirdLEDOn);

MAIV2DLL_EXPORT_CHAR	GetDLLVersion();
MAIV2DLL_EXPORT_CHAR	GetLIBVersion();
MAIV2DLL_EXPORT		GetCardIDBySerial(char Serial[], uint * nCardID);
MAIV2DLL_EXPORT		GetDeviceInfo(uint nCardID, int * nDeviceType, char Serial[]);


MAIV2DLL_EXPORT		GetNumberOfBurstsOnADController(uint nCardID, uint * nNumberOfBursts);
MAIV2DLL_EXPORT		GetNumberOfBurstsOnCTController(uint nCardID, uint * nNumberOfBursts);
MAIV2DLL_EXPORT		AlteraRegisterRead(uint nCardID, int   nAdress,  uint * nRegisterValue);
MAIV2DLL_EXPORT		AlteraRegisterWrite(uint nCardID, int   nAdress,  uint  nRegisterValue);

//#ifdef DEBUG
//MAIV2DLL_EXPORT		InternalFlashDataRead(uint nInstance, uint EEPromOffsetStart, uchar PrivateData[], uint nLength);
//MAIV2DLL_EXPORT		InternalFlashDataWrite(uint nInstance, uint EEPromOffsetStart, uchar PrivateData[], uint nLength);
//MAIV2DLL_EXPORT		InternalFlashDataClear(uint nInstance, uint EEPromOffsetStart);
//#endif



