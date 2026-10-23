Option Explicit 
Public Declare Function UART_GetBaudRate LIB "maiv2dll.DLL" (ByVal nInstance As Long, ByVal nChannel As Long, ByRef nBaudRate As Long) As Long
Public Declare Function UART_SetBaudRate LIB "maiv2dll.DLL" (ByVal nInstance As Long, ByVal nChannel As Long, ByVal nBaudRate As Long) As Long
Public Declare Function UART_Flush LIB "maiv2dll.DLL" (ByVal nInstance As Long, ByVal nChannel As Long, ByVal nTimeout As Long) As Long
Public Declare Function UART_GetState LIB "maiv2dll.DLL" (ByVal nInstance As Long, ByVal nChannel As Long, ByRef bIsEnabled As Long) As Long
Public Declare Function UART_SetState LIB "maiv2dll.DLL" (ByVal nInstance As Long, ByVal nChannel As Long, ByVal bIsEnabled As Long) As Long
Public Declare Function UART_RX_Avail LIB "maiv2dll.DLL" (ByVal nInstance As Long, ByVal nChannel As Long, ByRef bRX_Avail As Boolean) As Long
Public Declare Function UART_TX_Avail LIB "maiv2dll.DLL" (ByVal nInstance As Long, ByVal nChannel As Long, ByRef bTX_Avail As Boolean) As Long
Public Declare Function UART_ReadChar LIB "maiv2dll.DLL" (ByVal nInstance As Long, ByVal nChannel As Long, ByRef cRX As Byte) As Long
Public Declare Function UART_WriteChar LIB "maiv2dll.DLL" (ByVal nInstance As Long, ByVal nChannel As Long, ByVal cTX As Byte) As Long
Public Declare Function UART_Read LIB "maiv2dll.DLL" (ByVal nInstance As Long, ByVal nChannel As Long, ByRef bInStringBuffer As Byte, ByRef nLength As Long, ByVal nTimeout As Long) As Long
Public Declare Function UART_Write LIB "maiv2dll.DLL" (ByVal nInstance As Long, ByVal nChannel As Long, ByRef bOutStringBuffer As Byte, ByRef nLength As Long, ByVal nTimeout As Long) As Long
