Option Explicit 
Public Declare Function SSI_SetBitWidth LIB "maiv2dll.DLL" (ByVal nInstance As Long, ByVal nBitWidth As Long) As Long
Public Declare Function SSI_ConfigSSI LIB "maiv2dll.DLL" (ByVal nInstance As Long, ByVal nReset As Long, ByVal nResetEdge As Long, ByVal nActivePassiveMode As Long, ByVal nClockFrequency As Long, ByVal nEdge As Long) As Long
