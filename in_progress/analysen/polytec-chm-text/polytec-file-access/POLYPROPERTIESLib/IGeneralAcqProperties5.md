# POLYPROPERTIESLib – IGeneralAcqProperties5

## IGeneralAcqProperties5 Interface

*Quelle: `POLYPROPERTIESLib~IGeneralAcqProperties5.html` · Polytec PolyProperties Type Library*

### Description

General acquisition properties. Item of the AcquisitonProperties collection.

### Remarks

It is recommended to cast to the GeneralAcqPropertiesContainer Object.

### Example


---

## IGeneralAcqProperties5 Interface Members

*Quelle: `POLYPROPERTIESLib~IGeneralAcqProperties5_members.html` · Polytec PolyProperties Type Library*

### Public Properties

| AutoRemeasure | Specifies, whether AutoRemeasure is enabled. |
|---|---|
| AutoRemeasureAutoRange | Specifies whether the vibrometer range should be adjusted when an overrange occurs during the scan. |
| BandWidthExtension | Specifies the bandwidth extension for the UHF vibrometer. |
| PrincipalComponentAnalysis | Specifies, whether principal component analysis (MIMO) is enabled. |
| RealSampleFrequency | The raw sampling frequency of the acquisition board before digital decimation is performed. |


---

## AutoRemeasure Property

*Quelle: `POLYPROPERTIESLib~IGeneralAcqProperties5~AutoRemeasure.html` · Polytec PolyProperties Type Library · IGeneralAcqProperties5 Interface : AutoRemeasure Property*

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

*Quelle: `POLYPROPERTIESLib~IGeneralAcqProperties5~AutoRemeasureAutoRange.html` · Polytec PolyProperties Type Library · IGeneralAcqProperties5 Interface : AutoRemeasureAutoRange Property*

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

*Quelle: `POLYPROPERTIESLib~IGeneralAcqProperties5~BandWidthExtension.html` · Polytec PolyProperties Type Library · IGeneralAcqProperties5 Interface : BandWidthExtension Property*

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

## PrincipalComponentAnalysis Property

*Quelle: `POLYPROPERTIESLib~IGeneralAcqProperties5~PrincipalComponentAnalysis.html` · Polytec PolyProperties Type Library · IGeneralAcqProperties5 Interface : PrincipalComponentAnalysis Property*

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

*Quelle: `POLYPROPERTIESLib~IGeneralAcqProperties5~RealSampleFrequency.html` · Polytec PolyProperties Type Library · IGeneralAcqProperties5 Interface : RealSampleFrequency Property*

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
