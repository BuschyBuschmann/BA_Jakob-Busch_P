# PSV – PositionDevice

## PositionDevice Object

*Quelle: `PSV~PositionDevice.html` · Polytec PSV Type Library*

### Description

The object controls the XY, Z or XYZ position device of the system.


---

## PositionDevice Object Members

*Quelle: `PSV~PositionDevice_members.html` · Polytec PSV Type Library*

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

*Quelle: `PSV~PositionDevice~GetPositionXY.html` · Polytec PSV Type Library · PositionDevice Object : GetPositionXY Method*

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

*Quelle: `PSV~PositionDevice~GetPositionZ.html` · Polytec PSV Type Library · PositionDevice Object : GetPositionZ Method*

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

*Quelle: `PSV~PositionDevice~StartMoveXY.html` · Polytec PSV Type Library · PositionDevice Object : StartMoveXY Method*

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

*Quelle: `PSV~PositionDevice~StartMoveZ.html` · Polytec PSV Type Library · PositionDevice Object : StartMoveZ Method*

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

*Quelle: `PSV~PositionDevice~HasXYAxes.html` · Polytec PSV Type Library · PositionDevice Object : HasXYAxes Property*

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

*Quelle: `PSV~PositionDevice~HasZAxis.html` · Polytec PSV Type Library · PositionDevice Object : HasZAxis Property*

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

*Quelle: `PSV~PositionDevice~IsMovingXY.html` · Polytec PSV Type Library · PositionDevice Object : IsMovingXY Property*

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

*Quelle: `PSV~PositionDevice~IsMovingZ.html` · Polytec PSV Type Library · PositionDevice Object : IsMovingZ Property*

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

*Quelle: `PSV~PositionDevice~IsReferencedXY.html` · Polytec PSV Type Library · PositionDevice Object : IsReferencedXY Property*

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

*Quelle: `PSV~PositionDevice~IsReferencedZ.html` · Polytec PSV Type Library · PositionDevice Object : IsReferencedZ Property*

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

*Quelle: `PSV~PositionDevice~JoystickAvailable.html` · Polytec PSV Type Library · PositionDevice Object : JoystickAvailable Property*

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

*Quelle: `PSV~PositionDevice~JoystickEnabled.html` · Polytec PSV Type Library · PositionDevice Object : JoystickEnabled Property*

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

*Quelle: `PSV~PositionDevice~Name.html` · Polytec PSV Type Library · PositionDevice Object : Name Property*

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

*Quelle: `PSV~PositionDevice~PositionXMax.html` · Polytec PSV Type Library · PositionDevice Object : PositionXMax Property*

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

*Quelle: `PSV~PositionDevice~PositionXMaxHardware.html` · Polytec PSV Type Library · PositionDevice Object : PositionXMaxHardware Property*

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

*Quelle: `PSV~PositionDevice~PositionXMin.html` · Polytec PSV Type Library · PositionDevice Object : PositionXMin Property*

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

*Quelle: `PSV~PositionDevice~PositionXMinHardware.html` · Polytec PSV Type Library · PositionDevice Object : PositionXMinHardware Property*

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

*Quelle: `PSV~PositionDevice~PositionYMax.html` · Polytec PSV Type Library · PositionDevice Object : PositionYMax Property*

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

*Quelle: `PSV~PositionDevice~PositionYMaxHardware.html` · Polytec PSV Type Library · PositionDevice Object : PositionYMaxHardware Property*

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

*Quelle: `PSV~PositionDevice~PositionYMin.html` · Polytec PSV Type Library · PositionDevice Object : PositionYMin Property*

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

*Quelle: `PSV~PositionDevice~PositionYMinHardware.html` · Polytec PSV Type Library · PositionDevice Object : PositionYMinHardware Property*

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

*Quelle: `PSV~PositionDevice~PositionZMax.html` · Polytec PSV Type Library · PositionDevice Object : PositionZMax Property*

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

*Quelle: `PSV~PositionDevice~PositionZMaxHardware.html` · Polytec PSV Type Library · PositionDevice Object : PositionZMaxHardware Property*

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

*Quelle: `PSV~PositionDevice~PositionZMin.html` · Polytec PSV Type Library · PositionDevice Object : PositionZMin Property*

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

*Quelle: `PSV~PositionDevice~PositionZMinHardware.html` · Polytec PSV Type Library · PositionDevice Object : PositionZMinHardware Property*

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

*Quelle: `PSV~PositionDevice~Type.html` · Polytec PSV Type Library · PositionDevice Object : Type Property*

### Description

Returns ptcInfoPositionDevice. Can be used as index to the InfosAcq collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Type As PTCInfoType
```
