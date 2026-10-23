# PSV – ChannelAcqProperties

## ChannelAcqProperties Object

*Quelle: `PSV~ChannelAcqProperties.html` · Polytec PSV Type Library*

### Description

Channel acquisition properties. Item of the ChannelsAcqProperties collection.

### Object Model


---

## ChannelAcqProperties Object Members

*Quelle: `PSV~ChannelAcqProperties_members.html` · Polytec PSV Type Library*

### Public Properties

| Active | Specifies whether the channel is active. True, if channel is active. |
|---|---|
| Calibration | The calibration factor in SI units. |
| DifferentialInput | Specifies whether the channel expects differential input. |
| DigitalFilter | The digital filter that is applied to the input signal of this channel. |
| DirectionOfVibration | Specifies the direction of vibration of this channel. |
| EncoderConnectionType | The encoder connection type. |
| EncoderGearRatio | The factor that describes the gear ratio of the encoder. |
| EncoderOperationMode | The operating mode of the encoder. |
| EncoderPowerSupply | The power supply of the encoder. |
| EncoderPulsesPerRotation | The pulses per revolution of the encoder. |
| ICPInput | Specifies whether the channel is set to be connected with an ICP device. |
| InputCoupling | The input coupling of the channel. |
| InputImpedance | Specifies the input impedance of the channel in Ohm. |
| InputRange | The input range in volt. |
| IntDiffPhysicalQuantity | The physical quantity which the integration / differentiation digital filter calculates from the original physical quantity of the channel (see property Quantity ). |
| Name | The descriptor of the channel. |
| Quantity | The physical quantity of the channel. |
| Reference | Specifies whether the channel is selected as references. True, if the channel is a reference. |
| ReferencePointIndex | Specifies the one-based scan point index of the reference point. |
| SEActive | Specifies, whether signal enhancement (SE) is active for the channel. True, if SE is active. |
| ShortName | The abbreviated descriptor of the channel. |
| SignalDelay | The signal delay of the channel in second. |
| Type | The signal type of the channel. |
| Unit | The unit of the channel's physical quantity. |
| VibrometerIndex | The index of the vibrometer connected to this channel. |
| WindowFunction | The window function of the channel. |
| WindowFunctionParams | The parameters of the window function. |
| WindowFunctionRMSCorrection | The RMS correction factor of the window function. |


---

## Active Property

*Quelle: `PSV~ChannelAcqProperties~Active.html` · Polytec PSV Type Library · ChannelAcqProperties Object : Active Property*

### Description

Specifies whether the channel is active. True, if channel is active.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Active As Boolean
```


---

## Calibration Property

*Quelle: `PSV~ChannelAcqProperties~Calibration.html` · Polytec PSV Type Library · ChannelAcqProperties Object : Calibration Property*

### Description

The calibration factor in SI units.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Calibration As Double
```


---

## DifferentialInput Property

*Quelle: `PSV~ChannelAcqProperties~DifferentialInput.html` · Polytec PSV Type Library · ChannelAcqProperties Object : DifferentialInput Property*

### Description

Specifies whether the channel expects differential input.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property DifferentialInput As Boolean
```


---

## DigitalFilter Property

*Quelle: `PSV~ChannelAcqProperties~DigitalFilter.html` · Polytec PSV Type Library · ChannelAcqProperties Object : DigitalFilter Property*

### Description

The digital filter that is applied to the input signal of this channel.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property DigitalFilter As IDigitalFilter
```

### Remarks

The DigitalFilter property returns / accepts objects of type DigitalFilterLowpass, DigitalFilterHighpass, DigitalFilterBandpass, DigitalFilterNotch or DigitalFilterNone. DigitalFilter returns DigitalFilterNone if no digital filter is specified for this channel. To remove any digital filter for this channel set this property to an instance of the object DigitalFilterNone.


---

## DirectionOfVibration Property

*Quelle: `PSV~ChannelAcqProperties~DirectionOfVibration.html` · Polytec PSV Type Library · ChannelAcqProperties Object : DirectionOfVibration Property*

### Description

Specifies the direction of vibration of this channel.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property DirectionOfVibration As PTCVibrationDirection
```


---

## EncoderConnectionType Property

*Quelle: `PSV~ChannelAcqProperties~EncoderConnectionType.html` · Polytec PSV Type Library · ChannelAcqProperties Object : EncoderConnectionType Property*

### Description

The encoder connection type.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property EncoderConnectionType As PTCEncoderConnectionType
```

### Remarks

Select the connection type for signal transmission: Single Ended: To use the rotary encoder, connect only one cable for the signal (A/A+, B/B+, N/N+) and the reference potential. The inverted signals are ignored. Differential: To use the rotary encoder with cable lengths > 5 m, pulse frequncies > 1 MHz, or in an environment subject to interference, connect both signals (A/A+ and A, B/B+ and B, N/N+ and N)


---

## EncoderGearRatio Property

*Quelle: `PSV~ChannelAcqProperties~EncoderGearRatio.html` · Polytec PSV Type Library · ChannelAcqProperties Object : EncoderGearRatio Property*

### Description

The factor that describes the gear ratio of the encoder.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property EncoderGearRatio As Double
```


---

## EncoderOperationMode Property

*Quelle: `PSV~ChannelAcqProperties~EncoderOperationMode.html` · Polytec PSV Type Library · ChannelAcqProperties Object : EncoderOperationMode Property*

### Description

The operating mode of the encoder.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property EncoderOperationMode As PTCEncoderOperationMode
```

### Remarks

Quadrature (A/B): You connect both signals and can use signed RPM signals (minus = counter-clockwise). Single Channel (A): You connect only signal A and can use only positive RPM signals.


---

## EncoderPowerSupply Property

*Quelle: `PSV~ChannelAcqProperties~EncoderPowerSupply.html` · Polytec PSV Type Library · ChannelAcqProperties Object : EncoderPowerSupply Property*

### Description

The power supply of the encoder.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property EncoderPowerSupply As PTCEncoderPowerSupply
```

### Remarks

If you wish to power the rotary encoder, select the appropriate supply voltage (5V/12 V).


---

## EncoderPulsesPerRotation Property

*Quelle: `PSV~ChannelAcqProperties~EncoderPulsesPerRotation.html` · Polytec PSV Type Library · ChannelAcqProperties Object : EncoderPulsesPerRotation Property*

### Description

The pulses per revolution of the encoder.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property EncoderPulsesPerRotation As Long
```

### Remarks

Specify the number of electrical signals the rotary encoder generates during a complete 360-degree rotation.


---

## ICPInput Property

*Quelle: `PSV~ChannelAcqProperties~ICPInput.html` · Polytec PSV Type Library · ChannelAcqProperties Object : ICPInput Property*

### Description

Specifies whether the channel is set to be connected with an ICP device.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property ICPInput As Boolean
```


---

## InputCoupling Property

*Quelle: `PSV~ChannelAcqProperties~InputCoupling.html` · Polytec PSV Type Library · ChannelAcqProperties Object : InputCoupling Property*

### Description

The input coupling of the channel.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property InputCoupling As PTCInputCoupling
```


---

## InputImpedance Property

*Quelle: `PSV~ChannelAcqProperties~InputImpedance.html` · Polytec PSV Type Library · ChannelAcqProperties Object : InputImpedance Property*

### Description

Specifies the input impedance of the channel in Ohm.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property InputImpedance As Double
```


---

## InputRange Property

*Quelle: `PSV~ChannelAcqProperties~InputRange.html` · Polytec PSV Type Library · ChannelAcqProperties Object : InputRange Property*

### Description

The input range in volt.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property InputRange As Double
```


---

## IntDiffPhysicalQuantity Property

*Quelle: `PSV~ChannelAcqProperties~IntDiffPhysicalQuantity.html` · Polytec PSV Type Library · ChannelAcqProperties Object : IntDiffPhysicalQuantity Property*

### Description

The physical quantity which the integration / differentiation digital filter calculates from the original physical quantity of the channel (see property Quantity).

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property IntDiffPhysicalQuantity As PTCPhysicalQuantity
```

### Remarks

If IntDiffPhysicalQuantity is equal to Quantity no integration / differentiation takes place.


---

## Name Property

*Quelle: `PSV~ChannelAcqProperties~Name.html` · Polytec PSV Type Library · ChannelAcqProperties Object : Name Property*

### Description

The descriptor of the channel.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Name As String
```


---

## Quantity Property

*Quelle: `PSV~ChannelAcqProperties~Quantity.html` · Polytec PSV Type Library · ChannelAcqProperties Object : Quantity Property*

### Description

The physical quantity of the channel.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Quantity As PTCPhysicalQuantity
```


---

## Reference Property

*Quelle: `PSV~ChannelAcqProperties~Reference.html` · Polytec PSV Type Library · ChannelAcqProperties Object : Reference Property*

### Description

Specifies whether the channel is selected as references. True, if the channel is a reference.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Reference As Boolean
```


---

## ReferencePointIndex Property

*Quelle: `PSV~ChannelAcqProperties~ReferencePointIndex.html` · Polytec PSV Type Library · ChannelAcqProperties Object : ReferencePointIndex Property*

### Description

Specifies the one-based scan point index of the reference point.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property ReferencePointIndex As Long
```

### Remarks

This reference point index will be used during export to the universal file and ME'Scope file format when exporting FRF or cross power signals.


---

## SEActive Property

*Quelle: `PSV~ChannelAcqProperties~SEActive.html` · Polytec PSV Type Library · ChannelAcqProperties Object : SEActive Property*

### Description

Specifies, whether signal enhancement (SE) is active for the channel. True, if SE is active.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property SEActive As Boolean
```


---

## ShortName Property

*Quelle: `PSV~ChannelAcqProperties~ShortName.html` · Polytec PSV Type Library · ChannelAcqProperties Object : ShortName Property*

### Description

The abbreviated descriptor of the channel.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property ShortName As String
```

### Remarks

This name should not exceed 4 characters.


---

## SignalDelay Property

*Quelle: `PSV~ChannelAcqProperties~SignalDelay.html` · Polytec PSV Type Library · ChannelAcqProperties Object : SignalDelay Property*

### Description

The signal delay of the channel in second.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property SignalDelay As Double
```

### Remarks

The signal delay is used to compensate phase differences between vibrometer channels and reference channels when calculating the FFT. The signal delay is different from zero for channels connected to vibrometer controllers, that provide the signal delay for the active decoder range.

On PSV-500-H, PSV-500-3D-H and PSV-500-B systems, the reference channels have a signal delay value, too. The signal delay of all channels on PSV-500-H, PSV-500-3D-H and PSV-500-B systems is compensated (with a precision of a sample) in time domain, the rest of the compensation is performed when calculating the FFT.


---

## Type Property

*Quelle: `PSV~ChannelAcqProperties~Type.html` · Polytec PSV Type Library · ChannelAcqProperties Object : Type Property*

### Description

The signal type of the channel.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Type As PTCChannelType
```


---

## Unit Property

*Quelle: `PSV~ChannelAcqProperties~Unit.html` · Polytec PSV Type Library · ChannelAcqProperties Object : Unit Property*

### Description

The unit of the channel's physical quantity.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Unit As String
```


---

## VibrometerIndex Property

*Quelle: `PSV~ChannelAcqProperties~VibrometerIndex.html` · Polytec PSV Type Library · ChannelAcqProperties Object : VibrometerIndex Property*

### Description

The index of the vibrometer connected to this channel.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property VibrometerIndex As Long
```

### Return Type

One-based index of the connected vibrometer.

### Remarks

If the channel is not connected to a vibrometer 0 is returned. You can use the index as an index to the VibrometersAcqPropertiesContainer collection to find out the current settings of the vibrometer controller.


---

## WindowFunction Property

*Quelle: `PSV~ChannelAcqProperties~WindowFunction.html` · Polytec PSV Type Library · ChannelAcqProperties Object : WindowFunction Property*

### Description

The window function of the channel.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property WindowFunction As PTCWindowFunction
```

### Remarks

The window function applies only for FFT, Zoom-FFT or MultiFrame measurements.


---

## WindowFunctionParams Property

*Quelle: `PSV~ChannelAcqProperties~WindowFunctionParams.html` · Polytec PSV Type Library · ChannelAcqProperties Object : WindowFunctionParams Property*

### Description

The parameters of the window function.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property WindowFunctionParams As Double()
```


---

## WindowFunctionRMSCorrection Property

*Quelle: `PSV~ChannelAcqProperties~WindowFunctionRMSCorrection.html` · Polytec PSV Type Library · ChannelAcqProperties Object : WindowFunctionRMSCorrection Property*

### Description

The RMS correction factor of the window function.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property WindowFunctionRMSCorrection As Double
```
