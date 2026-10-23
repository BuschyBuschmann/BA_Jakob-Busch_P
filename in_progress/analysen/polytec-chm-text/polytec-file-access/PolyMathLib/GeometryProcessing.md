# PolyMathLib – GeometryProcessing

## GeometryProcessing Object

*Quelle: `PolyMathLib~GeometryProcessing.html` · Polytec PolyMath Type Library*

### Description

GeometryProcessing contains methods for processing geometry, e.g. calculating surface normals.


---

## GeometryProcessing Object Members

*Quelle: `PolyMathLib~GeometryProcessing_members.html` · Polytec PolyMath Type Library*

### Public Methods

| CalculateNormals | Calculates the surface normals for the points with the specified indices. |
|---|---|


---

## CalculateNormals Method

*Quelle: `PolyMathLib~GeometryProcessing~CalculateNormals.html` · Polytec PolyMath Type Library · GeometryProcessing Object : CalculateNormals Method*

### Description

Calculates the surface normals for the points with the specified indices.

### Syntax

*Visual Basic:*
```
Public Function CalculateNormals( _
   ByVal pointCoordinates() As Single, _
   ByVal Elements() As Long, _
   ByVal pointIndices() As Long _
) As Single()
```

### Parameters

pointCoordinates

The point coordinates.

Elements

The array of elements.

pointIndices

The point indices (one-based).

### Return Type

The calculated normals.

### Remarks

The normal at a point is calculated by averaging the normals of the triangles the point belongs to.
