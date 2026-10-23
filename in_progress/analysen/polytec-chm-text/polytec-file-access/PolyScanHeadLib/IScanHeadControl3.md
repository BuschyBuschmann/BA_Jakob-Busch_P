# PolyScanHeadLib – IScanHeadControl3

## IScanHeadControl3 Interface

*Quelle: `PolyScanHeadLib~IScanHeadControl3.html` · Polytec PolyScanHead Type Library*

### Description

Controls the scanning head.

### Object Model

### Remarks

It is recommended to cast to the ScanHeadControl Object.


---

## IScanHeadControl3 Interface Members

*Quelle: `PolyScanHeadLib~IScanHeadControl3_members.html` · Polytec PolyScanHead Type Library*

### Public Methods

| Init | Initializes the scanning head control. |
|---|---|

### Public Properties

| ScanHeadDevice | The scan head device. |
|---|---|
| ScannerControl | The scanner control object. |


---

## Init Method

*Quelle: `PolyScanHeadLib~IScanHeadControl3~Init.html` · Polytec PolyScanHead Type Library · IScanHeadControl3 Interface : Init Method*

### Description

Initializes the scanning head control.

### Syntax

*Visual Basic:*
```
Public Sub Init( _
   ByVal pVal As IPolyDac _
)
```

### Parameters

pVal

Interface to the software component used for D/A conversion to control the scanners.


---

## ScanHeadDevice Property

*Quelle: `PolyScanHeadLib~IScanHeadControl3~ScanHeadDevice.html` · Polytec PolyScanHead Type Library · IScanHeadControl3 Interface : ScanHeadDevice Property*

### Description

The scan head device.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property ScanHeadDevice As IScanHeadDevice
```


---

## ScannerControl Property

*Quelle: `PolyScanHeadLib~IScanHeadControl3~ScannerControl.html` · Polytec PolyScanHead Type Library · IScanHeadControl3 Interface : ScannerControl Property*

### Description

The scanner control object.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property ScannerControl As IScannerControl
```
