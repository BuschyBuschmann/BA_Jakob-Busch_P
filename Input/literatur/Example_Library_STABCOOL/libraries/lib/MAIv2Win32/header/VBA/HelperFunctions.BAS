Option Explicit

Private Declare Sub CopyMem Lib "kernel32" Alias "RtlMoveMemory" (pTo As Any, uFrom As Any, ByVal lSize As Long)
Private Declare Function lstrlenA Lib "kernel32" (ByVal lpString As Long) As Long

Private Function StrFromPtr(ByVal lPtr As Long) As String
    Dim lLen As Long
    Dim abytBuf() As Byte
    lLen = lstrlenA(lPtr)
    If lLen > 0 Then
        ReDim abytBuf(lLen)
        Call CopyMem(abytBuf(0), ByVal lPtr, lLen)
        StrFromPtr = StrConv(abytBuf, 64)
    End If
End Function
