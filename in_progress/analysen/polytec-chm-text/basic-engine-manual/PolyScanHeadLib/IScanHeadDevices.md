# PolyScanHeadLib – IScanHeadDevices

## IScanHeadDevices Collection

*Quelle: `PolyScanHeadLib~IScanHeadDevices.html` · Polytec PolyScanHead Type Library*

### Description

Collection of the scanning head devices of a PSV system.

### Object Model

### Remarks

It is recommended to cast to the ScanHeadDevices collection.


---

## IScanHeadDevices Collection Members

*Quelle: `PolyScanHeadLib~IScanHeadDevices_members.html` · Polytec PolyScanHead Type Library*

### Public Properties

| Count | The number of items in the collection. |
|---|---|
| Item | Returns an item of the collection with the given index. |
| ScanHeadType | The type object of the scanning heads. |


---

## Count Property

*Quelle: `PolyScanHeadLib~IScanHeadDevices~Count.html` · Polytec PolyScanHead Type Library · IScanHeadDevices Collection : Count Property*

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

*Quelle: `PolyScanHeadLib~IScanHeadDevices~Item.html` · Polytec PolyScanHead Type Library · IScanHeadDevices Collection : Item Property*

### Description

Returns an item of the collection with the given index.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Item( _
   ByVal Index As Long _
) As IScanHeadDevice
```

### Parameters

Index

The index of the item.


---

## ScanHeadType Property

*Quelle: `PolyScanHeadLib~IScanHeadDevices~ScanHeadType.html` · Polytec PolyScanHead Type Library · IScanHeadDevices Collection : ScanHeadType Property*

### Description

The type object of the scanning heads.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property ScanHeadType As ScanHeadType
```
