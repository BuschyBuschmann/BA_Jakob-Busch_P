# POLYPROPERTIESLib – IFftAcqPropertiesValidator

## IFftAcqPropertiesValidator Interface

*Quelle: `POLYPROPERTIESLib~IFftAcqPropertiesValidator.html` · Polytec PolyProperties Type Library*

### Description

The FFT properties validator acts as a validation buffer for FFT acquisition settings before they are committed to the actual acquisition settings.

### Remarks

It lets clients construct a candidate set of FFT parameters (bandwidth, start/end frequency, lines, overlap, samples), inspect valid ranges for each, and validate the combination as a whole  without side effects on the live acquisition until Validate Method succeeds and the validator is applied via FftAcqPropertiesValidator Property.

### Example

For an example see FftAcqPropertiesValidator Property.

Typical Usage Flow
1. Obtain a validator via FftAcqPropertiesValidator Property (pre-populated with current live settings).
2. Modify properties (Bandwidth, Lines, StartFrequency, etc.) on the validator.
3. Call Validate to check consistency, or pass the validator to FftAcqPropertiesValidator Property, which validates and then applies all settings atomically to the live acquisition settings.


---

## IFftAcqPropertiesValidator Interface Members

*Quelle: `POLYPROPERTIESLib~IFftAcqPropertiesValidator_members.html` · Polytec PolyProperties Type Library*

### Public Methods

| GetMinMaxFrequencyRange | Gets the minimum and maximum of the available frequency range for the specified bandwidth and lines. |
|---|---|
| GetMinMaxOverlap | Gets the minimum and maximum overlap in percent. |
| GetMinMaxSamples | Gets the minimum and maximum number of samples used for calculating the FFT. |
| Validate | Validates the specified settings. |

### Public Properties

| AvailableBandwidths | The available bandwidths. |
|---|---|
| AvailableLines | The available FFT lines. |
| Bandwidth | The current bandwidth. |
| EndFrequency | The end frequency of the frequency range. |
| Lines | The number of FFT lines. |
| Overlap | The overlap of the FFTs in percent. |
| Samples | The number of samples for Multi Frame measurements. |
| StartFrequency | The start frequency of the frequency range. |


---

## GetMinMaxFrequencyRange Method

*Quelle: `POLYPROPERTIESLib~IFftAcqPropertiesValidator~GetMinMaxFrequencyRange.html` · Polytec PolyProperties Type Library · IFftAcqPropertiesValidator Interface : GetMinMaxFrequencyRange Method*

### Description

Gets the minimum and maximum of the available frequency range for the specified bandwidth and lines.

### Syntax

*Visual Basic:*
```
Public Sub GetMinMaxFrequencyRange( _
   ByRef minFrequency As Double, _
   ByRef maxFrequency As Double _
)
```

### Parameters

minFrequency

After the call, receives the minimum of the available frequency range.

maxFrequency

After the call, receives the maximum of the available frequency range.

### Remarks

Before calling this method, set the Bandwidth Property and the Lines Property.


---

## GetMinMaxOverlap Method

*Quelle: `POLYPROPERTIESLib~IFftAcqPropertiesValidator~GetMinMaxOverlap.html` · Polytec PolyProperties Type Library · IFftAcqPropertiesValidator Interface : GetMinMaxOverlap Method*

### Description

Gets the minimum and maximum overlap in percent.

### Syntax

*Visual Basic:*
```
Public Sub GetMinMaxOverlap( _
   ByRef minOverlap As Long, _
   ByRef maxOverlap As Long _
)
```

### Parameters

minOverlap

The minimum overlap in percent.

maxOverlap

The maximum overlap in percent.

### Remarks

Returns 0/0 if overlap isn't supported.


---

## GetMinMaxSamples Method

*Quelle: `POLYPROPERTIESLib~IFftAcqPropertiesValidator~GetMinMaxSamples.html` · Polytec PolyProperties Type Library · IFftAcqPropertiesValidator Interface : GetMinMaxSamples Method*

### Description

Gets the minimum and maximum number of samples used for calculating the FFT.

### Syntax

*Visual Basic:*
```
Public Sub GetMinMaxSamples( _
   ByRef minSamples As Long, _
   ByRef maxSamples As Long _
)
```

### Parameters

minSamples

The minimum number of samples.

maxSamples

The maximum number of samples.

### Remarks

Returns 0/0 if multi-frame isn't supported.


---

## Validate Method

*Quelle: `POLYPROPERTIESLib~IFftAcqPropertiesValidator~Validate.html` · Polytec PolyProperties Type Library · IFftAcqPropertiesValidator Interface : Validate Method*

### Description

Validates the specified settings.

### Syntax

*Visual Basic:*
```
Public Sub Validate()
```


---

## AvailableBandwidths Property

*Quelle: `POLYPROPERTIESLib~IFftAcqPropertiesValidator~AvailableBandwidths.html` · Polytec PolyProperties Type Library · IFftAcqPropertiesValidator Interface : AvailableBandwidths Property*

### Description

The available bandwidths.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property AvailableBandwidths As Double()
```

### Return Type

An array of the available bandwidths in Hz.

### Remarks

Set the Bandwidth Property to one of the returned values to retreive further information about the bandwidth.


---

## AvailableLines Property

*Quelle: `POLYPROPERTIESLib~IFftAcqPropertiesValidator~AvailableLines.html` · Polytec PolyProperties Type Library · IFftAcqPropertiesValidator Interface : AvailableLines Property*

### Description

The available FFT lines.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property AvailableLines As Long()
```

### Return Type

An array with the available FFT lines for the current Bandwidth.

### Remarks

Set the Lines Property to one of the returned values.


---

## Bandwidth Property

*Quelle: `POLYPROPERTIESLib~IFftAcqPropertiesValidator~Bandwidth.html` · Polytec PolyProperties Type Library · IFftAcqPropertiesValidator Interface : Bandwidth Property*

### Description

The current bandwidth.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Bandwidth As Double
```

### Remarks

On put, snaps the value to the nearest supported bandwidth.


---

## EndFrequency Property

*Quelle: `POLYPROPERTIESLib~IFftAcqPropertiesValidator~EndFrequency.html` · Polytec PolyProperties Type Library · IFftAcqPropertiesValidator Interface : EndFrequency Property*

### Description

The end frequency of the frequency range.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property EndFrequency As Double
```


---

## Lines Property

*Quelle: `POLYPROPERTIESLib~IFftAcqPropertiesValidator~Lines.html` · Polytec PolyProperties Type Library · IFftAcqPropertiesValidator Interface : Lines Property*

### Description

The number of FFT lines.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Lines As Long
```

### Remarks

On put, snaps to the nearest valid FFT line count for the current bandwidth.


---

## Overlap Property

*Quelle: `POLYPROPERTIESLib~IFftAcqPropertiesValidator~Overlap.html` · Polytec PolyProperties Type Library · IFftAcqPropertiesValidator Interface : Overlap Property*

### Description

The overlap of the FFTs in percent.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Overlap As Long
```


---

## Samples Property

*Quelle: `POLYPROPERTIESLib~IFftAcqPropertiesValidator~Samples.html` · Polytec PolyProperties Type Library · IFftAcqPropertiesValidator Interface : Samples Property*

### Description

The number of samples for Multi Frame measurements.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Samples As Long
```


---

## StartFrequency Property

*Quelle: `POLYPROPERTIESLib~IFftAcqPropertiesValidator~StartFrequency.html` · Polytec PolyProperties Type Library · IFftAcqPropertiesValidator Interface : StartFrequency Property*

### Description

The start frequency of the frequency range.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property StartFrequency As Double
```
