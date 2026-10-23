# Polytec_IO_VibInterfaces – ISensorHead

## ISensorHead Interface

*Quelle: `Polytec_IO_VibInterfaces~ISensorHead.html` · Polytec IO VibInterfaces Type Library*

### Description

The sensor head object allows to control and access information from the sensor head attached to the vibrometer controller.

### Object Model

### Example

To access the ISensorHead interface of a connected Vibrometer you have to navigate through the InfosAcq Collection of the Acquisition Object.

- Access to ISensorHead Interface (VB.NET)

```
Dim oInfosAcq As InfosAcq
oInfosAcq = Acquisition.Infos
Debug.Print oInfosAcq.Vibrometers(1).Controllers(0).SensorHeads(0).SignalLevel
```


---

## ISensorHead Interface Members

*Quelle: `Polytec_IO_VibInterfaces~ISensorHead_members.html` · Polytec IO VibInterfaces Type Library*

### Public Methods

| GetReticles | Gets the names of all available reticles of the sensor head. |
|---|---|
| ResetAutoFocusArea | Resets the automatic focus area to the full range. |
| SetAlignmentLaserShutterOpen | Sets the state of the alignment laser shutter. |
| SetAutoFocusArea | Sets the autofocus area, but does not start the autofocusing. This area is then used in a call of StartAutoFocus() unless StartAutoFocusInArea() , StartAutoFocusInRange() , or ResetAutoFocusArea() is called before. |
| SetCoherenceOptimizerOn | Activates or deactivates the coherence optimizer of the sensor head. |
| SetExternalScannerControlOn | Activates or deactivates the external scanner control of the sensor head. |
| SetFocusPosition | Sets the focus position. |
| SetLaserOn | Sets the state of the laser beam shutter. |
| SetLaserPowerSupplyOn | Sets the laser power supply on or off. |
| SetManualFocusLock | Sets a value indicating whether the hardware focus-ring is coupled or not coupled to the focusing unit. |
| SetQTecOn | Sets the QTec mode on or off. |
| SetReticle | Sets the reticle of the sensor head. |
| SetRGBLedColorIndex | Sets the index of the RGB color of the LED. |
| SetRSSILevelBlink | Switches the RSSI level blinking on or off, e.g. for a MPV system. |
| SetSensitivity | Sets the sensitivity state of the sensor head. |
| StartAutoFocus | Starts the automatic focusing process. |
| StartAutoFocusInArea | Starts the automatic focusing process limited to the given area. |
| StartAutoFocusInRange | Starts the automatic focusing process limited to the given range. |
| StartFocusStepReference | Starts the focus step reference run. |
| StartSeekFocusStepDeviation | Starts the laser focusing unit to seek for focus step deviations. |
| StopFocus | Stops a focusing process started with SetFocusPosition . |
| Update | Updates the sensor head status. |
| UpdateFocusPosition | Reads the focus position from the hardware and updates the FocusPosition property . |

### Public Properties

| AlignmentLaserShutterOpen | Returns true if the alignment laser shutter is open. |
|---|---|
| AutoFocusAreaLowerBound | Gets the current autofocus area lower bound, which has been set by SetAutoFocusArea() . |
| AutoFocusAreaUpperBound | Gets the current autofocus area upper bound, which has been set by SetAutoFocusArea() . |
| AutoFocusInProgress | Indicates whether an autofocusing process is active or not. |
| AutoFocusState | The result of an automatic focusing process. |
| CoherenceOptimizerOn | Returns true if the coherence optimizer is on. |
| CoherenceOptimizerPower | Gets the current control power level of the coherence optimizer control circuit. |
| CoherenceOptimizerStatus | The current status of the coherence optimizer control circuit. |
| externalScannerControlOn | Returns true if the external scanner control is on. |
| FocusInProgress | Indicates whether a focusing process is active or not. |
| FocusLimit | Gets whether the focus motor is currently at one of its limit positions or not. |
| FocusPosition | The focus position. |
| FocusStepReferenceInProgress | Indicates whether a reference run of the laser focusing unit is in progress or not. |
| Key | The identifier of the sensor head. |
| LaserOn | Returns true if the laser is on. |
| LaserTemperature | The laser temperature in degree Celsius. |
| LaserTemperatureOutOfRange | Returns true if the laser temperature is out of range. |
| LaserWavelengthStable | Returns true if the laser wavelength is stable and false if it is still stabilizing. |
| ManualFocusLock | Indicates whether the hardware focus-ring is coupled or not coupled to the focusing unit. |
| Name | The name of the sensor head. |
| ObjectiveTemperature | Returns the temperature of the objective in degree Celsius. |
| QTecOn | Returns true if QTec mode is on. |
| Reticle | The current reticle of the sensor head. |
| RGBLedColorIndex | Gets the zero-based index of the RGB color of the LED. |
| RSSILevelBlink | Gets a Boolean indicating whether the RSSI level blinking is switched on or off. |
| SeekFocusStepDeviationInProgress | Indicates whether the laser focusing currently seeks for focus step deviations. |
| SeekFocusStepDeviationResult | Gets the result of the seek for focus step deviations process. |
| Sensitivity | The sensitivity state of the sensor head. |
| SensorHeadInfo | The information about the sensor head. |
| SignalBalance | The balance of the signal. |
| SignalLevel | The level of the signal in percent. |
| SignalLevelB | The level of the signal B of the sensor head in percent. |
| Temperature | The current temperature of the sensor head in degree Celsius. |
| TemperatureState | The current temperature state of the sensor head. |
| VideoCamera | The video camera of the sensor head. |


---

## GetReticles Method

*Quelle: `Polytec_IO_VibInterfaces~ISensorHead~GetReticles.html` · Polytec IO VibInterfaces Type Library · ISensorHead Interface : GetReticles Method*

### Description

Gets the names of all available reticles of the sensor head.

### Syntax

*Visual Basic:*
```
Public Function GetReticles() As String()
```


---

## ResetAutoFocusArea Method

*Quelle: `Polytec_IO_VibInterfaces~ISensorHead~ResetAutoFocusArea.html` · Polytec IO VibInterfaces Type Library · ISensorHead Interface : ResetAutoFocusArea Method*

### Description

Resets the automatic focus area to the full range.

### Syntax

*Visual Basic:*
```
Public Sub ResetAutoFocusArea()
```


---

## SetAlignmentLaserShutterOpen Method

*Quelle: `Polytec_IO_VibInterfaces~ISensorHead~SetAlignmentLaserShutterOpen.html` · Polytec IO VibInterfaces Type Library · ISensorHead Interface : SetAlignmentLaserShutterOpen Method*

### Description

Sets the state of the alignment laser shutter.

### Syntax

*Visual Basic:*
```
Public Sub SetAlignmentLaserShutterOpen( _
   ByVal alignmentLaserShutterOpenParam As Boolean _
)
```

### Parameters

alignmentLaserShutterOpenParam

True to open the alignment shutter (activate alignment mode of the sensor head). False to close the alignment shutter (activate measurement mode of the sensor head).

### Example


---

## SetAutoFocusArea Method

*Quelle: `Polytec_IO_VibInterfaces~ISensorHead~SetAutoFocusArea.html` · Polytec IO VibInterfaces Type Library · ISensorHead Interface : SetAutoFocusArea Method*

### Description

Sets the autofocus area, but does not start the autofocusing. This area is then used in a call of StartAutoFocus() unless StartAutoFocusInArea(), StartAutoFocusInRange(), or ResetAutoFocusArea() is called before.

### Syntax

*Visual Basic:*
```
Public Sub SetAutoFocusArea( _
   ByVal lowerBound As Long, _
   ByVal upperBound As Long _
)
```

### Parameters

lowerBound

The lower bound of the autofocus area in focus step.

upperBound

The upper bound of the autofocus area in focus step.


---

## SetCoherenceOptimizerOn Method

*Quelle: `Polytec_IO_VibInterfaces~ISensorHead~SetCoherenceOptimizerOn.html` · Polytec IO VibInterfaces Type Library · ISensorHead Interface : SetCoherenceOptimizerOn Method*

### Description

Activates or deactivates the coherence optimizer of the sensor head.

### Syntax

*Visual Basic:*
```
Public Sub SetCoherenceOptimizerOn( _
   ByVal CoherenceOptimizerOn As Boolean _
)
```

### Parameters

CoherenceOptimizerOn

If set to true, the coherence optimizer will be activated.


---

## SetExternalScannerControlOn Method

*Quelle: `Polytec_IO_VibInterfaces~ISensorHead~SetExternalScannerControlOn.html` · Polytec IO VibInterfaces Type Library · ISensorHead Interface : SetExternalScannerControlOn Method*

### Description

Activates or deactivates the external scanner control of the sensor head.

### Syntax

*Visual Basic:*
```
Public Sub SetExternalScannerControlOn( _
   ByVal externalScannerControlOn As Boolean _
)
```

### Parameters

externalScannerControlOn

If set to true, the external scanner control will be activated.

### Remarks

The sensor head must have the SensorHeadCaps2_ExternalScannerControl cap.


---

## SetFocusPosition Method

*Quelle: `Polytec_IO_VibInterfaces~ISensorHead~SetFocusPosition.html` · Polytec IO VibInterfaces Type Library · ISensorHead Interface : SetFocusPosition Method*

### Description

Sets the focus position.

### Syntax

*Visual Basic:*
```
Public Sub SetFocusPosition( _
   ByVal focus As Long _
)
```

### Parameters

focus

The focus position.

### Remarks

You can specify FocusNearLimit or FocusFarLimit to start a focusing process towards the given limits. Please note that the focusing starts asynchronously after setting the property. Use the FocusInProgress Property to poll the current state of the focusing.


---

## SetLaserOn Method

*Quelle: `Polytec_IO_VibInterfaces~ISensorHead~SetLaserOn.html` · Polytec IO VibInterfaces Type Library · ISensorHead Interface : SetLaserOn Method*

### Description

Sets the state of the laser beam shutter.

### Syntax

*Visual Basic:*
```
Public Sub SetLaserOn( _
   ByVal LaserOn As Boolean _
)
```

### Parameters

LaserOn

True to activate the laser beam, false to close the shutter.


---

## SetLaserPowerSupplyOn Method

*Quelle: `Polytec_IO_VibInterfaces~ISensorHead~SetLaserPowerSupplyOn.html` · Polytec IO VibInterfaces Type Library · ISensorHead Interface : SetLaserPowerSupplyOn Method*

### Description

Sets the laser power supply on or off.

### Syntax

*Visual Basic:*
```
Public Sub SetLaserPowerSupplyOn( _
   ByVal laserPowerSupplyOn As Boolean _
)
```

### Parameters

laserPowerSupplyOn

True to enable, false to disable the laser power supply.


---

## SetManualFocusLock Method

*Quelle: `Polytec_IO_VibInterfaces~ISensorHead~SetManualFocusLock.html` · Polytec IO VibInterfaces Type Library · ISensorHead Interface : SetManualFocusLock Method*

### Description

Sets a value indicating whether the hardware focus-ring is coupled or not coupled to the focusing unit.

### Syntax

*Visual Basic:*
```
Public Sub SetManualFocusLock( _
   ByVal focusLock As Boolean _
)
```

### Parameters

focusLock

The focus lock.

### Remarks

A coupled focus ring (focusLock is true) indicates that manual focusing is disabled. Otherwise (focusLock is false) the focus ring is not coupled to the focusing unit and manual focusing is enabled.


---

## SetQTecOn Method

*Quelle: `Polytec_IO_VibInterfaces~ISensorHead~SetQTecOn.html` · Polytec IO VibInterfaces Type Library · ISensorHead Interface : SetQTecOn Method*

### Description

Sets the QTec mode on or off.

### Syntax

*Visual Basic:*
```
Public Sub SetQTecOn( _
   ByVal QTecOn As Boolean _
)
```

### Parameters

QTecOn

True to activate QTec mode, false to deactivate QTec mode.


---

## SetReticle Method

*Quelle: `Polytec_IO_VibInterfaces~ISensorHead~SetReticle.html` · Polytec IO VibInterfaces Type Library · ISensorHead Interface : SetReticle Method*

### Description

Sets the reticle of the sensor head.

### Syntax

*Visual Basic:*
```
Public Sub SetReticle( _
   ByVal Reticle As String _
)
```

### Parameters

Reticle

The reticle.

### Remarks

For a list of the available reticles of the sensor head, see the GetReticles Method.


---

## SetRGBLedColorIndex Method

*Quelle: `Polytec_IO_VibInterfaces~ISensorHead~SetRGBLedColorIndex.html` · Polytec IO VibInterfaces Type Library · ISensorHead Interface : SetRGBLedColorIndex Method*

### Description

Sets the index of the RGB color of the LED.

### Syntax

*Visual Basic:*
```
Public Sub SetRGBLedColorIndex( _
   ByVal colorIndex As Long _
)
```

### Parameters

colorIndex

The zero-based index of the color.

### Remarks

The admissible color index range can be queried by the properties MinRGBLedColorIndex and MaxRGBLedColorIndex of the SensorHeadInfo object.


---

## SetRSSILevelBlink Method

*Quelle: `Polytec_IO_VibInterfaces~ISensorHead~SetRSSILevelBlink.html` · Polytec IO VibInterfaces Type Library · ISensorHead Interface : SetRSSILevelBlink Method*

### Description

Switches the RSSI level blinking on or off, e.g. for a MPV system.

### Syntax

*Visual Basic:*
```
Public Sub SetRSSILevelBlink( _
   ByVal blinkOn As Boolean _
)
```

### Parameters

blinkOn

True to switch the blinking on, False to switch it off.

### Remarks

This refers to a LED whose blinking frequency indicates the signal level value.


---

## SetSensitivity Method

*Quelle: `Polytec_IO_VibInterfaces~ISensorHead~SetSensitivity.html` · Polytec IO VibInterfaces Type Library · ISensorHead Interface : SetSensitivity Method*

### Description

Sets the sensitivity state of the sensor head.

### Syntax

*Visual Basic:*
```
Public Sub SetSensitivity( _
   ByVal SensitivityState As SensitivityState _
)
```

### Parameters

SensitivityState

| Value | Description |
|---|---|
| SensitivityState_High | The sensitivity is high. |
| SensitivityState_Normal | The sensitivity is normal. |
The sensitivity state.


---

## StartAutoFocus Method

*Quelle: `Polytec_IO_VibInterfaces~ISensorHead~StartAutoFocus.html` · Polytec IO VibInterfaces Type Library · ISensorHead Interface : StartAutoFocus Method*

### Description

Starts the automatic focusing process.

### Syntax

*Visual Basic:*
```
Public Sub StartAutoFocus()
```


---

## StartAutoFocusInArea Method

*Quelle: `Polytec_IO_VibInterfaces~ISensorHead~StartAutoFocusInArea.html` · Polytec IO VibInterfaces Type Library · ISensorHead Interface : StartAutoFocusInArea Method*

### Description

Starts the automatic focusing process limited to the given area.

### Syntax

*Visual Basic:*
```
Public Sub StartAutoFocusInArea( _
   ByVal lowerBound As Long, _
   ByVal upperBound As Long _
)
```

### Parameters

lowerBound

The lower bound of the autofocus area in focus step.

upperBound

The upper bound of the autofocus area in focus step.

### Remarks

The limitation to the area saves time compared to an autofocus covering the complete area.


---

## StartAutoFocusInRange Method

*Quelle: `Polytec_IO_VibInterfaces~ISensorHead~StartAutoFocusInRange.html` · Polytec IO VibInterfaces Type Library · ISensorHead Interface : StartAutoFocusInRange Method*

### Description

Starts the automatic focusing process limited to the given range.

### Syntax

*Visual Basic:*
```
Public Sub StartAutoFocusInRange( _
   ByVal AutoFocusRange As AutoFocusRange _
)
```

### Parameters

AutoFocusRange

| Value | Description |
|---|---|
| AutoFocusRange_Full | Full range. |
| AutoFocusRange_Medium | Medium range. |
| AutoFocusRange_Small | Small range. |
The autofocus range.

### Remarks

The limitation of the range saves time compared to an autofocus covering the full range.


---

## StartFocusStepReference Method

*Quelle: `Polytec_IO_VibInterfaces~ISensorHead~StartFocusStepReference.html` · Polytec IO VibInterfaces Type Library · ISensorHead Interface : StartFocusStepReference Method*

### Description

Starts the focus step reference run.

### Syntax

*Visual Basic:*
```
Public Sub StartFocusStepReference()
```

### Remarks

The laser focusing unit will travel to the reference position.


---

## StartSeekFocusStepDeviation Method

*Quelle: `Polytec_IO_VibInterfaces~ISensorHead~StartSeekFocusStepDeviation.html` · Polytec IO VibInterfaces Type Library · ISensorHead Interface : StartSeekFocusStepDeviation Method*

### Description

Starts the laser focusing unit to seek for focus step deviations.

### Syntax

*Visual Basic:*
```
Public Sub StartSeekFocusStepDeviation()
```

### Remarks

The laser focusing unit will travel to the reference position and will report the deviation of the current focus position from the target focus position.


---

## StopFocus Method

*Quelle: `Polytec_IO_VibInterfaces~ISensorHead~StopFocus.html` · Polytec IO VibInterfaces Type Library · ISensorHead Interface : StopFocus Method*

### Description

Stops a focusing process started with SetFocusPosition.

### Syntax

*Visual Basic:*
```
Public Sub StopFocus()
```


---

## Update Method

*Quelle: `Polytec_IO_VibInterfaces~ISensorHead~Update.html` · Polytec IO VibInterfaces Type Library · ISensorHead Interface : Update Method*

### Description

Updates the sensor head status.

### Syntax

*Visual Basic:*
```
Public Sub Update()
```

### Remarks

The sensor status is updated periodically. By calling this method you can force an update.


---

## UpdateFocusPosition Method

*Quelle: `Polytec_IO_VibInterfaces~ISensorHead~UpdateFocusPosition.html` · Polytec IO VibInterfaces Type Library · ISensorHead Interface : UpdateFocusPosition Method*

### Description

Reads the focus position from the hardware and updates the FocusPosition property.

### Syntax

*Visual Basic:*
```
Public Sub UpdateFocusPosition()
```


---

## AlignmentLaserShutterOpen Property

*Quelle: `Polytec_IO_VibInterfaces~ISensorHead~AlignmentLaserShutterOpen.html` · Polytec IO VibInterfaces Type Library · ISensorHead Interface : AlignmentLaserShutterOpen Property*

### Description

Returns true if the alignment laser shutter is open.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property AlignmentLaserShutterOpen As Boolean
```

### Return Type

True, if the alignment laser shutter is open, i.e. that the sensor head is in alignment mode.

### Example


---

## AutoFocusAreaLowerBound Property

*Quelle: `Polytec_IO_VibInterfaces~ISensorHead~AutoFocusAreaLowerBound.html` · Polytec IO VibInterfaces Type Library · ISensorHead Interface : AutoFocusAreaLowerBound Property*

### Description

Gets the current autofocus area lower bound, which has been set by SetAutoFocusArea().

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property AutoFocusAreaLowerBound As Long
```

### Return Type

The autofocus area lower bound.


---

## AutoFocusAreaUpperBound Property

*Quelle: `Polytec_IO_VibInterfaces~ISensorHead~AutoFocusAreaUpperBound.html` · Polytec IO VibInterfaces Type Library · ISensorHead Interface : AutoFocusAreaUpperBound Property*

### Description

Gets the current autofocus area upper bound, which has been set by SetAutoFocusArea().

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property AutoFocusAreaUpperBound As Long
```

### Return Type

The autofocus area upper bound.


---

## AutoFocusInProgress Property

*Quelle: `Polytec_IO_VibInterfaces~ISensorHead~AutoFocusInProgress.html` · Polytec IO VibInterfaces Type Library · ISensorHead Interface : AutoFocusInProgress Property*

### Description

Indicates whether an autofocusing process is active or not.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property AutoFocusInProgress As Boolean
```

### Example


---

## AutoFocusState Property

*Quelle: `Polytec_IO_VibInterfaces~ISensorHead~AutoFocusState.html` · Polytec IO VibInterfaces Type Library · ISensorHead Interface : AutoFocusState Property*

### Description

The result of an automatic focusing process.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property AutoFocusState As AutoFocusResult
```


---

## CoherenceOptimizerOn Property

*Quelle: `Polytec_IO_VibInterfaces~ISensorHead~CoherenceOptimizerOn.html` · Polytec IO VibInterfaces Type Library · ISensorHead Interface : CoherenceOptimizerOn Property*

### Description

Returns true if the coherence optimizer is on.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property CoherenceOptimizerOn As Boolean
```

### Example


---

## CoherenceOptimizerPower Property

*Quelle: `Polytec_IO_VibInterfaces~ISensorHead~CoherenceOptimizerPower.html` · Polytec IO VibInterfaces Type Library · ISensorHead Interface : CoherenceOptimizerPower Property*

### Description

Gets the current control power level of the coherence optimizer control circuit.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property CoherenceOptimizerPower As Long
```

### Return Type

The control power level in percent (0 - 100).


---

## CoherenceOptimizerStatus Property

*Quelle: `Polytec_IO_VibInterfaces~ISensorHead~CoherenceOptimizerStatus.html` · Polytec IO VibInterfaces Type Library · ISensorHead Interface : CoherenceOptimizerStatus Property*

### Description

The current status of the coherence optimizer control circuit.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property CoherenceOptimizerStatus As CoherenceOptimizerStatusValue
```


---

## externalScannerControlOn Property

*Quelle: `Polytec_IO_VibInterfaces~ISensorHead~externalScannerControlOn.html` · Polytec IO VibInterfaces Type Library · ISensorHead Interface : externalScannerControlOn Property*

### Description

Returns true if the external scanner control is on.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property externalScannerControlOn As Boolean
```


---

## FocusInProgress Property

*Quelle: `Polytec_IO_VibInterfaces~ISensorHead~FocusInProgress.html` · Polytec IO VibInterfaces Type Library · ISensorHead Interface : FocusInProgress Property*

### Description

Indicates whether a focusing process is active or not.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property FocusInProgress As Boolean
```


---

## FocusLimit Property

*Quelle: `Polytec_IO_VibInterfaces~ISensorHead~FocusLimit.html` · Polytec IO VibInterfaces Type Library · ISensorHead Interface : FocusLimit Property*

### Description

Gets whether the focus motor is currently at one of its limit positions or not.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property FocusLimit As FocusLimitState
```


---

## FocusPosition Property

*Quelle: `Polytec_IO_VibInterfaces~ISensorHead~FocusPosition.html` · Polytec IO VibInterfaces Type Library · ISensorHead Interface : FocusPosition Property*

### Description

The focus position.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property FocusPosition As Long
```


---

## FocusStepReferenceInProgress Property

*Quelle: `Polytec_IO_VibInterfaces~ISensorHead~FocusStepReferenceInProgress.html` · Polytec IO VibInterfaces Type Library · ISensorHead Interface : FocusStepReferenceInProgress Property*

### Description

Indicates whether a reference run of the laser focusing unit is in progress or not.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property FocusStepReferenceInProgress As Boolean
```


---

## Key Property

*Quelle: `Polytec_IO_VibInterfaces~ISensorHead~Key.html` · Polytec IO VibInterfaces Type Library · ISensorHead Interface : Key Property*

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

## LaserOn Property

*Quelle: `Polytec_IO_VibInterfaces~ISensorHead~LaserOn.html` · Polytec IO VibInterfaces Type Library · ISensorHead Interface : LaserOn Property*

### Description

Returns true if the laser is on.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property LaserOn As Boolean
```


---

## LaserTemperature Property

*Quelle: `Polytec_IO_VibInterfaces~ISensorHead~LaserTemperature.html` · Polytec IO VibInterfaces Type Library · ISensorHead Interface : LaserTemperature Property*

### Description

The laser temperature in degree Celsius.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property LaserTemperature As Double
```


---

## LaserTemperatureOutOfRange Property

*Quelle: `Polytec_IO_VibInterfaces~ISensorHead~LaserTemperatureOutOfRange.html` · Polytec IO VibInterfaces Type Library · ISensorHead Interface : LaserTemperatureOutOfRange Property*

### Description

Returns true if the laser temperature is out of range.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property LaserTemperatureOutOfRange As Boolean
```


---

## LaserWavelengthStable Property

*Quelle: `Polytec_IO_VibInterfaces~ISensorHead~LaserWavelengthStable.html` · Polytec IO VibInterfaces Type Library · ISensorHead Interface : LaserWavelengthStable Property*

### Description

Returns true if the laser wavelength is stable and false if it is still stabilizing.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property LaserWavelengthStable As Boolean
```


---

## ManualFocusLock Property

*Quelle: `Polytec_IO_VibInterfaces~ISensorHead~ManualFocusLock.html` · Polytec IO VibInterfaces Type Library · ISensorHead Interface : ManualFocusLock Property*

### Description

Indicates whether the hardware focus-ring is coupled or not coupled to the focusing unit.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property ManualFocusLock As Boolean
```

### Remarks

A coupled focus ring (ManualFocusLock is true) indicates that manual focusing is disabled. Otherwise (ManualFocusLock is false) the focus ring is not coupled to the focusing unit and manual focusing is enabled.


---

## Name Property

*Quelle: `Polytec_IO_VibInterfaces~ISensorHead~Name.html` · Polytec IO VibInterfaces Type Library · ISensorHead Interface : Name Property*

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

## ObjectiveTemperature Property

*Quelle: `Polytec_IO_VibInterfaces~ISensorHead~ObjectiveTemperature.html` · Polytec IO VibInterfaces Type Library · ISensorHead Interface : ObjectiveTemperature Property*

### Description

Returns the temperature of the objective in degree Celsius.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property ObjectiveTemperature As Double
```

### Example


---

## QTecOn Property

*Quelle: `Polytec_IO_VibInterfaces~ISensorHead~QTecOn.html` · Polytec IO VibInterfaces Type Library · ISensorHead Interface : QTecOn Property*

### Description

Returns true if QTec mode is on.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property QTecOn As Boolean
```

### Remarks

To switch the QTec mode on or off use the SetQTecOn Method.


---

## Reticle Property

*Quelle: `Polytec_IO_VibInterfaces~ISensorHead~Reticle.html` · Polytec IO VibInterfaces Type Library · ISensorHead Interface : Reticle Property*

### Description

The current reticle of the sensor head.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Reticle As String
```


---

## RGBLedColorIndex Property

*Quelle: `Polytec_IO_VibInterfaces~ISensorHead~RGBLedColorIndex.html` · Polytec IO VibInterfaces Type Library · ISensorHead Interface : RGBLedColorIndex Property*

### Description

Gets the zero-based index of the RGB color of the LED.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property RGBLedColorIndex As Long
```

### Return Type

The zero-based index of the color.


---

## RSSILevelBlink Property

*Quelle: `Polytec_IO_VibInterfaces~ISensorHead~RSSILevelBlink.html` · Polytec IO VibInterfaces Type Library · ISensorHead Interface : RSSILevelBlink Property*

### Description

Gets a Boolean indicating whether the RSSI level blinking is switched on or off.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property RSSILevelBlink As Boolean
```

### Return Type

True if the blinking is switched on, False if it is switched off.


---

## SeekFocusStepDeviationInProgress Property

*Quelle: `Polytec_IO_VibInterfaces~ISensorHead~SeekFocusStepDeviationInProgress.html` · Polytec IO VibInterfaces Type Library · ISensorHead Interface : SeekFocusStepDeviationInProgress Property*

### Description

Indicates whether the laser focusing currently seeks for focus step deviations.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property SeekFocusStepDeviationInProgress As Boolean
```


---

## SeekFocusStepDeviationResult Property

*Quelle: `Polytec_IO_VibInterfaces~ISensorHead~SeekFocusStepDeviationResult.html` · Polytec IO VibInterfaces Type Library · ISensorHead Interface : SeekFocusStepDeviationResult Property*

### Description

Gets the result of the seek for focus step deviations process.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property SeekFocusStepDeviationResult As Long
```

### Return Type

Returns the deviation of the current focus position from the target focus position in focusing unit steps.


---

## Sensitivity Property

*Quelle: `Polytec_IO_VibInterfaces~ISensorHead~Sensitivity.html` · Polytec IO VibInterfaces Type Library · ISensorHead Interface : Sensitivity Property*

### Description

The sensitivity state of the sensor head.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Sensitivity As SensitivityState
```


---

## SensorHeadInfo Property

*Quelle: `Polytec_IO_VibInterfaces~ISensorHead~SensorHeadInfo.html` · Polytec IO VibInterfaces Type Library · ISensorHead Interface : SensorHeadInfo Property*

### Description

The information about the sensor head.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property SensorHeadInfo As SensorHeadInfo
```


---

## SignalBalance Property

*Quelle: `Polytec_IO_VibInterfaces~ISensorHead~SignalBalance.html` · Polytec IO VibInterfaces Type Library · ISensorHead Interface : SignalBalance Property*

### Description

The balance of the signal.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property SignalBalance As SignalBalanceState
```


---

## SignalLevel Property

*Quelle: `Polytec_IO_VibInterfaces~ISensorHead~SignalLevel.html` · Polytec IO VibInterfaces Type Library · ISensorHead Interface : SignalLevel Property*

### Description

The level of the signal in percent.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property SignalLevel As Double
```


---

## SignalLevelB Property

*Quelle: `Polytec_IO_VibInterfaces~ISensorHead~SignalLevelB.html` · Polytec IO VibInterfaces Type Library · ISensorHead Interface : SignalLevelB Property*

### Description

The level of the signal B of the sensor head in percent.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property SignalLevelB As Double
```

### Example


---

## Temperature Property

*Quelle: `Polytec_IO_VibInterfaces~ISensorHead~Temperature.html` · Polytec IO VibInterfaces Type Library · ISensorHead Interface : Temperature Property*

### Description

The current temperature of the sensor head in degree Celsius.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Temperature As Double
```


---

## TemperatureState Property

*Quelle: `Polytec_IO_VibInterfaces~ISensorHead~TemperatureState.html` · Polytec IO VibInterfaces Type Library · ISensorHead Interface : TemperatureState Property*

### Description

The current temperature state of the sensor head.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property TemperatureState As SensorHeadTemperatureState
```


---

## VideoCamera Property

*Quelle: `Polytec_IO_VibInterfaces~ISensorHead~VideoCamera.html` · Polytec IO VibInterfaces Type Library · ISensorHead Interface : VideoCamera Property*

### Description

The video camera of the sensor head.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property VideoCamera As IVideoCamera
```
