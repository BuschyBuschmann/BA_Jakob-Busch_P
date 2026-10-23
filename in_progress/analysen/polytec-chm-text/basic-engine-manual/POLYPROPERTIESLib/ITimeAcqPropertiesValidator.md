# POLYPROPERTIESLib – ITimeAcqPropertiesValidator

## ITimeAcqPropertiesValidator Interface

*Quelle: `POLYPROPERTIESLib~ITimeAcqPropertiesValidator.html` · Polytec PolyProperties Type Library*

### Description

The time properties validator acts as a staging/validation buffer for time-domain acquisition settings before they are committed to the actual acquisition settings.

### Remarks

It lets clients construct a candidate pair of time acquisition settings, inspect the valid ranges/lists for each, and validate the combination as a whole  without side effects on the live acquisition until Validate succeeds and the validator is applied via TimeAcqPropertiesValidator Property.

Note that time settings are read-only when the acquisition mode is ptcAcqModeIQ.

### Example

For an example see TimeAcqPropertiesValidator Property.

Typical Usage Flow
1. Obtain a validator via TimeAcqPropertiesValidator Property (pre-populated with current live settings).
2. Modify SampleFrequency and/or Samples on the validator.
3. Call Validate to check consistency, or pass the validator to TimeAcqPropertiesValidator Property, which validates and then applies both settings atomically to the live acquisition settings.


---

## ITimeAcqPropertiesValidator Interface Members

*Quelle: `POLYPROPERTIESLib~ITimeAcqPropertiesValidator_members.html` · Polytec PolyProperties Type Library*

### Public Methods

| GetMinMaxSamplesRange | Returns the min/max sample count achievable for the current SampleFrequency . |
|---|---|
| Validate | Performs a full consistency check of the currently staged values: 1. Validates that SampleFrequency / Samples is a supported combination. 2. Validates the Signal Enhancement (SE) time/average constraint. 3. Validates that the sample frequency is supported when an external trigger is active. |

### Public Properties

| AvailableSampleFrequencies | Returns the full list of supported sample frequencies (including BWX-extended values, deduplicated) |
|---|---|
| AvailableSamples | Returns the list of valid sample counts for the current SampleFrequency . |
| SampleFrequency | The sample frequency in Hz. |
| Samples | The sample count. |


---

## GetMinMaxSamplesRange Method

*Quelle: `POLYPROPERTIESLib~ITimeAcqPropertiesValidator~GetMinMaxSamplesRange.html` · Polytec PolyProperties Type Library · ITimeAcqPropertiesValidator Interface : GetMinMaxSamplesRange Method*

### Description

Returns the min/max sample count achievable for the current SampleFrequency.

### Syntax

*Visual Basic:*
```
Public Sub GetMinMaxSamplesRange( _
   ByRef minSamples As Long, _
   ByRef maxSamples As Long _
)
```

### Parameters

minSamples

Receives the minimum sample count.

maxSamples

Receives the maximum sample count.


---

## Validate Method

*Quelle: `POLYPROPERTIESLib~ITimeAcqPropertiesValidator~Validate.html` · Polytec PolyProperties Type Library · ITimeAcqPropertiesValidator Interface : Validate Method*

### Description

Performs a full consistency check of the currently staged values:
1. Validates that SampleFrequency/Samples is a supported combination.
2. Validates the Signal Enhancement (SE) time/average constraint.
3. Validates that the sample frequency is supported when an external trigger is active.

### Syntax

*Visual Basic:*
```
Public Sub Validate()
```


---

## AvailableSampleFrequencies Property

*Quelle: `POLYPROPERTIESLib~ITimeAcqPropertiesValidator~AvailableSampleFrequencies.html` · Polytec PolyProperties Type Library · ITimeAcqPropertiesValidator Interface : AvailableSampleFrequencies Property*

### Description

Returns the full list of supported sample frequencies (including BWX-extended values, deduplicated)

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property AvailableSampleFrequencies As Double()
```

### Return Type

The list of sample frequencies in Hz.


---

## AvailableSamples Property

*Quelle: `POLYPROPERTIESLib~ITimeAcqPropertiesValidator~AvailableSamples.html` · Polytec PolyProperties Type Library · ITimeAcqPropertiesValidator Interface : AvailableSamples Property*

### Description

Returns the list of valid sample counts for the current SampleFrequency.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property AvailableSamples As Long()
```

### Return Type

The valid sample count.


---

## SampleFrequency Property

*Quelle: `POLYPROPERTIESLib~ITimeAcqPropertiesValidator~SampleFrequency.html` · Polytec PolyProperties Type Library · ITimeAcqPropertiesValidator Interface : SampleFrequency Property*

### Description

The sample frequency in Hz.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property SampleFrequency As Double
```

### Remarks

On put, snaps the value to the nearest supported sample frequency, which is derived from the standard and bandwidth-extension (BWX) frequency lists.


---

## Samples Property

*Quelle: `POLYPROPERTIESLib~ITimeAcqPropertiesValidator~Samples.html` · Polytec PolyProperties Type Library · ITimeAcqPropertiesValidator Interface : Samples Property*

### Description

The sample count.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Samples As Long
```

### Return Type

The sample count.
