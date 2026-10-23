# POLYFILELib – Elements

## Elements Collection

*Quelle: `POLYFILELib~Elements.html` · Polytec PolyFile Type Library*

### Description

Item of the Infos collection. Standard collection of Element objects. Elements represent the surface elements connecting the scan points. They are used for the graphical display of scan data in MPV/PSV. Available in MPV/PSV files only.

### Object Model


---

## Elements Collection Members

*Quelle: `POLYFILELib~Elements_members.html` · Polytec PolyFile Type Library*

### Public Methods

| Add | Adds a new element to the elements collection and returns it. |
|---|---|
| AddRange | Adds a range of elements to the Elements collection and returns the number of elements added. |
| Clear | Removes all elements from the Elements collection. |
| Remove | Removes an element from the element collection. |
| Save | Commits the changes to the elements collection to the file. |
| ToArray | Converts the elements collection to an array. |

### Public Properties

| Count | Returns the number of Element objects in the Elements collection. |
|---|---|
| Item | Returns an item of the Elements collection. |
| Name | Returns "Elements. Can be used as an index into the Infos collection . |
| Type | Returns ptcInfoElements. Can be used as an index into the Infos collection . |


---

## Add Method

*Quelle: `POLYFILELib~Elements~Add.html` · Polytec PolyFile Type Library · Elements Collection : Add Method*

### Description

Adds a new element to the elements collection and returns it.

### Syntax

*Visual Basic:*
```
Public Function Add( _
   ByVal saIndicesOrLabels() As Long, _
   ByVal vbLabels As Boolean _
) As Element
```

### Parameters

saIndicesOrLabels

0-based, 1 dimensional array of integers either with the 1-based indexes of the scan points or with the labels.

vbLabels

If true, labels of scan points are passed, otherwise indexes are passed.

### Return Type

The created element.

### Remarks

In the user interface of the MPV/PSV software labels are called indexes and indexes are called numbers. If you want to add a large number of elements consider using the AddRange method instead.


---

## AddRange Method

*Quelle: `POLYFILELib~Elements~AddRange.html` · Polytec PolyFile Type Library · Elements Collection : AddRange Method*

### Description

Adds a range of elements to the Elements collection and returns the number of elements added.

### Syntax

*Visual Basic:*
```
Public Function AddRange( _
   ByVal saIndicesOrLabels() As Long, _
   ByVal vbLabels As Boolean _
) As Long
```

### Parameters

saIndicesOrLabels

0-based, 1 dimensional array of integers either with the 1-based indexes of the scan points or with the labels. For every element the array must contain the number of the points in the element followed by the point indexes or labels.

vbLabels

If true, labels of scan points are passed, otherwise indexes are passed.

### Remarks

In the user interface of the MPV/PSV software labels are called indexes and indexes are called numbers.

### Example

Adds a range of elements to the Elements collection

- Adding Elements (Visual Basic)

```
Dim oElements As Elements
Set oElements = oFile.Infos.Type(ptcInfoElements)

Dim indexes(0 To 11) As Long

indexes(0) = 3 ' the first element has 3 indexes
indexes(1) = 123
indexes(2) = 456
indexes(3) = 78
indexes(4) = 2 ' the second element has 2 indexes
indexes(5) = 17
indexes(6) = 19
indexes(7) = 4 ' the third element has 4 indexes
indexes(8) = 23
indexes(9) = 25
indexes(10) = 27
indexes(11) = 30

Debug.Print oElements.AddRange(indexes, False)
```


---

## Clear Method

*Quelle: `POLYFILELib~Elements~Clear.html` · Polytec PolyFile Type Library · Elements Collection : Clear Method*

### Description

Removes all elements from the Elements collection.

### Syntax

*Visual Basic:*
```
Public Sub Clear()
```


---

## Remove Method

*Quelle: `POLYFILELib~Elements~Remove.html` · Polytec PolyFile Type Library · Elements Collection : Remove Method*

### Description

Removes an element from the element collection.

### Syntax

*Visual Basic:*
```
Public Sub Remove( _
   ByVal lIndex As Long _
)
```

### Parameters

lIndex

Index of the element to remove.


---

## Save Method

*Quelle: `POLYFILELib~Elements~Save.html` · Polytec PolyFile Type Library · Elements Collection : Save Method*

### Description

Commits the changes to the elements collection to the file.

### Syntax

*Visual Basic:*
```
Public Sub Save()
```


---

## ToArray Method

*Quelle: `POLYFILELib~Elements~ToArray.html` · Polytec PolyFile Type Library · Elements Collection : ToArray Method*

### Description

Converts the elements collection to an array.

### Syntax

*Visual Basic:*
```
Public Function ToArray( _
   ByVal vbLabels As Boolean _
) As Long()
```

### Parameters

vbLabels

If true, the array contains labels of scan points, otherwise indexes.

### Return Type

0-based, 1 dimensional array of integers either with the 1-based indexes of the scan points or with the labels. For every element the array contains the number of the points in the element followed by the point indexes or labels.

### Remarks

In the user interface of the MPV/PSV software labels are called indexes and indexes are called numbers. The returned array can be used as an input to the AddRange method of another Elements collection to copy the elements.

### Example


---

## Count Property

*Quelle: `POLYFILELib~Elements~Count.html` · Polytec PolyFile Type Library · Elements Collection : Count Property*

### Description

Returns the number of Element objects in the Elements collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Count As Long
```


---

## Item Property

*Quelle: `POLYFILELib~Elements~Item.html` · Polytec PolyFile Type Library · Elements Collection : Item Property*

### Description

Returns an item of the Elements collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Item( _
   ByVal Index As Long _
) As Element
```

### Parameters

Index

The index of the item.


---

## Name Property

*Quelle: `POLYFILELib~Elements~Name.html` · Polytec PolyFile Type Library · Elements Collection : Name Property*

### Description

Returns "Elements. Can be used as an index into the Infos collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Name As String
```

### Return Type

Always "Elements".


---

## Type Property

*Quelle: `POLYFILELib~Elements~Type.html` · Polytec PolyFile Type Library · Elements Collection : Type Property*

### Description

Returns ptcInfoElements. Can be used as an index into the Infos collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Type As PTCInfoType
```

### Return Type

Always ptcInfoElements.
