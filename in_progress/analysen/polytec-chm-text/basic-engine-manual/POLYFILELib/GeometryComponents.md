# POLYFILELib – GeometryComponents

## GeometryComponents Collection

*Quelle: `POLYFILELib~GeometryComponents.html` · Polytec PolyFile Type Library*

### Description

Collection of GeometryComponent objects.

### Object Model


---

## GeometryComponents Collection Members

*Quelle: `POLYFILELib~GeometryComponents_members.html` · Polytec PolyFile Type Library*

### Public Methods

| Add | Adds a new geometry component with the given name to the collection and returns the new object. |
|---|---|
| Clear | Clears the collection by removing all geometry component objects. |
| Remove | Removes an item with the given index or name from the collection. |

### Public Properties

| Count | Retrieves the number of items in this collection. |
|---|---|
| Item | Returns an item of the collection. |


---

## Add Method

*Quelle: `POLYFILELib~GeometryComponents~Add.html` · Polytec PolyFile Type Library · GeometryComponents Collection : Add Method*

### Description

Adds a new geometry component with the given name to the collection and returns the new object.

### Syntax

*Visual Basic:*
```
Public Function Add( _
   ByVal bstrName As String _
) As GeometryComponent
```

### Parameters

bstrName

Name of the new component. Names have to be unique in the collection.

### Return Type

GeometryComponent object.


---

## Clear Method

*Quelle: `POLYFILELib~GeometryComponents~Clear.html` · Polytec PolyFile Type Library · GeometryComponents Collection : Clear Method*

### Description

Clears the collection by removing all geometry component objects.

### Syntax

*Visual Basic:*
```
Public Sub Clear()
```


---

## Remove Method

*Quelle: `POLYFILELib~GeometryComponents~Remove.html` · Polytec PolyFile Type Library · GeometryComponents Collection : Remove Method*

### Description

Removes an item with the given index or name from the collection.

### Syntax

*Visual Basic:*
```
Public Sub Remove( _
   ByVal Index As Variant _
)
```

### Parameters

Index

Index (integer) or name (string) of the item.


---

## Count Property

*Quelle: `POLYFILELib~GeometryComponents~Count.html` · Polytec PolyFile Type Library · GeometryComponents Collection : Count Property*

### Description

Retrieves the number of items in this collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Count As Long
```


---

## Item Property

*Quelle: `POLYFILELib~GeometryComponents~Item.html` · Polytec PolyFile Type Library · GeometryComponents Collection : Item Property*

### Description

Returns an item of the collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Item( _
   ByVal Index As Variant _
) As GeometryComponent
```

### Parameters

Index

Index (integer) or name (string) of the item.
