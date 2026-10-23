# Polytec_IO_VibInterfaces – IDecoderRange

## IDecoderRange Interface

*Quelle: `Polytec_IO_VibInterfaces~IDecoderRange.html` · Polytec IO VibInterfaces Type Library*

### Description

The range of a decoder. Item of the IDecoderRangeCollection.

### Object Model


---

## IDecoderRange Interface Members

*Quelle: `Polytec_IO_VibInterfaces~IDecoderRange_members.html` · Polytec IO VibInterfaces Type Library*

### Public Properties

| AnalogCalibrationFactor | The analog calibration factor per Volt in , e.g. m/s/V. |
|---|---|
| CalibrationFactor | The calibration factor of the range. |
| Decoder | The decoder of the range. |
| FrequencyLimit | The upper frequency limit of the range in Hz. |
| FringeCounterBit | The fringe counter bit of the range. |
| FringeCounterResolution | The fringe counter resolution of the range in m. |
| Name | The name of the range of the decoder. |
| Resolution | The resolution of the decoder in SI units. |
| SignalDelay | The signal delay of the decoder range in s. |


---

## AnalogCalibrationFactor Property

*Quelle: `Polytec_IO_VibInterfaces~IDecoderRange~AnalogCalibrationFactor.html` · Polytec IO VibInterfaces Type Library · IDecoderRange Interface : AnalogCalibrationFactor Property*

### Description

The analog calibration factor per Volt in , e.g. m/s/V.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property AnalogCalibrationFactor As Double
```


---

## CalibrationFactor Property

*Quelle: `Polytec_IO_VibInterfaces~IDecoderRange~CalibrationFactor.html` · Polytec IO VibInterfaces Type Library · IDecoderRange Interface : CalibrationFactor Property*

### Description

The calibration factor of the range.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property CalibrationFactor As Double
```

### Remarks

The unit of the calibration factor depends on the quantity of the decoder. For a velocity decoder the calibration factor is in m/s / V.


---

## Decoder Property

*Quelle: `Polytec_IO_VibInterfaces~IDecoderRange~Decoder.html` · Polytec IO VibInterfaces Type Library · IDecoderRange Interface : Decoder Property*

### Description

The decoder of the range.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Decoder As IDecoder
```


---

## FrequencyLimit Property

*Quelle: `Polytec_IO_VibInterfaces~IDecoderRange~FrequencyLimit.html` · Polytec IO VibInterfaces Type Library · IDecoderRange Interface : FrequencyLimit Property*

### Description

The upper frequency limit of the range in Hz.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property FrequencyLimit As Double
```


---

## FringeCounterBit Property

*Quelle: `Polytec_IO_VibInterfaces~IDecoderRange~FringeCounterBit.html` · Polytec IO VibInterfaces Type Library · IDecoderRange Interface : FringeCounterBit Property*

### Description

The fringe counter bit of the range.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property FringeCounterBit As Long
```


---

## FringeCounterResolution Property

*Quelle: `Polytec_IO_VibInterfaces~IDecoderRange~FringeCounterResolution.html` · Polytec IO VibInterfaces Type Library · IDecoderRange Interface : FringeCounterResolution Property*

### Description

The fringe counter resolution of the range in m.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property FringeCounterResolution As Double
```


---

## Name Property

*Quelle: `Polytec_IO_VibInterfaces~IDecoderRange~Name.html` · Polytec IO VibInterfaces Type Library · IDecoderRange Interface : Name Property*

### Description

The name of the range of the decoder.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Name As String
```


---

## Resolution Property

*Quelle: `Polytec_IO_VibInterfaces~IDecoderRange~Resolution.html` · Polytec IO VibInterfaces Type Library · IDecoderRange Interface : Resolution Property*

### Description

The resolution of the decoder in SI units.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Resolution As Double
```

### Remarks

The unit of the resolution depends on the quantity of the decoder. For a displacement decoder the resolution is in m.


---

## SignalDelay Property

*Quelle: `Polytec_IO_VibInterfaces~IDecoderRange~SignalDelay.html` · Polytec IO VibInterfaces Type Library · IDecoderRange Interface : SignalDelay Property*

### Description

The signal delay of the decoder range in s.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property SignalDelay As Double
```
