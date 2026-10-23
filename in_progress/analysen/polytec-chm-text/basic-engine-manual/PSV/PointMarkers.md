# PSV – PointMarkers

## PointMarkers Collection

*Quelle: `PSV~PointMarkers.html` · Polytec PSV Type Library*

### Description

A collection of point markers.

### Object Model

### Remarks

The collection stores point markers that can be tracked to compensate for the movement of measurement objects. You can use the Transform3DProcessing Object to calculate a coordinate transform to update the 3D alignment.


---

## PointMarkers Collection Members

*Quelle: `PSV~PointMarkers_members.html` · Polytec PSV Type Library*

### Public Methods

| Add | Adds a new point marker object to the collection. |
|---|---|
| Clear | Clears the collection by removing all point markers. |
| Remove | Removes the point marker with the specified index from the collection. |

### Public Properties

| Count | The number of point markers in the collection. |
|---|---|
| FirstPositionCoordinatesToArray | Returns an array of the 3D coordinates of the first positions of the point markers. |
| Item | Returns the point marker with the specified index. |
| SecondPositionCoordinatesToArray | Returns an array of the 3D coordinates of the first positions of the point markers. |


---

## Add Method

*Quelle: `PSV~PointMarkers~Add.html` · Polytec PSV Type Library · PointMarkers Collection : Add Method*

### Description

Adds a new point marker object to the collection.

### Syntax

*Visual Basic:*
```
Public Function Add() As PointMarker
```

### Return Type

The new point marker.


---

## Clear Method

*Quelle: `PSV~PointMarkers~Clear.html` · Polytec PSV Type Library · PointMarkers Collection : Clear Method*

### Description

Clears the collection by removing all point markers.

### Syntax

*Visual Basic:*
```
Public Sub Clear()
```


---

## Remove Method

*Quelle: `PSV~PointMarkers~Remove.html` · Polytec PSV Type Library · PointMarkers Collection : Remove Method*

### Description

Removes the point marker with the specified index from the collection.

### Syntax

*Visual Basic:*
```
Public Sub Remove( _
   ByVal Index As Long _
)
```

### Parameters

Index

The one-based index of the point marker to remove.


---

## Count Property

*Quelle: `PSV~PointMarkers~Count.html` · Polytec PSV Type Library · PointMarkers Collection : Count Property*

### Description

The number of point markers in the collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Count As Long
```


---

## FirstPositionCoordinatesToArray Property

*Quelle: `PSV~PointMarkers~FirstPositionCoordinatesToArray.html` · Polytec PSV Type Library · PointMarkers Collection : FirstPositionCoordinatesToArray Property*

### Description

Returns an array of the 3D coordinates of the first positions of the point markers.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property FirstPositionCoordinatesToArray As Single()
```

### Return Type

Array of the interleaved (x0, y0, z0, x1, y1, z1, ...) first 3D coordinates of the point markers.


---

## Item Property

*Quelle: `PSV~PointMarkers~Item.html` · Polytec PSV Type Library · PointMarkers Collection : Item Property*

### Description

Returns the point marker with the specified index.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Item( _
   ByVal Index As Long _
) As PointMarker
```

### Parameters

Index

The one-based index of the point marker.

### Return Type

The point marker.


---

## SecondPositionCoordinatesToArray Property

*Quelle: `PSV~PointMarkers~SecondPositionCoordinatesToArray.html` · Polytec PSV Type Library · PointMarkers Collection : SecondPositionCoordinatesToArray Property*

### Description

Returns an array of the 3D coordinates of the first positions of the point markers.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property SecondPositionCoordinatesToArray As Single()
```

### Return Type

Array of the interleaved (x0, y0, z0, x1, y1, z1, ...) second 3D coordinates of the point markers.
