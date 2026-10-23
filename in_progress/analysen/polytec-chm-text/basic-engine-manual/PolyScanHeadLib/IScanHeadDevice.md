# PolyScanHeadLib – IScanHeadDevice

## IScanHeadDevice Interface

*Quelle: `PolyScanHeadLib~IScanHeadDevice.html` · Polytec PolyScanHead Type Library*

### Description

The scanning head device. Item of the ScanHeadDevices collection.

### Object Model

### Remarks

It is recommended to cast to the ScanHeadDevice object.


---

## IScanHeadDevice Interface Members

*Quelle: `PolyScanHeadLib~IScanHeadDevice_members.html` · Polytec PolyScanHead Type Library*

### Public Properties

| Caps | The scanning head capabilities. |
|---|---|
| DistanceSensorControl | The distance sensor control object. |
| Focus | The scanning head focus object. |
| LensMagnification | The objective magnification. |
| PanTiltHead | Specifies, whether the pan-tilt head is used. |
| RollAngle | The roll angle of the scanning head. |
| ScanHeadDevices | The scanning head devices object. |
| Scanner | The scanning head scanner object. |
| SensorHeadName | The name of the sensor head. |
| SensorHeadNames | Returns an array of all possible sensor head names. |
| Video | The scanning head video object. |


---

## Caps Property

*Quelle: `PolyScanHeadLib~IScanHeadDevice~Caps.html` · Polytec PolyScanHead Type Library · IScanHeadDevice Interface : Caps Property*

### Description

The scanning head capabilities.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Caps As PTCScanHeadCapsType
```


---

## DistanceSensorControl Property

*Quelle: `PolyScanHeadLib~IScanHeadDevice~DistanceSensorControl.html` · Polytec PolyScanHead Type Library · IScanHeadDevice Interface : DistanceSensorControl Property*

### Description

The distance sensor control object.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property DistanceSensorControl As IDistanceSensorControl
```


---

## Focus Property

*Quelle: `PolyScanHeadLib~IScanHeadDevice~Focus.html` · Polytec PolyScanHead Type Library · IScanHeadDevice Interface : Focus Property*

### Description

The scanning head focus object.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Focus As IScanHeadLaserFocus
```


---

## LensMagnification Property

*Quelle: `PolyScanHeadLib~IScanHeadDevice~LensMagnification.html` · Polytec PolyScanHead Type Library · IScanHeadDevice Interface : LensMagnification Property*

### Description

The objective magnification.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property LensMagnification As Double
```

### Remarks

Beginning with the software releases in July 2018, a "lens" is called "objective" in the GUI of the applications.


---

## PanTiltHead Property

*Quelle: `PolyScanHeadLib~IScanHeadDevice~PanTiltHead.html` · Polytec PolyScanHead Type Library · IScanHeadDevice Interface : PanTiltHead Property*

### Description

Specifies, whether the pan-tilt head is used.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property PanTiltHead As Boolean
```


---

## RollAngle Property

*Quelle: `PolyScanHeadLib~IScanHeadDevice~RollAngle.html` · Polytec PolyScanHead Type Library · IScanHeadDevice Interface : RollAngle Property*

### Description

The roll angle of the scanning head.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property RollAngle As Double
```


---

## ScanHeadDevices Property

*Quelle: `PolyScanHeadLib~IScanHeadDevice~ScanHeadDevices.html` · Polytec PolyScanHead Type Library · IScanHeadDevice Interface : ScanHeadDevices Property*

### Description

The scanning head devices object.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property ScanHeadDevices As ScanHeadDevices
```


---

## Scanner Property

*Quelle: `PolyScanHeadLib~IScanHeadDevice~Scanner.html` · Polytec PolyScanHead Type Library · IScanHeadDevice Interface : Scanner Property*

### Description

The scanning head scanner object.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Scanner As ScanHeadScanner
```


---

## SensorHeadName Property

*Quelle: `PolyScanHeadLib~IScanHeadDevice~SensorHeadName.html` · Polytec PolyScanHead Type Library · IScanHeadDevice Interface : SensorHeadName Property*

### Description

The name of the sensor head.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property SensorHeadName As String
```


---

## SensorHeadNames Property

*Quelle: `PolyScanHeadLib~IScanHeadDevice~SensorHeadNames.html` · Polytec PolyScanHead Type Library · IScanHeadDevice Interface : SensorHeadNames Property*

### Description

Returns an array of all possible sensor head names.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property SensorHeadNames As String()
```


---

## Video Property

*Quelle: `PolyScanHeadLib~IScanHeadDevice~Video.html` · Polytec PolyScanHead Type Library · IScanHeadDevice Interface : Video Property*

### Description

The scanning head video object.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Video As ScanHeadVideo
```
