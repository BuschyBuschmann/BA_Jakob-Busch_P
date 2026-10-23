unit AD_Functions;

interface


function AD_ClearChannelList(nInstance: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'AD_ClearChannelList';
function AD_AddChannelToList(nInstance: Cardinal; nChannel: Cardinal; nOversampling: Cardinal; nGain: Cardinal; nBipolar: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'AD_AddChannelToList';
function AD_GetChannelListSize(nInstance: Cardinal; var nCLSize: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'AD_GetChannelListSize';
function AD_ReadSingleValue(nInstance: Cardinal; nChannel: Cardinal; nOversampling: Cardinal; nGain: Cardinal; nBipolar: Cardinal; var nRawValue: Integer):LongInt; stdcall; external 'maiv2dll.DLL' name 'AD_ReadSingleValue';
function AD_ReadSingleValueExt(nInstance: Cardinal; nChannel: Cardinal; nOversampling: Cardinal; nGain: Cardinal; nBipolar: Cardinal; var nRawValue: Integer; var dVoltage: Double; var fVoltage: Single):LongInt; stdcall; external 'maiv2dll.DLL' name 'AD_ReadSingleValueExt';
function AD_ReadSingleVoltage(nInstance: Cardinal; nChannel: Cardinal; nOversampling: Cardinal; nGain: Cardinal; nBipolar: Cardinal; var bVoltage: Double):LongInt; stdcall; external 'maiv2dll.DLL' name 'AD_ReadSingleVoltage';
function AD_SetFrequency(nInstance: Cardinal; fFrequency: Double):LongInt; stdcall; external 'maiv2dll.DLL' name 'AD_SetFrequency';
function AD_GetFrequency(nInstance: Cardinal; var fFrequency: Double):LongInt; stdcall; external 'maiv2dll.DLL' name 'AD_GetFrequency';
function AD_ReadLastBurst(nInstance: Cardinal; RawData: PInteger; Value: PDouble; var nNumberOfValues: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'AD_ReadLastBurst';
function AD_ReadData(nInstance: Cardinal; nChannelListEntry: Cardinal; RawData: PInteger; Value: PDouble; var nValuesPerChannel: Cardinal; bPartBlock: Cardinal; bSkipData: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'AD_ReadData';
function AD_ReadDataExt(nInstance: Cardinal; nChannelListEntry: Cardinal; pRawData: PInteger; pDoubleValues: PDouble; pFloatValues: PSingle; var nValuesPerChannel: Cardinal; bPartBlock: Cardinal; var AODateTimeT0: Int64; var AODateTimeDeltaT: Double):LongInt; stdcall; external 'maiv2dll.DLL' name 'AD_ReadDataExt';
function AD_ReadBinaryData(nInstance: Cardinal; BinaryData: PByte; var nLength: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'AD_ReadBinaryData';
function AD_GetBinaryWordsizePerChannel(nInstance: Cardinal; var nSingleADWordSize: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'AD_GetBinaryWordsizePerChannel';
function AD_ConvertBinaryBurstToDoublePerChannel(nInstance: Cardinal; BinaryData: PByte; var nConvertedBurst: Double):LongInt; stdcall; external 'maiv2dll.DLL' name 'AD_ConvertBinaryBurstToDoublePerChannel';
function AD_GetStreamPipeLevel(nInstance: Cardinal; var fStreamPipeLevel: Double):LongInt; stdcall; external 'maiv2dll.DLL' name 'AD_GetStreamPipeLevel';
function AD_GetNumberOfValues(nInstance: Cardinal; var nNumberOfValues: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'AD_GetNumberOfValues';
function AD_StartMeasure(nInstance: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'AD_StartMeasure';
function AD_StopMeasure(nInstance: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'AD_StopMeasure';
function AD_SetIEPE(nInstance: Cardinal; nChannel: Cardinal; nIEPEMode: Cardinal; bGain: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'AD_SetIEPE';
function AD_SetIEPEOnAudioModul(nInstance: Cardinal; nChannel: Cardinal; bIEPEOn: Cardinal; bDCOn: Cardinal; bCurrentSourceOn: Cardinal; bGainOn: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'AD_SetIEPEOnAudioModul';
function AD_SetEventToBeRaisedWhenNumberOfBurstsAvailable(nInstance: Cardinal; hEventHandle: Pointer; nNumberOfBursts: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'AD_SetEventToBeRaisedWhenNumberOfBurstsAvailable';
function AD_Audio_SetHPFilter(nInstance: Cardinal; nChannel: Cardinal; bFilterOn: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'AD_Audio_SetHPFilter';
function AD_Audio_SetHPFilterResponse(nInstance: Cardinal; nADCNr: Cardinal; bLowGroupDelayResponseOn: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'AD_Audio_SetHPFilterResponse';
function AD_ResetIEPE(nInstance: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'AD_ResetIEPE';
function AD_GetIEPEType(nInstance: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'AD_GetIEPEType';
function AD_GetCorrectionValue(nInstance: Cardinal; nChannel: Cardinal; var fValue: Single):LongInt; stdcall; external 'maiv2dll.DLL' name 'AD_GetCorrectionValue';
function AD_SetCorrectionValue(nInstance: Cardinal; nChannel: Cardinal; fValue: Single):LongInt; stdcall; external 'maiv2dll.DLL' name 'AD_SetCorrectionValue';
function AD_WriteCorrectionValuesToDevice(nInstance: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'AD_WriteCorrectionValuesToDevice';

implementation

end.
