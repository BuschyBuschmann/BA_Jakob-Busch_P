

////////////////////////////////////////////////////////////////////////////////////////////////////
/// <category>	Online-Funktionen. </category>
/// <categoryE>	online functions. </categoryE>
///
///
/// <filesummary>	bei DSP-Karten, bei denen die jeweilige Online Funktion freigeschaltet ist,
/// 				stehen diese Funktionen zur Steuerung zur Verfügung </filesummary>
/// <filesummaryE>	for DSP cards, which have installed the corresponding online functions, these 
/// 				functions are available: </filesummaryE>
////////////////////////////////////////////////////////////////////////////////////////////////////


MAIV2DLL_EXPORT Realtime_AddTriggerEntry(uint nInstance, uint nChannelListEntry, uint nStartTriggerAktiv, double dStartSchwellwert1, double dStartSchwellwert2, 
											 uint nStartTriggerTyp, uint nStartEnableAtStart, uint nStartTriggerMessung, uint nStartTriggerSetTTL, uint nStartTriggerTTLKlemme, 
											 uint nStartTriggerTTLZustand, uint nStartTriggerTTLFlanke, uint nStopTriggerAktiv, double dStopSchwellwert1, double dStopSchwellwert2, 
											 uint nStopTriggerTyp, uint nStopEnableAtStart, uint nStopTriggerMessung, uint nStopTriggerSetTTL, uint nStopTriggerTTLKlemme, 
											 uint nStopTriggerTTLZustand, uint nStopTriggerTTLFlanke, uint nRetriggerbar, uint* AOIndexInChannelsRTList);

MAIV2DLL_EXPORT Realtime_AddFilterEntry(uint nInstance, uint AIChannelListEntry, uint AIFilterMode, uint AIFilterOrder, double AICoefficients[], double AIOutputGainFactor, uint* AOIndexIndChannelsRTList);		

MAIV2DLL_EXPORT Realtime_DesignIIRFilter( double AISampleRate, uint AIFilterType, double AICutoffFreqency, double AICutoffFreqency2,  bool AIFrequenciesAreNormalized,
											double AIPassabsorbtion, double AIStopbandattenuation,
											uint AIDesignMethod, uint AIOrder, 
											// Ausgabe:
											uint* AOFilterMode, double AOCoefficientsList[], double* AOGain);		

MAIV2DLL_EXPORT Realtime_DesignFIRFilter(  double AISampleRate, uint AIFilterType, double AICutoffFreqLow, double AICutoffFreqHigh,  bool AIFrequenciesAreNormalized,
										   uint AIOrder, uint AIFilterWindow, double AIWindowParameter,bool AIScalePassband,
											// Ausgabe: 
											uint* AOFilterMode, double AOCoefficientsList[]);		

MAIV2DLL_EXPORT Realtime_AddPIDEntry(uint nInstance, uint nChannelListEntry, double dPAnteil, double dIAnteil, double dDAnteil, uint nReglerArt, double Gain, double dSollwert, double dMinValue, double dMaxValue, uint nDAKanal, double nSampleFreq, uint* AOIndexInChannelsRTList);

MAIV2DLL_EXPORT Realtime_ChangePID_Params(uint nInstance, uint nChannelListEntry, uint nIndexInChannelsRTList ,double dPAnteil, double dIAnteil, double dDAnteil);

MAIV2DLL_EXPORT Realtime_ChangePID_NominalValue(uint nInstance, uint nChannelListEntry, uint nIndexInChannelsRTList ,double dSollwert);

MAIV2DLL_EXPORT Realtime_AddFFTEntry(uint nInstance, uint nChannelListEntry, uint nAnzahlPunkte, uint nSpektrum, double dGain, uint nFensterFunktion, double dParameter, uint* AOIndexInChannelsRTList);

MAIV2DLL_EXPORT Realtime_FFT_ReadData(uint nInstance, uint nChannelListEntry, double FFTData[], uint * nNumberOfValues);


