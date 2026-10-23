# POLYPROPERTIESLib – AnalyzerViewSettings

## AnalyzerViewSettings Object

*Quelle: `POLYPROPERTIESLib~AnalyzerViewSettings.html` · Polytec PolyProperties Type Library*

### Description

User interface settings of an analyzer view.

### Object Model


---

## AnalyzerViewSettings Object Members

*Quelle: `POLYPROPERTIESLib~AnalyzerViewSettings_members.html` · Polytec PolyProperties Type Library*

### Public Methods

| Clone | Creates a copy of the settings object. The new object will be detached. |
|---|---|
| Copy | Copies the properties of the given settings object to this settings object. |
| Equal | Compares all properties of this settings object with the properties of the other settings object. Returns true, if all properties have equal values. |

### Public Properties

| AxisLabelTickScale | The scale of the axes labels and ticks. |
|---|---|
| BackColor | Specifies the background color. |
| ChannelPinned | Specifies the pinned to area view state of the associated channel. |
| ChannelSelection | Specifies the channel selection string. |
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
| SignalDirection | Specifies which directions of a signal of a 3D channel are displayed in the analyzer. |
| Title | Specifies the title. |
| TitleFont | Specifies the font of the title. |
| XRangeSettings | Specifies the settings of the ranges of the x-axis. |
| YRangeSettings | Specifies the settings of the ranges of the y-axes. |


---

## Clone Method

*Quelle: `POLYPROPERTIESLib~AnalyzerViewSettings~Clone.html` · Polytec PolyProperties Type Library · AnalyzerViewSettings Object : Clone Method*

### Description

Creates a copy of the settings object. The new object will be detached.

### Syntax

*Visual Basic:*
```
Public Function Clone() As IUISettings
```


---

## Copy Method

*Quelle: `POLYPROPERTIESLib~AnalyzerViewSettings~Copy.html` · Polytec PolyProperties Type Library · AnalyzerViewSettings Object : Copy Method*

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

*Quelle: `POLYPROPERTIESLib~AnalyzerViewSettings~Equal.html` · Polytec PolyProperties Type Library · AnalyzerViewSettings Object : Equal Method*

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

## AxisLabelTickScale Property

*Quelle: `POLYPROPERTIESLib~AnalyzerViewSettings~AxisLabelTickScale.html` · Polytec PolyProperties Type Library · AnalyzerViewSettings Object : AxisLabelTickScale Property*

### Description

The scale of the axes labels and ticks.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property AxisLabelTickScale As Double
```

### Remarks

By setting a larger value than 1 you can scale-up the axes labels and ticks for better readability for e.g. in screen shots or printouts. Recommended values are 1, 1.25, 1.5, 1.75 or 2.


---

## BackColor Property

*Quelle: `POLYPROPERTIESLib~AnalyzerViewSettings~BackColor.html` · Polytec PolyProperties Type Library · AnalyzerViewSettings Object : BackColor Property*

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

## ChannelPinned Property

*Quelle: `POLYPROPERTIESLib~AnalyzerViewSettings~ChannelPinned.html` · Polytec PolyProperties Type Library · AnalyzerViewSettings Object : ChannelPinned Property*

### Description

Specifies the pinned to area view state of the associated channel.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property ChannelPinned As Boolean
```

### Remarks

This setting is available only for Multipoint Vibrometer files.


---

## ChannelSelection Property

*Quelle: `POLYPROPERTIESLib~AnalyzerViewSettings~ChannelSelection.html` · Polytec PolyProperties Type Library · AnalyzerViewSettings Object : ChannelSelection Property*

### Description

Specifies the channel selection string.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property ChannelSelection As String
```

### Remarks

This setting is available only for Multipoint Vibrometer files.


---

## CurrentFrame Property

*Quelle: `POLYPROPERTIESLib~AnalyzerViewSettings~CurrentFrame.html` · Polytec PolyProperties Type Library · AnalyzerViewSettings Object : CurrentFrame Property*

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

*Quelle: `POLYPROPERTIESLib~AnalyzerViewSettings~CursorSettings.html` · Polytec PolyProperties Type Library · AnalyzerViewSettings Object : CursorSettings Property*

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

*Quelle: `POLYPROPERTIESLib~AnalyzerViewSettings~CursorType.html` · Polytec PolyProperties Type Library · AnalyzerViewSettings Object : CursorType Property*

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

*Quelle: `POLYPROPERTIESLib~AnalyzerViewSettings~DisplaySettings.html` · Polytec PolyProperties Type Library · AnalyzerViewSettings Object : DisplaySettings Property*

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

*Quelle: `POLYPROPERTIESLib~AnalyzerViewSettings~GridColor.html` · Polytec PolyProperties Type Library · AnalyzerViewSettings Object : GridColor Property*

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

*Quelle: `POLYPROPERTIESLib~AnalyzerViewSettings~GridStyle.html` · Polytec PolyProperties Type Library · AnalyzerViewSettings Object : GridStyle Property*

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

*Quelle: `POLYPROPERTIESLib~AnalyzerViewSettings~LegendColor.html` · Polytec PolyProperties Type Library · AnalyzerViewSettings Object : LegendColor Property*

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

*Quelle: `POLYPROPERTIESLib~AnalyzerViewSettings~LineSettings.html` · Polytec PolyProperties Type Library · AnalyzerViewSettings Object : LineSettings Property*

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

*Quelle: `POLYPROPERTIESLib~AnalyzerViewSettings~Modified.html` · Polytec PolyProperties Type Library · AnalyzerViewSettings Object : Modified Property*

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

*Quelle: `POLYPROPERTIESLib~AnalyzerViewSettings~Parent.html` · Polytec PolyProperties Type Library · AnalyzerViewSettings Object : Parent Property*

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

*Quelle: `POLYPROPERTIESLib~AnalyzerViewSettings~SelectedFrames.html` · Polytec PolyProperties Type Library · AnalyzerViewSettings Object : SelectedFrames Property*

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

*Quelle: `POLYPROPERTIESLib~AnalyzerViewSettings~ShowGrid.html` · Polytec PolyProperties Type Library · AnalyzerViewSettings Object : ShowGrid Property*

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

*Quelle: `POLYPROPERTIESLib~AnalyzerViewSettings~ShowTitle.html` · Polytec PolyProperties Type Library · AnalyzerViewSettings Object : ShowTitle Property*

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

*Quelle: `POLYPROPERTIESLib~AnalyzerViewSettings~SignalDirection.html` · Polytec PolyProperties Type Library · AnalyzerViewSettings Object : SignalDirection Property*

### Description

Specifies which directions of a signal of a 3D channel are displayed in the analyzer.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property SignalDirection As PTCSignalDirection
```

### Return Type

A combination of the X, Y and Z direction flags of the PTCSignalDirection Enumeration.

### Remarks

The property returns the flag for the direction none when the channel is no 3D channel.


---

## Title Property

*Quelle: `POLYPROPERTIESLib~AnalyzerViewSettings~Title.html` · Polytec PolyProperties Type Library · AnalyzerViewSettings Object : Title Property*

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

*Quelle: `POLYPROPERTIESLib~AnalyzerViewSettings~TitleFont.html` · Polytec PolyProperties Type Library · AnalyzerViewSettings Object : TitleFont Property*

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

*Quelle: `POLYPROPERTIESLib~AnalyzerViewSettings~XRangeSettings.html` · Polytec PolyProperties Type Library · AnalyzerViewSettings Object : XRangeSettings Property*

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

*Quelle: `POLYPROPERTIESLib~AnalyzerViewSettings~YRangeSettings.html` · Polytec PolyProperties Type Library · AnalyzerViewSettings Object : YRangeSettings Property*

### Description

Specifies the settings of the ranges of the y-axes.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property YRangeSettings As RangeSettingsColl
```
