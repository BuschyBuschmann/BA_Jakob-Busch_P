unit PoolFunctions;

interface


function GetFirstDevice():LongInt; stdcall; external 'maiv2dll.DLL' name 'GetFirstDevice';
function GetNumberOfDevices():LongInt; stdcall; external 'maiv2dll.DLL' name 'GetNumberOfDevices';
function GetDeviceHandles(Handles: PCardinal; var iHandleCount: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'GetDeviceHandles';
function GetDeviceHandlesMultichoiceETH(Handles: PCardinal; var iHandleCount: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'GetDeviceHandlesMultichoiceETH';
function GetDeviceHandlesMultichoicePCI(Handles: PCardinal; var iHandleCount: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'GetDeviceHandlesMultichoicePCI';
function GetDeviceHandlesMultichoiceUSB(Handles: PCardinal; var iHandleCount: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'GetDeviceHandlesMultichoiceUSB';
function GetDeviceHandlesMultichoiceUSBBasic(Handles: PCardinal; var iHandleCount: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'GetDeviceHandlesMultichoiceUSBBasic';
function GetFirstDeviceByType(DeviceType: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'GetFirstDeviceByType';
function OpenDevice(nInstance: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'OpenDevice';
function CloseDevice(nInstance: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'CloseDevice';
function IsDeviceOpen(nInstance: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'IsDeviceOpen';
function GetErrorDescription(nInstance: Cardinal; ErrorNumber: Integer; ErrorDescription: PAnsiChar):LongInt; stdcall; external 'maiv2dll.DLL' name 'GetErrorDescription';
function SetGPCIFile(AIFilePath: PAnsiChar; nLength: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'SetGPCIFile';
function GetGPCIFilePath():PAnsiChar; stdcall; external 'maiv2dll.DLL' name 'GetGPCIFilePath';
function ReCreateDeviceListOmittingDeviceTypes(AICreatePCI: Boolean; AICreateUSBMC4: Boolean; CreateUSBBasic: Boolean):LongInt; stdcall; external 'maiv2dll.DLL' name 'ReCreateDeviceListOmittingDeviceTypes';
function ShowMessageBoxOnDeviceCreationError(AIShowMsgBox: Boolean):LongInt; stdcall; external 'maiv2dll.DLL' name 'ShowMessageBoxOnDeviceCreationError';
function GetNumberOfUninitializedDevices():LongInt; stdcall; external 'maiv2dll.DLL' name 'GetNumberOfUninitializedDevices';
function GetDeviceCreationErrorMessage(nNumber: Cardinal; AOText: PAnsiChar; nTextBufferLength: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'GetDeviceCreationErrorMessage';

implementation

end.
