# POLYFILELib – IDataBands

## IDataBands Collection

*Quelle: `POLYFILELib~IDataBands.html` · Polytec PolyFile Type Library*

### Description

Named collection of the data bands.

### Object Model

### Remarks

It is recommended to cast to the DataBands collection.


---

## IDataBands Collection Members

*Quelle: `POLYFILELib~IDataBands_members.html` · Polytec PolyFile Type Library*

### Public Properties

| Count | Returns the number of items in the data bands collection. |
|---|---|
| Exists | Returns True if the item of the given name exists in the DataBands collection. |
| Item | Returns an item of the data bands collection. |


---

## Count Property

*Quelle: `POLYFILELib~IDataBands~Count.html` · Polytec PolyFile Type Library · IDataBands Collection : Count Property*

### Description

Returns the number of items in the data bands collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Count As Long
```


---

## Exists Property

*Quelle: `POLYFILELib~IDataBands~Exists.html` · Polytec PolyFile Type Library · IDataBands Collection : Exists Property*

### Description

Returns True if the item of the given name exists in the DataBands collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Exists( _
   ByVal Name As Variant _
) As Boolean
```

### Parameters

Name

The name of the DataBand.


---

## Item Property

*Quelle: `POLYFILELib~IDataBands~Item.html` · Polytec PolyFile Type Library · IDataBands Collection : Item Property*

### Description

Returns an item of the data bands collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Item( _
   ByVal IndexOrName As Variant _
) As IDataBand
```

### Parameters

IndexOrName

Name (string) or Index (integer) of the DataBand object
