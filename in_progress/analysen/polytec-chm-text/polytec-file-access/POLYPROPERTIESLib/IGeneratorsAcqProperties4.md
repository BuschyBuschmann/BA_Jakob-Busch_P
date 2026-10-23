# POLYPROPERTIESLib – IGeneratorsAcqProperties4

## IGeneratorsAcqProperties4 Collection

*Quelle: `POLYPROPERTIESLib~IGeneratorsAcqProperties4.html` · Polytec PolyProperties Type Library*

### Description

Generators acquisition properties. Item of the AcquisitionProperties collection.

### Object Model

### Remarks

It is recommended to cast to the GeneratorsAcqPropertiesContainer Collection.


---

## IGeneratorsAcqProperties4 Collection Members

*Quelle: `POLYPROPERTIESLib~IGeneratorsAcqProperties4_members.html` · Polytec PolyProperties Type Library*

### Public Properties

| Count | The number of items in the collection. |
|---|---|
| Item | Returns the item with the given index from the collection. |


---

## Count Property

*Quelle: `POLYPROPERTIESLib~IGeneratorsAcqProperties4~Count.html` · Polytec PolyProperties Type Library · IGeneratorsAcqProperties4 Collection : Count Property*

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

*Quelle: `POLYPROPERTIESLib~IGeneratorsAcqProperties4~Item.html` · Polytec PolyProperties Type Library · IGeneratorsAcqProperties4 Collection : Item Property*

### Description

Returns the item with the given index from the collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Item( _
   ByVal nIndex As Long _
) As IGeneratorAcqProperties4
```

### Parameters

nIndex

The index of the item.
