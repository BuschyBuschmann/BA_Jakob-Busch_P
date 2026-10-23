# PolyFrontEndLib – FrontEndControlDioDac

## FrontEndControlDioDac Object

*Quelle: `PolyFrontEndLib~FrontEndControlDioDac.html` · Polytec PolyFrontEnd Type Library*

### Description

Controls the digital analog converters and the digital i/o lines of the junction box.


---

## FrontEndControlDioDac Object Members

*Quelle: `PolyFrontEndLib~FrontEndControlDioDac_members.html` · Polytec PolyFrontEnd Type Library*

### Public Methods

| GetDacValues | Gets the current DAC values of those channels that are listed in the Channels array. |
|---|---|
| GetMaxRange | Returns the maximum value of the DAC range in DAC steps. |
| GetMaxVoltage | Returns the maximum value of the DAC range in volts. |
| GetMinRange | Returns the minimum value of the DAC range in DAC steps. |
| GetMinVoltage | Returns the minimum value of the DAC range in volts. |
| SetDacValues | Sets the DAC values of those channels that are listed in the Channels array. For every channel you can specify a target value in DAC steps in the Values array, a move time in the MoveTimes array and a move type in the MoveTypes array. |
| StartSpeckleTracking | Starts speckle tracking, i.e. moving the laser on a track around the current position. The Positions array contains successive pairs of DAC values in DAC steps, that will be continuously added to the current DAC values for the different channels. |
| StopSpeckleTracking | Stops speckle tracking. |

### Public Properties

| Channels | The number of available digital analog converter channels. |
|---|---|
| Gate | The current status of the gate input of the junction box. |
| Handset | A bit-coded value representing the current status of the buttons of the handset (PSV-A-051). |
| MaxPositionCount | The maximum number of positions that can be used for speckle tracking. |
| MaxTimePerStep | The maximum time per step that can be used for speckle tracking in second. |
| MinPositionCount | The minimum number of positions that can be used for speckle tracking. |
| MinTimePerStep | The minimum time per step that can be used for speckle tracking in second. |
| PanTilt | Specifies a bit-coded value controlling the pan tilt head. |
| SpeckleTracking | True, if speckle tracking is currently active. |


---

## GetDacValues Method

*Quelle: `PolyFrontEndLib~FrontEndControlDioDac~GetDacValues.html` · Polytec PolyFrontEnd Type Library · FrontEndControlDioDac Object : GetDacValues Method*

### Description

Gets the current DAC values of those channels that are listed in the Channels array.

### Syntax

*Visual Basic:*
```
Public Function GetDacValues( _
   ByVal psaChannels() As Long _
) As Long()
```

### Parameters

psaChannels

The channels to get the DAC values for.

### Example


---

## GetMaxRange Method

*Quelle: `PolyFrontEndLib~FrontEndControlDioDac~GetMaxRange.html` · Polytec PolyFrontEnd Type Library · FrontEndControlDioDac Object : GetMaxRange Method*

### Description

Returns the maximum value of the DAC range in DAC steps.

### Syntax

*Visual Basic:*
```
Public Function GetMaxRange( _
   ByVal lChannel As Long _
) As Long
```

### Parameters

lChannel

The 0-based number of the channel.

### Example


---

## GetMaxVoltage Method

*Quelle: `PolyFrontEndLib~FrontEndControlDioDac~GetMaxVoltage.html` · Polytec PolyFrontEnd Type Library · FrontEndControlDioDac Object : GetMaxVoltage Method*

### Description

Returns the maximum value of the DAC range in volts.

### Syntax

*Visual Basic:*
```
Public Function GetMaxVoltage( _
   ByVal lChannel As Long _
) As Double
```

### Parameters

lChannel

The 0-based number of the channel.

### Example


---

## GetMinRange Method

*Quelle: `PolyFrontEndLib~FrontEndControlDioDac~GetMinRange.html` · Polytec PolyFrontEnd Type Library · FrontEndControlDioDac Object : GetMinRange Method*

### Description

Returns the minimum value of the DAC range in DAC steps.

### Syntax

*Visual Basic:*
```
Public Function GetMinRange( _
   ByVal lChannel As Long _
) As Long
```

### Parameters

lChannel

The 0-based number of the channel.

### Example


---

## GetMinVoltage Method

*Quelle: `PolyFrontEndLib~FrontEndControlDioDac~GetMinVoltage.html` · Polytec PolyFrontEnd Type Library · FrontEndControlDioDac Object : GetMinVoltage Method*

### Description

Returns the minimum value of the DAC range in volts.

### Syntax

*Visual Basic:*
```
Public Function GetMinVoltage( _
   ByVal lChannel As Long _
) As Double
```

### Parameters

lChannel

The 0-based number of the channel.

### Example


---

## SetDacValues Method

*Quelle: `PolyFrontEndLib~FrontEndControlDioDac~SetDacValues.html` · Polytec PolyFrontEnd Type Library · FrontEndControlDioDac Object : SetDacValues Method*

### Description

Sets the DAC values of those channels that are listed in the Channels array. For every channel you can specify a target value in DAC steps in the Values array, a move time in the MoveTimes array and a move type in the MoveTypes array.

### Syntax

*Visual Basic:*
```
Public Sub SetDacValues( _
   ByVal psaChannels() As Long, _
   ByVal psaValues() As Long, _
   ByVal psaMoveTimes() As Double, _
   ByVal psaMoveTypes() As PTCFrontEndDacMovingType _
)
```

### Parameters

psaChannels

The 0-based array of 0-based channel numbers.

psaValues

The 0-based array of DAC values.

psaMoveTimes

The 0-based array of move times in s.

psaMoveTypes

| Value | Description |
|---|---|
| ptcFrontEndDacMovingTypeBestehornSinoid | Bestehorn Sinoid. |
| ptcFrontEndDacMovingTypeGutmannSinoid | Gutmanns Sinoid. |
| ptcFrontEndDacMovingTypeStep | Instantaneous step. |
The 0-based array of move types.

### Remarks

The arrays passed to this method must have the same size. The Bestehorn and Gutmanns sinoid can only be used, if you set the values for two channels, the numbers of channels are successive, the first number is even and the second number is odd. Only in this case both channels belong to the same scanning head and the mirrors can be moved simultaneously.

### Example


---

## StartSpeckleTracking Method

*Quelle: `PolyFrontEndLib~FrontEndControlDioDac~StartSpeckleTracking.html` · Polytec PolyFrontEnd Type Library · FrontEndControlDioDac Object : StartSpeckleTracking Method*

### Description

Starts speckle tracking, i.e. moving the laser on a track around the current position. The Positions array contains successive pairs of DAC values in DAC steps, that will be continuously added to the current DAC values for the different channels.

### Syntax

*Visual Basic:*
```
Public Sub StartSpeckleTracking( _
   ByVal psaPositionsTop() As Long, _
   ByVal psaPositionsLeft() As Long, _
   ByVal psaPositionsRight() As Long, _
   ByVal dTimePerStep As Double _
)
```

### Parameters

psaPositionsTop

The positions for the scanning head top.

psaPositionsLeft

The positions for the scanning head left.

psaPositionsRight

The positions for the scanning head right.

dTimePerStep

The time per step in second.


---

## StopSpeckleTracking Method

*Quelle: `PolyFrontEndLib~FrontEndControlDioDac~StopSpeckleTracking.html` · Polytec PolyFrontEnd Type Library · FrontEndControlDioDac Object : StopSpeckleTracking Method*

### Description

Stops speckle tracking.

### Syntax

*Visual Basic:*
```
Public Sub StopSpeckleTracking()
```


---

## Channels Property

*Quelle: `PolyFrontEndLib~FrontEndControlDioDac~Channels.html` · Polytec PolyFrontEnd Type Library · FrontEndControlDioDac Object : Channels Property*

### Description

The number of available digital analog converter channels.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Channels As Long
```


---

## Gate Property

*Quelle: `PolyFrontEndLib~FrontEndControlDioDac~Gate.html` · Polytec PolyFrontEnd Type Library · FrontEndControlDioDac Object : Gate Property*

### Description

The current status of the gate input of the junction box.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Gate As Boolean
```

### Example


---

## Handset Property

*Quelle: `PolyFrontEndLib~FrontEndControlDioDac~Handset.html` · Polytec PolyFrontEnd Type Library · FrontEndControlDioDac Object : Handset Property*

### Description

A bit-coded value representing the current status of the buttons of the handset (PSV-A-051).

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Handset As Long
```


---

## MaxPositionCount Property

*Quelle: `PolyFrontEndLib~FrontEndControlDioDac~MaxPositionCount.html` · Polytec PolyFrontEnd Type Library · FrontEndControlDioDac Object : MaxPositionCount Property*

### Description

The maximum number of positions that can be used for speckle tracking.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property MaxPositionCount As Long
```


---

## MaxTimePerStep Property

*Quelle: `PolyFrontEndLib~FrontEndControlDioDac~MaxTimePerStep.html` · Polytec PolyFrontEnd Type Library · FrontEndControlDioDac Object : MaxTimePerStep Property*

### Description

The maximum time per step that can be used for speckle tracking in second.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property MaxTimePerStep As Double
```


---

## MinPositionCount Property

*Quelle: `PolyFrontEndLib~FrontEndControlDioDac~MinPositionCount.html` · Polytec PolyFrontEnd Type Library · FrontEndControlDioDac Object : MinPositionCount Property*

### Description

The minimum number of positions that can be used for speckle tracking.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property MinPositionCount As Long
```


---

## MinTimePerStep Property

*Quelle: `PolyFrontEndLib~FrontEndControlDioDac~MinTimePerStep.html` · Polytec PolyFrontEnd Type Library · FrontEndControlDioDac Object : MinTimePerStep Property*

### Description

The minimum time per step that can be used for speckle tracking in second.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property MinTimePerStep As Double
```


---

## PanTilt Property

*Quelle: `PolyFrontEndLib~FrontEndControlDioDac~PanTilt.html` · Polytec PolyFrontEnd Type Library · FrontEndControlDioDac Object : PanTilt Property*

### Description

Specifies a bit-coded value controlling the pan tilt head.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property PanTilt As Long
```

### Remarks

Bits 0-3 are used. all other bits have to be 0. A set bit moves the pan tilt head into the corresponding direction. You have to set the property again with a value of 0 to stop the movement.


---

## SpeckleTracking Property

*Quelle: `PolyFrontEndLib~FrontEndControlDioDac~SpeckleTracking.html` · Polytec PolyFrontEnd Type Library · FrontEndControlDioDac Object : SpeckleTracking Property*

### Description

True, if speckle tracking is currently active.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property SpeckleTracking As Boolean
```
