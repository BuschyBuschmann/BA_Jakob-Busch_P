# PSV – ScanHeadDevicesInfoAcq

## ScanHeadDevicesInfoAcq Object

*Quelle: `PSV~ScanHeadDevicesInfoAcq.html` · Polytec PSV Type Library*

### Description

Item of the InfosAcq collection. Contains information about the scanning head used for PSV measurement. Available in PSV files only.

### Object Model


---

## ScanHeadDevicesInfoAcq Object Members

*Quelle: `PSV~ScanHeadDevicesInfoAcq_members.html` · Polytec PSV Type Library*

### Public Properties

| Name | Returns "ScanHeadDevices". This can be used as an index to the InfosAcq collection . |
|---|---|
| ScanHeadDevices | Returns a ScanHeadDevices collection . |
| ScanHeadName | The scanning head name. |
| ScanHeadType | The scanning head type. |
| Type | Returns ptcInfoScanHeadDevices. This can be used as an index to the InfosAcq collection . |


---

## Name Property

*Quelle: `PSV~ScanHeadDevicesInfoAcq~Name.html` · Polytec PSV Type Library · ScanHeadDevicesInfoAcq Object : Name Property*

### Description

Returns "ScanHeadDevices". This can be used as an index to the InfosAcq collection.

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

*Quelle: `PSV~ScanHeadDevicesInfoAcq~ScanHeadDevices.html` · Polytec PSV Type Library · ScanHeadDevicesInfoAcq Object : ScanHeadDevices Property*

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

*Quelle: `PSV~ScanHeadDevicesInfoAcq~ScanHeadName.html` · Polytec PSV Type Library · ScanHeadDevicesInfoAcq Object : ScanHeadName Property*

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

*Quelle: `PSV~ScanHeadDevicesInfoAcq~ScanHeadType.html` · Polytec PSV Type Library · ScanHeadDevicesInfoAcq Object : ScanHeadType Property*

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

*Quelle: `PSV~ScanHeadDevicesInfoAcq~Type.html` · Polytec PSV Type Library · ScanHeadDevicesInfoAcq Object : Type Property*

### Description

Returns ptcInfoScanHeadDevices. This can be used as an index to the InfosAcq collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Type As PTCInfoType
```

### Return Type

Always ptcInfoScanHeadDevices.
