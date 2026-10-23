unit UART_Functions;

interface


function UART_GetBaudRate(nInstance: Cardinal; nChannel: Cardinal; var nBaudRate: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'UART_GetBaudRate';
function UART_SetBaudRate(nInstance: Cardinal; nChannel: Cardinal; nBaudRate: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'UART_SetBaudRate';
function UART_Flush(nInstance: Cardinal; nChannel: Cardinal; nTimeout: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'UART_Flush';
function UART_GetState(nInstance: Cardinal; nChannel: Cardinal; var bIsEnabled: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'UART_GetState';
function UART_SetState(nInstance: Cardinal; nChannel: Cardinal; bIsEnabled: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'UART_SetState';
function UART_RX_Avail(nInstance: Cardinal; nChannel: Cardinal; var bRX_Avail: Boolean):LongInt; stdcall; external 'maiv2dll.DLL' name 'UART_RX_Avail';
function UART_TX_Avail(nInstance: Cardinal; nChannel: Cardinal; var bTX_Avail: Boolean):LongInt; stdcall; external 'maiv2dll.DLL' name 'UART_TX_Avail';
function UART_ReadChar(nInstance: Cardinal; nChannel: Cardinal; var cRX: AnsiChar):LongInt; stdcall; external 'maiv2dll.DLL' name 'UART_ReadChar';
function UART_WriteChar(nInstance: Cardinal; nChannel: Cardinal; cTX: AnsiChar):LongInt; stdcall; external 'maiv2dll.DLL' name 'UART_WriteChar';
function UART_Read(nInstance: Cardinal; nChannel: Cardinal; var bInStringBuffer: AnsiChar; var nLength: Cardinal; nTimeout: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'UART_Read';
function UART_Write(nInstance: Cardinal; nChannel: Cardinal; var bOutStringBuffer: AnsiChar; var nLength: Cardinal; nTimeout: Cardinal):LongInt; stdcall; external 'maiv2dll.DLL' name 'UART_Write';

implementation

end.
