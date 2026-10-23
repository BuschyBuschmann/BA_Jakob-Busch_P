# PSV – GeneralAcqProperties

## GeneralAcqProperties Object

*Quelle: `PSV~GeneralAcqProperties.html` · Polytec PSV Type Library*

### Description

General acquisition properties. Item of the AcquisitonProperties collection.


---

## GeneralAcqProperties Object Members

*Quelle: `PSV~GeneralAcqProperties_members.html` · Polytec PSV Type Library*

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

*Quelle: `PSV~GeneralAcqProperties~AutoRemeasure.html` · Polytec PSV Type Library · GeneralAcqProperties Object : AutoRemeasure Property*

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

*Quelle: `PSV~GeneralAcqProperties~AutoRemeasureAutoRange.html` · Polytec PSV Type Library · GeneralAcqProperties Object : AutoRemeasureAutoRange Property*

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

*Quelle: `PSV~GeneralAcqProperties~BandWidthExtension.html` · Polytec PSV Type Library · GeneralAcqProperties Object : BandWidthExtension Property*

### Description

Specifies the bandwidth extension for the UHF vibrometer.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property BandWidthExtension As PTCBandWidthExtension
```

### Example


---

## IsAutoRemeasurePossible Property

*Quelle: `PSV~GeneralAcqProperties~IsAutoRemeasurePossible.html` · Polytec PSV Type Library · GeneralAcqProperties Object : IsAutoRemeasurePossible Property*

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

*Quelle: `PSV~GeneralAcqProperties~PrincipalComponentAnalysis.html` · Polytec PSV Type Library · GeneralAcqProperties Object : PrincipalComponentAnalysis Property*

### Description

Specifies, whether principal component analysis (MIMO) is enabled.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property PrincipalComponentAnalysis As Boolean
```


---

## RealSampleFrequency Property

*Quelle: `PSV~GeneralAcqProperties~RealSampleFrequency.html` · Polytec PSV Type Library · GeneralAcqProperties Object : RealSampleFrequency Property*

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

*Quelle: `PSV~GeneralAcqProperties~SaveTimeDataForScan.html` · Polytec PSV Type Library · GeneralAcqProperties Object : SaveTimeDataForScan Property*

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
