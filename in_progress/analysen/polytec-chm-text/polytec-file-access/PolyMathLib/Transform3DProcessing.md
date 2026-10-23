# PolyMathLib – Transform3DProcessing

## Transform3DProcessing Object

*Quelle: `PolyMathLib~Transform3DProcessing.html` · Polytec PolyMath Type Library*

### Description

Provides a transformation from one Cartesian 3D coordinate system to another.


---

## Transform3DProcessing Object Members

*Quelle: `PolyMathLib~Transform3DProcessing_members.html` · Polytec PolyMath Type Library*

### Public Methods

| CalculateTransformation | Calculates the transformation from pairs of 3D coordinates given in the first and second coordinate system. |
|---|---|
| CalculateTransformationAndQuality | Calculates the transformation from pairs of 3D coordinates given in the first and second coordinate system. |
| GetPointQuality | Calculates the quality of the transformation of the specified point sets. |
| Transform3DPoints | Transforms points with 3D coordinates given in the first system to 3D coordinates in the second system. |

### Public Properties

| TransformationQuality | Returns the quality of the transformation. |
|---|---|


---

## CalculateTransformation Method

*Quelle: `PolyMathLib~Transform3DProcessing~CalculateTransformation.html` · Polytec PolyMath Type Library · Transform3DProcessing Object : CalculateTransformation Method*

### Description

Calculates the transformation from pairs of 3D coordinates given in the first and second coordinate system.

### Syntax

*Visual Basic:*
```
Public Function CalculateTransformation( _
   ByVal pointMatchFirst() As Single, _
   ByVal pointMatchSecond() As Single _
) As Boolean
```

### Parameters

pointMatchFirst

One-dimensional array of 3D coordinates (interleaved x0, y0, z0, x1, y1, z1, ...) in the first coordinate system. The length of the array must be dividable by 3.

pointMatchSecond

One-dimensional array of 3D coordinates (interleaved x0, y0, z0, x1, y1, z1, ...) in the second coordinate system. The length of the array must be dividable by 3 and the same as the array for the coordinates from the first system.

### Return Type

True if the calculation succeeded.

### Remarks

At least three pairs of points must be given.


---

## CalculateTransformationAndQuality Method

*Quelle: `PolyMathLib~Transform3DProcessing~CalculateTransformationAndQuality.html` · Polytec PolyMath Type Library · Transform3DProcessing Object : CalculateTransformationAndQuality Method*

### Description

Calculates the transformation from pairs of 3D coordinates given in the first and second coordinate system.

### Syntax

*Visual Basic:*
```
Public Function CalculateTransformationAndQuality( _
   ByVal pointMatchFirst() As Single, _
   ByVal pointMatchSecond() As Single, _
   ByRef quality As Double _
) As Boolean
```

### Parameters

pointMatchFirst

One-dimensional array of 3D coordinates (interleaved x0, y0, z0, x1, y1, z1, ...) in the first coordinate system. The length of the array must be dividable by 3.

pointMatchSecond

One-dimensional array of 3D coordinates (interleaved x0, y0, z0, x1, y1, z1, ...) in the second coordinate system. The length of the array must be dividable by 3 and the same as the array for the coordinates from the first system.

quality

Receives the quality of the calculated transformation as the average distance between target coordinates and the transformed actual coordinates.

### Return Type

True if the calculation succeeded.

### Remarks

At least three pairs of points must be given.


---

## GetPointQuality Method

*Quelle: `PolyMathLib~Transform3DProcessing~GetPointQuality.html` · Polytec PolyMath Type Library · Transform3DProcessing Object : GetPointQuality Method*

### Description

Calculates the quality of the transformation of the specified point sets.

### Syntax

*Visual Basic:*
```
Public Function GetPointQuality( _
   ByVal firstPointCoordinates() As Single, _
   ByVal secondPointCoordinates() As Single _
) As Double
```

### Parameters

firstPointCoordinates

One-dimensional array of 3D coordinates (interleaved x0, y0, z0, x1, y1, z1, ...) in the first coordinate system. The length of the array must be dividable by 3.

secondPointCoordinates

One-dimensional array of 3D coordinates (interleaved x0, y0, z0, x1, y1, z1, ...) in the second coordinate system. The length of the array must be dividable by 3 and the same as the array for the coordinates from the first system.

### Return Type

The quality of the transformation of the specified point sets as the average distance between target coordinates and the transformed actual coordinates.


---

## Transform3DPoints Method

*Quelle: `PolyMathLib~Transform3DProcessing~Transform3DPoints.html` · Polytec PolyMath Type Library · Transform3DProcessing Object : Transform3DPoints Method*

### Description

Transforms points with 3D coordinates given in the first system to 3D coordinates in the second system.

### Syntax

*Visual Basic:*
```
Public Function Transform3DPoints( _
   ByVal pointCoordinates() As Single _
) As Single()
```

### Parameters

pointCoordinates

One-dimensional array of 3D coordinates (interleaved x0, y0, z0, x1, y1, z1, ...) in the first coordinate system. The length of the array must be dividable by 3.

### Return Type

One-dimensional array of 3D coordinates (interleaved x0, y0, z0, x1, y1, z1, ...) in the second coordinate system.


---

## TransformationQuality Property

*Quelle: `PolyMathLib~Transform3DProcessing~TransformationQuality.html` · Polytec PolyMath Type Library · Transform3DProcessing Object : TransformationQuality Property*

### Description

Returns the quality of the transformation.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property TransformationQuality As Double
```

### Return Type

Receives the quality of the calculated transformation as the average distance between target coordinates and the transformed actual coordinates.
