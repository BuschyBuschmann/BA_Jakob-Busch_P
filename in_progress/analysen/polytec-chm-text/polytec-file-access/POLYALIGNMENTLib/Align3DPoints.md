# POLYALIGNMENTLib – Align3DPoints

## Align3DPoints Collection

*Quelle: `POLYALIGNMENTLib~Align3DPoints.html` · Polytec PolyAlignment Type Library*

### Description

Collection of Align3DPoint objects.

### Object Model


---

## Align3DPoints Collection Members

*Quelle: `POLYALIGNMENTLib~Align3DPoints_members.html` · Polytec PolyAlignment Type Library*

### Public Methods

| Add | Adds a new Align3DPoint to the collection and returns it. |
|---|---|
| Clear | Removes all items from the collection. |
| Copy | Copies the Align3DPoints from the input parameter to this object. |
| IsEqual | Returns true if the input Align3DPoints collection is equal to this collection. |
| Remove | Removes an item from the collection. |

### Public Properties

| Count | The number of items in this collection. |
|---|---|
| Item | Returns an item of the collection. |


---

## Add Method

*Quelle: `POLYALIGNMENTLib~Align3DPoints~Add.html` · Polytec PolyAlignment Type Library · Align3DPoints Collection : Add Method*

### Description

Adds a new Align3DPoint to the collection and returns it.

### Syntax

*Visual Basic:*
```
Public Function Add() As Align3DPoint
```


---

## Clear Method

*Quelle: `POLYALIGNMENTLib~Align3DPoints~Clear.html` · Polytec PolyAlignment Type Library · Align3DPoints Collection : Clear Method*

### Description

Removes all items from the collection.

### Syntax

*Visual Basic:*
```
Public Sub Clear()
```


---

## Copy Method

*Quelle: `POLYALIGNMENTLib~Align3DPoints~Copy.html` · Polytec PolyAlignment Type Library · Align3DPoints Collection : Copy Method*

### Description

Copies the Align3DPoints from the input parameter to this object.

### Syntax

*Visual Basic:*
```
Public Sub Copy( _
   ByVal pIAlign3DPoints As Align3DPoints _
)
```

### Parameters

pIAlign3DPoints

Source Align3DPoints object.


---

## IsEqual Method

*Quelle: `POLYALIGNMENTLib~Align3DPoints~IsEqual.html` · Polytec PolyAlignment Type Library · Align3DPoints Collection : IsEqual Method*

### Description

Returns true if the input Align3DPoints collection is equal to this collection.

### Syntax

*Visual Basic:*
```
Public Function IsEqual( _
   ByVal pIAlign3DPoints As Align3DPoints _
) As Boolean
```

### Parameters

pIAlign3DPoints

Align3DPoints object to be compared with.


---

## Remove Method

*Quelle: `POLYALIGNMENTLib~Align3DPoints~Remove.html` · Polytec PolyAlignment Type Library · Align3DPoints Collection : Remove Method*

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

Index of the item.


---

## Count Property

*Quelle: `POLYALIGNMENTLib~Align3DPoints~Count.html` · Polytec PolyAlignment Type Library · Align3DPoints Collection : Count Property*

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

*Quelle: `POLYALIGNMENTLib~Align3DPoints~Item.html` · Polytec PolyAlignment Type Library · Align3DPoints Collection : Item Property*

### Description

Returns an item of the collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Item( _
   ByVal lIndex As Long _
) As Align3DPoint
```

### Parameters

lIndex

The index of the item.
