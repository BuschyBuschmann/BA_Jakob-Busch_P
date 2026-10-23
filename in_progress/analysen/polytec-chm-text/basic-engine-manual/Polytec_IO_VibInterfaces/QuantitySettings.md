# Polytec_IO_VibInterfaces – QuantitySettings

## QuantitySettings Object

*Quelle: `Polytec_IO_VibInterfaces~QuantitySettings.html` · Polytec IO VibInterfaces Type Library*

### Description

The settings for a quantity. Item of the QuantitySettingsCollection.

### Object Model


---

## QuantitySettings Object Members

*Quelle: `Polytec_IO_VibInterfaces~QuantitySettings_members.html` · Polytec IO VibInterfaces Type Library*

### Public Methods

| Clone | Creates and returns a copy of the settings object. |
|---|---|

### Public Properties

| BandwidthRange | The name of the active decoder bandwidth range of the quantity. |
|---|---|
| DecoderInfo | The information about the decoder of the quantity. |
| Key | The type of the quantity. |
| MaxVelocityRange | The maximum velocity range. |
| Name | The name of the quantity. |
| OutputActive | A flag that specifies whether the output of the corresponding quantity is active or not. |
| Overrun | The overrun mode. |
| Range | The name of the active decoder range of the quantity. |
| VibAnalogOutput |  |

### Events

| OnCOMPropertyChanged | The event is fired when the Range property or BandwidthRange property has changed. |
|---|---|


---

## Clone Method

*Quelle: `Polytec_IO_VibInterfaces~QuantitySettings~Clone.html` · Polytec IO VibInterfaces Type Library · QuantitySettings Object : Clone Method*

### Description

Creates and returns a copy of the settings object.

### Syntax

*Visual Basic:*
```
Public Function Clone() As Variant
```


---

## BandwidthRange Property

*Quelle: `Polytec_IO_VibInterfaces~QuantitySettings~BandwidthRange.html` · Polytec IO VibInterfaces Type Library · QuantitySettings Object : BandwidthRange Property*

### Description

The name of the active decoder bandwidth range of the quantity.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property BandwidthRange As String
```


---

## DecoderInfo Property

*Quelle: `Polytec_IO_VibInterfaces~QuantitySettings~DecoderInfo.html` · Polytec IO VibInterfaces Type Library · QuantitySettings Object : DecoderInfo Property*

### Description

The information about the decoder of the quantity.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property DecoderInfo As DecoderInfo
```


---

## Key Property

*Quelle: `Polytec_IO_VibInterfaces~QuantitySettings~Key.html` · Polytec IO VibInterfaces Type Library · QuantitySettings Object : Key Property*

### Description

The type of the quantity.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Key As QuantityType
```

### Remarks

The quantity type can be used as a parameter to the ByKey method and Contains method.


---

## MaxVelocityRange Property

*Quelle: `Polytec_IO_VibInterfaces~QuantitySettings~MaxVelocityRange.html` · Polytec IO VibInterfaces Type Library · QuantitySettings Object : MaxVelocityRange Property*

### Description

The maximum velocity range.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property MaxVelocityRange As String
```


---

## Name Property

*Quelle: `Polytec_IO_VibInterfaces~QuantitySettings~Name.html` · Polytec IO VibInterfaces Type Library · QuantitySettings Object : Name Property*

### Description

The name of the quantity.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Name As String
```

### Remarks

The name of the quantity can be used as a parameter to the Contains method and Item property.


---

## OutputActive Property

*Quelle: `Polytec_IO_VibInterfaces~QuantitySettings~OutputActive.html` · Polytec IO VibInterfaces Type Library · QuantitySettings Object : OutputActive Property*

### Description

A flag that specifies whether the output of the corresponding quantity is active or not.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property OutputActive As Boolean
```

### Return Type

If true, the output is active.

### Remarks

Note that the hardware might not be able to switch the output off if you set this property to false.


---

## Overrun Property

*Quelle: `Polytec_IO_VibInterfaces~QuantitySettings~Overrun.html` · Polytec IO VibInterfaces Type Library · QuantitySettings Object : Overrun Property*

### Description

The overrun mode.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Overrun As String
```


---

## Range Property

*Quelle: `Polytec_IO_VibInterfaces~QuantitySettings~Range.html` · Polytec IO VibInterfaces Type Library · QuantitySettings Object : Range Property*

### Description

The name of the active decoder range of the quantity.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Range As String
```


---

## VibAnalogOutput Property

*Quelle: `Polytec_IO_VibInterfaces~QuantitySettings~VibAnalogOutput.html` · Polytec IO VibInterfaces Type Library · QuantitySettings Object : VibAnalogOutput Property*

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property VibAnalogOutput As QuantityType
```


---

## OnCOMPropertyChanged Event

*Quelle: `Polytec_IO_VibInterfaces~QuantitySettings~OnCOMPropertyChanged_EV.html` · Polytec IO VibInterfaces Type Library · QuantitySettings Object : OnCOMPropertyChanged Event*

### Description

The event is fired when the Range property or BandwidthRange property has changed.

### Syntax

*Visual Basic:*
```
Public Event OnCOMPropertyChanged( _
   ByVal property As VibrometerProperty _
)
```

### Parameters

property

| Value | Description |
|---|---|
| VibrometerProperty_AutoFocusInProgress | The AutoFocusInProgress property. |
| VibrometerProperty_BandwidthRange | The BandwidthRange property. |
| VibrometerProperty_BandwidthRanges | The BandwidthRanges property. |
| VibrometerProperty_ClockSync | The clock synchronization property. |
| VibrometerProperty_CoherenceOptimizerPower | The CoherenceOptimizerPower property. |
| VibrometerProperty_CoherenceOptimizerStatus | The CoherenceOptimizerStatus property. |
| VibrometerProperty_DecoderAvailable | The DecoderAvailable property. |
| VibrometerProperty_DecoderClearMode | The DecoderClearMode property. |
| VibrometerProperty_Dimmer | The Dimmer property. |
| VibrometerProperty_FocusInProgress | The FocusInProgress property. |
| VibrometerProperty_IlluminationIntensity | The IlluminationIntensity property. |
| VibrometerProperty_IlluminationState | The IlluminationState property. |
| VibrometerProperty_LaserOn | The LaserOn property. |
| VibrometerProperty_LaserTemperature | The LaserTemperature property. |
| VibrometerProperty_LaserTemperatureOutOfRange | The LaserTemperatureOutOfRange property. |
| VibrometerProperty_LaserWavelengthStabilizationState | The LaserWavelengthStabilizationState property. |
| VibrometerProperty_MaxAcceleration | The MaxAcceleration property. |
| VibrometerProperty_MaxVelocityRange | The MaxVelocityRange property. |
| VibrometerProperty_MaxVelocityRanges | The MaxVelocityRanges property. |
| VibrometerProperty_ObjectiveTemperature | The ObjectiveTemperature property. |
| VibrometerProperty_OptimumRange | The OptimumgRange property. |
| VibrometerProperty_OutputActive | The OutputActive property. |
| VibrometerProperty_Overrange | The Overrange property. |
| VibrometerProperty_Overrun | The Overrun property. |
| VibrometerProperty_OverrunModes | The OverrunModes property. |
| VibrometerProperty_Range | The Range property. |
| VibrometerProperty_Ranges | The Ranges property. |
| VibrometerProperty_Readout | The Readout property. |
| VibrometerProperty_SignalBalance | The SignalBalance property. |
| VibrometerProperty_SignalLevel | The SignalLevel property. |
| VibrometerProperty_Temperature | The Temperature property. |
| VibrometerProperty_TemperatureState | The TemperatureState property. |
| VibrometerProperty_VibAnalogOutput | The VibAnalogOutput property. |
The property that has changed.
