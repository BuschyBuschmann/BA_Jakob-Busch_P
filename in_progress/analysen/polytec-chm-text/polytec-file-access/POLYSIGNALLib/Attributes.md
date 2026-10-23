# POLYSIGNALLib – Attributes

## Attributes Collection

*Quelle: `POLYSIGNALLib~Attributes.html` · Polytec PolySignal Type Library*

### Description

Named collection of attribute items.

### Object Model

### Remarks

Attributes are used to attach additional values to objects like e.g. the description of a signal. The attributes are persisted with the object they are attached to.


---

## Attributes Collection Members

*Quelle: `POLYSIGNALLib~Attributes_members.html` · Polytec PolySignal Type Library*

### Public Methods

| Add | Adds an attribute to the collection and returns the created attribute. |
|---|---|
| Clear | Removes all items from the collection. |
| Clone | Creates and returns a copy of the collection. |
| Copy | Copies all items of the given collection to this collection. |
| IsEqual | Returns whether the collection is equal to the given collection. |
| Remove | Removes the item with the given index or name from the collection. |

### Public Properties

| Count | The number of items in the collection. |
|---|---|
| Exists | Returns whether the item with the given name or index exists in the collection. |
| Item | The item with the given index or name. |


---

## Add Method

*Quelle: `POLYSIGNALLib~Attributes~Add.html` · Polytec PolySignal Type Library · Attributes Collection : Add Method*

### Description

Adds an attribute to the collection and returns the created attribute.

### Syntax

*Visual Basic:*
```
Public Function Add( _
   ByVal bstrName As String, _
   ByVal vValue As Variant _
) As Attribute
```

### Parameters

bstrName

The name of the attribute.

vValue

The value of the attribute.

### Return Type

The newly created attribute.

### Remarks

The name of the attribute must be unique, i.e. an attribute with the same name must not exist in the Attributes Collection. The following variant types are supported: VT_I2, VT_I4, VT_R4, VT_R8, VT_DATE, VT_BSTR, VT_BOOL, VT_DECIMAL, VT_I1, VT_UI1, VT_UI2, VT_UI4, VT_I8, VT_INT, VT_UINT, VT_LPSTR, VT_LPWSTR, VT_FILETIME. Variants passed by reference (VT_BYREF) are copied. Arrays are not supported. The properties Description, Quantity, and Unit of the created Attribute Object are initialized with empty strings.

### Example


---

## Clear Method

*Quelle: `POLYSIGNALLib~Attributes~Clear.html` · Polytec PolySignal Type Library · Attributes Collection : Clear Method*

### Description

Removes all items from the collection.

### Syntax

*Visual Basic:*
```
Public Sub Clear()
```


---

## Clone Method

*Quelle: `POLYSIGNALLib~Attributes~Clone.html` · Polytec PolySignal Type Library · Attributes Collection : Clone Method*

### Description

Creates and returns a copy of the collection.

### Syntax

*Visual Basic:*
```
Public Function Clone() As Attributes
```


---

## Copy Method

*Quelle: `POLYSIGNALLib~Attributes~Copy.html` · Polytec PolySignal Type Library · Attributes Collection : Copy Method*

### Description

Copies all items of the given collection to this collection.

### Syntax

*Visual Basic:*
```
Public Sub Copy( _
   ByVal pIAttributes As Attributes _
)
```

### Parameters

pIAttributes

The collection to copy the items from.


---

## IsEqual Method

*Quelle: `POLYSIGNALLib~Attributes~IsEqual.html` · Polytec PolySignal Type Library · Attributes Collection : IsEqual Method*

### Description

Returns whether the collection is equal to the given collection.

### Syntax

*Visual Basic:*
```
Public Function IsEqual( _
   ByVal pIAttributes As Attributes _
) As Boolean
```

### Parameters

pIAttributes

The collection to compare with.


---

## Remove Method

*Quelle: `POLYSIGNALLib~Attributes~Remove.html` · Polytec PolySignal Type Library · Attributes Collection : Remove Method*

### Description

Removes the item with the given index or name from the collection.

### Syntax

*Visual Basic:*
```
Public Sub Remove( _
   ByVal vtIndex As Variant _
)
```

### Parameters

vtIndex

The name or 1-based index of the item.


---

## Count Property

*Quelle: `POLYSIGNALLib~Attributes~Count.html` · Polytec PolySignal Type Library · Attributes Collection : Count Property*

### Description

The number of items in the collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Count As Long
```


---

## Exists Property

*Quelle: `POLYSIGNALLib~Attributes~Exists.html` · Polytec PolySignal Type Library · Attributes Collection : Exists Property*

### Description

Returns whether the item with the given name or index exists in the collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Exists( _
   ByVal Index As Variant _
) As Boolean
```

### Parameters

Index

The name or 1-based index of the item.


---

## Item Property

*Quelle: `POLYSIGNALLib~Attributes~Item.html` · Polytec PolySignal Type Library · Attributes Collection : Item Property*

### Description

The item with the given index or name.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Item( _
   ByVal vtIndex As Variant _
) As Attribute
```

### Parameters

vtIndex

The name or 1-based index of the item.
