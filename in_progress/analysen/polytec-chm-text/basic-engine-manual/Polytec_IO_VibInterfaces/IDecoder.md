# Polytec_IO_VibInterfaces – IDecoder

## IDecoder Interface

*Quelle: `Polytec_IO_VibInterfaces~IDecoder.html` · Polytec IO VibInterfaces Type Library*

### Description

The decoder of a controller. Item of the IDecoderCollection.

### Object Model


---

## IDecoder Interface Members

*Quelle: `Polytec_IO_VibInterfaces~IDecoder_members.html` · Polytec IO VibInterfaces Type Library*

### Public Methods

| DecoderClear | Clears the offset of the decoder, e.g. for VibroOne and VibroFlex systems. |
|---|---|
| HasCap | Returns true, if the decoder has the given capability. |
| HasMeasurementMode | Returns true, if the decoder has the given measurement mode. |
| ResetDcOffset | Resets the DC offset of the decoder, i.e. resets a displacement decoder to the value zero, e.g. for OFV-5000 systems. |

### Public Properties

| AnalogOutputRange | The analog output range of the decoder in V. |
|---|---|
| BandwidthRanges | The bandwidth ranges of the decoder. |
| Caps | The capabilities of the decoder. |
| DecoderAvailable | Returns whether the decoder is currently available. |
| DecoderInfo | The information about the decoder. |
| DecoderQuantityType | The type of the quantity where this decoder belongs to. |
| Impedance | The impedance of the decoder. |
| MaxAcceleration | The current maximum acceleration of the decoder. |
| MaxVelocityRanges | The maximum velocity ranges of the decoder. |
| MeasurementMode | The measurement mode of the decoder. |
| Name | The name of the decoder. |
| OptimumRange | Gets the optimum range of the decoder for the currently active bandwidth. |
| OutputMode | The output mode of the decoder. |
| Ranges | The ranges of the decoder. |


---

## DecoderClear Method

*Quelle: `Polytec_IO_VibInterfaces~IDecoder~DecoderClear.html` · Polytec IO VibInterfaces Type Library · IDecoder Interface : DecoderClear Method*

### Description

Clears the offset of the decoder, e.g. for VibroOne and VibroFlex systems.

### Syntax

*Visual Basic:*
```
Public Sub DecoderClear()
```


---

## HasCap Method

*Quelle: `Polytec_IO_VibInterfaces~IDecoder~HasCap.html` · Polytec IO VibInterfaces Type Library · IDecoder Interface : HasCap Method*

### Description

Returns true, if the decoder has the given capability.

### Syntax

*Visual Basic:*
```
Public Function HasCap( _
   ByVal cap As DecoderCaps _
) As Boolean
```

### Parameters

cap

| Value | Description |
|---|---|
| DecoderCaps_AnalogCalibrationFactor | The decoder supports an analog calibration factor. |
| DecoderCaps_AnalogOutputRange | The decoder has information about the analog output range. |
| DecoderCaps_Bandwidth | The decoder has bandwidth ranges. |
| DecoderCaps_DecoderAvailable | The decoder supports the decoder available property, e.g. for the VFX-F-110 system. |
| DecoderCaps_DecoderClear | The decoder supports clearing the offset, e.g. for VibroOne and VibroFlex systems. |
| DecoderCaps_Digital | The decoder is a digital decoder. |
| DecoderCaps_FrequencyLimit | The ranges of the decoder have a frequency limit. |
| DecoderCaps_FringeCounter | The decoder is a fringe counter decoder. |
| DecoderCaps_FullscaleRanges | The ranges of the decoder are specified as full scale, e.g. 10 mm/s, not as per Volt, e.g. 10 mm/s/V. |
| DecoderCaps_Impedance | The decoder supports impedance. |
| DecoderCaps_MaxAcceleration | The decoder supports maximum acceleration, e.g. for the VFX-F-110 system. |
| DecoderCaps_MaxVelocity | The decoder supports maximum velocity, e.g. for the VFX-F-110 system. |
| DecoderCaps_MeasurementMode | The decoder supports the measurement mode, e.g. as for the PSV-500-M system. |
| DecoderCaps_None | No capabilities. |
| DecoderCaps_OptimumRange | The decoder supports the optimum range property, e.g. for the VFX-F-110 system. |
| DecoderCaps_OutputActive | The decoder supports the output active property, e.g. for the VGO-200 system. |
| DecoderCaps_OutputMode | The decoder supports different output modes. |
| DecoderCaps_Overrange | The decoder supports the overrange property, e.g. as for the IVS-500 system. |
| DecoderCaps_Overrun | The decoder has an overrun mode. |
| DecoderCaps_Ranges | The decoder has ranges. |
| DecoderCaps_ResetDcOffset | The decoder can reset the DC offset, e.g. for OFV-5000 systems. |
| DecoderCaps_Resolution | The ranges of the decoder have a known resolution. |
| DecoderCaps_Rpm | The decoder is a RPM decoder, e.g. as for the RLV-5000 system. |
| DecoderCaps_SignalDelay | The ranges of the decoder have a known signal delay. |
| DecoderCaps_VibAnalogOut | The decoder has a vibrometer analog output. |
The capabilities of the decoder.


---

## HasMeasurementMode Method

*Quelle: `Polytec_IO_VibInterfaces~IDecoder~HasMeasurementMode.html` · Polytec IO VibInterfaces Type Library · IDecoder Interface : HasMeasurementMode Method*

### Description

Returns true, if the decoder has the given measurement mode.

### Syntax

*Visual Basic:*
```
Public Function HasMeasurementMode( _
   ByVal MeasurementMode As DecoderMeasurementMode _
) As Boolean
```

### Parameters

MeasurementMode

| Value | Description |
|---|---|
| DecoderMeasurementMode_Test | The decoder generates a test signal. |
| DecoderMeasurementMode_Velocity | The decoder measures velocity. |
| DecoderMeasurementMode_Vibrometer | The deocoder measures as a vibrometer. |


---

## ResetDcOffset Method

*Quelle: `Polytec_IO_VibInterfaces~IDecoder~ResetDcOffset.html` · Polytec IO VibInterfaces Type Library · IDecoder Interface : ResetDcOffset Method*

### Description

Resets the DC offset of the decoder, i.e. resets a displacement decoder to the value zero, e.g. for OFV-5000 systems.

### Syntax

*Visual Basic:*
```
Public Sub ResetDcOffset()
```


---

## AnalogOutputRange Property

*Quelle: `Polytec_IO_VibInterfaces~IDecoder~AnalogOutputRange.html` · Polytec IO VibInterfaces Type Library · IDecoder Interface : AnalogOutputRange Property*

### Description

The analog output range of the decoder in V.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property AnalogOutputRange As Double
```


---

## BandwidthRanges Property

*Quelle: `Polytec_IO_VibInterfaces~IDecoder~BandwidthRanges.html` · Polytec IO VibInterfaces Type Library · IDecoder Interface : BandwidthRanges Property*

### Description

The bandwidth ranges of the decoder.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property BandwidthRanges As IBandwidthRangeCollection
```

### Example


---

## Caps Property

*Quelle: `Polytec_IO_VibInterfaces~IDecoder~Caps.html` · Polytec IO VibInterfaces Type Library · IDecoder Interface : Caps Property*

### Description

The capabilities of the decoder.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Caps As DecoderCaps
```


---

## DecoderAvailable Property

*Quelle: `Polytec_IO_VibInterfaces~IDecoder~DecoderAvailable.html` · Polytec IO VibInterfaces Type Library · IDecoder Interface : DecoderAvailable Property*

### Description

Returns whether the decoder is currently available.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property DecoderAvailable As Boolean
```

### Return Type

True if the decoder is currently available.

### Remarks

On VFX-F-110 front-ends the acceleration decoder may be only available for specific bandwidths.


---

## DecoderInfo Property

*Quelle: `Polytec_IO_VibInterfaces~IDecoder~DecoderInfo.html` · Polytec IO VibInterfaces Type Library · IDecoder Interface : DecoderInfo Property*

### Description

The information about the decoder.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property DecoderInfo As DecoderInfo
```


---

## DecoderQuantityType Property

*Quelle: `Polytec_IO_VibInterfaces~IDecoder~DecoderQuantityType.html` · Polytec IO VibInterfaces Type Library · IDecoder Interface : DecoderQuantityType Property*

### Description

The type of the quantity where this decoder belongs to.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property DecoderQuantityType As QuantityType
```


---

## Impedance Property

*Quelle: `Polytec_IO_VibInterfaces~IDecoder~Impedance.html` · Polytec IO VibInterfaces Type Library · IDecoder Interface : Impedance Property*

### Description

The impedance of the decoder.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Impedance As ImpedanceType
```


---

## MaxAcceleration Property

*Quelle: `Polytec_IO_VibInterfaces~IDecoder~MaxAcceleration.html` · Polytec IO VibInterfaces Type Library · IDecoder Interface : MaxAcceleration Property*

### Description

The current maximum acceleration of the decoder.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property MaxAcceleration As String
```

### Return Type

The current maximum acceleration.


---

## MaxVelocityRanges Property

*Quelle: `Polytec_IO_VibInterfaces~IDecoder~MaxVelocityRanges.html` · Polytec IO VibInterfaces Type Library · IDecoder Interface : MaxVelocityRanges Property*

### Description

The maximum velocity ranges of the decoder.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property MaxVelocityRanges As IMaxVelocityRangeCollection
```

### Return Type

The collection of the maximum velocity ranges.


---

## MeasurementMode Property

*Quelle: `Polytec_IO_VibInterfaces~IDecoder~MeasurementMode.html` · Polytec IO VibInterfaces Type Library · IDecoder Interface : MeasurementMode Property*

### Description

The measurement mode of the decoder.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property MeasurementMode As DecoderMeasurementMode
```

### Example


---

## Name Property

*Quelle: `Polytec_IO_VibInterfaces~IDecoder~Name.html` · Polytec IO VibInterfaces Type Library · IDecoder Interface : Name Property*

### Description

The name of the decoder.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Name As String
```

### Remarks

The name can be used as a parameter to the Contains method and the Item property.


---

## OptimumRange Property

*Quelle: `Polytec_IO_VibInterfaces~IDecoder~OptimumRange.html` · Polytec IO VibInterfaces Type Library · IDecoder Interface : OptimumRange Property*

### Description

Gets the optimum range of the decoder for the currently active bandwidth.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property OptimumRange As String
```

### Return Type

The optimum range.

### Remarks

The decoder must have the DecoderCaps_OptimumRange caps.


---

## OutputMode Property

*Quelle: `Polytec_IO_VibInterfaces~IDecoder~OutputMode.html` · Polytec IO VibInterfaces Type Library · IDecoder Interface : OutputMode Property*

### Description

The output mode of the decoder.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property OutputMode As DecoderOutputMode
```

### Example


---

## Ranges Property

*Quelle: `Polytec_IO_VibInterfaces~IDecoder~Ranges.html` · Polytec IO VibInterfaces Type Library · IDecoder Interface : Ranges Property*

### Description

The ranges of the decoder.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Ranges As IDecoderRangeCollection
```
