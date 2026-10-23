# POLYFILELib – MeasPoints

## MeasPoints Collection

*Quelle: `POLYFILELib~MeasPoints.html` · Polytec PolyFile Type Library*

### Description

Item of the Infos collection. Standard collection of the measurement points. Available in MPV/PSV files only.

### Object Model


---

## MeasPoints Collection Members

*Quelle: `POLYFILELib~MeasPoints_members.html` · Polytec PolyFile Type Library*

### Public Methods

| Add | Adds a new MeasPoint to the MeasPoints collection and returns the new MeasPoint object. |
|---|---|
| AddPoints | Adds the specified number of points to the collection. |
| Calculate3DCoordinates | Calculates the 3D coordinates of the measurement points from the quantities of the scanners and the distance of the scanning head to the measurement object. |
| Clear | Removes all MeasPoints from the MeasPoints collection. |
| GetVideoRect | Gets the video rectangle defining the video coordinate system. |
| InvalidateAllNonOptimalPoints | Invalidates or validates all measurement points that do not have the optimal status. |
| LabelToIndex | Converts a given MeasPoint label to a MeasPoint index of the MeasPoints collection. |
| Remove | Removes a MeasPoint with the given index from the MeasPoints collection. |
| Save | Commits the changes to the MeasPoints collection to the file. This will also calculated the corrected average spectrum. |
| SetLabels | Changes the label for several MeasPoint items in the collection. |

### Public Properties

| AverageSigma | Returns the signal enhancement average sigma for all measurement points. |
|---|---|
| Component | Returns the root component of the geometry components hierarchy. |
| CoordinatesToArray | Gets the 3D coordinates for all points in an array. |
| Count | Returns the number of measurement points in the collection. |
| Has3DCoordinates | Returns whether the measurement points are defined with a 3D geometry. |
| HasNonOptimalPointsToInvalidate | Returns whether there is any measurement point that has status not optimal and that can be invalidated. |
| HasSigma | Returns whether the signal enhancement average sigma is valid. |
| Is3DCalculationPossible | Returns whether a calculation of the 3D coordinates of the measurement points is possible. |
| Item | Returns an item of the MeasPoints collection. |
| Name | Returns "MeasPoints. Can be used as an index into the Infos collection . |
| Type | Returns ptcInfoMeasPoints. Can be used as an index into the Infos collection . |
| VideoCoordinatesToArray | Gets the video coordinates for all points in an array. |


---

## Add Method

*Quelle: `POLYFILELib~MeasPoints~Add.html` · Polytec PolyFile Type Library · MeasPoints Collection : Add Method*

### Description

Adds a new MeasPoint to the MeasPoints collection and returns the new MeasPoint object.

### Syntax

*Visual Basic:*
```
Public Function Add() As MeasPoint
```

### Return Type

The new MeasPoint object.

### Remarks

When you want to add many points use the more efficient AddPoints Method.


---

## AddPoints Method

*Quelle: `POLYFILELib~MeasPoints~AddPoints.html` · Polytec PolyFile Type Library · MeasPoints Collection : AddPoints Method*

### Description

Adds the specified number of points to the collection.

### Syntax

*Visual Basic:*
```
Public Sub AddPoints( _
   ByVal lCount As Long _
)
```

### Parameters

lCount

The number of points to add.


---

## Calculate3DCoordinates Method

*Quelle: `POLYFILELib~MeasPoints~Calculate3DCoordinates.html` · Polytec PolyFile Type Library · MeasPoints Collection : Calculate3DCoordinates Method*

### Description

Calculates the 3D coordinates of the measurement points from the quantities of the scanners and the distance of the scanning head to the measurement object.

### Syntax

*Visual Basic:*
```
Public Sub Calculate3DCoordinates()
```

### Remarks

The method only succeeds if the file is not a combined file, is not a file created by Polytec File Access, and has no valid 3D alignment.

The distance of the scanning head to the measurement object in meter is specified by the value of the property Alignment2D.ScanHeadDistance of the applied 2D alignment.


---

## Clear Method

*Quelle: `POLYFILELib~MeasPoints~Clear.html` · Polytec PolyFile Type Library · MeasPoints Collection : Clear Method*

### Description

Removes all MeasPoints from the MeasPoints collection.

### Syntax

*Visual Basic:*
```
Public Sub Clear()
```


---

## GetVideoRect Method

*Quelle: `POLYFILELib~MeasPoints~GetVideoRect.html` · Polytec PolyFile Type Library · MeasPoints Collection : GetVideoRect Method*

### Description

Gets the video rectangle defining the video coordinate system.

### Syntax

*Visual Basic:*
```
Public Sub GetVideoRect( _
   ByRef pfLeft As Single, _
   ByRef pfTop As Single, _
   ByRef pfRight As Single, _
   ByRef pfBottom As Single _
)
```

### Parameters

pfLeft

receives the left side of the video rectangle

pfTop

receives the top side of the video rectangle

pfRight

receives the right side of the video rectangle

pfBottom

receives the bottom side of the video rectangle

### Remarks

The rectangle contains the video coordinates of the corners of the video image. VideoXY, Lines and VideoOffset return coordinates in this system.


---

## InvalidateAllNonOptimalPoints Method

*Quelle: `POLYFILELib~MeasPoints~InvalidateAllNonOptimalPoints.html` · Polytec PolyFile Type Library · MeasPoints Collection : InvalidateAllNonOptimalPoints Method*

### Description

Invalidates or validates all measurement points that do not have the optimal status.

### Syntax

*Visual Basic:*
```
Public Sub InvalidateAllNonOptimalPoints( _
   Optional ByVal vbInvalidate As Boolean = True _
)
```

### Parameters

vbInvalidate

Set to true if you want to invalidate.

### Remarks

The average spectrum will not be updated until you call the Save method of the MeasPoints collection.


---

## LabelToIndex Method

*Quelle: `POLYFILELib~MeasPoints~LabelToIndex.html` · Polytec PolyFile Type Library · MeasPoints Collection : LabelToIndex Method*

### Description

Converts a given MeasPoint label to a MeasPoint index of the MeasPoints collection.

### Syntax

*Visual Basic:*
```
Public Function LabelToIndex( _
   ByVal lLabel As Long _
) As Long
```

### Parameters

lLabel

Label of an existing MeasPoint.

### Return Type

Corresponding Index of MeasPoints collection.


---

## Remove Method

*Quelle: `POLYFILELib~MeasPoints~Remove.html` · Polytec PolyFile Type Library · MeasPoints Collection : Remove Method*

### Description

Removes a MeasPoint with the given index from the MeasPoints collection.

### Syntax

*Visual Basic:*
```
Public Sub Remove( _
   ByVal lIndex As Long _
)
```

### Parameters

lIndex

Index of the MeasPoint item to remove.


---

## Save Method

*Quelle: `POLYFILELib~MeasPoints~Save.html` · Polytec PolyFile Type Library · MeasPoints Collection : Save Method*

### Description

Commits the changes to the MeasPoints collection to the file. This will also calculated the corrected average spectrum.

### Syntax

*Visual Basic:*
```
Public Sub Save()
```


---

## SetLabels Method

*Quelle: `POLYFILELib~MeasPoints~SetLabels.html` · Polytec PolyFile Type Library · MeasPoints Collection : SetLabels Method*

### Description

Changes the label for several MeasPoint items in the collection.

### Syntax

*Visual Basic:*
```
Public Sub SetLabels( _
   ByVal pIndex() As Long, _
   ByVal pLabel() As Long _
)
```

### Parameters

pIndex

0-based, one dimensional array with indices of MeasPoints collection.

pLabel

0-based, one dimensional array new labels of MeasPoint items for the
 corresponding indices.

### Remarks

Both arrays passed as parameters must be of the same size.


---

## AverageSigma Property

*Quelle: `POLYFILELib~MeasPoints~AverageSigma.html` · Polytec PolyFile Type Library · MeasPoints Collection : AverageSigma Property*

### Description

Returns the signal enhancement average sigma for all measurement points.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property AverageSigma As Single
```


---

## Component Property

*Quelle: `POLYFILELib~MeasPoints~Component.html` · Polytec PolyFile Type Library · MeasPoints Collection : Component Property*

### Description

Returns the root component of the geometry components hierarchy.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Component As GeometryComponent
```


---

## CoordinatesToArray Property

*Quelle: `POLYFILELib~MeasPoints~CoordinatesToArray.html` · Polytec PolyFile Type Library · MeasPoints Collection : CoordinatesToArray Property*

### Description

Gets the 3D coordinates for all points in an array.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property CoordinatesToArray As Single()
```

### Return Type

The 3D coordinates.

### Remarks

The returned array contains the x, y, z coordinate of the first point, then the x, y, z coordinate of the second point and so on. Getting the coordinates via this properties is more efficient than iterating over all MeasPoint Objects and calling the CoordXYZ Method.


---

## Count Property

*Quelle: `POLYFILELib~MeasPoints~Count.html` · Polytec PolyFile Type Library · MeasPoints Collection : Count Property*

### Description

Returns the number of measurement points in the collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Count As Long
```


---

## Has3DCoordinates Property

*Quelle: `POLYFILELib~MeasPoints~Has3DCoordinates.html` · Polytec PolyFile Type Library · MeasPoints Collection : Has3DCoordinates Property*

### Description

Returns whether the measurement points are defined with a 3D geometry.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Has3DCoordinates As Boolean
```


---

## HasNonOptimalPointsToInvalidate Property

*Quelle: `POLYFILELib~MeasPoints~HasNonOptimalPointsToInvalidate.html` · Polytec PolyFile Type Library · MeasPoints Collection : HasNonOptimalPointsToInvalidate Property*

### Description

Returns whether there is any measurement point that has status not optimal and that can be invalidated.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property HasNonOptimalPointsToInvalidate As Boolean
```


---

## HasSigma Property

*Quelle: `POLYFILELib~MeasPoints~HasSigma.html` · Polytec PolyFile Type Library · MeasPoints Collection : HasSigma Property*

### Description

Returns whether the signal enhancement average sigma is valid.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property HasSigma As Boolean
```


---

## Is3DCalculationPossible Property

*Quelle: `POLYFILELib~MeasPoints~Is3DCalculationPossible.html` · Polytec PolyFile Type Library · MeasPoints Collection : Is3DCalculationPossible Property*

### Description

Returns whether a calculation of the 3D coordinates of the measurement points is possible.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Is3DCalculationPossible As Boolean
```

### Example


---

## Item Property

*Quelle: `POLYFILELib~MeasPoints~Item.html` · Polytec PolyFile Type Library · MeasPoints Collection : Item Property*

### Description

Returns an item of the MeasPoints collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Item( _
   ByVal Index As Long _
) As MeasPoint
```

### Parameters

Index

The measurement point index.


---

## Name Property

*Quelle: `POLYFILELib~MeasPoints~Name.html` · Polytec PolyFile Type Library · MeasPoints Collection : Name Property*

### Description

Returns "MeasPoints. Can be used as an index into the Infos collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Name As String
```


---

## Type Property

*Quelle: `POLYFILELib~MeasPoints~Type.html` · Polytec PolyFile Type Library · MeasPoints Collection : Type Property*

### Description

Returns ptcInfoMeasPoints. Can be used as an index into the Infos collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Type As PTCInfoType
```


---

## VideoCoordinatesToArray Property

*Quelle: `POLYFILELib~MeasPoints~VideoCoordinatesToArray.html` · Polytec PolyFile Type Library · MeasPoints Collection : VideoCoordinatesToArray Property*

### Description

Gets the video coordinates for all points in an array.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property VideoCoordinatesToArray As Single()
```

### Return Type

The video coordinates.

### Remarks

The returned array contains the x, y video coordinate of the first point, then the x, y video coordinate of the second point and so on. Getting the coordinates via this properties is more efficient than iterating over all MeasPoint Objects and calling the VideoXY Method. The returned coordinates are in the coordinate system defined by the rectangle returned by the GetVideoRect Method.
