# PSV – Documents

## Documents Collection

*Quelle: `PSV~Documents.html` · Polytec PSV Type Library*

### Description

The collection of documents.

### Object Model


---

## Documents Collection Members

*Quelle: `PSV~Documents_members.html` · Polytec PSV Type Library*

### Public Methods

| Open | Opens a document and returns the new document object. |
|---|---|

### Public Properties

| Count | The number of items in the collection. |
|---|---|
| Item | Returns an item with the given index. |


---

## Open Method

*Quelle: `PSV~Documents~Open.html` · Polytec PSV Type Library · Documents Collection : Open Method*

### Description

Opens a document and returns the new document object.

### Syntax

*Visual Basic:*
```
Public Function Open( _
   ByVal FileName As String _
) As Document
```

### Parameters

FileName

The file name of the document.


---

## Count Property

*Quelle: `PSV~Documents~Count.html` · Polytec PSV Type Library · Documents Collection : Count Property*

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

## Item Property

*Quelle: `PSV~Documents~Item.html` · Polytec PSV Type Library · Documents Collection : Item Property*

### Description

Returns an item with the given index.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Item( _
   ByVal nIndex As Long _
) As Document
```

### Parameters

nIndex

The index of the item.
