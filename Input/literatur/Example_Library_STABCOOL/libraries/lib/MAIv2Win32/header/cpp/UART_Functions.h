
MAIV2DLL_EXPORT UART_GetBaudRate(uint nInstance, uint nChannel, uint* nBaudRate);
MAIV2DLL_EXPORT UART_SetBaudRate(uint nInstance, uint nChannel, uint nBaudRate);
MAIV2DLL_EXPORT UART_Flush(uint nInstance, uint nChannel, uint nTimeout);
MAIV2DLL_EXPORT UART_GetState(uint nInstance, uint nChannel, uint* bIsEnabled);
MAIV2DLL_EXPORT UART_SetState(uint nInstance, uint nChannel, uint  bIsEnabled);

MAIV2DLL_EXPORT UART_RX_Avail(uint nInstance, uint nChannel, bool* bRX_Avail );
MAIV2DLL_EXPORT UART_TX_Avail(uint nInstance, uint nChannel, bool* bTX_Avail );
MAIV2DLL_EXPORT UART_ReadChar(uint nInstance, uint nChannel, char* cRX );
MAIV2DLL_EXPORT UART_WriteChar(uint nInstance, uint nChannel, char cTX );

MAIV2DLL_EXPORT UART_Read(uint nInstance, uint nChannel, char** bInStringBuffer, uint* nLength, uint nTimeout);
MAIV2DLL_EXPORT UART_Write(uint nInstance, uint nChannel, char* bOutStringBuffer, uint* nLength, uint nTimeout);