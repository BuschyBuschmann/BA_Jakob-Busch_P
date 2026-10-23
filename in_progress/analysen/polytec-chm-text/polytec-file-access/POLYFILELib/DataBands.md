# POLYFILELib – DataBands

## DataBands Collection

*Quelle: `POLYFILELib~DataBands.html` · Polytec PolyFile Type Library*

### Description

Named collection of the data bands.

### Object Model


---

## DataBands Collection Members

*Quelle: `POLYFILELib~DataBands_members.html` · Polytec PolyFile Type Library*

### Public Properties

| BandDefinitions | Returns the collection of the band definitions of the bands in this collection. |
|---|---|
| Count | Returns the number of items in the data bands collection. |
| Exists | Returns True if the item of the given name exists in the DataBands collection. |
| Item | Returns an item of the data bands collection. |


---

## BandDefinitions Property

*Quelle: `POLYFILELib~DataBands~BandDefinitions.html` · Polytec PolyFile Type Library · DataBands Collection : BandDefinitions Property*

### Description

Returns the collection of the band definitions of the bands in this collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property BandDefinitions As IBandDefs3
```


---

## Count Property

*Quelle: `POLYFILELib~DataBands~Count.html` · Polytec PolyFile Type Library · DataBands Collection : Count Property*

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

*Quelle: `POLYFILELib~DataBands~Exists.html` · Polytec PolyFile Type Library · DataBands Collection : Exists Property*

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

*Quelle: `POLYFILELib~DataBands~Item.html` · Polytec PolyFile Type Library · DataBands Collection : Item Property*

### Description

Returns an item of the data bands collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Item( _
   ByVal IndexOrName As Variant _
) As DataBand
```

### Parameters

IndexOrName

Name (string) or Index (integer) of the DataBand object
