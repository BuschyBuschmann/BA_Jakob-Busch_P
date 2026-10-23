unit Realtime_Functions;

interface


function Realtime_AddTriggerEntry(nInstance: Cardinal; nChannelListEntry: Cardinal; nStartTriggerAktiv: Cardinal; dStartSchwellwert1: Double; dStartSchwellwert2: Double; nStartTriggerTyp: Cardinal; nStartEnableAtStart: Cardinal; nStartTriggerMessung: Cardinal; nStartTriggerSetTTL: Cardinal; nStartTriggerTTLKlemme: Cardinal; nStartTriggerTTLZustand: Cardinal; nStartTriggerTTLFlanke: Cardinal; nStopTriggerAktiv: Cardinal; dStopSchwellwert1: Double; dStopSchwellwert2: Double; nStopTriggerTyp: Cardinal; nStopEnableAtStart: Cardinal; nStopTriggerMessung: Cardinal; nStopTriggerSetTTL: Cardinal; nStopTriggerTTLKlemme: Cardinal; nStopTriggerTTLZustand: Cardinal; nStopTriggerTTLFlanke: Cardinal; nRetriggerbar: Cardinal; var AOIndexInChannelsRTList: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'Realtime_AddTriggerEntry';
function Realtime_AddFilterEntry(nInstance: Cardinal; AIChannelListEntry: Cardinal; AIFilterMode: Cardinal; AIFilterOrder: Cardinal; AICoefficients: PDouble; AIOutputGainFactor: Double; var AOIndexIndChannelsRTList: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'Realtime_AddFilterEntry';
function Realtime_DesignIIRFilter(AISampleRate: Double; AIFilterType: Cardinal; AICutoffFreqency: Double; AICutoffFreqency2: Double; AIFrequenciesAreNormalized: Boolean; AIPassabsorbtion: Double; AIStopbandattenuation: Double; AIDesignMethod: Cardinal; AIOrder: Cardinal; var AOFilterMode: Cardinal; AOCoefficientsList: PDouble; var AOGain: Double):LongInt; stdcall; external 'maiv2dll.DLL' name 'Realtime_DesignIIRFilter';
function Realtime_DesignFIRFilter(AISampleRate: Double; AIFilterType: Cardinal; AICutoffFreqLow: Double; AICutoffFreqHigh: Double; AIFrequenciesAreNormalized: Boolean; AIOrder: Cardinal; AIFilterWindow: Cardinal; AIWindowParameter: Double; AIScalePassband: Boolean; var AOFilterMode: Cardinal; AOCoefficientsList: PDouble):LongInt; stdcall; external 'maiv2dll.DLL' name 'Realtime_DesignFIRFilter';
function Realtime_AddPIDEntry(nInstance: Cardinal; nChannelListEntry: Cardinal; dPAnteil: Double; dIAnteil: Double; dDAnteil: Double; nReglerArt: Cardinal; Gain: Double; dSollwert: Double; dMinValue: Double; dMaxValue: Double; nDAKanal: Cardinal; nSampleFreq: Double; var AOIndexInChannelsRTList: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'Realtime_AddPIDEntry';
function Realtime_ChangePID_Params(nInstance: Cardinal; nChannelListEntry: Cardinal; nIndexInChannelsRTList: Cardinal; dPAnteil: Double; dIAnteil: Double; dDAnteil: Double):LongInt; stdcall; external 'maiv2dll.DLL' name 'Realtime_ChangePID_Params';
function Realtime_ChangePID_NominalValue(nInstance: Cardinal; nChannelListEntry: Cardinal; nIndexInChannelsRTList: Cardinal; dSollwert: Double):LongInt; stdcall; external 'maiv2dll.DLL' name 'Realtime_ChangePID_NominalValue';
function Realtime_AddFFTEntry(nInstance: Cardinal; nChannelListEntry: Cardinal; nAnzahlPunkte: Cardinal; nSpektrum: Cardinal; dGain: Double; nFensterFunktion: Cardinal; dParameter: Double; var AOIndexInChannelsRTList: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'Realtime_AddFFTEntry';
function Realtime_FFT_ReadData(nInstance: Cardinal; nChannelListEntry: Cardinal; FFTData: PDouble; var nNumberOfValues: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'Realtime_FFT_ReadData';

implementation

end.
