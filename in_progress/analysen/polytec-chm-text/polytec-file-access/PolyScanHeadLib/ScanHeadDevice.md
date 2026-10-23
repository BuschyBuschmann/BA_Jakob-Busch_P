# PolyScanHeadLib – ScanHeadDevice

## ScanHeadDevice Object

*Quelle: `PolyScanHeadLib~ScanHeadDevice.html` · Polytec PolyScanHead Type Library*

### Description

The scanning head device. Item of the ScanHeadDevices collection.

### Object Model


---

## ScanHeadDevice Object Members

*Quelle: `PolyScanHeadLib~ScanHeadDevice_members.html` · Polytec PolyScanHead Type Library*

### Public Properties

| Caps | The scanning head capabilities. |
|---|---|
| DistanceSensorControl | The distance sensor control object. |
| Focus | The scanning head focus object. |
| LensMagnification | The objective magnification. |
| PanTiltHead | Specifies, whether the pan-tilt head is used. |
| RollAngle | The roll angle of the scanning head. |
| ScanHeadControl | The scan head control object. |
| ScanHeadDevices | The scanning head devices object. |
| Scanner | The scanning head scanner object. |
| SensorHeadName | The name of the sensor head. |
| SensorHeadNames | Returns an array of all possible sensor head names. |
| Video | The scanning head video object. |
| ZStageControl | The scanning head Z-Stage object. |


---

## Caps Property

*Quelle: `PolyScanHeadLib~ScanHeadDevice~Caps.html` · Polytec PolyScanHead Type Library · ScanHeadDevice Object : Caps Property*

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

*Quelle: `PolyScanHeadLib~ScanHeadDevice~DistanceSensorControl.html` · Polytec PolyScanHead Type Library · ScanHeadDevice Object : DistanceSensorControl Property*

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

*Quelle: `PolyScanHeadLib~ScanHeadDevice~Focus.html` · Polytec PolyScanHead Type Library · ScanHeadDevice Object : Focus Property*

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

*Quelle: `PolyScanHeadLib~ScanHeadDevice~LensMagnification.html` · Polytec PolyScanHead Type Library · ScanHeadDevice Object : LensMagnification Property*

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

*Quelle: `PolyScanHeadLib~ScanHeadDevice~PanTiltHead.html` · Polytec PolyScanHead Type Library · ScanHeadDevice Object : PanTiltHead Property*

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

*Quelle: `PolyScanHeadLib~ScanHeadDevice~RollAngle.html` · Polytec PolyScanHead Type Library · ScanHeadDevice Object : RollAngle Property*

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

## ScanHeadControl Property

*Quelle: `PolyScanHeadLib~ScanHeadDevice~ScanHeadControl.html` · Polytec PolyScanHead Type Library · ScanHeadDevice Object : ScanHeadControl Property*

### Description

The scan head control object.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property ScanHeadControl As IScanHeadControl3
```


---

## ScanHeadDevices Property

*Quelle: `PolyScanHeadLib~ScanHeadDevice~ScanHeadDevices.html` · Polytec PolyScanHead Type Library · ScanHeadDevice Object : ScanHeadDevices Property*

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

*Quelle: `PolyScanHeadLib~ScanHeadDevice~Scanner.html` · Polytec PolyScanHead Type Library · ScanHeadDevice Object : Scanner Property*

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

*Quelle: `PolyScanHeadLib~ScanHeadDevice~SensorHeadName.html` · Polytec PolyScanHead Type Library · ScanHeadDevice Object : SensorHeadName Property*

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

*Quelle: `PolyScanHeadLib~ScanHeadDevice~SensorHeadNames.html` · Polytec PolyScanHead Type Library · ScanHeadDevice Object : SensorHeadNames Property*

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

*Quelle: `PolyScanHeadLib~ScanHeadDevice~Video.html` · Polytec PolyScanHead Type Library · ScanHeadDevice Object : Video Property*

### Description

The scanning head video object.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Video As ScanHeadVideo
```


---

## ZStageControl Property

*Quelle: `PolyScanHeadLib~ScanHeadDevice~ZStageControl.html` · Polytec PolyScanHead Type Library · ScanHeadDevice Object : ZStageControl Property*

### Description

The scanning head Z-Stage object.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property ZStageControl As IZStageControl
```
