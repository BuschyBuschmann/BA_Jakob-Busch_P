# POLYFILELib – GeometryComponent

## GeometryComponent Object

*Quelle: `POLYFILELib~GeometryComponent.html` · Polytec PolyFile Type Library*

### Description

Component of the geometry. A hierarchy of components where each component can have a set of measurement points attached to it.

### Object Model


---

## GeometryComponent Object Members

*Quelle: `POLYFILELib~GeometryComponent_members.html` · Polytec PolyFile Type Library*

### Public Properties

| Components | Returns the collection of the child components of this geometry component. |
|---|---|
| Description | Returns or specifies the description of the geometry component. |
| ID | Returns the unique identifier of this geometry component. |
| Indices | Returns or specifies the indices of the measurement points attached to this component. |
| Labels | Returns the labels of the measurement points attached to this geometry component. |
| Name | Returns or specifies the name of the geometry component. Names have to be unique in the parent's components collection. |


---

## Components Property

*Quelle: `POLYFILELib~GeometryComponent~Components.html` · Polytec PolyFile Type Library · GeometryComponent Object : Components Property*

### Description

Returns the collection of the child components of this geometry component.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Components As GeometryComponents
```


---

## Description Property

*Quelle: `POLYFILELib~GeometryComponent~Description.html` · Polytec PolyFile Type Library · GeometryComponent Object : Description Property*

### Description

Returns or specifies the description of the geometry component.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Description As String
```


---

## ID Property

*Quelle: `POLYFILELib~GeometryComponent~ID.html` · Polytec PolyFile Type Library · GeometryComponent Object : ID Property*

### Description

Returns the unique identifier of this geometry component.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property ID As Long
```


---

## Indices Property

*Quelle: `POLYFILELib~GeometryComponent~Indices.html` · Polytec PolyFile Type Library · GeometryComponent Object : Indices Property*

### Description

Returns or specifies the indices of the measurement points attached to this component.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Indices As Long()
```

### Return Type

1 dimensional, 0 based array of integers.


---

## Labels Property

*Quelle: `POLYFILELib~GeometryComponent~Labels.html` · Polytec PolyFile Type Library · GeometryComponent Object : Labels Property*

### Description

Returns the labels of the measurement points attached to this geometry component.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Labels As Long()
```

### Return Type

1 dimensional, 0 based array of integers.


---

## Name Property

*Quelle: `POLYFILELib~GeometryComponent~Name.html` · Polytec PolyFile Type Library · GeometryComponent Object : Name Property*

### Description

Returns or specifies the name of the geometry component. Names have to be unique in the parent's components collection.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Name As String
```
