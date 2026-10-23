# PolyFrontEndLib – FrontEndControl

## FrontEndControl Object

*Quelle: `PolyFrontEndLib~FrontEndControl.html` · Polytec PolyFrontEnd Type Library*

### Description

The FrontEndControl object controls the hardware of the front-end.

### Object Model

### Remarks

This object is only available for controllable front-ends. See the Caps property to find out, if a front-end is controllable.


---

## FrontEndControl Object Members

*Quelle: `PolyFrontEndLib~FrontEndControl_members.html` · Polytec PolyFrontEnd Type Library*

### Public Methods

| AuxOutPulse | Generates a pulse at the AuxOut digital i/o line with the specified level and duration. |
|---|---|
| GetFrontendDevice | Queries a front-end device. |
| TriggerNextScannerPosition | Triggers the next scanner position. |

### Public Properties

| AuxInState | Returns the current state of the AuxIn digital input line. |
|---|---|
| AuxOutMode | Specifies the mode of the SYNC output of the VibroScan. |
| AuxOutState | Specifies the current state of the Aux digital output line. |
| Caps | The front-end control capabilities. |
| ContinuousIlluminationIntensity | Specifies the continuous illumination intensity. |
| DifferentialInputEnabled | Specifies whether differential input is enabled. |
| DioDac | Returns the object to control the digital analog converters and the digital i/o lines of the junction box. |
| FrontEnd | The parent front-end object. |
| GeneratorAmplifierEnabled | Specifies whether the generator amplifier is enabled. |
| GeneratorAmplifierFactor | Returns the amplification factor of the generator amplifier. |
| GeneratorOutEnabled | Specifies whether the generator output is enabled. |
| ICPEnabled | Specifies whether ICP is active for the channels. |
| ICPMask | Returns which channels support ICP. |
| IlluminationState | Specifies the illumination state. |
| LaserMask | The laser mask. |
| LaserOn | Specifies whether the lasers are on or off. |
| MaxAuxOutPulseDuration | The maximum auxiliary output pulse duration in µs. |
| MaxIlluminationIntensity | The maximum illumination intensity. |
| MinAuxOutPulseDuration | The minimum auxiliary output pulse duration in µs. |
| MinIlluminationIntensity | The minimum illumination intensity. |
| OperatingState | Specifies the operating state of the junction box. |
| RangeFinderEnabled | Specifies whether the distance sensor is enabled. |
| RangeFinderInProgress | Returns while the mirror for the distance sensor is moving. |
| StrobeIlluminationIntensity | Specifies the strobe illumination intensity. |
| StrobeLatency | The strobe latency in s. |
| SuppressDataByScannerMovement | Specifies whether the front-end suppresses data while the scanners are moving by setting a corresponding bit in the data stream. |
| TriggerDelay | The delay of the trigger in second. |
| VideoMUXChannel | Specifies the active channel of the video multiplexer. |


---

## AuxOutPulse Method

*Quelle: `PolyFrontEndLib~FrontEndControl~AuxOutPulse.html` · Polytec PolyFrontEnd Type Library · FrontEndControl Object : AuxOutPulse Method*

### Description

Generates a pulse at the AuxOut digital i/o line with the specified level and duration.

### Syntax

*Visual Basic:*
```
Public Function AuxOutPulse( _
   ByVal vbHigh As Boolean, _
   ByVal lDurationTarget As Long _
) As Long
```

### Parameters

vbHigh

If true, the level of the pulse is high.

lDurationTarget

The target duration of the pulse in µs.

### Return Type

The actual duration of the pulse in µs.


---

## GetFrontendDevice Method

*Quelle: `PolyFrontEndLib~FrontEndControl~GetFrontendDevice.html` · Polytec PolyFrontEnd Type Library · FrontEndControl Object : GetFrontendDevice Method*

### Description

Queries a front-end device.

### Syntax

*Visual Basic:*
```
Public Function GetFrontendDevice( _
   ByVal deviceType As PTCFrontEndDeviceType _
) As Object
```

### Parameters

deviceType

| Value | Description |
|---|---|
| ptcAdcBoardDevice0 | The first analog to digital converter board. |
| ptcAdcBoardDevice1 | The second analog to digital converter board. |
| ptcAdcBoardDevice2 | The third analog to digital converter board. |
| ptcAdcBoardDevice3 | The fourth analog to digital converter board. |
| ptcAdcBoardDevice4 | The fifth analog to digital converter board. |
| ptcDacBoardDevice | The digital to analog converter board. |
| ptcDigitalIODevice | The digital i/o device. |
| ptcPanTiltHeadDevice | The pan tilt head device. |
The type of the front-end device to query.


---

## TriggerNextScannerPosition Method

*Quelle: `PolyFrontEndLib~FrontEndControl~TriggerNextScannerPosition.html` · Polytec PolyFrontEnd Type Library · FrontEndControl Object : TriggerNextScannerPosition Method*

### Description

Triggers the next scanner position.

### Syntax

*Visual Basic:*
```
Public Sub TriggerNextScannerPosition()
```


---

## AuxInState Property

*Quelle: `PolyFrontEndLib~FrontEndControl~AuxInState.html` · Polytec PolyFrontEnd Type Library · FrontEndControl Object : AuxInState Property*

### Description

Returns the current state of the AuxIn digital input line.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property AuxInState As PTCFrontEndAuxStateType
```


---

## AuxOutMode Property

*Quelle: `PolyFrontEndLib~FrontEndControl~AuxOutMode.html` · Polytec PolyFrontEnd Type Library · FrontEndControl Object : AuxOutMode Property*

### Description

Specifies the mode of the SYNC output of the VibroScan.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property AuxOutMode As PTCFrontEndAuxOutModeType
```

### Remarks

By setting the corresponding value, you can use the SYNC output of the VibroScan either as Aux Out output or as SYNC signal of the generator. When setting the level of the Aux Out output via the AuxOutState Property the mode is automatically set to Aux Out.

### Example

- Example (VB.NET)

```
Sub Main
	Debug.Clear
	Dim oFrontEnd As FrontEnd = Application.Acquisition.Infos.Hardware.ActiveFrontEnd
	Dim oFrontEndControl As FrontEndControl = oFrontEnd.Control
	Dim currentAuxOutMode As PTCFrontEndAuxOutModeType = oFrontEndControl.AuxOutMode

	oFrontEndControl.AuxOutState = PTCFrontEndAuxStateType.ptcFrontEndAuxStateHighPulse
	Dim tempMode As Integer = oFrontEndControl.AuxOutMode
	Debug.WriteLine("OutMode: " + tempMode.ToString())

	oFrontEndControl.AuxOutMode = PTCFrontEndAuxOutModeType.ptcFrontEndAuxOutModeSync
	tempMode  = oFrontEndControl.AuxOutMode
	Debug.WriteLine("OutMode: " + tempMode.ToString())

	oFrontEndControl.AuxOutState = PTCFrontEndAuxStateType.ptcFrontEndAuxStateHighPulse
	tempMode  = oFrontEndControl.AuxOutMode
	Debug.WriteLine("OutMode: " + tempMode.ToString())

	oFrontEndControl.AuxOutMode = currentAuxOutMode
	tempMode  = oFrontEndControl.AuxOutMode
	Debug.WriteLine("OutMode: " + tempMode.ToString())

End Sub
```


---

## AuxOutState Property

*Quelle: `PolyFrontEndLib~FrontEndControl~AuxOutState.html` · Polytec PolyFrontEnd Type Library · FrontEndControl Object : AuxOutState Property*

### Description

Specifies the current state of the Aux digital output line.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property AuxOutState As PTCFrontEndAuxStateType
```


---

## Caps Property

*Quelle: `PolyFrontEndLib~FrontEndControl~Caps.html` · Polytec PolyFrontEnd Type Library · FrontEndControl Object : Caps Property*

### Description

The front-end control capabilities.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Caps As PTCFrontEndControlCapsType
```

### Remarks

Not all front-end control objects have the same capabilities. Use this property to find out which capabilities are available.


---

## ContinuousIlluminationIntensity Property

*Quelle: `PolyFrontEndLib~FrontEndControl~ContinuousIlluminationIntensity.html` · Polytec PolyFrontEnd Type Library · FrontEndControl Object : ContinuousIlluminationIntensity Property*

### Description

Specifies the continuous illumination intensity.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property ContinuousIlluminationIntensity As Long
```


---

## DifferentialInputEnabled Property

*Quelle: `PolyFrontEndLib~FrontEndControl~DifferentialInputEnabled.html` · Polytec PolyFrontEnd Type Library · FrontEndControl Object : DifferentialInputEnabled Property*

### Description

Specifies whether differential input is enabled.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property DifferentialInputEnabled As Boolean
```


---

## DioDac Property

*Quelle: `PolyFrontEndLib~FrontEndControl~DioDac.html` · Polytec PolyFrontEnd Type Library · FrontEndControl Object : DioDac Property*

### Description

Returns the object to control the digital analog converters and the digital i/o lines of the junction box.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property DioDac As FrontEndControlDioDac
```


---

## FrontEnd Property

*Quelle: `PolyFrontEndLib~FrontEndControl~FrontEnd.html` · Polytec PolyFrontEnd Type Library · FrontEndControl Object : FrontEnd Property*

### Description

The parent front-end object.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property FrontEnd As IFrontEnd
```


---

## GeneratorAmplifierEnabled Property

*Quelle: `PolyFrontEndLib~FrontEndControl~GeneratorAmplifierEnabled.html` · Polytec PolyFrontEnd Type Library · FrontEndControl Object : GeneratorAmplifierEnabled Property*

### Description

Specifies whether the generator amplifier is enabled.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property GeneratorAmplifierEnabled As Boolean
```


---

## GeneratorAmplifierFactor Property

*Quelle: `PolyFrontEndLib~FrontEndControl~GeneratorAmplifierFactor.html` · Polytec PolyFrontEnd Type Library · FrontEndControl Object : GeneratorAmplifierFactor Property*

### Description

Returns the amplification factor of the generator amplifier.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property GeneratorAmplifierFactor As Double
```


---

## GeneratorOutEnabled Property

*Quelle: `PolyFrontEndLib~FrontEndControl~GeneratorOutEnabled.html` · Polytec PolyFrontEnd Type Library · FrontEndControl Object : GeneratorOutEnabled Property*

### Description

Specifies whether the generator output is enabled.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property GeneratorOutEnabled As Boolean
```


---

## ICPEnabled Property

*Quelle: `PolyFrontEndLib~FrontEndControl~ICPEnabled.html` · Polytec PolyFrontEnd Type Library · FrontEndControl Object : ICPEnabled Property*

### Description

Specifies whether ICP is active for the channels.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property ICPEnabled As Long
```

### Remarks

The bit 0 of the value corresponds to channel 1, bit 1 to channel 2 etc. See the ICPMask property to find out, which channels support ICP.


---

## ICPMask Property

*Quelle: `PolyFrontEndLib~FrontEndControl~ICPMask.html` · Polytec PolyFrontEnd Type Library · FrontEndControl Object : ICPMask Property*

### Description

Returns which channels support ICP.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property ICPMask As Long
```

### Remarks

The bit 0 of the value corresponds to channel 1, bit 1 to channel 2 etc.


---

## IlluminationState Property

*Quelle: `PolyFrontEndLib~FrontEndControl~IlluminationState.html` · Polytec PolyFrontEnd Type Library · FrontEndControl Object : IlluminationState Property*

### Description

Specifies the illumination state.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property IlluminationState As PTCFrontEndIlluminationStateType
```


---

## LaserMask Property

*Quelle: `PolyFrontEndLib~FrontEndControl~LaserMask.html` · Polytec PolyFrontEnd Type Library · FrontEndControl Object : LaserMask Property*

### Description

The laser mask.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property LaserMask As PTCFrontEndLaserType
```

### Remarks

Values set in this mask can be set to the LaserOn property.


---

## LaserOn Property

*Quelle: `PolyFrontEndLib~FrontEndControl~LaserOn.html` · Polytec PolyFrontEnd Type Library · FrontEndControl Object : LaserOn Property*

### Description

Specifies whether the lasers are on or off.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property LaserOn As PTCFrontEndLaserType
```

### Remarks

See the LaserMask property for allowed values for this property.


---

## MaxAuxOutPulseDuration Property

*Quelle: `PolyFrontEndLib~FrontEndControl~MaxAuxOutPulseDuration.html` · Polytec PolyFrontEnd Type Library · FrontEndControl Object : MaxAuxOutPulseDuration Property*

### Description

The maximum auxiliary output pulse duration in µs.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property MaxAuxOutPulseDuration As Long
```


---

## MaxIlluminationIntensity Property

*Quelle: `PolyFrontEndLib~FrontEndControl~MaxIlluminationIntensity.html` · Polytec PolyFrontEnd Type Library · FrontEndControl Object : MaxIlluminationIntensity Property*

### Description

The maximum illumination intensity.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property MaxIlluminationIntensity As Long
```


---

## MinAuxOutPulseDuration Property

*Quelle: `PolyFrontEndLib~FrontEndControl~MinAuxOutPulseDuration.html` · Polytec PolyFrontEnd Type Library · FrontEndControl Object : MinAuxOutPulseDuration Property*

### Description

The minimum auxiliary output pulse duration in µs.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property MinAuxOutPulseDuration As Long
```


---

## MinIlluminationIntensity Property

*Quelle: `PolyFrontEndLib~FrontEndControl~MinIlluminationIntensity.html` · Polytec PolyFrontEnd Type Library · FrontEndControl Object : MinIlluminationIntensity Property*

### Description

The minimum illumination intensity.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property MinIlluminationIntensity As Long
```


---

## OperatingState Property

*Quelle: `PolyFrontEndLib~FrontEndControl~OperatingState.html` · Polytec PolyFrontEnd Type Library · FrontEndControl Object : OperatingState Property*

### Description

Specifies the operating state of the junction box.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property OperatingState As PTCFrontEndOperatingStateType
```


---

## RangeFinderEnabled Property

*Quelle: `PolyFrontEndLib~FrontEndControl~RangeFinderEnabled.html` · Polytec PolyFrontEnd Type Library · FrontEndControl Object : RangeFinderEnabled Property*

### Description

Specifies whether the distance sensor is enabled.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property RangeFinderEnabled As Boolean
```

### Remarks

Changing this property causes a mirror to move in the scanning head. This takes some time. See the RangeFinderInProgress property to find out, if the mirror is still moving.


---

## RangeFinderInProgress Property

*Quelle: `PolyFrontEndLib~FrontEndControl~RangeFinderInProgress.html` · Polytec PolyFrontEnd Type Library · FrontEndControl Object : RangeFinderInProgress Property*

### Description

Returns while the mirror for the distance sensor is moving.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property RangeFinderInProgress As Boolean
```

### Remarks

Changing RangeFinderEnabled Property causes a mirror to move in the scanning head. This takes some time. While the mirror is moving, this property returns true.


---

## StrobeIlluminationIntensity Property

*Quelle: `PolyFrontEndLib~FrontEndControl~StrobeIlluminationIntensity.html` · Polytec PolyFrontEnd Type Library · FrontEndControl Object : StrobeIlluminationIntensity Property*

### Description

Specifies the strobe illumination intensity.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property StrobeIlluminationIntensity As Long
```


---

## StrobeLatency Property

*Quelle: `PolyFrontEndLib~FrontEndControl~StrobeLatency.html` · Polytec PolyFrontEnd Type Library · FrontEndControl Object : StrobeLatency Property*

### Description

The strobe latency in s.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property StrobeLatency As Double
```

### Example


---

## SuppressDataByScannerMovement Property

*Quelle: `PolyFrontEndLib~FrontEndControl~SuppressDataByScannerMovement.html` · Polytec PolyFrontEnd Type Library · FrontEndControl Object : SuppressDataByScannerMovement Property*

### Description

Specifies whether the front-end suppresses data while the scanners are moving by setting a corresponding bit in the data stream.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property SuppressDataByScannerMovement As Boolean
```

### Example


---

## TriggerDelay Property

*Quelle: `PolyFrontEndLib~FrontEndControl~TriggerDelay.html` · Polytec PolyFrontEnd Type Library · FrontEndControl Object : TriggerDelay Property*

### Description

The delay of the trigger in second.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property TriggerDelay As Double
```


---

## VideoMUXChannel Property

*Quelle: `PolyFrontEndLib~FrontEndControl~VideoMUXChannel.html` · Polytec PolyFrontEnd Type Library · FrontEndControl Object : VideoMUXChannel Property*

### Description

Specifies the active channel of the video multiplexer.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property VideoMUXChannel As Long
```
