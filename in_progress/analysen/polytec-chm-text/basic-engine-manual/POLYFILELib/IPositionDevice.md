# POLYFILELib – IPositionDevice

## IPositionDevice Interface

*Quelle: `POLYFILELib~IPositionDevice.html` · Polytec PolyFile Type Library*

### Description

The object controls the XY, Z or XYZ position device of the system.

### Remarks

It is recommended to cast to the PositionDevice Object.


---

## IPositionDevice Interface Members

*Quelle: `POLYFILELib~IPositionDevice_members.html` · Polytec PolyFile Type Library*

### Public Methods

| GetPositionXY | Gets the current positions of the x- and the y-axis in meter. |
|---|---|
| GetPositionZ | Gets the current position of the z-axis in meter. |
| StartMoveXY | Starts moving the x- and the y-axis to the specified positions. |
| StartMoveZ | Starts moving the z-axis to the specified position. |

### Public Properties

| HasXYAxes | Returns whether the system has a x- and a y-axis. |
|---|---|
| HasZAxis | Returns whether the system has a z-axis. |
| IsMovingXY | Returns whether the x- and the y-axis move. |
| IsMovingZ | Returns whether the z-axis moves. |
| IsReferencedXY | Returns whether the x- and the y-axis are referenced. |
| IsReferencedZ | Returns whether the z-axis is referenced. |
| JoystickAvailable | Returns whether a joystick is available. |
| JoystickEnabled | Specifies whether the joystick is enabled. |
| Name | Returns the name of the position device. |
| PositionXMax | Specifies the maximum position of the x-axis in meter. |
| PositionXMaxHardware | Returns the maximum position of the x-axis in meter. |
| PositionXMin | Specifies the minimum position of the x-axis in meter. |
| PositionXMinHardware | Returns the minimum position of the x-axis in meter. |
| PositionYMax | Specifies the maximum position of the y-axis in meter. |
| PositionYMaxHardware | Returns the maximum position of the y-axis in meter. |
| PositionYMin | Specifies the minimum position of the y-axis in meter. |
| PositionYMinHardware | Returns the minimum position of the y-axis in meter. |
| PositionZMax | Specifies the maximum position of the z-axis in meter. |
| PositionZMaxHardware | Returns the maximum position of the z-axis in meter. |
| PositionZMin | Specifies the minimum position of the z-axis in meter. |
| PositionZMinHardware | Returns the minimum position of the z-axis in meter. |
| Type | Returns ptcInfoPositionDevice. Can be used as index to the InfosAcq collection . |


---

## GetPositionXY Method

*Quelle: `POLYFILELib~IPositionDevice~GetPositionXY.html` · Polytec PolyFile Type Library · IPositionDevice Interface : GetPositionXY Method*

### Description

Gets the current positions of the x- and the y-axis in meter.

### Syntax

*Visual Basic:*
```
Public Sub GetPositionXY( _
   ByRef posX As Double, _
   ByRef posY As Double _
)
```

### Parameters

posX

The current position of the x-axis in meter.

posY

The current position of the y-axis in meter.


---

## GetPositionZ Method

*Quelle: `POLYFILELib~IPositionDevice~GetPositionZ.html` · Polytec PolyFile Type Library · IPositionDevice Interface : GetPositionZ Method*

### Description

Gets the current position of the z-axis in meter.

### Syntax

*Visual Basic:*
```
Public Sub GetPositionZ( _
   ByRef posZ As Double _
)
```

### Parameters

posZ

The current position of the z-axis in meter.


---

## StartMoveXY Method

*Quelle: `POLYFILELib~IPositionDevice~StartMoveXY.html` · Polytec PolyFile Type Library · IPositionDevice Interface : StartMoveXY Method*

### Description

Starts moving the x- and the y-axis to the specified positions.

### Syntax

*Visual Basic:*
```
Public Sub StartMoveXY( _
   ByVal posX As Double, _
   ByVal posY As Double _
)
```

### Parameters

posX

The target position for the x-axis in meter.

posY

The target position for the y-axis in meter.


---

## StartMoveZ Method

*Quelle: `POLYFILELib~IPositionDevice~StartMoveZ.html` · Polytec PolyFile Type Library · IPositionDevice Interface : StartMoveZ Method*

### Description

Starts moving the z-axis to the specified position.

### Syntax

*Visual Basic:*
```
Public Sub StartMoveZ( _
   ByVal posZ As Double _
)
```

### Parameters

posZ

The target position for the z-axis in meter.


---

## HasXYAxes Property

*Quelle: `POLYFILELib~IPositionDevice~HasXYAxes.html` · Polytec PolyFile Type Library · IPositionDevice Interface : HasXYAxes Property*

### Description

Returns whether the system has a x- and a y-axis.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property HasXYAxes As Boolean
```


---

## HasZAxis Property

*Quelle: `POLYFILELib~IPositionDevice~HasZAxis.html` · Polytec PolyFile Type Library · IPositionDevice Interface : HasZAxis Property*

### Description

Returns whether the system has a z-axis.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property HasZAxis As Boolean
```


---

## IsMovingXY Property

*Quelle: `POLYFILELib~IPositionDevice~IsMovingXY.html` · Polytec PolyFile Type Library · IPositionDevice Interface : IsMovingXY Property*

### Description

Returns whether the x- and the y-axis move.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property IsMovingXY As Boolean
```


---

## IsMovingZ Property

*Quelle: `POLYFILELib~IPositionDevice~IsMovingZ.html` · Polytec PolyFile Type Library · IPositionDevice Interface : IsMovingZ Property*

### Description

Returns whether the z-axis moves.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property IsMovingZ As Boolean
```


---

## IsReferencedXY Property

*Quelle: `POLYFILELib~IPositionDevice~IsReferencedXY.html` · Polytec PolyFile Type Library · IPositionDevice Interface : IsReferencedXY Property*

### Description

Returns whether the x- and the y-axis are referenced.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property IsReferencedXY As Boolean
```


---

## IsReferencedZ Property

*Quelle: `POLYFILELib~IPositionDevice~IsReferencedZ.html` · Polytec PolyFile Type Library · IPositionDevice Interface : IsReferencedZ Property*

### Description

Returns whether the z-axis is referenced.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property IsReferencedZ As Boolean
```


---

## JoystickAvailable Property

*Quelle: `POLYFILELib~IPositionDevice~JoystickAvailable.html` · Polytec PolyFile Type Library · IPositionDevice Interface : JoystickAvailable Property*

### Description

Returns whether a joystick is available.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property JoystickAvailable As Boolean
```


---

## JoystickEnabled Property

*Quelle: `POLYFILELib~IPositionDevice~JoystickEnabled.html` · Polytec PolyFile Type Library · IPositionDevice Interface : JoystickEnabled Property*

### Description

Specifies whether the joystick is enabled.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property JoystickEnabled As Boolean
```


---

## Name Property

*Quelle: `POLYFILELib~IPositionDevice~Name.html` · Polytec PolyFile Type Library · IPositionDevice Interface : Name Property*

### Description

Returns the name of the position device.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Name As String
```


---

## PositionXMax Property

*Quelle: `POLYFILELib~IPositionDevice~PositionXMax.html` · Polytec PolyFile Type Library · IPositionDevice Interface : PositionXMax Property*

### Description

Specifies the maximum position of the x-axis in meter.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property PositionXMax As Double
```


---

## PositionXMaxHardware Property

*Quelle: `POLYFILELib~IPositionDevice~PositionXMaxHardware.html` · Polytec PolyFile Type Library · IPositionDevice Interface : PositionXMaxHardware Property*

### Description

Returns the maximum position of the x-axis in meter.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property PositionXMaxHardware As Double
```


---

## PositionXMin Property

*Quelle: `POLYFILELib~IPositionDevice~PositionXMin.html` · Polytec PolyFile Type Library · IPositionDevice Interface : PositionXMin Property*

### Description

Specifies the minimum position of the x-axis in meter.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property PositionXMin As Double
```


---

## PositionXMinHardware Property

*Quelle: `POLYFILELib~IPositionDevice~PositionXMinHardware.html` · Polytec PolyFile Type Library · IPositionDevice Interface : PositionXMinHardware Property*

### Description

Returns the minimum position of the x-axis in meter.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property PositionXMinHardware As Double
```


---

## PositionYMax Property

*Quelle: `POLYFILELib~IPositionDevice~PositionYMax.html` · Polytec PolyFile Type Library · IPositionDevice Interface : PositionYMax Property*

### Description

Specifies the maximum position of the y-axis in meter.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property PositionYMax As Double
```


---

## PositionYMaxHardware Property

*Quelle: `POLYFILELib~IPositionDevice~PositionYMaxHardware.html` · Polytec PolyFile Type Library · IPositionDevice Interface : PositionYMaxHardware Property*

### Description

Returns the maximum position of the y-axis in meter.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property PositionYMaxHardware As Double
```


---

## PositionYMin Property

*Quelle: `POLYFILELib~IPositionDevice~PositionYMin.html` · Polytec PolyFile Type Library · IPositionDevice Interface : PositionYMin Property*

### Description

Specifies the minimum position of the y-axis in meter.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property PositionYMin As Double
```


---

## PositionYMinHardware Property

*Quelle: `POLYFILELib~IPositionDevice~PositionYMinHardware.html` · Polytec PolyFile Type Library · IPositionDevice Interface : PositionYMinHardware Property*

### Description

Returns the minimum position of the y-axis in meter.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property PositionYMinHardware As Double
```


---

## PositionZMax Property

*Quelle: `POLYFILELib~IPositionDevice~PositionZMax.html` · Polytec PolyFile Type Library · IPositionDevice Interface : PositionZMax Property*

### Description

Specifies the maximum position of the z-axis in meter.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property PositionZMax As Double
```


---

## PositionZMaxHardware Property

*Quelle: `POLYFILELib~IPositionDevice~PositionZMaxHardware.html` · Polytec PolyFile Type Library · IPositionDevice Interface : PositionZMaxHardware Property*

### Description

Returns the maximum position of the z-axis in meter.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property PositionZMaxHardware As Double
```


---

## PositionZMin Property

*Quelle: `POLYFILELib~IPositionDevice~PositionZMin.html` · Polytec PolyFile Type Library · IPositionDevice Interface : PositionZMin Property*

### Description

Specifies the minimum position of the z-axis in meter.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property PositionZMin As Double
```


---

## PositionZMinHardware Property

*Quelle: `POLYFILELib~IPositionDevice~PositionZMinHardware.html` · Polytec PolyFile Type Library · IPositionDevice Interface : PositionZMinHardware Property*

### Description

Returns the minimum position of the z-axis in meter.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property PositionZMinHardware As Double
```


---

## Type Property

*Quelle: `POLYFILELib~IPositionDevice~Type.html` · Polytec PolyFile Type Library · IPositionDevice Interface : Type Property*

### Description

Returns ptcInfoPositionDevice. Can be used as index to the InfosAcq collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Type As PTCInfoType
```
