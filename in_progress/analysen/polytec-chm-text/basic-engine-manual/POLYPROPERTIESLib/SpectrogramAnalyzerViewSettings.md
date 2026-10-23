# POLYPROPERTIESLib – SpectrogramAnalyzerViewSettings

## SpectrogramAnalyzerViewSettings Object

*Quelle: `POLYPROPERTIESLib~SpectrogramAnalyzerViewSettings.html` · Polytec PolyProperties Type Library*

### Description

User interface settings of an analyzer view of a spectrogram or Campbell diagram.

### Object Model


---

## SpectrogramAnalyzerViewSettings Object Members

*Quelle: `POLYPROPERTIESLib~SpectrogramAnalyzerViewSettings_members.html` · Polytec PolyProperties Type Library*

### Public Methods

| Clone | Creates a copy of the settings object. The new object will be detached. |
|---|---|
| Copy | Copies the properties of the given settings object to this settings object. |
| Equal | Compares all properties of this settings object with the properties of the other settings object. Returns true, if all properties have equal values. |

### Public Properties

| BackColor | Specifies the background color. |
|---|---|
| CurrentFrame | Specifies the number of the current frame used for the display of cursor values in the cursor readout region of the analyzer view. |
| CursorSettings | Specifies the settings of the cursor. |
| CursorType | Specifies the type of the current cursor. |
| DisplaySettings | Specifies the display settings of the analyzer view. |
| GridColor | Specifies the color of the grid. |
| GridStyle | Specifies the style of the grid. |
| LegendColor | Specifies the color of the legend. |
| LineSettings | Specifies the settings of the lines. |
| Modified | Returns whether the settings object has been modified. |
| Parent | The parent of the settings object, if the object is attached, or nothing. |
| SelectedFrames | Specifies the numbers of the data frames that are selected. |
| ShowGrid | Specifies whether a grid is displayed. |
| ShowTitle | Specifies whether a title is shown. |
| Title | Specifies the title. |
| TitleFont | Specifies the font of the title. |
| XRangeSettings | Specifies the settings of the ranges of the x-axis. |
| YRangeSettings | Specifies the settings of the ranges of the y-axes. |


---

## Clone Method

*Quelle: `POLYPROPERTIESLib~SpectrogramAnalyzerViewSettings~Clone.html` · Polytec PolyProperties Type Library · SpectrogramAnalyzerViewSettings Object : Clone Method*

### Description

Creates a copy of the settings object. The new object will be detached.

### Syntax

*Visual Basic:*
```
Public Function Clone() As IUISettings
```


---

## Copy Method

*Quelle: `POLYPROPERTIESLib~SpectrogramAnalyzerViewSettings~Copy.html` · Polytec PolyProperties Type Library · SpectrogramAnalyzerViewSettings Object : Copy Method*

### Description

Copies the properties of the given settings object to this settings object.

### Syntax

*Visual Basic:*
```
Public Sub Copy( _
   ByVal UISettings As IUISettings _
)
```

### Parameters

UISettings

The other settings object.


---

## Equal Method

*Quelle: `POLYPROPERTIESLib~SpectrogramAnalyzerViewSettings~Equal.html` · Polytec PolyProperties Type Library · SpectrogramAnalyzerViewSettings Object : Equal Method*

### Description

Compares all properties of this settings object with the properties of the other settings object. Returns true, if all properties have equal values.

### Syntax

*Visual Basic:*
```
Public Function Equal( _
   ByVal UISettings As IUISettings _
) As Boolean
```

### Parameters

UISettings

The other settings object.

### Return Type

True if all properties are equal.


---

## BackColor Property

*Quelle: `POLYPROPERTIESLib~SpectrogramAnalyzerViewSettings~BackColor.html` · Polytec PolyProperties Type Library · SpectrogramAnalyzerViewSettings Object : BackColor Property*

### Description

Specifies the background color.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property BackColor As PTCColor
```


---

## CurrentFrame Property

*Quelle: `POLYPROPERTIESLib~SpectrogramAnalyzerViewSettings~CurrentFrame.html` · Polytec PolyProperties Type Library · SpectrogramAnalyzerViewSettings Object : CurrentFrame Property*

### Description

Specifies the number of the current frame used for the display of cursor values in the cursor readout region of the analyzer view.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property CurrentFrame As Long
```

### Remarks

This is one of the numbers returned by the AvailableFrames property of the AnalyzerView.


---

## CursorSettings Property

*Quelle: `POLYPROPERTIESLib~SpectrogramAnalyzerViewSettings~CursorSettings.html` · Polytec PolyProperties Type Library · SpectrogramAnalyzerViewSettings Object : CursorSettings Property*

### Description

Specifies the settings of the cursor.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property CursorSettings As IDataCursorSettings
```


---

## CursorType Property

*Quelle: `POLYPROPERTIESLib~SpectrogramAnalyzerViewSettings~CursorType.html` · Polytec PolyProperties Type Library · SpectrogramAnalyzerViewSettings Object : CursorType Property*

### Description

Specifies the type of the current cursor.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property CursorType As PTCCursorType
```


---

## DisplaySettings Property

*Quelle: `POLYPROPERTIESLib~SpectrogramAnalyzerViewSettings~DisplaySettings.html` · Polytec PolyProperties Type Library · SpectrogramAnalyzerViewSettings Object : DisplaySettings Property*

### Description

Specifies the display settings of the analyzer view.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property DisplaySettings As DisplaySettings
```


---

## GridColor Property

*Quelle: `POLYPROPERTIESLib~SpectrogramAnalyzerViewSettings~GridColor.html` · Polytec PolyProperties Type Library · SpectrogramAnalyzerViewSettings Object : GridColor Property*

### Description

Specifies the color of the grid.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property GridColor As PTCColor
```


---

## GridStyle Property

*Quelle: `POLYPROPERTIESLib~SpectrogramAnalyzerViewSettings~GridStyle.html` · Polytec PolyProperties Type Library · SpectrogramAnalyzerViewSettings Object : GridStyle Property*

### Description

Specifies the style of the grid.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property GridStyle As PTCGridStyle
```


---

## LegendColor Property

*Quelle: `POLYPROPERTIESLib~SpectrogramAnalyzerViewSettings~LegendColor.html` · Polytec PolyProperties Type Library · SpectrogramAnalyzerViewSettings Object : LegendColor Property*

### Description

Specifies the color of the legend.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property LegendColor As PTCColor
```


---

## LineSettings Property

*Quelle: `POLYPROPERTIESLib~SpectrogramAnalyzerViewSettings~LineSettings.html` · Polytec PolyProperties Type Library · SpectrogramAnalyzerViewSettings Object : LineSettings Property*

### Description

Specifies the settings of the lines.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property LineSettings As LineSettingsColl
```


---

## Modified Property

*Quelle: `POLYPROPERTIESLib~SpectrogramAnalyzerViewSettings~Modified.html` · Polytec PolyProperties Type Library · SpectrogramAnalyzerViewSettings Object : Modified Property*

### Description

Returns whether the settings object has been modified.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Modified As Boolean
```


---

## Parent Property

*Quelle: `POLYPROPERTIESLib~SpectrogramAnalyzerViewSettings~Parent.html` · Polytec PolyProperties Type Library · SpectrogramAnalyzerViewSettings Object : Parent Property*

### Description

The parent of the settings object, if the object is attached, or nothing.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Parent As Object
```


---

## SelectedFrames Property

*Quelle: `POLYPROPERTIESLib~SpectrogramAnalyzerViewSettings~SelectedFrames.html` · Polytec PolyProperties Type Library · SpectrogramAnalyzerViewSettings Object : SelectedFrames Property*

### Description

Specifies the numbers of the data frames that are selected.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property SelectedFrames As Long()
```

### Remarks

This is a subset of the frame numbers returned by the AvailableFrames property of the AnalyzerView.


---

## ShowGrid Property

*Quelle: `POLYPROPERTIESLib~SpectrogramAnalyzerViewSettings~ShowGrid.html` · Polytec PolyProperties Type Library · SpectrogramAnalyzerViewSettings Object : ShowGrid Property*

### Description

Specifies whether a grid is displayed.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property ShowGrid As Boolean
```


---

## ShowTitle Property

*Quelle: `POLYPROPERTIESLib~SpectrogramAnalyzerViewSettings~ShowTitle.html` · Polytec PolyProperties Type Library · SpectrogramAnalyzerViewSettings Object : ShowTitle Property*

### Description

Specifies whether a title is shown.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property ShowTitle As Boolean
```


---

## Title Property

*Quelle: `POLYPROPERTIESLib~SpectrogramAnalyzerViewSettings~Title.html` · Polytec PolyProperties Type Library · SpectrogramAnalyzerViewSettings Object : Title Property*

### Description

Specifies the title.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Title As String
```


---

## TitleFont Property

*Quelle: `POLYPROPERTIESLib~SpectrogramAnalyzerViewSettings~TitleFont.html` · Polytec PolyProperties Type Library · SpectrogramAnalyzerViewSettings Object : TitleFont Property*

### Description

Specifies the font of the title.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property TitleFont As Font
```


---

## XRangeSettings Property

*Quelle: `POLYPROPERTIESLib~SpectrogramAnalyzerViewSettings~XRangeSettings.html` · Polytec PolyProperties Type Library · SpectrogramAnalyzerViewSettings Object : XRangeSettings Property*

### Description

Specifies the settings of the ranges of the x-axis.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property XRangeSettings As RangeSettings
```


---

## YRangeSettings Property

*Quelle: `POLYPROPERTIESLib~SpectrogramAnalyzerViewSettings~YRangeSettings.html` · Polytec PolyProperties Type Library · SpectrogramAnalyzerViewSettings Object : YRangeSettings Property*

### Description

Specifies the settings of the ranges of the y-axes.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property YRangeSettings As RangeSettingsColl
```
