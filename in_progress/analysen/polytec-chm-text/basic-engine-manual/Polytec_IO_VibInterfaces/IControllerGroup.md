# Polytec_IO_VibInterfaces – IControllerGroup

## IControllerGroup Interface

*Quelle: `Polytec_IO_VibInterfaces~IControllerGroup.html` · Polytec IO VibInterfaces Type Library*

### Description

A group of vibrometer controllers.

### Object Model

### Remarks

A group of vibrometer controllers contains controllers that have the same properties and settings. A change to a single controller in this group will be propagated to the other members of the group. Calling a method or changing a property of the group will always affect all controllers in the group.

A vibrometer controller group is for example used in PSV-3D systems to control the three vibrometer controllers top, left and right. Via the group the controllers appear as a single controller.

For some properties of the vibrometer controller, e.g. the current signal level of the sensor head, it is necessary to access the individual controllers of the group. You can use the Controllers property to access the IControllerCollection collection and the individual controllers in this group.


---

## IControllerGroup Interface Members

*Quelle: `Polytec_IO_VibInterfaces~IControllerGroup_members.html` · Polytec IO VibInterfaces Type Library*

### Public Methods

| Disconnect | Disconnects the controller from the hardware. |
|---|---|
| GetSelectedBandwidthRange | Returns the active decoder bandwidth range for the given quantity. |
| GetSelectedDecoderRange | Returns the active decoder range for the given quantity. |
| GetSelectedFilterRange | Returns the active filter range for the given filter type. |
| GetSelectedMaxVelocityRange | Finds the selected maximum velocity range. |

### Public Properties

| ControllerInfo | The information about the controller. |
|---|---|
| Controllers | The controllers that are members of this controller group. |
| DecoderClearModes | The clear modes of the controller. |
| Decoders | The decoders of the controller. |
| DigitalDemodulation | The digital demodulation object of the controller. |
| Filters | The filters of the controller. |
| FrontEndIPAddress | Returns the IP address of the front end. |
| GroupControllerUnit | Gets the group controller unit, e.g. for a MPV system. |
| GroupLaserUnit | Gets the group laser unit, e.g. for a MPV system. |
| PowerUp | The power-up settings of the controller. |
| Quantities | The quantities of the controller. |
| Settings | The settings of the controller. |


---

## Disconnect Method

*Quelle: `Polytec_IO_VibInterfaces~IControllerGroup~Disconnect.html` · Polytec IO VibInterfaces Type Library · IControllerGroup Interface : Disconnect Method*

### Description

Disconnects the controller from the hardware.

### Syntax

*Visual Basic:*
```
Public Sub Disconnect()
```


---

## GetSelectedBandwidthRange Method

*Quelle: `Polytec_IO_VibInterfaces~IControllerGroup~GetSelectedBandwidthRange.html` · Polytec IO VibInterfaces Type Library · IControllerGroup Interface : GetSelectedBandwidthRange Method*

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

*Quelle: `Polytec_IO_VibInterfaces~IControllerGroup~GetSelectedDecoderRange.html` · Polytec IO VibInterfaces Type Library · IControllerGroup Interface : GetSelectedDecoderRange Method*

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

*Quelle: `Polytec_IO_VibInterfaces~IControllerGroup~GetSelectedFilterRange.html` · Polytec IO VibInterfaces Type Library · IControllerGroup Interface : GetSelectedFilterRange Method*

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

*Quelle: `Polytec_IO_VibInterfaces~IControllerGroup~GetSelectedMaxVelocityRange.html` · Polytec IO VibInterfaces Type Library · IControllerGroup Interface : GetSelectedMaxVelocityRange Method*

### Description

Finds the selected maximum velocity range.

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

### Return Type

The selected maximum velocity range or nothing if no range is selected.


---

## ControllerInfo Property

*Quelle: `Polytec_IO_VibInterfaces~IControllerGroup~ControllerInfo.html` · Polytec IO VibInterfaces Type Library · IControllerGroup Interface : ControllerInfo Property*

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

## Controllers Property

*Quelle: `Polytec_IO_VibInterfaces~IControllerGroup~Controllers.html` · Polytec IO VibInterfaces Type Library · IControllerGroup Interface : Controllers Property*

### Description

The controllers that are members of this controller group.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Controllers As IControllerCollection
```


---

## DecoderClearModes Property

*Quelle: `Polytec_IO_VibInterfaces~IControllerGroup~DecoderClearModes.html` · Polytec IO VibInterfaces Type Library · IControllerGroup Interface : DecoderClearModes Property*

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

*Quelle: `Polytec_IO_VibInterfaces~IControllerGroup~Decoders.html` · Polytec IO VibInterfaces Type Library · IControllerGroup Interface : Decoders Property*

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

*Quelle: `Polytec_IO_VibInterfaces~IControllerGroup~DigitalDemodulation.html` · Polytec IO VibInterfaces Type Library · IControllerGroup Interface : DigitalDemodulation Property*

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

*Quelle: `Polytec_IO_VibInterfaces~IControllerGroup~Filters.html` · Polytec IO VibInterfaces Type Library · IControllerGroup Interface : Filters Property*

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

*Quelle: `Polytec_IO_VibInterfaces~IControllerGroup~FrontEndIPAddress.html` · Polytec IO VibInterfaces Type Library · IControllerGroup Interface : FrontEndIPAddress Property*

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

## GroupControllerUnit Property

*Quelle: `Polytec_IO_VibInterfaces~IControllerGroup~GroupControllerUnit.html` · Polytec IO VibInterfaces Type Library · IControllerGroup Interface : GroupControllerUnit Property*

### Description

Gets the group controller unit, e.g. for a MPV system.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property GroupControllerUnit As IGroupControllerUnit
```

### Return Type

The interface of the group controller unit if such is available, null otherwise.


---

## GroupLaserUnit Property

*Quelle: `Polytec_IO_VibInterfaces~IControllerGroup~GroupLaserUnit.html` · Polytec IO VibInterfaces Type Library · IControllerGroup Interface : GroupLaserUnit Property*

### Description

Gets the group laser unit, e.g. for a MPV system.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property GroupLaserUnit As IGroupLaserUnit
```

### Return Type

The interface of the group laser unit if such is available, null otherwise.


---

## PowerUp Property

*Quelle: `Polytec_IO_VibInterfaces~IControllerGroup~PowerUp.html` · Polytec IO VibInterfaces Type Library · IControllerGroup Interface : PowerUp Property*

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

*Quelle: `Polytec_IO_VibInterfaces~IControllerGroup~Quantities.html` · Polytec IO VibInterfaces Type Library · IControllerGroup Interface : Quantities Property*

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

## Settings Property

*Quelle: `Polytec_IO_VibInterfaces~IControllerGroup~Settings.html` · Polytec IO VibInterfaces Type Library · IControllerGroup Interface : Settings Property*

### Description

The settings of the controller.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Settings As ControllerSettings
```
