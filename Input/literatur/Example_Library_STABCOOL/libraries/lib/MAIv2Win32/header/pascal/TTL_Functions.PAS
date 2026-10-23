unit TTL_Functions;

interface


function TTL_ClearChannelList(nInstance: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'TTL_ClearChannelList';
function TTL_AddChannelToList(nInstance: Cardinal; nChannel: Cardinal; bToADList: Boolean; nDigitalType: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'TTL_AddChannelToList';
function TTL_GetChannelListSize(nInstance: Cardinal; var nCLSize: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'TTL_GetChannelListSize';
function TTL_SetFrequency(nInstance: Cardinal; fFrequency: Double):LongInt; stdcall; external 'maiv2dll.DLL' name 'TTL_SetFrequency';
function TTL_SetChannelDirection(nInstance: Cardinal; nChannel: Cardinal; nDirectionValue: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'TTL_SetChannelDirection';
function TTL_GetChannelDirection(nInstance: Cardinal; nChannel: Cardinal; var nDirection: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'TTL_GetChannelDirection';
function TTL_GetIsChannelDirectionFixed(nInstance: Cardinal; nChannel: Cardinal; var nDirectionFixed: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'TTL_GetIsChannelDirectionFixed';
function TTL_ReadData(nInstance: Cardinal; pBuffer: PCardinal; var nNumberOfBursts: Cardinal; bPartBlock: Cardinal; bSkipData: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'TTL_ReadData';
function TTL_ReadData8(nInstance: Cardinal; var pBuffer: Byte; var nNUmberOfBursts: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'TTL_ReadData8';
function TTL_ReadData16(nInstance: Cardinal; var pBuffer: Word; var nNUmberOfBursts: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'TTL_ReadData16';
function TTL_ReadData32(nInstance: Cardinal; var pBuffer: Cardinal; var nNUmberOfBursts: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'TTL_ReadData32';
function TTL_ReadData64(nInstance: Cardinal; var pBuffer: UInt64; var nNUmberOfBursts: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'TTL_ReadData64';
function TTL_GetBurstSize(nInstance: Cardinal; var nBurstSizeInBytes: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'TTL_GetBurstSize';
function TTL_ReadDataExt(nInstance: Cardinal; var pBuffer: Byte; var nNUmberOfBursts: Cardinal; nBurstSizeInBytes: Cardinal; var AODateTimeT0: Int64; var AODateTimeDeltaT: Double):LongInt; stdcall; external 'maiv2dll.DLL' name 'TTL_ReadDataExt';
function TTL_ReadPort(nInstance: Cardinal; nPort: Cardinal; var nPortValue: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'TTL_ReadPort';
function TTL_WritePort(nInstance: Cardinal; nPort: Cardinal; nPortValue: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'TTL_WritePort';
function TTL_ReadBit(nInstance: Cardinal; nChannel: Cardinal; var nBit: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'TTL_ReadBit';
function TTL_WriteBit(nInstance: Cardinal; nChannel: Cardinal; nBit: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'TTL_WriteBit';
function TTL_GetStreamPipeLevel(nInstance: Cardinal; var fStreamPipeLevel: Double):LongInt; stdcall; external 'maiv2dll.DLL' name 'TTL_GetStreamPipeLevel';
function TTL_GetNumberOfValues(nInstance: Cardinal; var nNumberOfValues: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'TTL_GetNumberOfValues';
function TTL_InitializeTargetSettings(nInstance: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'TTL_InitializeTargetSettings';
function TTL_StartMeasure(nInstance: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'TTL_StartMeasure';
function TTL_StopMeasure(nInstance: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'TTL_StopMeasure';
function TTL_GetPortInfos(nInstance: Cardinal; var NumberOfPorts: Cardinal; var PortWidth: Cardinal; var NumberOfDigIn: Cardinal; var NumberOfDigOut: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'TTL_GetPortInfos';

implementation

end.
