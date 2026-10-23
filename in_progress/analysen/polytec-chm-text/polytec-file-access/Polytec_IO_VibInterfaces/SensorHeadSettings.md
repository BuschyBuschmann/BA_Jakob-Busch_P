# Polytec_IO_VibInterfaces – SensorHeadSettings

## SensorHeadSettings Object

*Quelle: `Polytec_IO_VibInterfaces~SensorHeadSettings.html` · Polytec IO VibInterfaces Type Library*

### Description

The settings of the sensor head.

### Object Model

### Example

PSV/VibSoft support up to two groups of Vibrometer controllers attached to the system. For a 3D system the first group contains three Vibrometers. Below the dimmer setting of the first sensor head of the first controller of the first Vibrometer group is printed. Please note that the VibrometersAcqPropertiesContainer Collection uses 1-based indices, the SensorHeadSettingsCollection Collection uses 0-based indices.

- Access the sensor head settings stored in a file (VB.NET)

```
Dim oVibrometerAcqProperties As VibrometerAcqProperties
oVibrometerAcqProperties = oFile.Infos.AcquisitionInfoModes.ActiveProperties.VibrometersProperties(1)
Dim oSensorHeadSettings As SensorHeadSettings
oSensorHeadSettings = oVibrometerAcqProperties.VibControllerSettings.SensorHeadSettingsCollection(0)
Debug.Print oSensorHeadSettings.Dimmer
```


---

## SensorHeadSettings Object Members

*Quelle: `Polytec_IO_VibInterfaces~SensorHeadSettings_members.html` · Polytec IO VibInterfaces Type Library*

### Public Methods

| Clone | Creates and returns a copy of the settings object. |
|---|---|
| Copy | Copies all properties of the given settings object to this object. |

### Public Properties

| Dimmer | The dimmer value of the sensor head. |
|---|---|
| IlluminationIntensity | The illumination intensity. |
| IlluminationState | The illumination state. |
| Key | The identifier of the sensor head. |
| Name | The name of the sensor head. |
| SensorHeadInfo | The information about the sensor head. |
| VideoCameraSettings | The settings of the video camera. |

### Events

| OnCOMPropertyChanged | The event is fired when a property of the sensor head settings has changed. |
|---|---|


---

## Clone Method

*Quelle: `Polytec_IO_VibInterfaces~SensorHeadSettings~Clone.html` · Polytec IO VibInterfaces Type Library · SensorHeadSettings Object : Clone Method*

### Description

Creates and returns a copy of the settings object.

### Syntax

*Visual Basic:*
```
Public Function Clone() As Variant
```


---

## Copy Method

*Quelle: `Polytec_IO_VibInterfaces~SensorHeadSettings~Copy.html` · Polytec IO VibInterfaces Type Library · SensorHeadSettings Object : Copy Method*

### Description

Copies all properties of the given settings object to this object.

### Syntax

*Visual Basic:*
```
Public Sub Copy( _
   ByVal SensorHeadSettings As SensorHeadSettings _
)
```

### Parameters

SensorHeadSettings

The settings object to copy the properties from.


---

## Dimmer Property

*Quelle: `Polytec_IO_VibInterfaces~SensorHeadSettings~Dimmer.html` · Polytec IO VibInterfaces Type Library · SensorHeadSettings Object : Dimmer Property*

### Description

The dimmer value of the sensor head.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Dimmer As Long
```


---

## IlluminationIntensity Property

*Quelle: `Polytec_IO_VibInterfaces~SensorHeadSettings~IlluminationIntensity.html` · Polytec IO VibInterfaces Type Library · SensorHeadSettings Object : IlluminationIntensity Property*

### Description

The illumination intensity.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property IlluminationIntensity As Long
```


---

## IlluminationState Property

*Quelle: `Polytec_IO_VibInterfaces~SensorHeadSettings~IlluminationState.html` · Polytec IO VibInterfaces Type Library · SensorHeadSettings Object : IlluminationState Property*

### Description

The illumination state.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property IlluminationState As IlluminationStateType
```


---

## Key Property

*Quelle: `Polytec_IO_VibInterfaces~SensorHeadSettings~Key.html` · Polytec IO VibInterfaces Type Library · SensorHeadSettings Object : Key Property*

### Description

The identifier of the sensor head.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Key As SensorHeadIdentifier
```


---

## Name Property

*Quelle: `Polytec_IO_VibInterfaces~SensorHeadSettings~Name.html` · Polytec IO VibInterfaces Type Library · SensorHeadSettings Object : Name Property*

### Description

The name of the sensor head.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Name As String
```


---

## SensorHeadInfo Property

*Quelle: `Polytec_IO_VibInterfaces~SensorHeadSettings~SensorHeadInfo.html` · Polytec IO VibInterfaces Type Library · SensorHeadSettings Object : SensorHeadInfo Property*

### Description

The information about the sensor head.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property SensorHeadInfo As SensorHeadInfo
```


---

## VideoCameraSettings Property

*Quelle: `Polytec_IO_VibInterfaces~SensorHeadSettings~VideoCameraSettings.html` · Polytec IO VibInterfaces Type Library · SensorHeadSettings Object : VideoCameraSettings Property*

### Description

The settings of the video camera.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property VideoCameraSettings As VideoCameraSettings
```

### Remarks

The property returns Nothing, if no video camera is present.


---

## OnCOMPropertyChanged Event

*Quelle: `Polytec_IO_VibInterfaces~SensorHeadSettings~OnCOMPropertyChanged_EV.html` · Polytec IO VibInterfaces Type Library · SensorHeadSettings Object : OnCOMPropertyChanged Event*

### Description

The event is fired when a property of the sensor head settings has changed.

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
