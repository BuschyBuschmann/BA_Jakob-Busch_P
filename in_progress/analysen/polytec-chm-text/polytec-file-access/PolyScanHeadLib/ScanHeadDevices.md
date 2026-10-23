# PolyScanHeadLib – ScanHeadDevices

## ScanHeadDevices Collection

*Quelle: `PolyScanHeadLib~ScanHeadDevices.html` · Polytec PolyScanHead Type Library*

### Description

Collection of the scanning head devices of a PSV system.

### Object Model

### Remarks

On PSV-3D systems this collection contains three scanning head devices. On other PSV systems, the collection contains a single scanning head device.


---

## ScanHeadDevices Collection Members

*Quelle: `PolyScanHeadLib~ScanHeadDevices_members.html` · Polytec PolyScanHead Type Library*

### Public Properties

| Count | The number of items in the collection. |
|---|---|
| Item | Returns an item of the collection with the given index. |
| ScanHeadType | The type object of the scanning heads. |


---

## Count Property

*Quelle: `PolyScanHeadLib~ScanHeadDevices~Count.html` · Polytec PolyScanHead Type Library · ScanHeadDevices Collection : Count Property*

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

*Quelle: `PolyScanHeadLib~ScanHeadDevices~Item.html` · Polytec PolyScanHead Type Library · ScanHeadDevices Collection : Item Property*

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

*Quelle: `PolyScanHeadLib~ScanHeadDevices~ScanHeadType.html` · Polytec PolyScanHead Type Library · ScanHeadDevices Collection : ScanHeadType Property*

### Description

The type object of the scanning heads.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property ScanHeadType As ScanHeadType
```
