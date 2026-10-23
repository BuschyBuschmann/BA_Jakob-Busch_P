
////////////////////////////////////////////////////////////////////////////////////////////////////
/// <category>	PWM-Funktionen. </category>
/// <categoryE>	PWM functions. </categoryE>
///
///
/// <filesummary>	zur Steuerung bzw. Messung der PWM Kanäle stehen die folgenden Funktionne zur Verfügung:. </filesummary>
/// <filesummaryE>	for controlling and measuring PWM Channels these functions are available: </filesummaryE>
////////////////////////////////////////////////////////////////////////////////////////////////////
MAIV2DLL_EXPORT PWM_StartOutput(uint nInstance);
MAIV2DLL_EXPORT PWM_StopOutput(uint nInstance);
MAIV2DLL_EXPORT PWM_PreparePWMOutput(uint nInstance, uint nChannel, uint StartFrequency, uint nStartRatio);
MAIV2DLL_EXPORT PWM_PrepareFMOutput(uint nInstance, uint nChannel, uint StartFrequency, uint nPulsWidthRatio);
MAIV2DLL_EXPORT PWM_WriteNewPWMRatio(uint nInstance, uint nChannel, uint nRatio);
MAIV2DLL_EXPORT PWM_WriteNewFMFrequency(uint nInstance, uint nChannel, uint Frequency); 
MAIV2DLL_EXPORT PWM_GetPWMRatio(uint nInstance, uint nChannel, uint* nRatio);
MAIV2DLL_EXPORT PWM_GetFMFrequency(uint nInstance, uint nChannel, uint* Frequency); 



