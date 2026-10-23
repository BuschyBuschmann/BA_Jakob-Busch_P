# POLYALIGNMENTLib – Align2DPoints

## Align2DPoints Collection

*Quelle: `POLYALIGNMENTLib~Align2DPoints.html` · Polytec PolyAlignment Type Library*

### Description

Collection of Align2DPoint objects.

### Object Model


---

## Align2DPoints Collection Members

*Quelle: `POLYALIGNMENTLib~Align2DPoints_members.html` · Polytec PolyAlignment Type Library*

### Public Methods

| Add | Adds a new Align2DPoint to the collection and returns it. |
|---|---|
| Clear | Removes all items from the collection. |
| Copy | Copies the Align2DPoints from the input parameter to this object. |
| IsEqual | Returns true if the input Align2DPoints collection is equal to this collection. |
| Remove | Removes an item from the collection. |

### Public Properties

| Count | The number of items in this collection. |
|---|---|
| Item | Returns an item of the collection. |


---

## Add Method

*Quelle: `POLYALIGNMENTLib~Align2DPoints~Add.html` · Polytec PolyAlignment Type Library · Align2DPoints Collection : Add Method*

### Description

Adds a new Align2DPoint to the collection and returns it.

### Syntax

*Visual Basic:*
```
Public Function Add() As Align2DPoint
```


---

## Clear Method

*Quelle: `POLYALIGNMENTLib~Align2DPoints~Clear.html` · Polytec PolyAlignment Type Library · Align2DPoints Collection : Clear Method*

### Description

Removes all items from the collection.

### Syntax

*Visual Basic:*
```
Public Sub Clear()
```


---

## Copy Method

*Quelle: `POLYALIGNMENTLib~Align2DPoints~Copy.html` · Polytec PolyAlignment Type Library · Align2DPoints Collection : Copy Method*

### Description

Copies the Align2DPoints from the input parameter to this object.

### Syntax

*Visual Basic:*
```
Public Sub Copy( _
   ByVal pIAlign2DPoints As Align2DPoints _
)
```

### Parameters

pIAlign2DPoints

The input Align2DPoints object.


---

## IsEqual Method

*Quelle: `POLYALIGNMENTLib~Align2DPoints~IsEqual.html` · Polytec PolyAlignment Type Library · Align2DPoints Collection : IsEqual Method*

### Description

Returns true if the input Align2DPoints collection is equal to this collection.

### Syntax

*Visual Basic:*
```
Public Function IsEqual( _
   ByVal pIAlign2DPoints As Align2DPoints _
) As Boolean
```

### Parameters

pIAlign2DPoints

The input Align2DPoints object.


---

## Remove Method

*Quelle: `POLYALIGNMENTLib~Align2DPoints~Remove.html` · Polytec PolyAlignment Type Library · Align2DPoints Collection : Remove Method*

### Description

Removes an item from the collection.

### Syntax

*Visual Basic:*
```
Public Sub Remove( _
   ByVal lIndex As Long _
)
```

### Parameters

lIndex

The index of the item.


---

## Count Property

*Quelle: `POLYALIGNMENTLib~Align2DPoints~Count.html` · Polytec PolyAlignment Type Library · Align2DPoints Collection : Count Property*

### Description

The number of items in this collection.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Count As Long
```


---

## Item Property

*Quelle: `POLYALIGNMENTLib~Align2DPoints~Item.html` · Polytec PolyAlignment Type Library · Align2DPoints Collection : Item Property*

### Description

Returns an item of the collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Item( _
   ByVal lIndex As Long _
) As Align2DPoint
```

### Parameters

lIndex

1-based index of the Align2DPoint in the collection.
