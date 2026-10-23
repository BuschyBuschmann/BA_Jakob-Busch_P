# POLYFILELib – ScanHeadDevicesInfo

## ScanHeadDevicesInfo Object

*Quelle: `POLYFILELib~ScanHeadDevicesInfo.html` · Polytec PolyFile Type Library*

### Description

Item of the Infos collection. Contains information about the scanning head used for PSV measurement. Available in PSV files only.

### Object Model


---

## ScanHeadDevicesInfo Object Members

*Quelle: `POLYFILELib~ScanHeadDevicesInfo_members.html` · Polytec PolyFile Type Library*

### Public Properties

| Name | Returns "ScanHeadDevices". This can be used as an index to the Infos collection . |
|---|---|
| ScanHeadDevices | Returns a ScanHeadDevices collection . |
| ScanHeadName | The scanning head name. |
| ScanHeadType | The scanning head type. |
| Type | Returns ptcInfoScanHeadDevices. This can be used as an index to the Infos collection . |


---

## Name Property

*Quelle: `POLYFILELib~ScanHeadDevicesInfo~Name.html` · Polytec PolyFile Type Library · ScanHeadDevicesInfo Object : Name Property*

### Description

Returns "ScanHeadDevices". This can be used as an index to the Infos collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Name As String
```

### Return Type

Always "ScanHeadDevices".


---

## ScanHeadDevices Property

*Quelle: `POLYFILELib~ScanHeadDevicesInfo~ScanHeadDevices.html` · Polytec PolyFile Type Library · ScanHeadDevicesInfo Object : ScanHeadDevices Property*

### Description

Returns a ScanHeadDevices collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property ScanHeadDevices As IScanHeadDevices
```

### Return Type

ScanHeadDevices


---

## ScanHeadName Property

*Quelle: `POLYFILELib~ScanHeadDevicesInfo~ScanHeadName.html` · Polytec PolyFile Type Library · ScanHeadDevicesInfo Object : ScanHeadName Property*

### Description

The scanning head name.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property ScanHeadName As String
```


---

## ScanHeadType Property

*Quelle: `POLYFILELib~ScanHeadDevicesInfo~ScanHeadType.html` · Polytec PolyFile Type Library · ScanHeadDevicesInfo Object : ScanHeadType Property*

### Description

The scanning head type.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property ScanHeadType As PTCScanHeadType
```

### Return Type

PTCScanHeadType


---

## Type Property

*Quelle: `POLYFILELib~ScanHeadDevicesInfo~Type.html` · Polytec PolyFile Type Library · ScanHeadDevicesInfo Object : Type Property*

### Description

Returns ptcInfoScanHeadDevices. This can be used as an index to the Infos collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Type As PTCInfoType
```

### Return Type

Always ptcInfoScanHeadDevices.
