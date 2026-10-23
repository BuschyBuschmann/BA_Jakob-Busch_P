Option Explicit 
Public Declare Function GetFirstDevice LIB "maiv2dll.DLL" () As Long
Public Declare Function GetNumberOfDevices LIB "maiv2dll.DLL" () As Long
Public Declare Function GetDeviceHandles LIB "maiv2dll.DLL" (ByRef Handles As Long, ByRef iHandleCount As Long) As Long
Public Declare Function GetDeviceHandlesMultichoiceETH LIB "maiv2dll.DLL" (ByRef Handles As Long, ByRef iHandleCount As Long) As Long
Public Declare Function GetDeviceHandlesMultichoicePCI LIB "maiv2dll.DLL" (ByRef Handles As Long, ByRef iHandleCount As Long) As Long
Public Declare Function GetDeviceHandlesMultichoiceUSB LIB "maiv2dll.DLL" (ByRef Handles As Long, ByRef iHandleCount As Long) As Long
Public Declare Function GetDeviceHandlesMultichoiceUSBBasic LIB "maiv2dll.DLL" (ByRef Handles As Long, ByRef iHandleCount As Long) As Long
Public Declare Function GetFirstDeviceByType LIB "maiv2dll.DLL" (ByVal DeviceType As Long) As Long
Public Declare Function OpenDevice LIB "maiv2dll.DLL" (ByVal nInstance As Long) As Long
Public Declare Function CloseDevice LIB "maiv2dll.DLL" (ByVal nInstance As Long) As Long
Public Declare Function IsDeviceOpen LIB "maiv2dll.DLL" (ByVal nInstance As Long) As Long
Public Declare Function GetErrorDescription LIB "maiv2dll.DLL" (ByVal nInstance As Long, ByVal ErrorNumber As Long, ByRef ErrorDescription As Byte) As Long
Public Declare Function SetGPCIFile LIB "maiv2dll.DLL" (ByRef AIFilePath As Long, ByVal nLength As Long) As Long
Public Declare Function GetGPCIFilePath LIB "maiv2dll.DLL" () As Long
Public Declare Function ReCreateDeviceListOmittingDeviceTypes LIB "maiv2dll.DLL" (ByVal AICreatePCI As Boolean, ByVal AICreateUSBMC4 As Boolean, ByVal CreateUSBBasic As Boolean) As Long
Public Declare Function ShowMessageBoxOnDeviceCreationError LIB "maiv2dll.DLL" (ByVal AIShowMsgBox As Boolean) As Long
Public Declare Function GetNumberOfUninitializedDevices LIB "maiv2dll.DLL" () As Long
Public Declare Function GetDeviceCreationErrorMessage LIB "maiv2dll.DLL" (ByVal nNumber As Long, ByRef AOText As Long, ByVal nTextBufferLength As Long) As Long
