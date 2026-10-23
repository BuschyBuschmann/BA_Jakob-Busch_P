# Polytec_IO_VibInterfaces – ControllerSettings

## ControllerSettings Object

*Quelle: `Polytec_IO_VibInterfaces~ControllerSettings.html` · Polytec IO VibInterfaces Type Library*

### Description

The settings of the vibrometer controller.

### Object Model

### Example

To access the controller settings of a Vibrometer that was attached to the system during a measurement, you have to navigate to the VibrometersAcqPropertiesContainer Collection of the active AcquisitionPropertiesContainer Collection.

- Access controller settings stored in a file (VB.NET)

```
Dim oVibrometerAcqProperties As VibrometerAcqProperties
oVibrometerAcqProperties = oFile.Infos.AcquisitionInfoModes.ActiveProperties.VibrometersProperties(1)
Dim oControllerSettings As ControllerSettings
oControllerSettings = oVibrometerAcqProperties.VibControllerSettings
Debug.Print oControllerSettings.ControllerInfo.DeviceName
```


---

## ControllerSettings Object Members

*Quelle: `Polytec_IO_VibInterfaces~ControllerSettings_members.html` · Polytec IO VibInterfaces Type Library*

### Public Methods

| Clone | Creates and returns a copy of the settings object. |
|---|---|
| Copy | Copies all properties of the given settings object to this object. |
| Equals | Checks if the properties of the given settings object are equal to the properties of this object. |
| Load | Loads the state of this object and all of its children from the specified XML fragment. |
| Save | Returns an XML fragment representing the state of this object and all of its children. |

### Public Properties

| ControllerInfo | The information about the controller. |
|---|---|
| DecoderClearMode | The decoder clear mode. |
| FilterSettingsCollection | The settings of the filters. |
| QuantitySettingsCollection | The settings of the quantities. |
| SensorHeadSettingsCollection | The settings of the sensor heads. |

### Events

| OnCOMPropertyChanged | The event is fired when a property of the controller settings has changed. |
|---|---|


---

## Clone Method

*Quelle: `Polytec_IO_VibInterfaces~ControllerSettings~Clone.html` · Polytec IO VibInterfaces Type Library · ControllerSettings Object : Clone Method*

### Description

Creates and returns a copy of the settings object.

### Syntax

*Visual Basic:*
```
Public Function Clone() As Variant
```


---

## Copy Method

*Quelle: `Polytec_IO_VibInterfaces~ControllerSettings~Copy.html` · Polytec IO VibInterfaces Type Library · ControllerSettings Object : Copy Method*

### Description

Copies all properties of the given settings object to this object.

### Syntax

*Visual Basic:*
```
Public Sub Copy( _
   ByVal ControllerSettings As ControllerSettings _
)
```

### Parameters

ControllerSettings

The settings object to copy the properties from.


---

## Equals Method

*Quelle: `Polytec_IO_VibInterfaces~ControllerSettings~Equals.html` · Polytec IO VibInterfaces Type Library · ControllerSettings Object : Equals Method*

### Description

Checks if the properties of the given settings object are equal to the properties of this object.

### Syntax

*Visual Basic:*
```
Public Function Equals( _
   ByVal value As Variant _
) As Boolean
```

### Parameters

value

The other settings object to compare the properties with.

### Return Type

True, if all properties of both objects are the same.


---

## Load Method

*Quelle: `Polytec_IO_VibInterfaces~ControllerSettings~Load.html` · Polytec IO VibInterfaces Type Library · ControllerSettings Object : Load Method*

### Description

Loads the state of this object and all of its children from the specified XML fragment.

### Syntax

*Visual Basic:*
```
Public Sub Load( _
   ByVal content As String _
)
```

### Parameters

content

The XML fragment.

### Remarks

The format of the XML fragment is not documented. Use the Save Method to get an XML fragment for the current state of the object.


---

## Save Method

*Quelle: `Polytec_IO_VibInterfaces~ControllerSettings~Save.html` · Polytec IO VibInterfaces Type Library · ControllerSettings Object : Save Method*

### Description

Returns an XML fragment representing the state of this object and all of its children.

### Syntax

*Visual Basic:*
```
Public Function Save() As String
```

### Return Type

The XML fragment.

### Remarks

The format of the XML fragment is not documented. You can use the Load Method to restore the state of this object at a later time using the returned XML fragment.

### Example


---

## ControllerInfo Property

*Quelle: `Polytec_IO_VibInterfaces~ControllerSettings~ControllerInfo.html` · Polytec IO VibInterfaces Type Library · ControllerSettings Object : ControllerInfo Property*

### Description

The information about the controller.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property ControllerInfo As ControllerInfo
```


---

## DecoderClearMode Property

*Quelle: `Polytec_IO_VibInterfaces~ControllerSettings~DecoderClearMode.html` · Polytec IO VibInterfaces Type Library · ControllerSettings Object : DecoderClearMode Property*

### Description

The decoder clear mode.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property DecoderClearMode As String
```


---

## FilterSettingsCollection Property

*Quelle: `Polytec_IO_VibInterfaces~ControllerSettings~FilterSettingsCollection.html` · Polytec IO VibInterfaces Type Library · ControllerSettings Object : FilterSettingsCollection Property*

### Description

The settings of the filters.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property FilterSettingsCollection As FilterSettingsCollection
```


---

## QuantitySettingsCollection Property

*Quelle: `Polytec_IO_VibInterfaces~ControllerSettings~QuantitySettingsCollection.html` · Polytec IO VibInterfaces Type Library · ControllerSettings Object : QuantitySettingsCollection Property*

### Description

The settings of the quantities.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property QuantitySettingsCollection As QuantitySettingsCollection
```


---

## SensorHeadSettingsCollection Property

*Quelle: `Polytec_IO_VibInterfaces~ControllerSettings~SensorHeadSettingsCollection.html` · Polytec IO VibInterfaces Type Library · ControllerSettings Object : SensorHeadSettingsCollection Property*

### Description

The settings of the sensor heads.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property SensorHeadSettingsCollection As SensorHeadSettingsCollection
```


---

## OnCOMPropertyChanged Event

*Quelle: `Polytec_IO_VibInterfaces~ControllerSettings~OnCOMPropertyChanged_EV.html` · Polytec IO VibInterfaces Type Library · ControllerSettings Object : OnCOMPropertyChanged Event*

### Description

The event is fired when a property of the controller settings has changed.

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
