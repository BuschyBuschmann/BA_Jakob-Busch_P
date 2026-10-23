# POLYALIGNMENTLib – Align3DPoint

## Align3DPoint Object

*Quelle: `POLYALIGNMENTLib~Align3DPoint.html` · Polytec PolyAlignment Type Library*

### Description

Item of the Align3DPoints collection.


---

## Align3DPoint Object Members

*Quelle: `POLYALIGNMENTLib~Align3DPoint_members.html` · Polytec PolyAlignment Type Library*

### Public Methods

| Copy | Copies the Align3DPoint from the input parameter to this object. |
|---|---|
| IsEqual | Returns true if the Input Align3DPoint is equal to this 3D alignment point. |

### Public Properties

| Caps | The capabilities of the 3D alignment point. |
|---|---|
| Distance | The distance of the 3D alignment point. |
| Label | The label of the 3D alignment point. |
| PointType | The type of the 3D alignment point. |
| Quality | The quality in meter of the 3D alignment point. |
| ScannerX | Horizontal scanner value (angle or displacement) of the 3D alignment point. |
| ScannerY | Vertical scanner value (angle or displacement) of the 3D alignment point. |
| VideoX | X video coordinate of the 3D alignment point. |
| VideoY | Y video coordinate of the 3D alignment point. |
| X | The X value of the 3D coordinate of the 3D alignment point. |
| Y | The Y value of the 3D coordinate of the 3D alignment point. |
| Z | The Z value of the 3D coordinate of the 3D alignment point. |


---

## Copy Method

*Quelle: `POLYALIGNMENTLib~Align3DPoint~Copy.html` · Polytec PolyAlignment Type Library · Align3DPoint Object : Copy Method*

### Description

Copies the Align3DPoint from the input parameter to this object.

### Syntax

*Visual Basic:*
```
Public Sub Copy( _
   ByVal pIAlign3DPoint As Align3DPoint _
)
```

### Parameters

pIAlign3DPoint

Source Align3DPoint object.


---

## IsEqual Method

*Quelle: `POLYALIGNMENTLib~Align3DPoint~IsEqual.html` · Polytec PolyAlignment Type Library · Align3DPoint Object : IsEqual Method*

### Description

Returns true if the Input Align3DPoint is equal to this 3D alignment point.

### Syntax

*Visual Basic:*
```
Public Function IsEqual( _
   ByVal pIAlign3DPoint As Align3DPoint _
) As Boolean
```

### Parameters

pIAlign3DPoint

Align3DPoint object to be compared with.


---

## Caps Property

*Quelle: `POLYALIGNMENTLib~Align3DPoint~Caps.html` · Polytec PolyAlignment Type Library · Align3DPoint Object : Caps Property*

### Description

The capabilities of the 3D alignment point.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Caps As PTCAlign3DPointCapsType
```

### Remarks

Only if the corresponding flags in this property are set, the corresponding value is taken into account. After setting the property you have to set the corresponding flag, too.


---

## Distance Property

*Quelle: `POLYALIGNMENTLib~Align3DPoint~Distance.html` · Polytec PolyAlignment Type Library · Align3DPoint Object : Distance Property*

### Description

The distance of the 3D alignment point.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Distance As Double
```

### Remarks

This value is only valid if the property Caps contains the flag ptcAlign3DPointCapsDistance.


---

## Label Property

*Quelle: `POLYALIGNMENTLib~Align3DPoint~Label.html` · Polytec PolyAlignment Type Library · Align3DPoint Object : Label Property*

### Description

The label of the 3D alignment point.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Label As Long
```

### Remarks

The label is used to identify and link alignment points that are defined for different scanning heads.


---

## PointType Property

*Quelle: `POLYALIGNMENTLib~Align3DPoint~PointType.html` · Polytec PolyAlignment Type Library · Align3DPoint Object : PointType Property*

### Description

The type of the 3D alignment point.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property PointType As PTCAlign3DPointType
```


---

## Quality Property

*Quelle: `POLYALIGNMENTLib~Align3DPoint~Quality.html` · Polytec PolyAlignment Type Library · Align3DPoint Object : Quality Property*

### Description

The quality in meter of the 3D alignment point.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Quality As Double
```

### Remarks

This value is only valid if the property Caps contains the flag ptcAlign3DpointCapsQuality.


---

## ScannerX Property

*Quelle: `POLYALIGNMENTLib~Align3DPoint~ScannerX.html` · Polytec PolyAlignment Type Library · Align3DPoint Object : ScannerX Property*

### Description

Horizontal scanner value (angle or displacement) of the 3D alignment point.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property ScannerX As Double
```

### Remarks

This value is only valid if the property Caps contains the flag ptcAlign3DPointCapsScanner.


---

## ScannerY Property

*Quelle: `POLYALIGNMENTLib~Align3DPoint~ScannerY.html` · Polytec PolyAlignment Type Library · Align3DPoint Object : ScannerY Property*

### Description

Vertical scanner value (angle or displacement) of the 3D alignment point.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property ScannerY As Double
```

### Remarks

This value is only valid if the property Caps contains the flag ptcAlign3DPointCapsScanner.


---

## VideoX Property

*Quelle: `POLYALIGNMENTLib~Align3DPoint~VideoX.html` · Polytec PolyAlignment Type Library · Align3DPoint Object : VideoX Property*

### Description

X video coordinate of the 3D alignment point.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property VideoX As Single
```

### Remarks

This value is only valid if the property Caps contains the flag ptcAlign3DPointCapsVideo.


---

## VideoY Property

*Quelle: `POLYALIGNMENTLib~Align3DPoint~VideoY.html` · Polytec PolyAlignment Type Library · Align3DPoint Object : VideoY Property*

### Description

Y video coordinate of the 3D alignment point.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property VideoY As Single
```

### Remarks

This value is only valid if the property Caps contains the flag ptcAlign3DPointCapsVideo.


---

## X Property

*Quelle: `POLYALIGNMENTLib~Align3DPoint~X.html` · Polytec PolyAlignment Type Library · Align3DPoint Object : X Property*

### Description

The X value of the 3D coordinate of the 3D alignment point.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property X As Double
```

### Remarks

This value is only valid if the property Caps contains the flag ptcAlign3DPointCaps3DCoord.


---

## Y Property

*Quelle: `POLYALIGNMENTLib~Align3DPoint~Y.html` · Polytec PolyAlignment Type Library · Align3DPoint Object : Y Property*

### Description

The Y value of the 3D coordinate of the 3D alignment point.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Y As Double
```

### Remarks

This value is only valid if the property Caps contains the flag ptcAlign3DPointCaps3DCoord.


---

## Z Property

*Quelle: `POLYALIGNMENTLib~Align3DPoint~Z.html` · Polytec PolyAlignment Type Library · Align3DPoint Object : Z Property*

### Description

The Z value of the 3D coordinate of the 3D alignment point.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Z As Double
```

### Remarks

This value is only valid if the property Caps contains the flag ptcAlign3DPointCaps3DCoord.
