# PolyScanHeadLib – ScanHeadControl

## ScanHeadControl Object

*Quelle: `PolyScanHeadLib~ScanHeadControl.html` · Polytec PolyScanHead Type Library*

### Description

Controls the scanning head.

### Object Model


---

## ScanHeadControl Object Members

*Quelle: `PolyScanHeadLib~ScanHeadControl_members.html` · Polytec PolyScanHead Type Library*

### Public Methods

| GetGeoScannerOffset | Gets the horizontal and vertical offset of the geometry scan unit laser to the vibrometer laser in the quantity of the scanning head. |
|---|---|
| Init | Initializes the scanning head control. |
| InterpolatedLaserIntensityData | Interpolates the laser intensity data read from the scanning head. |
| ReadFocusData | Reads the data about the focal length and the infinite focus position from the scanning head. |
| ReadLaserIntensityData | Reads the laser intensity data from the scanning head. |
| ReadMirrorAdjustmentData | Reads the adjustment data for the scanning mirrors from the scanning head. |
| SetGeoScannerOffset | Sets the horizontal and vertical offset of the geometry scan unit laser to the vibrometer laser in the quantity of the scanning head. |
| WriteFocusDataFactorySettings | Writes the factory settings for the infinite focus position and the focal length to the scanning head. |
| WriteFocusDataFocalLength | Writes the current focal length to the scanning head. |
| WriteFocusDataInfinitePos | Writes the infinite focus position to the scanning head. |
| WriteLaserIntensityData | Writes the laser intensity data to the scanning head. |
| WriteMirrorAdjustmentData | Writes the adjustment data for the scanning mirrors from the scanning head. |

### Public Properties

| ScanHeadDevice | The scan head device. |
|---|---|
| ScannerControl | The scanner control object. |


---

## GetGeoScannerOffset Method

*Quelle: `PolyScanHeadLib~ScanHeadControl~GetGeoScannerOffset.html` · Polytec PolyScanHead Type Library · ScanHeadControl Object : GetGeoScannerOffset Method*

### Description

Gets the horizontal and vertical offset of the geometry scan unit laser to the vibrometer laser in the quantity of the scanning head.

### Syntax

*Visual Basic:*
```
Public Sub GetGeoScannerOffset( _
   ByRef geoScannerOffsetX As Single, _
   ByRef geoScannerOffsetY As Single _
)
```

### Parameters

geoScannerOffsetX

The horizontal offset of the geometry scan unit in the quantity of the scanning head.

geoScannerOffsetY

The vertical offset of the geometry scan unit in the quantity of the scanning head.


---

## Init Method

*Quelle: `PolyScanHeadLib~ScanHeadControl~Init.html` · Polytec PolyScanHead Type Library · ScanHeadControl Object : Init Method*

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

## InterpolatedLaserIntensityData Method

*Quelle: `PolyScanHeadLib~ScanHeadControl~InterpolatedLaserIntensityData.html` · Polytec PolyScanHead Type Library · ScanHeadControl Object : InterpolatedLaserIntensityData Method*

### Description

Interpolates the laser intensity data read from the scanning head.

### Syntax

*Visual Basic:*
```
Public Function InterpolatedLaserIntensityData( _
   ByVal intensityMin As Integer, _
   ByVal intensityMax As Integer _
) As Single()
```

### Parameters

intensityMin

The minimum laser intensity for the interpolation.

intensityMax

The maximum laser intensity for the interpolation.

### Return Type

The interpolated laser intensity data.

### Remarks

The laser intensity data is used on scanning heads with laser intensity control to allow for a transformation of laser intensities to the actual control values.


---

## ReadFocusData Method

*Quelle: `PolyScanHeadLib~ScanHeadControl~ReadFocusData.html` · Polytec PolyScanHead Type Library · ScanHeadControl Object : ReadFocusData Method*

### Description

Reads the data about the focal length and the infinite focus position from the scanning head.

### Syntax

*Visual Basic:*
```
Public Function ReadFocusData() As Single()
```

### Return Type

0-based array containing the focus data.

### Remarks

The array contains the following values: current focal length, current Infinite position, focal length factory setting, Infinite position factory setting.


---

## ReadLaserIntensityData Method

*Quelle: `PolyScanHeadLib~ScanHeadControl~ReadLaserIntensityData.html` · Polytec PolyScanHead Type Library · ScanHeadControl Object : ReadLaserIntensityData Method*

### Description

Reads the laser intensity data from the scanning head.

### Syntax

*Visual Basic:*
```
Public Function ReadLaserIntensityData() As Unsigned Integer()
```

### Return Type

The laser intensity data.

### Remarks

The laser intensity data is used on scanning heads with laser intensity control to allow for a transformation of laser intensities to the actual control values.


---

## ReadMirrorAdjustmentData Method

*Quelle: `PolyScanHeadLib~ScanHeadControl~ReadMirrorAdjustmentData.html` · Polytec PolyScanHead Type Library · ScanHeadControl Object : ReadMirrorAdjustmentData Method*

### Description

Reads the adjustment data for the scanning mirrors from the scanning head.

### Syntax

*Visual Basic:*
```
Public Function ReadMirrorAdjustmentData() As Single()
```

### Return Type

0-based array with the adjustment data.

### Remarks

The array contains the coefficients of a polynomial used to correct the angles of the scanners to the nominal values.


---

## SetGeoScannerOffset Method

*Quelle: `PolyScanHeadLib~ScanHeadControl~SetGeoScannerOffset.html` · Polytec PolyScanHead Type Library · ScanHeadControl Object : SetGeoScannerOffset Method*

### Description

Sets the horizontal and vertical offset of the geometry scan unit laser to the vibrometer laser in the quantity of the scanning head.

### Syntax

*Visual Basic:*
```
Public Sub SetGeoScannerOffset( _
   ByVal geoScannerOffsetX As Single, _
   ByVal geoScannerOffsetY As Single _
)
```

### Parameters

geoScannerOffsetX

The horizontal offset of the geometry scan unit in the quantity of the scanning head.

geoScannerOffsetY

The vertical offset of the geometry scan unit in the quantity of the scanning head.


---

## WriteFocusDataFactorySettings Method

*Quelle: `PolyScanHeadLib~ScanHeadControl~WriteFocusDataFactorySettings.html` · Polytec PolyScanHead Type Library · ScanHeadControl Object : WriteFocusDataFactorySettings Method*

### Description

Writes the factory settings for the infinite focus position and the focal length to the scanning head.

### Syntax

*Visual Basic:*
```
Public Sub WriteFocusDataFactorySettings( _
   ByVal focusDataInfinitePos As Long, _
   ByVal focusDataFocalLength As Single _
)
```

### Parameters

focusDataInfinitePos

The infinite focus position in focus units.

focusDataFocalLength

The focal length in meter.


---

## WriteFocusDataFocalLength Method

*Quelle: `PolyScanHeadLib~ScanHeadControl~WriteFocusDataFocalLength.html` · Polytec PolyScanHead Type Library · ScanHeadControl Object : WriteFocusDataFocalLength Method*

### Description

Writes the current focal length to the scanning head.

### Syntax

*Visual Basic:*
```
Public Sub WriteFocusDataFocalLength( _
   ByVal focusDataFocalLength As Single _
)
```

### Parameters

focusDataFocalLength

The focal length in meter.


---

## WriteFocusDataInfinitePos Method

*Quelle: `PolyScanHeadLib~ScanHeadControl~WriteFocusDataInfinitePos.html` · Polytec PolyScanHead Type Library · ScanHeadControl Object : WriteFocusDataInfinitePos Method*

### Description

Writes the infinite focus position to the scanning head.

### Syntax

*Visual Basic:*
```
Public Sub WriteFocusDataInfinitePos( _
   ByVal focusDataInfinitePos As Long _
)
```

### Parameters

focusDataInfinitePos

The infinite focus position in focus units.


---

## WriteLaserIntensityData Method

*Quelle: `PolyScanHeadLib~ScanHeadControl~WriteLaserIntensityData.html` · Polytec PolyScanHead Type Library · ScanHeadControl Object : WriteLaserIntensityData Method*

### Description

Writes the laser intensity data to the scanning head.

### Syntax

*Visual Basic:*
```
Public Sub WriteLaserIntensityData( _
   ByVal laserIntensityData() As Unsigned Integer _
)
```

### Parameters

laserIntensityData

The laser intensity data.

### Remarks

The laser intensity data is used on scanning heads with laser intensity control to allow for a transformation of laser intensities to the actual control values.


---

## WriteMirrorAdjustmentData Method

*Quelle: `PolyScanHeadLib~ScanHeadControl~WriteMirrorAdjustmentData.html` · Polytec PolyScanHead Type Library · ScanHeadControl Object : WriteMirrorAdjustmentData Method*

### Description

Writes the adjustment data for the scanning mirrors from the scanning head.

### Syntax

*Visual Basic:*
```
Public Sub WriteMirrorAdjustmentData( _
   ByVal mirrorAdjustmentData() As Single _
)
```

### Parameters

mirrorAdjustmentData

0-based array with the adjustment data.

### Remarks

The array contains the coefficients of a polynomial used to correct the angles of the scanners to the nominal values.


---

## ScanHeadDevice Property

*Quelle: `PolyScanHeadLib~ScanHeadControl~ScanHeadDevice.html` · Polytec PolyScanHead Type Library · ScanHeadControl Object : ScanHeadDevice Property*

### Description

The scan head device.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property ScanHeadDevice As ScanHeadDevice
```


---

## ScannerControl Property

*Quelle: `PolyScanHeadLib~ScanHeadControl~ScannerControl.html` · Polytec PolyScanHead Type Library · ScanHeadControl Object : ScannerControl Property*

### Description

The scanner control object.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property ScannerControl As ScannerControl
```
