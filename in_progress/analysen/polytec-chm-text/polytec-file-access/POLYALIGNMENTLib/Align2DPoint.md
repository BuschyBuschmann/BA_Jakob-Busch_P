# POLYALIGNMENTLib – Align2DPoint

## Align2DPoint Object

*Quelle: `POLYALIGNMENTLib~Align2DPoint.html` · Polytec PolyAlignment Type Library*

### Description

Item of the Align2DPoints collection.


---

## Align2DPoint Object Members

*Quelle: `POLYALIGNMENTLib~Align2DPoint_members.html` · Polytec PolyAlignment Type Library*

### Public Methods

| Copy | Copies the Align2DPoint from the input parameter to this object. |
|---|---|
| IsEqual | Returns true if the input Align2DPoint is equal to this 2D alignment point. |

### Public Properties

| ScannerX | Horizontal scanner value (angle or displacement) of the 2D alignment point. |
|---|---|
| ScannerY | Vertical scanner value (angle or displacement) of the 2D alignment point. |
| VideoX | X video coordinate of the 2D alignment point. |
| VideoY | Y video coordinate of the 2D alignment point. |


---

## Copy Method

*Quelle: `POLYALIGNMENTLib~Align2DPoint~Copy.html` · Polytec PolyAlignment Type Library · Align2DPoint Object : Copy Method*

### Description

Copies the Align2DPoint from the input parameter to this object.

### Syntax

*Visual Basic:*
```
Public Sub Copy( _
   ByVal pIAlign2DPoint As Align2DPoint _
)
```

### Parameters

pIAlign2DPoint

The input Align2DPoint.


---

## IsEqual Method

*Quelle: `POLYALIGNMENTLib~Align2DPoint~IsEqual.html` · Polytec PolyAlignment Type Library · Align2DPoint Object : IsEqual Method*

### Description

Returns true if the input Align2DPoint is equal to this 2D alignment point.

### Syntax

*Visual Basic:*
```
Public Function IsEqual( _
   ByVal pIAlign2DPoint As Align2DPoint _
) As Boolean
```

### Parameters

pIAlign2DPoint

The input Align2DPoint.


---

## ScannerX Property

*Quelle: `POLYALIGNMENTLib~Align2DPoint~ScannerX.html` · Polytec PolyAlignment Type Library · Align2DPoint Object : ScannerX Property*

### Description

Horizontal scanner value (angle or displacement) of the 2D alignment point.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property ScannerX As Double
```


---

## ScannerY Property

*Quelle: `POLYALIGNMENTLib~Align2DPoint~ScannerY.html` · Polytec PolyAlignment Type Library · Align2DPoint Object : ScannerY Property*

### Description

Vertical scanner value (angle or displacement) of the 2D alignment point.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property ScannerY As Double
```


---

## VideoX Property

*Quelle: `POLYALIGNMENTLib~Align2DPoint~VideoX.html` · Polytec PolyAlignment Type Library · Align2DPoint Object : VideoX Property*

### Description

X video coordinate of the 2D alignment point.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property VideoX As Single
```


---

## VideoY Property

*Quelle: `POLYALIGNMENTLib~Align2DPoint~VideoY.html` · Polytec PolyAlignment Type Library · Align2DPoint Object : VideoY Property*

### Description

Y video coordinate of the 2D alignment point.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property VideoY As Single
```
