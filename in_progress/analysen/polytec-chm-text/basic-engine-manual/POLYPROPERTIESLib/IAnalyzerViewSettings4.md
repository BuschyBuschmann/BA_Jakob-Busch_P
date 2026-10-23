# POLYPROPERTIESLib – IAnalyzerViewSettings4

## IAnalyzerViewSettings4 Interface

*Quelle: `POLYPROPERTIESLib~IAnalyzerViewSettings4.html` · Polytec PolyProperties Type Library*

### Description

User interface settings of an analyzer view.

### Object Model

### Remarks

It is recommended to cast to the AnalyzerViewSettings Object.


---

## IAnalyzerViewSettings4 Interface Members

*Quelle: `POLYPROPERTIESLib~IAnalyzerViewSettings4_members.html` · Polytec PolyProperties Type Library*

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

*Quelle: `POLYPROPERTIESLib~IAnalyzerViewSettings4~Clone.html` · Polytec PolyProperties Type Library · IAnalyzerViewSettings4 Interface : Clone Method*

### Description

Creates a copy of the settings object. The new object will be detached.

### Syntax

*Visual Basic:*
```
Public Function Clone() As IUISettings
```


---

## Copy Method

*Quelle: `POLYPROPERTIESLib~IAnalyzerViewSettings4~Copy.html` · Polytec PolyProperties Type Library · IAnalyzerViewSettings4 Interface : Copy Method*

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

*Quelle: `POLYPROPERTIESLib~IAnalyzerViewSettings4~Equal.html` · Polytec PolyProperties Type Library · IAnalyzerViewSettings4 Interface : Equal Method*

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

*Quelle: `POLYPROPERTIESLib~IAnalyzerViewSettings4~AxisLabelTickScale.html` · Polytec PolyProperties Type Library · IAnalyzerViewSettings4 Interface : AxisLabelTickScale Property*

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

*Quelle: `POLYPROPERTIESLib~IAnalyzerViewSettings4~BackColor.html` · Polytec PolyProperties Type Library · IAnalyzerViewSettings4 Interface : BackColor Property*

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

*Quelle: `POLYPROPERTIESLib~IAnalyzerViewSettings4~ChannelPinned.html` · Polytec PolyProperties Type Library · IAnalyzerViewSettings4 Interface : ChannelPinned Property*

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

*Quelle: `POLYPROPERTIESLib~IAnalyzerViewSettings4~ChannelSelection.html` · Polytec PolyProperties Type Library · IAnalyzerViewSettings4 Interface : ChannelSelection Property*

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

*Quelle: `POLYPROPERTIESLib~IAnalyzerViewSettings4~CurrentFrame.html` · Polytec PolyProperties Type Library · IAnalyzerViewSettings4 Interface : CurrentFrame Property*

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

*Quelle: `POLYPROPERTIESLib~IAnalyzerViewSettings4~CursorSettings.html` · Polytec PolyProperties Type Library · IAnalyzerViewSettings4 Interface : CursorSettings Property*

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

*Quelle: `POLYPROPERTIESLib~IAnalyzerViewSettings4~CursorType.html` · Polytec PolyProperties Type Library · IAnalyzerViewSettings4 Interface : CursorType Property*

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

*Quelle: `POLYPROPERTIESLib~IAnalyzerViewSettings4~DisplaySettings.html` · Polytec PolyProperties Type Library · IAnalyzerViewSettings4 Interface : DisplaySettings Property*

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

*Quelle: `POLYPROPERTIESLib~IAnalyzerViewSettings4~GridColor.html` · Polytec PolyProperties Type Library · IAnalyzerViewSettings4 Interface : GridColor Property*

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

*Quelle: `POLYPROPERTIESLib~IAnalyzerViewSettings4~GridStyle.html` · Polytec PolyProperties Type Library · IAnalyzerViewSettings4 Interface : GridStyle Property*

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

*Quelle: `POLYPROPERTIESLib~IAnalyzerViewSettings4~LegendColor.html` · Polytec PolyProperties Type Library · IAnalyzerViewSettings4 Interface : LegendColor Property*

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

*Quelle: `POLYPROPERTIESLib~IAnalyzerViewSettings4~LineSettings.html` · Polytec PolyProperties Type Library · IAnalyzerViewSettings4 Interface : LineSettings Property*

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

*Quelle: `POLYPROPERTIESLib~IAnalyzerViewSettings4~Modified.html` · Polytec PolyProperties Type Library · IAnalyzerViewSettings4 Interface : Modified Property*

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

*Quelle: `POLYPROPERTIESLib~IAnalyzerViewSettings4~Parent.html` · Polytec PolyProperties Type Library · IAnalyzerViewSettings4 Interface : Parent Property*

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

*Quelle: `POLYPROPERTIESLib~IAnalyzerViewSettings4~SelectedFrames.html` · Polytec PolyProperties Type Library · IAnalyzerViewSettings4 Interface : SelectedFrames Property*

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

*Quelle: `POLYPROPERTIESLib~IAnalyzerViewSettings4~ShowGrid.html` · Polytec PolyProperties Type Library · IAnalyzerViewSettings4 Interface : ShowGrid Property*

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

*Quelle: `POLYPROPERTIESLib~IAnalyzerViewSettings4~ShowTitle.html` · Polytec PolyProperties Type Library · IAnalyzerViewSettings4 Interface : ShowTitle Property*

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

*Quelle: `POLYPROPERTIESLib~IAnalyzerViewSettings4~SignalDirection.html` · Polytec PolyProperties Type Library · IAnalyzerViewSettings4 Interface : SignalDirection Property*

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

*Quelle: `POLYPROPERTIESLib~IAnalyzerViewSettings4~Title.html` · Polytec PolyProperties Type Library · IAnalyzerViewSettings4 Interface : Title Property*

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

*Quelle: `POLYPROPERTIESLib~IAnalyzerViewSettings4~TitleFont.html` · Polytec PolyProperties Type Library · IAnalyzerViewSettings4 Interface : TitleFont Property*

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

*Quelle: `POLYPROPERTIESLib~IAnalyzerViewSettings4~XRangeSettings.html` · Polytec PolyProperties Type Library · IAnalyzerViewSettings4 Interface : XRangeSettings Property*

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

*Quelle: `POLYPROPERTIESLib~IAnalyzerViewSettings4~YRangeSettings.html` · Polytec PolyProperties Type Library · IAnalyzerViewSettings4 Interface : YRangeSettings Property*

### Description

Specifies the settings of the ranges of the y-axes.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property YRangeSettings As RangeSettingsColl
```
