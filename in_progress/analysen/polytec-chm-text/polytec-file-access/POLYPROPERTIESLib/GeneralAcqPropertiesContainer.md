# POLYPROPERTIESLib – GeneralAcqPropertiesContainer

## GeneralAcqPropertiesContainer Object

*Quelle: `POLYPROPERTIESLib~GeneralAcqPropertiesContainer.html` · Polytec PolyProperties Type Library*

### Description

General acquisition properties. Item of the AcquisitonProperties collection.


---

## GeneralAcqPropertiesContainer Object Members

*Quelle: `POLYPROPERTIESLib~GeneralAcqPropertiesContainer_members.html` · Polytec PolyProperties Type Library*

### Public Properties

| AutoRemeasure | Specifies, whether AutoRemeasure is enabled. |
|---|---|
| AutoRemeasureAutoRange | Specifies whether the vibrometer range should be adjusted when an overrange occurs during the scan. |
| BandWidthExtension | Specifies the bandwidth extension for the UHF vibrometer. |
| IsAutoRemeasurePossible | Returns whether re-measuring automatically is possible. |
| PrincipalComponentAnalysis | Specifies, whether principal component analysis (MIMO) is enabled. |
| RealSampleFrequency | The raw sampling frequency of the acquisition board before digital decimation is performed. |
| SaveTimeDataForScan | Specifies whether time domain data is stored in scan file in addition to frequency domain data. |


---

## AutoRemeasure Property

*Quelle: `POLYPROPERTIESLib~GeneralAcqPropertiesContainer~AutoRemeasure.html` · Polytec PolyProperties Type Library · GeneralAcqPropertiesContainer Object : AutoRemeasure Property*

### Description

Specifies, whether AutoRemeasure is enabled.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property AutoRemeasure As Boolean
```

### Example


---

## AutoRemeasureAutoRange Property

*Quelle: `POLYPROPERTIESLib~GeneralAcqPropertiesContainer~AutoRemeasureAutoRange.html` · Polytec PolyProperties Type Library · GeneralAcqPropertiesContainer Object : AutoRemeasureAutoRange Property*

### Description

Specifies whether the vibrometer range should be adjusted when an overrange occurs during the scan.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property AutoRemeasureAutoRange As Boolean
```

### Remarks

If you want to activate the AutoRange feature, you also have to set the AutoRemeasure Property to true. The vibrometer range that was finally used to measure the scan point is available in the VibrometerRange Property.

### Example


---

## BandWidthExtension Property

*Quelle: `POLYPROPERTIESLib~GeneralAcqPropertiesContainer~BandWidthExtension.html` · Polytec PolyProperties Type Library · GeneralAcqPropertiesContainer Object : BandWidthExtension Property*

### Description

Specifies the bandwidth extension for the UHF vibrometer.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property BandWidthExtension As PTCBandWidthExtension
```


---

## IsAutoRemeasurePossible Property

*Quelle: `POLYPROPERTIESLib~GeneralAcqPropertiesContainer~IsAutoRemeasurePossible.html` · Polytec PolyProperties Type Library · GeneralAcqPropertiesContainer Object : IsAutoRemeasurePossible Property*

### Description

Returns whether re-measuring automatically is possible.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property IsAutoRemeasurePossible As Boolean
```

### Return Type

True if re-measuring automatically is possible.

### Example


---

## PrincipalComponentAnalysis Property

*Quelle: `POLYPROPERTIESLib~GeneralAcqPropertiesContainer~PrincipalComponentAnalysis.html` · Polytec PolyProperties Type Library · GeneralAcqPropertiesContainer Object : PrincipalComponentAnalysis Property*

### Description

Specifies, whether principal component analysis (MIMO) is enabled.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property PrincipalComponentAnalysis As Boolean
```

### Example


---

## RealSampleFrequency Property

*Quelle: `POLYPROPERTIESLib~GeneralAcqPropertiesContainer~RealSampleFrequency.html` · Polytec PolyProperties Type Library · GeneralAcqPropertiesContainer Object : RealSampleFrequency Property*

### Description

The raw sampling frequency of the acquisition board before digital decimation is performed.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property RealSampleFrequency As Double
```

### Example


---

## SaveTimeDataForScan Property

*Quelle: `POLYPROPERTIESLib~GeneralAcqPropertiesContainer~SaveTimeDataForScan.html` · Polytec PolyProperties Type Library · GeneralAcqPropertiesContainer Object : SaveTimeDataForScan Property*

### Description

Specifies whether time domain data is stored in scan file in addition to frequency domain data.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property SaveTimeDataForScan As Boolean
```

### Remarks

Saving time data in addition to frequency domain data is available for measurement modes FFT and FastScan. Signal enhancement will be automatically set to mode Fast in case this property is set to true.
