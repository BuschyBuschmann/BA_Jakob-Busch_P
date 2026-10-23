# POLYPROPERTIESLib – SigProAnalyzerViewSettings

## SigProAnalyzerViewSettings Object

*Quelle: `POLYPROPERTIESLib~SigProAnalyzerViewSettings.html` · Polytec PolyProperties Type Library*

### Description

User interface settings of an analyzer view of a signal processor window. The object is derived from the AnalyzerViewSettings object.

### Object Model


---

## SigProAnalyzerViewSettings Object Members

*Quelle: `POLYPROPERTIESLib~SigProAnalyzerViewSettings_members.html` · Polytec PolyProperties Type Library*

### Public Methods

| Clone | Creates a copy of the settings object. The new object will be detached. |
|---|---|
| Copy | Copies the properties of the given settings object to this settings object. |
| Equal | Compares all properties of this settings object with the properties of the other settings object. Returns true, if all properties have equal values. |

### Public Properties

| BackColor | Specifies the background color. |
|---|---|
| CurrentFrame | Specifies the number of the current frame used for the display of cursor values in the cursor readout region of the analyzer view. |
| CurrentPoint | Specifies the current point number. |
| CursorSettings | Specifies the settings of the cursor. |
| CursorType | Specifies the type of the current cursor. |
| DisplaySettings | Specifies the display settings of the analyzer view. |
| GridColor | Specifies the color of the grid. |
| GridStyle | Specifies the style of the grid. |
| LegendColor | Specifies the color of the legend. |
| LineSettings | Specifies the settings of the lines. |
| Modified | Returns whether the settings object has been modified. |
| Parent | The parent of the settings object, if the object is attached, or nothing. |
| Pinned | Specifies whether the analyzer view is pinned to a cell of the signal processor grid. |
| SelectedFrames | Specifies the numbers of the data frames that are selected. |
| ShowGrid | Specifies whether a grid is displayed. |
| ShowTitle | Specifies whether a title is shown. |
| SignalDirection | Specifies the direction of the signal (X, Y, Z) that is displayed in the analyzer view. |
| Title | Specifies the title. |
| TitleFont | Specifies the font of the title. |
| XRangeSettings | Specifies the settings of the ranges of the x-axis. |
| YRangeSettings | Specifies the settings of the ranges of the y-axes. |


---

## Clone Method

*Quelle: `POLYPROPERTIESLib~SigProAnalyzerViewSettings~Clone.html` · Polytec PolyProperties Type Library · SigProAnalyzerViewSettings Object : Clone Method*

### Description

Creates a copy of the settings object. The new object will be detached.

### Syntax

*Visual Basic:*
```
Public Function Clone() As IUISettings
```

### Remarks

This object can either be attached to a parent object or not. If it is attached, the Parent property returns the attached parent. In this case, changes to the object are directly applied to the user interface. You can create settings objects that are not attached to a parent by calling Clone() on a settings object or by creating a new settings object. Assigning such an object to a suitable Settings property of a parent object applies all properties to the user interface at the time of the assignment. Assignment of a settings object copies all properties to the settings object attached to its parent. The detached settings object will be still detached after the assignment.

You can quickly copy settings e.g. between different windows by directly assigning the settings object of one window to the settings property of the other.


---

## Copy Method

*Quelle: `POLYPROPERTIESLib~SigProAnalyzerViewSettings~Copy.html` · Polytec PolyProperties Type Library · SigProAnalyzerViewSettings Object : Copy Method*

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

*Quelle: `POLYPROPERTIESLib~SigProAnalyzerViewSettings~Equal.html` · Polytec PolyProperties Type Library · SigProAnalyzerViewSettings Object : Equal Method*

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

*Quelle: `POLYPROPERTIESLib~SigProAnalyzerViewSettings~BackColor.html` · Polytec PolyProperties Type Library · SigProAnalyzerViewSettings Object : BackColor Property*

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

*Quelle: `POLYPROPERTIESLib~SigProAnalyzerViewSettings~CurrentFrame.html` · Polytec PolyProperties Type Library · SigProAnalyzerViewSettings Object : CurrentFrame Property*

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

## CurrentPoint Property

*Quelle: `POLYPROPERTIESLib~SigProAnalyzerViewSettings~CurrentPoint.html` · Polytec PolyProperties Type Library · SigProAnalyzerViewSettings Object : CurrentPoint Property*

### Description

Specifies the current point number.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property CurrentPoint As Long
```

### Remarks

This is one of the numbers returned by the AvailablePoints property of the SigProAnalyzerView object.


---

## CursorSettings Property

*Quelle: `POLYPROPERTIESLib~SigProAnalyzerViewSettings~CursorSettings.html` · Polytec PolyProperties Type Library · SigProAnalyzerViewSettings Object : CursorSettings Property*

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

*Quelle: `POLYPROPERTIESLib~SigProAnalyzerViewSettings~CursorType.html` · Polytec PolyProperties Type Library · SigProAnalyzerViewSettings Object : CursorType Property*

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

*Quelle: `POLYPROPERTIESLib~SigProAnalyzerViewSettings~DisplaySettings.html` · Polytec PolyProperties Type Library · SigProAnalyzerViewSettings Object : DisplaySettings Property*

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

*Quelle: `POLYPROPERTIESLib~SigProAnalyzerViewSettings~GridColor.html` · Polytec PolyProperties Type Library · SigProAnalyzerViewSettings Object : GridColor Property*

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

*Quelle: `POLYPROPERTIESLib~SigProAnalyzerViewSettings~GridStyle.html` · Polytec PolyProperties Type Library · SigProAnalyzerViewSettings Object : GridStyle Property*

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

*Quelle: `POLYPROPERTIESLib~SigProAnalyzerViewSettings~LegendColor.html` · Polytec PolyProperties Type Library · SigProAnalyzerViewSettings Object : LegendColor Property*

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

*Quelle: `POLYPROPERTIESLib~SigProAnalyzerViewSettings~LineSettings.html` · Polytec PolyProperties Type Library · SigProAnalyzerViewSettings Object : LineSettings Property*

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

*Quelle: `POLYPROPERTIESLib~SigProAnalyzerViewSettings~Modified.html` · Polytec PolyProperties Type Library · SigProAnalyzerViewSettings Object : Modified Property*

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

*Quelle: `POLYPROPERTIESLib~SigProAnalyzerViewSettings~Parent.html` · Polytec PolyProperties Type Library · SigProAnalyzerViewSettings Object : Parent Property*

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

## Pinned Property

*Quelle: `POLYPROPERTIESLib~SigProAnalyzerViewSettings~Pinned.html` · Polytec PolyProperties Type Library · SigProAnalyzerViewSettings Object : Pinned Property*

### Description

Specifies whether the analyzer view is pinned to a cell of the signal processor grid.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Pinned As Boolean
```


---

## SelectedFrames Property

*Quelle: `POLYPROPERTIESLib~SigProAnalyzerViewSettings~SelectedFrames.html` · Polytec PolyProperties Type Library · SigProAnalyzerViewSettings Object : SelectedFrames Property*

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

*Quelle: `POLYPROPERTIESLib~SigProAnalyzerViewSettings~ShowGrid.html` · Polytec PolyProperties Type Library · SigProAnalyzerViewSettings Object : ShowGrid Property*

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

*Quelle: `POLYPROPERTIESLib~SigProAnalyzerViewSettings~ShowTitle.html` · Polytec PolyProperties Type Library · SigProAnalyzerViewSettings Object : ShowTitle Property*

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

## SignalDirection Property

*Quelle: `POLYPROPERTIESLib~SigProAnalyzerViewSettings~SignalDirection.html` · Polytec PolyProperties Type Library · SigProAnalyzerViewSettings Object : SignalDirection Property*

### Description

Specifies the direction of the signal (X, Y, Z) that is displayed in the analyzer view.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property SignalDirection As PTCSignalDirection
```


---

## Title Property

*Quelle: `POLYPROPERTIESLib~SigProAnalyzerViewSettings~Title.html` · Polytec PolyProperties Type Library · SigProAnalyzerViewSettings Object : Title Property*

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

*Quelle: `POLYPROPERTIESLib~SigProAnalyzerViewSettings~TitleFont.html` · Polytec PolyProperties Type Library · SigProAnalyzerViewSettings Object : TitleFont Property*

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

*Quelle: `POLYPROPERTIESLib~SigProAnalyzerViewSettings~XRangeSettings.html` · Polytec PolyProperties Type Library · SigProAnalyzerViewSettings Object : XRangeSettings Property*

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

*Quelle: `POLYPROPERTIESLib~SigProAnalyzerViewSettings~YRangeSettings.html` · Polytec PolyProperties Type Library · SigProAnalyzerViewSettings Object : YRangeSettings Property*

### Description

Specifies the settings of the ranges of the y-axes.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property YRangeSettings As RangeSettingsColl
```
