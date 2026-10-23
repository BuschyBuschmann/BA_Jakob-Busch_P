unit DA_Functions;

interface


function DA_SetRange(nInstance: Cardinal; nRange: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'DA_SetRange';
function DA_ClearChannelList(nInstance: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'DA_ClearChannelList';
function DA_AddChannelToList(nInstance: Cardinal; nChannel: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'DA_AddChannelToList';
function DA_GetChannelListSize(nInstance: Cardinal; var nCLSize: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'DA_GetChannelListSize';
function DA_SetFrequency(nInstance: Cardinal; fFrequency: Double):LongInt; stdcall; external 'maiv2dll.DLL' name 'DA_SetFrequency';
function DA_StartOutput(nInstance: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'DA_StartOutput';
function DA_StopOutput(nInstance: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'DA_StopOutput';
function DA_WriteChannelRaw(nInstance: Cardinal; nChannel: Cardinal; RawValue: Integer):LongInt; stdcall; external 'maiv2dll.DLL' name 'DA_WriteChannelRaw';
function DA_WriteChannelVoltage(nInstance: Cardinal; nChannel: Cardinal; VoltageValue: Double):LongInt; stdcall; external 'maiv2dll.DLL' name 'DA_WriteChannelVoltage';
function DA_WriteRawData(nInstance: Cardinal; nChannelListEntry: Cardinal; pBuffer: PInteger; var nLength: Cardinal; bPartBlock: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'DA_WriteRawData';
function DA_WriteScaledData(nInstance: Cardinal; nChannelListEntry: Cardinal; fScaledValues: PDouble; var nLength: Cardinal; bPartBlock: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'DA_WriteScaledData';
function DA_GetFifoState(nInstance: Cardinal; nChannel: Cardinal; var nNumberOfValues: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'DA_GetFifoState';
function DA_Audio_SetMonauralMode(nInstance: Cardinal; bLoopbackModeOn: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'DA_Audio_SetMonauralMode';
function DA_Audio_SetADLoopbackMode(nInstance: Cardinal; bLoopbackModeOn: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'DA_Audio_SetADLoopbackMode';

implementation

end.
