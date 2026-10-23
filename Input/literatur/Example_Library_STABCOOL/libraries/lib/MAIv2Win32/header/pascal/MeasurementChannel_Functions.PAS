unit MeasurementChannel_Functions;

interface

uses
	MAI_Types;

function MeasurementChannel_GetNumberOfValues(nInstance: Cardinal; eChannelType: TMeasurementChannelType; nChannelListEntry: Cardinal; var nNumberOfValues: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'MeasurementChannel_GetNumberOfValues';
function MeasurementChannel_ReadDataAsUInt32(nInstance: Cardinal; ChannelType: TMeasurementChannelType; nChannelListEntry: Integer; pData: PCardinal; var nNumberOfValues: Cardinal; bPartBlock: Cardinal; var DateTimeT0: Int64; var DateTimeDeltaT: Double):LongInt; stdcall; external 'maiv2dll.DLL' name 'MeasurementChannel_ReadDataAsUInt32';
function MeasurementChannel_ReadDataAsDouble(nInstance: Cardinal; ChannelType: TMeasurementChannelType; nChannelListEntry: Integer; pData: PDouble; var nNumberOfValues: Cardinal; bPartBlock: Cardinal; var DateTimeT0: Int64; var DateTimeDeltaT: Double):LongInt; stdcall; external 'maiv2dll.DLL' name 'MeasurementChannel_ReadDataAsDouble';

implementation

end.
