Option Explicit 
Public Declare Function PWM_StartOutput LIB "maiv2dll.DLL" (ByVal nInstance As Long) As Long
Public Declare Function PWM_StopOutput LIB "maiv2dll.DLL" (ByVal nInstance As Long) As Long
Public Declare Function PWM_PreparePWMOutput LIB "maiv2dll.DLL" (ByVal nInstance As Long, ByVal nChannel As Long, ByVal StartFrequency As Long, ByVal nStartRatio As Long) As Long
Public Declare Function PWM_PrepareFMOutput LIB "maiv2dll.DLL" (ByVal nInstance As Long, ByVal nChannel As Long, ByVal StartFrequency As Long, ByVal nPulsWidthRatio As Long) As Long
Public Declare Function PWM_WriteNewPWMRatio LIB "maiv2dll.DLL" (ByVal nInstance As Long, ByVal nChannel As Long, ByVal nRatio As Long) As Long
Public Declare Function PWM_WriteNewFMFrequency LIB "maiv2dll.DLL" (ByVal nInstance As Long, ByVal nChannel As Long, ByVal Frequency As Long) As Long
Public Declare Function PWM_GetPWMRatio LIB "maiv2dll.DLL" (ByVal nInstance As Long, ByVal nChannel As Long, ByRef nRatio As Long) As Long
Public Declare Function PWM_GetFMFrequency LIB "maiv2dll.DLL" (ByVal nInstance As Long, ByVal nChannel As Long, ByRef Frequency As Long) As Long
