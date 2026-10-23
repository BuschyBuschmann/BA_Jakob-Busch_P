unit CT_Functions;

interface


function CT_ClearChannelList(nInstance: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'CT_ClearChannelList';
function CT_AddChannelToList(nInstance: Cardinal; nChannel: Cardinal; bToADChannellist: Boolean):LongInt; stdcall; external 'maiv2dll.DLL' name 'CT_AddChannelToList';
function CT_GetChannelListSize(nInstance: Cardinal; var nCLSize: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'CT_GetChannelListSize';
function CT_SetFrequency(nInstance: Cardinal; fFreqency: Double):LongInt; stdcall; external 'maiv2dll.DLL' name 'CT_SetFrequency';
function CT_GetFrequency(nInstance: Cardinal; var fFrequency: Double):LongInt; stdcall; external 'maiv2dll.DLL' name 'CT_GetFrequency';
function CT_ScaleData(nInstance: Cardinal; nChannelListEntry: Cardinal; pInBuffer: PInteger; pOutBuffer: PDouble; nNumberOfValues: Cardinal; var ARFirstLastValue: Integer):LongInt; stdcall; external 'maiv2dll.DLL' name 'CT_ScaleData';
function CT_ReadData(nInstance: Cardinal; nChannelListEntry: Cardinal; pBuffer: PCardinal; var nNumberOfValues: Cardinal; bPartBlock: Cardinal; bSkipData: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'CT_ReadData';
function CT_ReadDataExt(nInstance: Cardinal; nChannelListEntry: Cardinal; pBuffer: PCardinal; var nNumberOfValues: Cardinal; bPartBlock: Cardinal; var AODateTimeT0: Int64; var AODateTimeDeltaT: Double):LongInt; stdcall; external 'maiv2dll.DLL' name 'CT_ReadDataExt';
function CT_ReadSingleValue(nInstance: Cardinal; nChannel: Cardinal; var SingleValue: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'CT_ReadSingleValue';
function CT_GetStreamPipeLevel(nInstance: Cardinal; var fStreamPipeLevel: Double):LongInt; stdcall; external 'maiv2dll.DLL' name 'CT_GetStreamPipeLevel';
function CT_GetNumberOfValues(nInstance: Cardinal; var nNumberOfValues: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'CT_GetNumberOfValues';
function CT_StartMeasure(nInstance: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'CT_StartMeasure';
function CT_StopMeasure(nInstance: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'CT_StopMeasure';
function CT_GetIncrementalCounterDirections(nInstance: Cardinal; var nDirectionValue: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'CT_GetIncrementalCounterDirections';
function CT_SetCounterParameter(nInstance: Cardinal; nChannelListEntry: Cardinal; eCOUNTERPARAMETER: Cardinal; nParameterValue: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'CT_SetCounterParameter';
function CT_GetCounterParameter(nInstance: Cardinal; nChannelListEntry: Cardinal; eCOUNTERPARAMETER: Cardinal; var nParameterValue: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'CT_GetCounterParameter';
function CT_GetCounterParametersForMode(nInstance: Cardinal; eCOUNTERMODE: Cardinal; var AvailableCounterParameters: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'CT_GetCounterParametersForMode';
function CT_GetCounterParameterBoundaries(nInstance: Cardinal; eCOUNTERPARAMETER: Cardinal; var nMinValue: Cardinal; var nMaxValue: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'CT_GetCounterParameterBoundaries';
function CT_GetAvailableCounterModes(nInstance: Cardinal; nChannel: Cardinal; var eCOUNTERMODES: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'CT_GetAvailableCounterModes';
function CT_SetCounterMode(nInstance: Cardinal; nChannelListEntry: Cardinal; eCOUNTERMODE: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'CT_SetCounterMode';
function CT_GetCounterMode(nInstance: Cardinal; nChannelListEntry: Cardinal; var eCOUNTERMODE: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'CT_GetCounterMode';
function CT_ImpulseCounter(nInstance: Cardinal; nChannel: Cardinal; nPresetValue: Cardinal; nUpDown: Cardinal; nEdge: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'CT_ImpulseCounter';
function CT_FrequencyCounter(nInstance: Cardinal; nChannel: Cardinal; nResolution: Cardinal; nEdge: Cardinal; nEachPeriod: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'CT_FrequencyCounter';
function CT_PeriodCounter(nInstance: Cardinal; nChannel: Cardinal; nResolution: Cardinal; nEdge: Cardinal; nEachPeriod: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'CT_PeriodCounter';
function CT_PulswidthCounter(nInstance: Cardinal; nChannel: Cardinal; nResolution: Cardinal; nEdge: Cardinal; nEachPeriod: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'CT_PulswidthCounter';
function CT_IncrementalCounter(nInstance: Cardinal; nChannel: Cardinal; nResolution: Cardinal; nEdge: Cardinal; nSoftwareReset: Cardinal; nHardwareReset: Cardinal; nHWResetEdge: Cardinal; nInterpolation: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'CT_IncrementalCounter';
function CT_IncrementalCounterExtensionTime(nInstance: Cardinal; nChannel: Cardinal; nResolution: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'CT_IncrementalCounterExtensionTime';
function CT_IncrementalCounterExtensionFlow(nInstance: Cardinal; nChannel: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'CT_IncrementalCounterExtensionFlow';
function CT_UpDownCounter(nInstance: Cardinal; nChannel: Cardinal; nPresetValue: Cardinal; nUpDown: Cardinal; nEdge: Cardinal; nSoftwareReset: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'CT_UpDownCounter';
function CT_SetCounterParameter_SingleValueMode(nInstance: Cardinal; nChannelNumber: Cardinal; eCOUNTERPARAMETER: Cardinal; nParameterValue: Integer):LongInt; stdcall; external 'maiv2dll.DLL' name 'CT_SetCounterParameter_SingleValueMode';
function CT_GetCounterParameter_SingleValueMode(nInstance: Cardinal; nChannelNumber: Cardinal; eCOUNTERPARAMETER: Cardinal; var nParameterValue: Integer):LongInt; stdcall; external 'maiv2dll.DLL' name 'CT_GetCounterParameter_SingleValueMode';
function CT_SetCounterMode_SingleValueMode(nInstance: Cardinal; nChannelNumber: Cardinal; eCOUNTERMODE: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'CT_SetCounterMode_SingleValueMode';
function CT_GetCounterMode_SingleValueMode(nInstance: Cardinal; nChannelNumber: Cardinal; var eCOUNTERMODE: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'CT_GetCounterMode_SingleValueMode';
function CT_Reset(nInstance: Cardinal; nHardwareChannelNumber: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'CT_Reset';

implementation

end.
