# PSV – GeneratorsAcqProperties

## GeneratorsAcqProperties Collection

*Quelle: `PSV~GeneratorsAcqProperties.html` · Polytec PSV Type Library*

### Description

Generators acquisition properties. Item of the AcquisitionProperties collection.


---

## GeneratorsAcqProperties Collection Members

*Quelle: `PSV~GeneratorsAcqProperties_members.html` · Polytec PSV Type Library*

### Public Properties

| Count | The number of items in the collection. |
|---|---|
| Item | Returns the item with the given index from the collection. |


---

## Count Property

*Quelle: `PSV~GeneratorsAcqProperties~Count.html` · Polytec PSV Type Library · GeneratorsAcqProperties Collection : Count Property*

### Description

The number of items in the collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Count As Long
```

### Remarks

The number of generators is currently at most one.


---

## Item Property

*Quelle: `PSV~GeneratorsAcqProperties~Item.html` · Polytec PSV Type Library · GeneratorsAcqProperties Collection : Item Property*

### Description

Returns the item with the given index from the collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Item( _
   ByVal nIndex As Long _
) As GeneratorAcqProperties
```

### Parameters

nIndex

The index of the item.
