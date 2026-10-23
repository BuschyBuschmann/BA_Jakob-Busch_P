unit SSI_Functions;

interface


function SSI_SetBitWidth(nInstance: Cardinal; nBitWidth: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'SSI_SetBitWidth';
function SSI_ConfigSSI(nInstance: Cardinal; nReset: Cardinal; nResetEdge: Cardinal; nActivePassiveMode: Cardinal; nClockFrequency: Cardinal; nEdge: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'SSI_ConfigSSI';

implementation

end.
