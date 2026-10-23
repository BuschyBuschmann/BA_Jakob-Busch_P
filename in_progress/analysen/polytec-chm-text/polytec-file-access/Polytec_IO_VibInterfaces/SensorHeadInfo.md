# Polytec_IO_VibInterfaces – SensorHeadInfo

## SensorHeadInfo Object

*Quelle: `Polytec_IO_VibInterfaces~SensorHeadInfo.html` · Polytec IO VibInterfaces Type Library*

### Description

The information about the sensor head.

### Example

PSV/VibSoft support up to two groups of Vibrometer controllers attached to the system. For a 3D system the first group contains three Vibrometers. Below the laser wavelength of the first sensor head of the first controller of the first Vibrometer group is printed. Please note that the VibrometersAcqPropertiesContainer Collection uses 1-based indices, the SensorHeadSettingsCollection Collection uses 0-based indices.

- Access the sensor head info stored in a file (VB.NET)

```
Dim oVibrometerAcqProperties As VibrometerAcqProperties
oVibrometerAcqProperties = oFile.Infos.AcquisitionInfoModes.ActiveProperties.VibrometersProperties(1)
Dim oSensorHeadSettings As SensorHeadSettings
oSensorHeadSettings = oVibrometerAcqProperties.VibControllerSettings.SensorHeadSettingsCollection(0)
Debug.Print oSensorHeadSettings.SensorHeadInfo.LaserWavelength
```


---

## SensorHeadInfo Object Members

*Quelle: `Polytec_IO_VibInterfaces~SensorHeadInfo_members.html` · Polytec IO VibInterfaces Type Library*

### Public Methods

| Clone | Creates and returns a copy of the sensor head info object. |
|---|---|
| HasCap | Returns true if the sensor head has the given capability. |
| HasCap2 | Returns true if the sensor head has the given extended capability. |

### Public Properties

| BeamGap | The beam gap of the sensor heads including the unit, e.g. for the RLV. |
|---|---|
| BraggCellFrequency | The frequency of the Bragg cell. |
| Caps | The capabilities of the sensor head. |
| Caps2 | The extended capabilities of the sensor head. |
| CoherenceOptimizerFirmwareVersion | The firmware version of the coherence optimizer. |
| Connected | Gets a Boolean indicating whether the sensor head is connected. |
| DimmerMax | The maximum transmission of the laser beam. |
| DimmerMin | The minimum transmission of the laser beam. |
| FirmwareVersion | The firmware version of the sensor head. |
| FocusFarLimit | The farthest focus position. |
| FocusNearLimit | The nearest focus position. |
| IlluminationIntensityMax | The maximum illumination intensity. |
| IlluminationIntensityMin | The minimum illumination intensity. |
| LaserDelay | The laser delay in second, e.g. for the UHF-120 vibrometer. |
| LaserFirmwareVersion | Gets the laser firmware version string, e.g. for the IR laser. This feature might not be supported by all sensor heads. |
| LaserPower | The laser power in milliwatt. |
| LaserWavelength | The laser wavelength in nanometer. |
| LowerObjectiveThresholdTemperature | The lower threshold temperature for the objective temperature regulation. |
| MaxRGBLedColorIndex | Gets the zero-based maximum index of the RGB color of the LED. |
| MaxSignalBalance | The end of the signal balance range. |
| MinRGBLedColorIndex | Gets the zero-based minimum index of the RGB color of the LED. |
| MinSignalBalance | The start of the signal balance range. |
| Name | The name of the sensor head. |
| SerialNumber | The serial number of the sensor head. |
| SondeName | Gets the name of the sonde. |
| StandoffDist | The stand off distance including the unit, e.g. for the RLV sensor heads. |
| SystemLaserPower | The system laser power in milliwatt. |
| UniqueID | The unique identifier of the sensor head. |
| UpperObjectiveThresholdTemperature | The upper threshold temperature for the objective temperature regulation. |


---

## Clone Method

*Quelle: `Polytec_IO_VibInterfaces~SensorHeadInfo~Clone.html` · Polytec IO VibInterfaces Type Library · SensorHeadInfo Object : Clone Method*

### Description

Creates and returns a copy of the sensor head info object.

### Syntax

*Visual Basic:*
```
Public Function Clone() As Variant
```


---

## HasCap Method

*Quelle: `Polytec_IO_VibInterfaces~SensorHeadInfo~HasCap.html` · Polytec IO VibInterfaces Type Library · SensorHeadInfo Object : HasCap Method*

### Description

Returns true if the sensor head has the given capability.

### Syntax

*Visual Basic:*
```
Public Function HasCap( _
   ByVal cap As SensorHeadCaps _
) As Boolean
```

### Parameters

cap

| Value | Description |
|---|---|
| SensorHeadCaps_AlignmentLaserShutter | The sensor head has an alignment laser shutter. |
| SensorHeadCaps_AutoFocus | The sensor head has the autofocus capability. |
| SensorHeadCaps_AutoFocusInArea | The sensor head supports autofocusing in a user-defined range. |
| SensorHeadCaps_AutoFocusInRange | The sensor head supports autofocusing in a predefined range. |
| SensorHeadCaps_BeamGap | The sensor head provides information about the beam gap. |
| SensorHeadCaps_BraggCellFrequency | The sensor head can provide the frequency of the Bragg cell. |
| SensorHeadCaps_CoherenceOptimizer | The sensor head has a coherence optimizer. |
| SensorHeadCaps_Dimmer | The sensor head has a dimmer. |
| SensorHeadCaps_FocusAbsolute | The sensor head can focus absolutely. |
| SensorHeadCaps_FocusLimit | The sensor head has the focus limit capability. |
| SensorHeadCaps_FocusProgress | The sensor head has the focus progress capability. |
| SensorHeadCaps_FocusRelative | The sensor head can focus relatively to the current focus position. |
| SensorHeadCaps_FocusStepDeviation | The sensor head supports the focus step deviation commands. |
| SensorHeadCaps_IlluminationIntensity | The sensor head supports the intensity of the illumination. |
| SensorHeadCaps_IlluminationState | The sensor head supports the state of the illumination. |
| SensorHeadCaps_LaserDelay | The sensor head provides information about the laser delay. |
| SensorHeadCaps_LaserWavelength | The sensor head provides information about the laser wavelength. |
| SensorHeadCaps_LaserWavelengthStabilization | The sensor head supports a laser wavelength stabilization. |
| SensorHeadCaps_ManualFocusEnable | The sensor head can enable and disable manual focusing. |
| SensorHeadCaps_None | The sensor head has no capabilities. |
| SensorHeadCaps_ObjectiveTemperature | The sensor head has an objective temperature regulation. |
| SensorHeadCaps_OverTemp | The sensor head has a temperature state. |
| SensorHeadCaps_PilotLaserDimmer | The sensor head supports the pilot laser dimming. |
| SensorHeadCaps_PilotLaserShutter | The sensor head has a pilot laser shutter. |
| SensorHeadCaps_Reticle | The sensor head has reticles. |
| SensorHeadCaps_Sensitivity | A sensitivity can be specified for the sensor head. |
| SensorHeadCaps_Shutter | The sensor head has a shutter. |
| SensorHeadCaps_SignalBalance | The sensor head has signal balance. |
| SensorHeadCaps_SignalLevel | The sensor head has signal level. |
| SensorHeadCaps_SignalLevelB | The sensor head has a signal level B indicator. |
| SensorHeadCaps_StandoffDist | The sensor head provides information about the stand off distance. |
| SensorHeadCaps_Temperature | The sensor head provides a temperature. |
| SensorHeadCaps_VideoCamera | The sensor head has a video camera. |
The capability of the sensor head to check.


---

## HasCap2 Method

*Quelle: `Polytec_IO_VibInterfaces~SensorHeadInfo~HasCap2.html` · Polytec IO VibInterfaces Type Library · SensorHeadInfo Object : HasCap2 Method*

### Description

Returns true if the sensor head has the given extended capability.

### Syntax

*Visual Basic:*
```
Public Function HasCap2( _
   ByVal cap As SensorHeadCaps2 _
) As Boolean
```

### Parameters

cap

| Value | Description |
|---|---|
| SensorHeadCaps2_DifferentialMeasurementMode | The sensor head supports the differential measurement mode, e.g. on MSA-600 systems. |
| SensorHeadCaps2_ExternalScannerControl | The sensor head supports external control of the scanners. |
| SensorHeadCaps2_LaserPower | The sensor head provides information about the nominal laser power. |
| SensorHeadCaps2_LaserPowerSupply | The sensor head has a laser power supply and supports switching the power supply on or off. |
| SensorHeadCaps2_LaserTemperature | The sensor head provides information about the laser temperature. |
| SensorHeadCaps2_LaserTemperatureOutOfRange | The sensor head provides information about whether the laser temperature is out of range. |
| SensorHeadCaps2_None | None of the capabilities is available. |
| SensorHeadCaps2_QTec | The sensor head supports QTec. |
| SensorHeadCaps2_RGBLedColor | The sensor head has a status LED with RGB color. |
| SensorHeadCaps2_RSSILevelBlink | The sensor head supports the RSSI level blinking, where the signal level value is indicated by the blinking frequency of the status LED. |
| SensorHeadCaps2_Sonde | The sensor head is a sonde. |
| SensorHeadCaps2_UniqueID | The sensor head provides a unique identifier. |
The extended capability of the sensor head to check.


---

## BeamGap Property

*Quelle: `Polytec_IO_VibInterfaces~SensorHeadInfo~BeamGap.html` · Polytec IO VibInterfaces Type Library · SensorHeadInfo Object : BeamGap Property*

### Description

The beam gap of the sensor heads including the unit, e.g. for the RLV.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property BeamGap As String
```


---

## BraggCellFrequency Property

*Quelle: `Polytec_IO_VibInterfaces~SensorHeadInfo~BraggCellFrequency.html` · Polytec IO VibInterfaces Type Library · SensorHeadInfo Object : BraggCellFrequency Property*

### Description

The frequency of the Bragg cell.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property BraggCellFrequency As Double
```

### Remarks

This property is only available for UHF vibrometers.


---

## Caps Property

*Quelle: `Polytec_IO_VibInterfaces~SensorHeadInfo~Caps.html` · Polytec IO VibInterfaces Type Library · SensorHeadInfo Object : Caps Property*

### Description

The capabilities of the sensor head.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Caps As SensorHeadCaps
```


---

## Caps2 Property

*Quelle: `Polytec_IO_VibInterfaces~SensorHeadInfo~Caps2.html` · Polytec IO VibInterfaces Type Library · SensorHeadInfo Object : Caps2 Property*

### Description

The extended capabilities of the sensor head.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Caps2 As SensorHeadCaps2
```


---

## CoherenceOptimizerFirmwareVersion Property

*Quelle: `Polytec_IO_VibInterfaces~SensorHeadInfo~CoherenceOptimizerFirmwareVersion.html` · Polytec IO VibInterfaces Type Library · SensorHeadInfo Object : CoherenceOptimizerFirmwareVersion Property*

### Description

The firmware version of the coherence optimizer.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property CoherenceOptimizerFirmwareVersion As String
```


---

## Connected Property

*Quelle: `Polytec_IO_VibInterfaces~SensorHeadInfo~Connected.html` · Polytec IO VibInterfaces Type Library · SensorHeadInfo Object : Connected Property*

### Description

Gets a Boolean indicating whether the sensor head is connected.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Connected As Boolean
```

### Return Type

True if the head is connected, False if it is not.


---

## DimmerMax Property

*Quelle: `Polytec_IO_VibInterfaces~SensorHeadInfo~DimmerMax.html` · Polytec IO VibInterfaces Type Library · SensorHeadInfo Object : DimmerMax Property*

### Description

The maximum transmission of the laser beam.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property DimmerMax As Long
```


---

## DimmerMin Property

*Quelle: `Polytec_IO_VibInterfaces~SensorHeadInfo~DimmerMin.html` · Polytec IO VibInterfaces Type Library · SensorHeadInfo Object : DimmerMin Property*

### Description

The minimum transmission of the laser beam.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property DimmerMin As Long
```


---

## FirmwareVersion Property

*Quelle: `Polytec_IO_VibInterfaces~SensorHeadInfo~FirmwareVersion.html` · Polytec IO VibInterfaces Type Library · SensorHeadInfo Object : FirmwareVersion Property*

### Description

The firmware version of the sensor head.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property FirmwareVersion As String
```


---

## FocusFarLimit Property

*Quelle: `Polytec_IO_VibInterfaces~SensorHeadInfo~FocusFarLimit.html` · Polytec IO VibInterfaces Type Library · SensorHeadInfo Object : FocusFarLimit Property*

### Description

The farthest focus position.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property FocusFarLimit As Long
```


---

## FocusNearLimit Property

*Quelle: `Polytec_IO_VibInterfaces~SensorHeadInfo~FocusNearLimit.html` · Polytec IO VibInterfaces Type Library · SensorHeadInfo Object : FocusNearLimit Property*

### Description

The nearest focus position.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property FocusNearLimit As Long
```


---

## IlluminationIntensityMax Property

*Quelle: `Polytec_IO_VibInterfaces~SensorHeadInfo~IlluminationIntensityMax.html` · Polytec IO VibInterfaces Type Library · SensorHeadInfo Object : IlluminationIntensityMax Property*

### Description

The maximum illumination intensity.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property IlluminationIntensityMax As Long
```


---

## IlluminationIntensityMin Property

*Quelle: `Polytec_IO_VibInterfaces~SensorHeadInfo~IlluminationIntensityMin.html` · Polytec IO VibInterfaces Type Library · SensorHeadInfo Object : IlluminationIntensityMin Property*

### Description

The minimum illumination intensity.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property IlluminationIntensityMin As Long
```


---

## LaserDelay Property

*Quelle: `Polytec_IO_VibInterfaces~SensorHeadInfo~LaserDelay.html` · Polytec IO VibInterfaces Type Library · SensorHeadInfo Object : LaserDelay Property*

### Description

The laser delay in second, e.g. for the UHF-120 vibrometer.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property LaserDelay As Double
```


---

## LaserFirmwareVersion Property

*Quelle: `Polytec_IO_VibInterfaces~SensorHeadInfo~LaserFirmwareVersion.html` · Polytec IO VibInterfaces Type Library · SensorHeadInfo Object : LaserFirmwareVersion Property*

### Description

Gets the laser firmware version string, e.g. for the IR laser. This feature might not be supported by all sensor heads.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property LaserFirmwareVersion As String
```

### Return Type

The laser firmware version string.


---

## LaserPower Property

*Quelle: `Polytec_IO_VibInterfaces~SensorHeadInfo~LaserPower.html` · Polytec IO VibInterfaces Type Library · SensorHeadInfo Object : LaserPower Property*

### Description

The laser power in milliwatt.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property LaserPower As Double
```


---

## LaserWavelength Property

*Quelle: `Polytec_IO_VibInterfaces~SensorHeadInfo~LaserWavelength.html` · Polytec IO VibInterfaces Type Library · SensorHeadInfo Object : LaserWavelength Property*

### Description

The laser wavelength in nanometer.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property LaserWavelength As Double
```


---

## LowerObjectiveThresholdTemperature Property

*Quelle: `Polytec_IO_VibInterfaces~SensorHeadInfo~LowerObjectiveThresholdTemperature.html` · Polytec IO VibInterfaces Type Library · SensorHeadInfo Object : LowerObjectiveThresholdTemperature Property*

### Description

The lower threshold temperature for the objective temperature regulation.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property LowerObjectiveThresholdTemperature As Double
```

### Return Type

The lower threshold in degree Celsius.

### Example


---

## MaxRGBLedColorIndex Property

*Quelle: `Polytec_IO_VibInterfaces~SensorHeadInfo~MaxRGBLedColorIndex.html` · Polytec IO VibInterfaces Type Library · SensorHeadInfo Object : MaxRGBLedColorIndex Property*

### Description

Gets the zero-based maximum index of the RGB color of the LED.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property MaxRGBLedColorIndex As Long
```

### Return Type

The zero-based maximum index of the RGB LED color.


---

## MaxSignalBalance Property

*Quelle: `Polytec_IO_VibInterfaces~SensorHeadInfo~MaxSignalBalance.html` · Polytec IO VibInterfaces Type Library · SensorHeadInfo Object : MaxSignalBalance Property*

### Description

The end of the signal balance range.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property MaxSignalBalance As SignalBalanceState
```


---

## MinRGBLedColorIndex Property

*Quelle: `Polytec_IO_VibInterfaces~SensorHeadInfo~MinRGBLedColorIndex.html` · Polytec IO VibInterfaces Type Library · SensorHeadInfo Object : MinRGBLedColorIndex Property*

### Description

Gets the zero-based minimum index of the RGB color of the LED.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property MinRGBLedColorIndex As Long
```

### Return Type

The zero-based minimum index of the RGB LED color.


---

## MinSignalBalance Property

*Quelle: `Polytec_IO_VibInterfaces~SensorHeadInfo~MinSignalBalance.html` · Polytec IO VibInterfaces Type Library · SensorHeadInfo Object : MinSignalBalance Property*

### Description

The start of the signal balance range.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property MinSignalBalance As SignalBalanceState
```


---

## Name Property

*Quelle: `Polytec_IO_VibInterfaces~SensorHeadInfo~Name.html` · Polytec IO VibInterfaces Type Library · SensorHeadInfo Object : Name Property*

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

## SerialNumber Property

*Quelle: `Polytec_IO_VibInterfaces~SensorHeadInfo~SerialNumber.html` · Polytec IO VibInterfaces Type Library · SensorHeadInfo Object : SerialNumber Property*

### Description

The serial number of the sensor head.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property SerialNumber As String
```


---

## SondeName Property

*Quelle: `Polytec_IO_VibInterfaces~SensorHeadInfo~SondeName.html` · Polytec IO VibInterfaces Type Library · SensorHeadInfo Object : SondeName Property*

### Description

Gets the name of the sonde.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property SondeName As String
```

### Return Type

The sonde name.


---

## StandoffDist Property

*Quelle: `Polytec_IO_VibInterfaces~SensorHeadInfo~StandoffDist.html` · Polytec IO VibInterfaces Type Library · SensorHeadInfo Object : StandoffDist Property*

### Description

The stand off distance including the unit, e.g. for the RLV sensor heads.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property StandoffDist As String
```


---

## SystemLaserPower Property

*Quelle: `Polytec_IO_VibInterfaces~SensorHeadInfo~SystemLaserPower.html` · Polytec IO VibInterfaces Type Library · SensorHeadInfo Object : SystemLaserPower Property*

### Description

The system laser power in milliwatt.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property SystemLaserPower As Double
```


---

## UniqueID Property

*Quelle: `Polytec_IO_VibInterfaces~SensorHeadInfo~UniqueID.html` · Polytec IO VibInterfaces Type Library · SensorHeadInfo Object : UniqueID Property*

### Description

The unique identifier of the sensor head.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property UniqueID As String
```


---

## UpperObjectiveThresholdTemperature Property

*Quelle: `Polytec_IO_VibInterfaces~SensorHeadInfo~UpperObjectiveThresholdTemperature.html` · Polytec IO VibInterfaces Type Library · SensorHeadInfo Object : UpperObjectiveThresholdTemperature Property*

### Description

The upper threshold temperature for the objective temperature regulation.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property UpperObjectiveThresholdTemperature As Double
```

### Return Type

The upper threshold in degree Celsius.

### Example
