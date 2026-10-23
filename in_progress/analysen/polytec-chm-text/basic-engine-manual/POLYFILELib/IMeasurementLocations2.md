# POLYFILELib – IMeasurementLocations2

## IMeasurementLocations2 Collection

*Quelle: `POLYFILELib~IMeasurementLocations2.html` · Polytec PolyFile Type Library*

### Description

Standard collection of the measurement locations.

### Object Model

### Remarks

It is recommended to cast to the MeasurementLocations Collection.


---

## IMeasurementLocations2 Collection Members

*Quelle: `POLYFILELib~IMeasurementLocations2_members.html` · Polytec PolyFile Type Library*

### Public Methods

| Add | Adds a new MeasurementLocation object to the collection and returns it. |
|---|---|
| CalculateDirections | Calculates the directions for the selected measurement locations. |
| CalculateNormals | Calculates the normals for the selected measurement locations. |
| Clear | Clears the collection, i.e. removes all contained MeasurementLocation objects. |
| GetMeasurementLocationsByMeasPointIndex | Retrieves the MeasurementLocation objects for the MeasPoint referenced by the specified index. |
| Remove | Removes a specified MeasurementLocation object from the collection. |
| Save | Saves the collection to the containing file. |

### Public Properties

| Count | Returns the number of items in the MeasurementLocations collection. |
|---|---|
| Item | Returns the item of the MeasurementLocations collection with the specified index. |
| Name | Returns "MeasurementLocations. Can be used as an index into the Infos collection . |
| Type | Returns ptcInfoMeasurementLocations . Can be used as an index into the Infos collection . |


---

## Add Method

*Quelle: `POLYFILELib~IMeasurementLocations2~Add.html` · Polytec PolyFile Type Library · IMeasurementLocations2 Collection : Add Method*

### Description

Adds a new MeasurementLocation object to the collection and returns it.

### Syntax

*Visual Basic:*
```
Public Function Add() As MeasurementLocation
```

### Return Type

The added MeasurementLocation object.


---

## CalculateDirections Method

*Quelle: `POLYFILELib~IMeasurementLocations2~CalculateDirections.html` · Polytec PolyFile Type Library · IMeasurementLocations2 Collection : CalculateDirections Method*

### Description

Calculates the directions for the selected measurement locations.

### Syntax

*Visual Basic:*
```
Public Sub CalculateDirections( _
   ByVal channelNames() As String _
)
```

### Parameters

channelNames

The list of the names of the channels for which to calculate the directions. An empty array indicates to calculate the directions for all measurement locations.

### Remarks

A direction for a channel can only be calculated, if there exists a measurement location for the position of the sensor and a measurement location for the position where the laser beam hits the object. Therefore for the given channel name a measurement location with a Status ptcScanStatusAssignedSensor and a measurement location with a Status ptcScanStatusAssignedChannel1D or ptcScanStatusAssignedChannel3D must exist. The Direction Property of the measurement locations corresponding to the positions where the laser beam hits the object will be updated.


---

## CalculateNormals Method

*Quelle: `POLYFILELib~IMeasurementLocations2~CalculateNormals.html` · Polytec PolyFile Type Library · IMeasurementLocations2 Collection : CalculateNormals Method*

### Description

Calculates the normals for the selected measurement locations.

### Syntax

*Visual Basic:*
```
Public Sub CalculateNormals( _
   ByVal pointIndices() As Long _
)
```

### Parameters

pointIndices

The list of the indices of the points for which to calculate the normals. An empty array indicates to calculate the normals for all measurement locations.

### Remarks

The normal at a measurement location is calculated by averaging the normals of the triangles the point belongs to.


---

## Clear Method

*Quelle: `POLYFILELib~IMeasurementLocations2~Clear.html` · Polytec PolyFile Type Library · IMeasurementLocations2 Collection : Clear Method*

### Description

Clears the collection, i.e. removes all contained MeasurementLocation objects.

### Syntax

*Visual Basic:*
```
Public Sub Clear()
```


---

## GetMeasurementLocationsByMeasPointIndex Method

*Quelle: `POLYFILELib~IMeasurementLocations2~GetMeasurementLocationsByMeasPointIndex.html` · Polytec PolyFile Type Library · IMeasurementLocations2 Collection : GetMeasurementLocationsByMeasPointIndex Method*

### Description

Retrieves the MeasurementLocation objects for the MeasPoint referenced by the specified index.

### Syntax

*Visual Basic:*
```
Public Function GetMeasurementLocationsByMeasPointIndex( _
   ByVal MeasPointIndex As Long _
) As Object()
```

### Parameters

MeasPointIndex

The index of the measurement point.


---

## Remove Method

*Quelle: `POLYFILELib~IMeasurementLocations2~Remove.html` · Polytec PolyFile Type Library · IMeasurementLocations2 Collection : Remove Method*

### Description

Removes a specified MeasurementLocation object from the collection.

### Syntax

*Visual Basic:*
```
Public Sub Remove( _
   ByVal Index As Long _
)
```

### Parameters

Index

The index of the MeasurementLocation object.


---

## Save Method

*Quelle: `POLYFILELib~IMeasurementLocations2~Save.html` · Polytec PolyFile Type Library · IMeasurementLocations2 Collection : Save Method*

### Description

Saves the collection to the containing file.

### Syntax

*Visual Basic:*
```
Public Sub Save()
```


---

## Count Property

*Quelle: `POLYFILELib~IMeasurementLocations2~Count.html` · Polytec PolyFile Type Library · IMeasurementLocations2 Collection : Count Property*

### Description

Returns the number of items in the MeasurementLocations collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Count As Long
```

### Return Type

The number of items.


---

## Item Property

*Quelle: `POLYFILELib~IMeasurementLocations2~Item.html` · Polytec PolyFile Type Library · IMeasurementLocations2 Collection : Item Property*

### Description

Returns the item of the MeasurementLocations collection with the specified index.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Item( _
   ByVal nIndex As Long _
) As MeasurementLocation
```

### Parameters

nIndex

The index of the MeasurementLocation object.

### Return Type

The addressed MeasurementLocation object.


---

## Name Property

*Quelle: `POLYFILELib~IMeasurementLocations2~Name.html` · Polytec PolyFile Type Library · IMeasurementLocations2 Collection : Name Property*

### Description

Returns "MeasurementLocations. Can be used as an index into the Infos collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Name As String
```


---

## Type Property

*Quelle: `POLYFILELib~IMeasurementLocations2~Type.html` · Polytec PolyFile Type Library · IMeasurementLocations2 Collection : Type Property*

### Description

Returns ptcInfoMeasurementLocations. Can be used as an index into the Infos collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Type As PTCInfoType
```
