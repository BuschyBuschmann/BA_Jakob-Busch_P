
////////////////////////////////////////////////////////////////////////////////////////////////////
/// <category>	SSI-Funktionen. </category>
/// <categoryE>	SSI functions. </categoryE>
///
///
/// <filesummary>	zur Steuerung bzw. Messung der SSI Kanäle stehen die folgenden Funktionne zur Verfügung:. </filesummary>
/// <filesummaryE>	for controlling and measuring SSI Channels these functions are available: </filesummaryE>
////////////////////////////////////////////////////////////////////////////////////////////////////
MAIV2DLL_EXPORT SSI_SetBitWidth(uint nInstance, uint nBitWidth);
MAIV2DLL_EXPORT SSI_ConfigSSI(uint nInstance, uint nReset, uint nResetEdge, uint nActivePassiveMode, uint nClockFrequency, uint nEdge);


