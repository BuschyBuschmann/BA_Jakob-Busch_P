# PSV – DataCursor

## DataCursor Object

*Quelle: `PSV~DataCursor.html` · Polytec PSV Type Library*

### Description

Base object for the cursor objects: SingleCursor, DoubleCursor, HarmonicCursor and PeakCursor.

### Remarks

Use the CursorType property to find out the cursor type and then cast this object to the more specific object. Use the CursorSettings Property to set additional settings of the cursor.

### Example

The following example code illustrates how to set the peak cursor type and how to configure its properties.

*Set and Configure the Peak Cursor:*
```
'#Language "WWB-NET"
Option Explicit
Sub Main
    Dim oAnalyzerWindow As AnalyzerWindow = Acquisition.Document.Windows(1)
    Dim oAnalyzerView As AnalyzerView = oAnalyzerWindow.AnalyzerView
    oAnalyzerView.Settings.CursorType = PTCCursorType.ptcCursorTypePeak

    Dim oPeakCursorSettings As PeakCursorSettings = oAnalyzerView.Settings.CursorSettings
    oPeakCursorSettings.LeftPosition =  900
    oPeakCursorSettings.RightPosition = 1100
End Sub
```


---

## DataCursor Object Members

*Quelle: `PSV~DataCursor_members.html` · Polytec PSV Type Library*

### Public Properties

| CursorType | The type of the data cursor. |
|---|---|


---

## CursorType Property

*Quelle: `PSV~DataCursor~CursorType.html` · Polytec PSV Type Library · DataCursor Object : CursorType Property*

### Description

The type of the data cursor.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property CursorType As PTCCursorType
```
