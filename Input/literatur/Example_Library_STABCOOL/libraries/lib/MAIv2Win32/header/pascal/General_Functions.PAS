unit General_Functions;

interface


function ClearAllChannelLists(nInstance: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'ClearAllChannelLists';
function ResetDevice(nInstance: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'ResetDevice';
function LoadFirmware(nInstance: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'LoadFirmware';
function StartMeasure(nInstance: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'StartMeasure';
function StopMeasure(nInstance: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'StopMeasure';
function SetStreamingMode(nInstance: Cardinal; nStreamingMode: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'SetStreamingMode';
function SetDataBufferModes(nInstance: Cardinal; bGetADDataInStreamBuffer: Cardinal; bGetCTDataInStreamBuffer: Cardinal; bGetTTLDataInStreamBuffer: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'SetDataBufferModes';
function SetRunningMode(nInstance: Cardinal; MasterSlave: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'SetRunningMode';
function SetRunningModeEx(nInstance: Cardinal; MasterSlave: Cardinal; AIMultipleMastersAllowed: Boolean):LongInt; stdcall; external 'maiv2dll.DLL' name 'SetRunningModeEx';
function EnableSoftwareClock(nInstance: Cardinal; AIFetchADDataInUserMode: Cardinal; =1: uintAISoftwareADBufferSizeInBursts):LongInt; stdcall; external 'maiv2dll.DLL' name 'EnableSoftwareClock';
function ConfigCard(nInstance: Cardinal; TriggerExtern: Cardinal; ExternEdge: Cardinal; DifferenzMode: Cardinal; p4: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'ConfigCard';
function SetGlobalTriggerValues(nInstance: Cardinal; nPreTrigger: Cardinal; nPostTrigger: Cardinal; nWaitForStartTrigger: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'SetGlobalTriggerValues';
function ConfigMeasure(nInstance: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'ConfigMeasure';
function IdentifierDevice(nInstance: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'IdentifierDevice';
function IsUSBHighSpeed(nInstance: Cardinal; var IsUSBHighSpeed: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'IsUSBHighSpeed';
function RemoteDeviceConnect(var nInstance: Cardinal; var sIPAdress: AnsiChar; nUDPINPort: Integer; bShowErrorMessage: Boolean; var bIsNewInDevicelist: Boolean):LongInt; stdcall; external 'maiv2dll.DLL' name 'RemoteDeviceConnect';
function RemoteDeviceDisconnect(nInstance: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'RemoteDeviceDisconnect';
function RemoteDevicesSearch():LongInt; stdcall; external 'maiv2dll.DLL' name 'RemoteDevicesSearch';
function RemoteDevicesSearchAndConnectAll():LongInt; stdcall; external 'maiv2dll.DLL' name 'RemoteDevicesSearchAndConnectAll';
function RemoteDevicesGetIPFromSearchResult(nIndex: Integer; sIPv4Address: PAnsiChar; nBuffersize: Integer):LongInt; stdcall; external 'maiv2dll.DLL' name 'RemoteDevicesGetIPFromSearchResult';
function RemoteDeviceGetIPFromPoolHandle(nInstance: Cardinal; sIPv4Address: PAnsiChar; nBuffersize: Integer; var nTCPPort: Cardinal; var nUDPPort: Integer):LongInt; stdcall; external 'maiv2dll.DLL' name 'RemoteDeviceGetIPFromPoolHandle';
function GetCardName(nInstance: Cardinal):PAnsiChar; stdcall; external 'maiv2dll.DLL' name 'GetCardName';
function GetCardProducer(nInstance: Cardinal):PAnsiChar; stdcall; external 'maiv2dll.DLL' name 'GetCardProducer';
function GetCardSeller(nInstance: Cardinal):PAnsiChar; stdcall; external 'maiv2dll.DLL' name 'GetCardSeller';
function GetManufacture_Name(nInstance: Cardinal):PAnsiChar; stdcall; external 'maiv2dll.DLL' name 'GetManufacture_Name';
function GetSerialNumber(nInstance: Cardinal):PAnsiChar; stdcall; external 'maiv2dll.DLL' name 'GetSerialNumber';
function GetCustomer_Name(nInstance: Cardinal):PAnsiChar; stdcall; external 'maiv2dll.DLL' name 'GetCustomer_Name';
function GetCustomer_Number(nInstance: Cardinal):PAnsiChar; stdcall; external 'maiv2dll.DLL' name 'GetCustomer_Number';
function GetCustomer_DateOfPurchase(nInstance: Cardinal):PAnsiChar; stdcall; external 'maiv2dll.DLL' name 'GetCustomer_DateOfPurchase';
function GetADChannels(nInstance: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'GetADChannels';
function GetADChannelsNumberOfOversamplingModes(nInstance: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'GetADChannelsNumberOfOversamplingModes';
function GetADChannelsNumberOfGainModes(nInstance: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'GetADChannelsNumberOfGainModes';
function GetADSampleWidth(nInstance: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'GetADSampleWidth';
function GetADSampleRate(nInstance: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'GetADSampleRate';
function GetDAChannels(nInstance: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'GetDAChannels';
function GetDASampleWidth(nInstance: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'GetDASampleWidth';
function GetDASampleRate(nInstance: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'GetDASampleRate';
function GetTTLChannels(nInstance: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'GetTTLChannels';
function GetTTLSampleWidth(nInstance: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'GetTTLSampleWidth';
function GetTTLSampleRate(nInstance: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'GetTTLSampleRate';
function GetCTChannels(nInstance: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'GetCTChannels';
function GetCTSampleWidth(nInstance: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'GetCTSampleWidth';
function GetCTSampleRate(nInstance: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'GetCTSampleRate';
function GetPWMChannels(nInstance: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'GetPWMChannels';
function GetPWMSampleWidth(nInstance: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'GetPWMSampleWidth';
function GetPWMSampleRate(nInstance: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'GetPWMSampleRate';
function GetSoftwareExtension(nInstance: Cardinal; var pSWExtension: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'GetSoftwareExtension';
function GetHardwareExtension(nInstance: Cardinal; var pHWExtension: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'GetHardwareExtension';
function GetDevicePropertyStringA(nInstance: Cardinal; var pszPropertyName: AnsiChar; var pData: AnsiChar; var pcbData: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'GetDevicePropertyStringA';
function GetMeasurementProcessorVersion(nInstance: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'GetMeasurementProcessorVersion';
function GetControllerFirmwareVersion(nInstance: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'GetControllerFirmwareVersion';
function GetSystemDriverVersion(nInstance: Cardinal; DLLVersion: PAnsiChar):LongInt; stdcall; external 'maiv2dll.DLL' name 'GetSystemDriverVersion';
function PrivateFlashDataRead(nInstance: Cardinal; PrivateData: PByte; nLength: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'PrivateFlashDataRead';
function PrivateFlashDataWrite(nInstance: Cardinal; PrivateData: PByte; nLength: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'PrivateFlashDataWrite';
function PrivateFlashDataClear(nInstance: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'PrivateFlashDataClear';
function SetLEDs(nInstance: Cardinal; AIRedOrFirstLEDOn: Boolean; AIGreenOrSecondLEDOn: Boolean; AIThirdLEDOn: Boolean):LongInt; stdcall; external 'maiv2dll.DLL' name 'SetLEDs';
function GetDLLVersion():PAnsiChar; stdcall; external 'maiv2dll.DLL' name 'GetDLLVersion';
function GetLIBVersion():PAnsiChar; stdcall; external 'maiv2dll.DLL' name 'GetLIBVersion';
function GetCardIDBySerial(Serial: PAnsiChar; var nCardID: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'GetCardIDBySerial';
function GetDeviceInfo(nCardID: Cardinal; var nDeviceType: Integer; Serial: PAnsiChar):LongInt; stdcall; external 'maiv2dll.DLL' name 'GetDeviceInfo';
function GetNumberOfBurstsOnADController(nCardID: Cardinal; var nNumberOfBursts: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'GetNumberOfBurstsOnADController';
function GetNumberOfBurstsOnCTController(nCardID: Cardinal; var nNumberOfBursts: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'GetNumberOfBurstsOnCTController';
function AlteraRegisterRead(nCardID: Cardinal; nAdress: Integer; var nRegisterValue: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'AlteraRegisterRead';
function AlteraRegisterWrite(nCardID: Cardinal; nAdress: Integer; nRegisterValue: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'AlteraRegisterWrite';

implementation

end.
