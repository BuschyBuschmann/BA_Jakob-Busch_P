# Polytec_IO_VibInterfaces – ControllerInfo

## ControllerInfo Object

*Quelle: `Polytec_IO_VibInterfaces~ControllerInfo.html` · Polytec IO VibInterfaces Type Library*

### Description

The information about the controller.

### Example

To access the controller info of a Vibrometer that was attached to the system during a measurement, you have to navigate to the VibrometersAcqPropertiesContainer Collection of the active AcquisitionPropertiesContainer Collection.

- Access the controller info stored in a file (VB.NET)

```
Dim oVibrometerAcqProperties As VibrometerAcqProperties
oVibrometerAcqProperties = oFile.Infos.AcquisitionInfoModes.ActiveProperties.VibrometersProperties(1)

Dim oControllerSettings As ControllerSettings
oControllerSettings = oVibrometerAcqProperties.VibControllerSettings
Debug.Print oControllerSettings.ControllerInfo.DeviceName
```


---

## ControllerInfo Object Members

*Quelle: `Polytec_IO_VibInterfaces~ControllerInfo_members.html` · Polytec IO VibInterfaces Type Library*

### Public Methods

| Clone | Creates and returns a copy of the controller information object. |
|---|---|
| HasCap | Returns true, if the controller has the given capability. |

### Public Properties

| Caps | The capabilities of the controller. |
|---|---|
| DeviceName | The general vibrometer controller name. |
| FirmwareVersion | The version of the firmware of the controller. |
| Name | The type of the controller. |
| SerialNumber | The serial number of the device. |
| UniqueID | The unique ID of the device. |


---

## Clone Method

*Quelle: `Polytec_IO_VibInterfaces~ControllerInfo~Clone.html` · Polytec IO VibInterfaces Type Library · ControllerInfo Object : Clone Method*

### Description

Creates and returns a copy of the controller information object.

### Syntax

*Visual Basic:*
```
Public Function Clone() As Variant
```


---

## HasCap Method

*Quelle: `Polytec_IO_VibInterfaces~ControllerInfo~HasCap.html` · Polytec IO VibInterfaces Type Library · ControllerInfo Object : HasCap Method*

### Description

Returns true, if the controller has the given capability.

### Syntax

*Visual Basic:*
```
Public Function HasCap( _
   ByVal cap As ControllerCaps _
) As Boolean
```

### Parameters

cap

| Value | Description |
|---|---|
| ControllerCaps_DecoderClearMode | The controller supports decoder clear modes. |
| ControllerCaps_DigitalDemodulation | The controller has digital demodulation. |
| ControllerCaps_FieldUpdate | The controller supports field updates. |
| ControllerCaps_IsPhysicalUnit | If set, the controller unit itself (not necessarily its sensor head or decoder) is physical, i.e. not logical. E.g. the controller number zero of a PSV-500-3D, the first and only controller of a PSV-500-1D or all three controllers of a PSV-400-3D (because this system is build in hardware of three independent controller units, instead of one controller unit (PSV-500-3D) with three connected sensor heads, decoders etc.). |
| ControllerCaps_MeasurementMode | The controller supports different measurement modes. |
| ControllerCaps_MultipleOverrange | The controller has multiple overrange indicators. |
| ControllerCaps_MultipleSensorHeads | The controller has multiple sensor heads. |
| ControllerCaps_NoDecoder | The controller has no decoder, i.e. no data acquisition, e.g. that of the MPV system. |
| ControllerCaps_None | No capabilities. |
| ControllerCaps_Overrange | The controller has at least one overrange indicator. |
| ControllerCaps_PowerUP | The controller has power up. |
| ControllerCaps_PSV500Behaviour | The controller behaves like a controller of the PSV-500 system. |
| ControllerCaps_Recorder | The controller has a recorder for vibration data e.g., VGO-200. |
| ControllerCaps_SensorHead | The controller has a sensor head. |
| ControllerCaps_ServiceMode | The controller has a service mode. |
| ControllerCaps_SignalEnhancement | The controller has signal enhancement. |
| ControllerCaps_WebServer | The controller has a web server. |
| ControllerCaps_WriteLock | The controller supports a write lock. |

The capability of the controller.


---

## Caps Property

*Quelle: `Polytec_IO_VibInterfaces~ControllerInfo~Caps.html` · Polytec IO VibInterfaces Type Library · ControllerInfo Object : Caps Property*

### Description

The capabilities of the controller.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Caps As ControllerCaps
```


---

## DeviceName Property

*Quelle: `Polytec_IO_VibInterfaces~ControllerInfo~DeviceName.html` · Polytec IO VibInterfaces Type Library · ControllerInfo Object : DeviceName Property*

### Description

The general vibrometer controller name.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property DeviceName As String
```


---

## FirmwareVersion Property

*Quelle: `Polytec_IO_VibInterfaces~ControllerInfo~FirmwareVersion.html` · Polytec IO VibInterfaces Type Library · ControllerInfo Object : FirmwareVersion Property*

### Description

The version of the firmware of the controller.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property FirmwareVersion As String
```


---

## Name Property

*Quelle: `Polytec_IO_VibInterfaces~ControllerInfo~Name.html` · Polytec IO VibInterfaces Type Library · ControllerInfo Object : Name Property*

### Description

The type of the controller.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Name As String
```


---

## SerialNumber Property

*Quelle: `Polytec_IO_VibInterfaces~ControllerInfo~SerialNumber.html` · Polytec IO VibInterfaces Type Library · ControllerInfo Object : SerialNumber Property*

### Description

The serial number of the device.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property SerialNumber As String
```


---

## UniqueID Property

*Quelle: `Polytec_IO_VibInterfaces~ControllerInfo~UniqueID.html` · Polytec IO VibInterfaces Type Library · ControllerInfo Object : UniqueID Property*

### Description

The unique ID of the device.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property UniqueID As String
```
