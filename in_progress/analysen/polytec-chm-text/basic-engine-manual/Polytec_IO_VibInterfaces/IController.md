# Polytec_IO_VibInterfaces – IController

## IController Interface

*Quelle: `Polytec_IO_VibInterfaces~IController.html` · Polytec IO VibInterfaces Type Library*

### Description

The vibrometer controller. Item of the IControllerCollection.

### Object Model


---

## IController Interface Members

*Quelle: `Polytec_IO_VibInterfaces~IController_members.html` · Polytec IO VibInterfaces Type Library*

### Public Methods

| Disconnect | Disconnects the controller from the hardware. |
|---|---|
| GetSelectedBandwidthRange | Returns the active decoder bandwidth range for the given quantity. |
| GetSelectedDecoderRange | Returns the active decoder range for the given quantity. |
| GetSelectedFilterRange | Returns the active filter range for the given filter type. |
| GetSelectedMaxVelocityRange | Returns the active maximum velocity range for the given quantity. |

### Public Properties

| ConnectionInfo | The information about the connection of the controller. |
|---|---|
| ControllerInfo | The information about the controller. |
| DecoderClearModes | The clear modes of the controller. |
| Decoders | The decoders of the controller. |
| DigitalDemodulation | The digital demodulation object of the controller. |
| Filters | The filters of the controller. |
| FrontEndIPAddress | Returns the IP address of the front end. |
| Group | The controller group the controller is a member of. |
| MeasurementMode | The measurement mode of the controller. |
| PowerUp | The power-up settings of the controller. |
| Quantities | The quantities of the controller. |
| Recorder | Returns the recorder object if the controller has a recorder mode, e.g. VGO-200. |
| SensorHeads | The sensor heads of the controller. |
| ServiceMode | The service mode object of the controller. |
| Settings | The settings of the controller. |
| SignalEnhancement | The signal enhancement of the controller. |


---

## Disconnect Method

*Quelle: `Polytec_IO_VibInterfaces~IController~Disconnect.html` · Polytec IO VibInterfaces Type Library · IController Interface : Disconnect Method*

### Description

Disconnects the controller from the hardware.

### Syntax

*Visual Basic:*
```
Public Sub Disconnect()
```


---

## GetSelectedBandwidthRange Method

*Quelle: `Polytec_IO_VibInterfaces~IController~GetSelectedBandwidthRange.html` · Polytec IO VibInterfaces Type Library · IController Interface : GetSelectedBandwidthRange Method*

### Description

Returns the active decoder bandwidth range for the given quantity.

### Syntax

*Visual Basic:*
```
Public Function GetSelectedBandwidthRange( _
   ByVal QuantityType As QuantityType _
) As IBandwidthRange
```

### Parameters

QuantityType

| Value | Description |
|---|---|
| QuantityType_Acceleration | Quantity acceleration. |
| QuantityType_Angle | Quantity angle. |
| QuantityType_AngleDegree | Quantity angle in degree. |
| QuantityType_AngularAcceleration | Quantity angular acceleration. |
| QuantityType_AngularAccelerationDegree | Quantity angular acceleration in degree. |
| QuantityType_AngularVelocity | Quantity angular velocity. |
| QuantityType_AngularVelocityDegree | Quantity angular velocity in degree. |
| QuantityType_Charge | Quantity charge. |
| QuantityType_Counts | Quantity counts. |
| QuantityType_Current | Quantity current. |
| QuantityType_Displacement | Quantity displacement. |
| QuantityType_Force | Quantity force. |
| QuantityType_Frequency | Quantity frequency. |
| QuantityType_GravitationalAcceleration | Quantity gravitational acceleration. |
| QuantityType_LuminousIntensity | Quantity luminous intensity. |
| QuantityType_Mass | Quantity mass. |
| QuantityType_None | No quantity. |
| QuantityType_Order | Quantity order. |
| QuantityType_Power | Quantity power. |
| QuantityType_Pressure | Quantity pressure. |
| QuantityType_Resistance | Quantity resistance. |
| QuantityType_Revolution | Quantity revolution. |
| QuantityType_Rpm | Quantity RPM. |
| QuantityType_SoundPressure | Quantity sound pressure. |
| QuantityType_Strain | Quantity strain. |
| QuantityType_Stress | Quantity stress. |
| QuantityType_Substance | Quantity substance. |
| QuantityType_Temperature | Quantity temperature. |
| QuantityType_Time | Quantity time. |
| QuantityType_Torque | Quantity torque. |
| QuantityType_User | Quantity user. |
| QuantityType_Velocity | Quantity velocity. |
| QuantityType_Voltage | Quantity voltage. |
| QuantityType_Volume | Quantity volume. |
| QuantityType_VolumeAcceleration | Quantity volume acceleration. |
| QuantityType_VolumeVelocity | Quantity volume velocity. |
| QuantityType_Work | Quantity work. |
The quantity to get the selected bandwidth range for.


---

## GetSelectedDecoderRange Method

*Quelle: `Polytec_IO_VibInterfaces~IController~GetSelectedDecoderRange.html` · Polytec IO VibInterfaces Type Library · IController Interface : GetSelectedDecoderRange Method*

### Description

Returns the active decoder range for the given quantity.

### Syntax

*Visual Basic:*
```
Public Function GetSelectedDecoderRange( _
   ByVal QuantityType As QuantityType _
) As IDecoderRange
```

### Parameters

QuantityType

| Value | Description |
|---|---|
| QuantityType_Acceleration | Quantity acceleration. |
| QuantityType_Angle | Quantity angle. |
| QuantityType_AngleDegree | Quantity angle in degree. |
| QuantityType_AngularAcceleration | Quantity angular acceleration. |
| QuantityType_AngularAccelerationDegree | Quantity angular acceleration in degree. |
| QuantityType_AngularVelocity | Quantity angular velocity. |
| QuantityType_AngularVelocityDegree | Quantity angular velocity in degree. |
| QuantityType_Charge | Quantity charge. |
| QuantityType_Counts | Quantity counts. |
| QuantityType_Current | Quantity current. |
| QuantityType_Displacement | Quantity displacement. |
| QuantityType_Force | Quantity force. |
| QuantityType_Frequency | Quantity frequency. |
| QuantityType_GravitationalAcceleration | Quantity gravitational acceleration. |
| QuantityType_LuminousIntensity | Quantity luminous intensity. |
| QuantityType_Mass | Quantity mass. |
| QuantityType_None | No quantity. |
| QuantityType_Order | Quantity order. |
| QuantityType_Power | Quantity power. |
| QuantityType_Pressure | Quantity pressure. |
| QuantityType_Resistance | Quantity resistance. |
| QuantityType_Revolution | Quantity revolution. |
| QuantityType_Rpm | Quantity RPM. |
| QuantityType_SoundPressure | Quantity sound pressure. |
| QuantityType_Strain | Quantity strain. |
| QuantityType_Stress | Quantity stress. |
| QuantityType_Substance | Quantity substance. |
| QuantityType_Temperature | Quantity temperature. |
| QuantityType_Time | Quantity time. |
| QuantityType_Torque | Quantity torque. |
| QuantityType_User | Quantity user. |
| QuantityType_Velocity | Quantity velocity. |
| QuantityType_Voltage | Quantity voltage. |
| QuantityType_Volume | Quantity volume. |
| QuantityType_VolumeAcceleration | Quantity volume acceleration. |
| QuantityType_VolumeVelocity | Quantity volume velocity. |
| QuantityType_Work | Quantity work. |
The type of the quantity.


---

## GetSelectedFilterRange Method

*Quelle: `Polytec_IO_VibInterfaces~IController~GetSelectedFilterRange.html` · Polytec IO VibInterfaces Type Library · IController Interface : GetSelectedFilterRange Method*

### Description

Returns the active filter range for the given filter type.

### Syntax

*Visual Basic:*
```
Public Function GetSelectedFilterRange( _
   ByVal FilterType As FilterType _
) As IBaseFilterRange
```

### Parameters

FilterType

| Value | Description |
|---|---|
| FilterType_AccelerationAse | The ASE filter for acceleration. |
| FilterType_AccelerationHighPass | The acceleration high pass filter. |
| FilterType_AccelerationLowPass | The acceleration low pass filter. |
| FilterType_Adaptive | The adaptive filter. |
| FilterType_Ase | The ASE filter, e.g. for a IVS-500 system. |
| FilterType_DCResponse | The DC response filter. |
| FilterType_DisplacementAse | The ASE filter for displacement. |
| FilterType_DisplacementHighPass | The displacement high pass filter. |
| FilterType_DisplacementLowPass | The displacement low pass filter. |
| FilterType_HighPass | The high pass filter. |
| FilterType_LowPass | The low pass filter. |
| FilterType_Rotation | The rotation filter. |
| FilterType_RpmResponse | The RPM response filter. |
| FilterType_Tracking | The tracking filter. |
| FilterType_Translation | The translation filter. |
The filter type.


---

## GetSelectedMaxVelocityRange Method

*Quelle: `Polytec_IO_VibInterfaces~IController~GetSelectedMaxVelocityRange.html` · Polytec IO VibInterfaces Type Library · IController Interface : GetSelectedMaxVelocityRange Method*

### Description

Returns the active maximum velocity range for the given quantity.

### Syntax

*Visual Basic:*
```
Public Function GetSelectedMaxVelocityRange( _
   ByVal QuantityType As QuantityType _
) As IMaxVelocityRange
```

### Parameters

QuantityType

| Value | Description |
|---|---|
| QuantityType_Acceleration | Quantity acceleration. |
| QuantityType_Angle | Quantity angle. |
| QuantityType_AngleDegree | Quantity angle in degree. |
| QuantityType_AngularAcceleration | Quantity angular acceleration. |
| QuantityType_AngularAccelerationDegree | Quantity angular acceleration in degree. |
| QuantityType_AngularVelocity | Quantity angular velocity. |
| QuantityType_AngularVelocityDegree | Quantity angular velocity in degree. |
| QuantityType_Charge | Quantity charge. |
| QuantityType_Counts | Quantity counts. |
| QuantityType_Current | Quantity current. |
| QuantityType_Displacement | Quantity displacement. |
| QuantityType_Force | Quantity force. |
| QuantityType_Frequency | Quantity frequency. |
| QuantityType_GravitationalAcceleration | Quantity gravitational acceleration. |
| QuantityType_LuminousIntensity | Quantity luminous intensity. |
| QuantityType_Mass | Quantity mass. |
| QuantityType_None | No quantity. |
| QuantityType_Order | Quantity order. |
| QuantityType_Power | Quantity power. |
| QuantityType_Pressure | Quantity pressure. |
| QuantityType_Resistance | Quantity resistance. |
| QuantityType_Revolution | Quantity revolution. |
| QuantityType_Rpm | Quantity RPM. |
| QuantityType_SoundPressure | Quantity sound pressure. |
| QuantityType_Strain | Quantity strain. |
| QuantityType_Stress | Quantity stress. |
| QuantityType_Substance | Quantity substance. |
| QuantityType_Temperature | Quantity temperature. |
| QuantityType_Time | Quantity time. |
| QuantityType_Torque | Quantity torque. |
| QuantityType_User | Quantity user. |
| QuantityType_Velocity | Quantity velocity. |
| QuantityType_Voltage | Quantity voltage. |
| QuantityType_Volume | Quantity volume. |
| QuantityType_VolumeAcceleration | Quantity volume acceleration. |
| QuantityType_VolumeVelocity | Quantity volume velocity. |
| QuantityType_Work | Quantity work. |
The quantity type.


---

## ConnectionInfo Property

*Quelle: `Polytec_IO_VibInterfaces~IController~ConnectionInfo.html` · Polytec IO VibInterfaces Type Library · IController Interface : ConnectionInfo Property*

### Description

The information about the connection of the controller.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property ConnectionInfo As IConnectionInfo
```


---

## ControllerInfo Property

*Quelle: `Polytec_IO_VibInterfaces~IController~ControllerInfo.html` · Polytec IO VibInterfaces Type Library · IController Interface : ControllerInfo Property*

### Description

The information about the controller.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property ControllerInfo As ControllerInfo
```


---

## DecoderClearModes Property

*Quelle: `Polytec_IO_VibInterfaces~IController~DecoderClearModes.html` · Polytec IO VibInterfaces Type Library · IController Interface : DecoderClearModes Property*

### Description

The clear modes of the controller.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property DecoderClearModes As DecoderClearModeCollection
```


---

## Decoders Property

*Quelle: `Polytec_IO_VibInterfaces~IController~Decoders.html` · Polytec IO VibInterfaces Type Library · IController Interface : Decoders Property*

### Description

The decoders of the controller.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Decoders As IDecoderCollection
```


---

## DigitalDemodulation Property

*Quelle: `Polytec_IO_VibInterfaces~IController~DigitalDemodulation.html` · Polytec IO VibInterfaces Type Library · IController Interface : DigitalDemodulation Property*

### Description

The digital demodulation object of the controller.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property DigitalDemodulation As IDigitalDemodulation
```


---

## Filters Property

*Quelle: `Polytec_IO_VibInterfaces~IController~Filters.html` · Polytec IO VibInterfaces Type Library · IController Interface : Filters Property*

### Description

The filters of the controller.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Filters As IFilterCollection
```


---

## FrontEndIPAddress Property

*Quelle: `Polytec_IO_VibInterfaces~IController~FrontEndIPAddress.html` · Polytec IO VibInterfaces Type Library · IController Interface : FrontEndIPAddress Property*

### Description

Returns the IP address of the front end.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property FrontEndIPAddress As String
```


---

## Group Property

*Quelle: `Polytec_IO_VibInterfaces~IController~Group.html` · Polytec IO VibInterfaces Type Library · IController Interface : Group Property*

### Description

The controller group the controller is a member of.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Group As IControllerGroup
```


---

## MeasurementMode Property

*Quelle: `Polytec_IO_VibInterfaces~IController~MeasurementMode.html` · Polytec IO VibInterfaces Type Library · IController Interface : MeasurementMode Property*

### Description

The measurement mode of the controller.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property MeasurementMode As IMeasurementModeInfo
```


---

## PowerUp Property

*Quelle: `Polytec_IO_VibInterfaces~IController~PowerUp.html` · Polytec IO VibInterfaces Type Library · IController Interface : PowerUp Property*

### Description

The power-up settings of the controller.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property PowerUp As IPowerUp
```


---

## Quantities Property

*Quelle: `Polytec_IO_VibInterfaces~IController~Quantities.html` · Polytec IO VibInterfaces Type Library · IController Interface : Quantities Property*

### Description

The quantities of the controller.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Quantities As IQuantityCollection
```


---

## Recorder Property

*Quelle: `Polytec_IO_VibInterfaces~IController~Recorder.html` · Polytec IO VibInterfaces Type Library · IController Interface : Recorder Property*

### Description

Returns the recorder object if the controller has a recorder mode, e.g. VGO-200.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Recorder As IRecorder
```


---

## SensorHeads Property

*Quelle: `Polytec_IO_VibInterfaces~IController~SensorHeads.html` · Polytec IO VibInterfaces Type Library · IController Interface : SensorHeads Property*

### Description

The sensor heads of the controller.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property SensorHeads As ISensorHeadCollection
```


---

## ServiceMode Property

*Quelle: `Polytec_IO_VibInterfaces~IController~ServiceMode.html` · Polytec IO VibInterfaces Type Library · IController Interface : ServiceMode Property*

### Description

The service mode object of the controller.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property ServiceMode As IServiceMode
```


---

## Settings Property

*Quelle: `Polytec_IO_VibInterfaces~IController~Settings.html` · Polytec IO VibInterfaces Type Library · IController Interface : Settings Property*

### Description

The settings of the controller.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Settings As ControllerSettings
```


---

## SignalEnhancement Property

*Quelle: `Polytec_IO_VibInterfaces~IController~SignalEnhancement.html` · Polytec IO VibInterfaces Type Library · IController Interface : SignalEnhancement Property*

### Description

The signal enhancement of the controller.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property SignalEnhancement As ISignalEnhancement
```
