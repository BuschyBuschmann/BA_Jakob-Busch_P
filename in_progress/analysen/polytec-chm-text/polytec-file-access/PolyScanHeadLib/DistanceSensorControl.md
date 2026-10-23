# PolyScanHeadLib – DistanceSensorControl

## DistanceSensorControl Object

*Quelle: `PolyScanHeadLib~DistanceSensorControl.html` · Polytec PolyScanHead Type Library*

### Description

Controls the distance sensor (geometry scan unit, PSV-A-420, PSV-G-500).

### Object Model


---

## DistanceSensorControl Object Members

*Quelle: `PolyScanHeadLib~DistanceSensorControl_members.html` · Polytec PolyScanHead Type Library*

### Public Methods

| ConnectSensor | Connects the distance sensor at given RS232 port. |
|---|---|
| ConnectSimulation | Connects the distance sensor simulation for test. |
| Disconnect | Disconnects the geometry scan unit. |
| GetDistance | Returns the measured distance. |
| GetDistanceEx | Returns the measured distance. |
| HasCap | Checks whether the distance sensor has the specified capabilities. |
| MeasureDistance | Starts a distance measurement. |

### Public Properties

| Caps | The capabilities of the distance sensor. |
|---|---|
| Connected | Returns true, if the geometry scan unit is connected. |
| FilterOn | Returns true if the filter of the geometry scan unit is switched on. |
| FirmwareVersion | The firmware version of the distance sensor. |
| LaserOn | Returns true if the geometry laser is on or switches the geometry laser on or off. |
| Name | The name of the distance sensor. |
| RangeFinderEnabled | Returns or specifies whether the distance sensor laser is active. |
| RemoteFilter | Returns true if the filter of the geometry scan unit is remote controlled. |
| ScanHeadDevice | Returns the ScanHeadDevice object. |
| SignalLevel | Returns the current signal level. |
| SignalLevelThresholdMax | The maximum threshold for the signal level for a valid distance measurement. |
| SignalLevelThresholdMin | The minimum threshold for the signal level for a valid distance measurement. |
| Type | The type of the distance sensor. |
| UpdateSignalLevel | Returns or specifies whether the signal level is continuously updated. |


---

## ConnectSensor Method

*Quelle: `PolyScanHeadLib~DistanceSensorControl~ConnectSensor.html` · Polytec PolyScanHead Type Library · DistanceSensorControl Object : ConnectSensor Method*

### Description

Connects the distance sensor at given RS232 port.

### Syntax

*Visual Basic:*
```
Public Function ConnectSensor( _
   ByVal lPortAddr As Long, _
   ByRef ptcType As PTCDistanceSensorType _
) As String
```

### Parameters

lPortAddr

The address o the RS232 port.

ptcType

| Value | Description |
|---|---|
| ptcDistanceSensorDLS_A_15 | Distance sensor DLS-A-15. |
| ptcDistanceSensorDLS_A_15_Filter | Distance sensor DLS-A-15 with filter control. |
| ptcDistanceSensorG500 | Distance sensor PSV-G-500. |
| ptcDistanceSensorG600 | Distance sensor PSV-G-600. |
| ptcDistanceSensorLSM215 | Distance sensor LSM2-15. |
| ptcDistanceSensorNone | No distance sensor. |
| ptcDistanceSensorPSV700 | Distance sensor VibroScan |
| ptcDistanceSensorSimulation | Simulated distance sensor. |

The connected distance sensor type.


---

## ConnectSimulation Method

*Quelle: `PolyScanHeadLib~DistanceSensorControl~ConnectSimulation.html` · Polytec PolyScanHead Type Library · DistanceSensorControl Object : ConnectSimulation Method*

### Description

Connects the distance sensor simulation for test.

### Syntax

*Visual Basic:*
```
Public Function ConnectSimulation( _
   ByRef ptcType As PTCDistanceSensorType _
) As String
```

### Parameters

ptcType

| Value | Description |
|---|---|
| ptcDistanceSensorDLS_A_15 | Distance sensor DLS-A-15. |
| ptcDistanceSensorDLS_A_15_Filter | Distance sensor DLS-A-15 with filter control. |
| ptcDistanceSensorG500 | Distance sensor PSV-G-500. |
| ptcDistanceSensorG600 | Distance sensor PSV-G-600. |
| ptcDistanceSensorLSM215 | Distance sensor LSM2-15. |
| ptcDistanceSensorNone | No distance sensor. |
| ptcDistanceSensorPSV700 | Distance sensor VibroScan |
| ptcDistanceSensorSimulation | Simulated distance sensor. |
The connected distance sensor type.


---

## Disconnect Method

*Quelle: `PolyScanHeadLib~DistanceSensorControl~Disconnect.html` · Polytec PolyScanHead Type Library · DistanceSensorControl Object : Disconnect Method*

### Description

Disconnects the geometry scan unit.

### Syntax

*Visual Basic:*
```
Public Sub Disconnect()
```


---

## GetDistance Method

*Quelle: `PolyScanHeadLib~DistanceSensorControl~GetDistance.html` · Polytec PolyScanHead Type Library · DistanceSensorControl Object : GetDistance Method*

### Description

Returns the measured distance.

### Syntax

*Visual Basic:*
```
Public Function GetDistance( _
   ByRef pVal As PTCDistanceSensorMeasStatus, _
   ByRef bstrMessage As String _
) As Double
```

### Parameters

pVal

| Value | Description |
|---|---|
| ptcDistanceSensorMeasStatusFailed | Measurement failed. |
| ptcDistanceSensorMeasStatusInProgress | Measurement is in progress. |
| ptcDistanceSensorMeasStatusNotActive | Measurement not active. |
| ptcDistanceSensorMeasStatusSucceeded | Measurement succeeded. |
The status of the distance measurement.

bstrMessage

The error message.

### Return Type

The measured distance.


---

## GetDistanceEx Method

*Quelle: `PolyScanHeadLib~DistanceSensorControl~GetDistanceEx.html` · Polytec PolyScanHead Type Library · DistanceSensorControl Object : GetDistanceEx Method*

### Description

Returns the measured distance.

### Syntax

*Visual Basic:*
```
Public Function GetDistanceEx( _
   ByRef pVal As PTCDistanceSensorMeasStatusEx, _
   ByRef bstrMessage As String _
) As Double
```

### Parameters

pVal

| Value | Description |
|---|---|
| ptcDistanceSensorMeasStatusExFailed | Measurement failed. |
| ptcDistanceSensorMeasStatusExInProgress | Measurement is in progress. |
| ptcDistanceSensorMeasStatusExNotActive | Measurement not active. |
| ptcDistanceSensorMeasStatusExOptimal | Succeeded with optimal signal level. |
| ptcDistanceSensorMeasStatusExSucceeded | Measurement succeeded. |
| ptcDistanceSensorMeasStatusExTooBright | Failed with too much light. |
| ptcDistanceSensorMeasStatusExTooDark | Failed with too little light. |
The status of the distance measurement.

bstrMessage

The error message.


---

## HasCap Method

*Quelle: `PolyScanHeadLib~DistanceSensorControl~HasCap.html` · Polytec PolyScanHead Type Library · DistanceSensorControl Object : HasCap Method*

### Description

Checks whether the distance sensor has the specified capabilities.

### Syntax

*Visual Basic:*
```
Public Function HasCap( _
   ByVal capToTest As PTCDistanceSensorControlCaps _
) As Boolean
```

### Parameters

capToTest

| Value | Description |
|---|---|
| ptcDistanceSensorControlCapsFirmwareVersion | The distance sensor has a firmware version. |
| ptcDistanceSensorControlCapsLaserOn | The distance sensor laser can be switched on and off. |
| ptcDistanceSensorControlCapsLaserOnAndSignalLevel | The distance sensor laser can be switched on and off and the laser has a signal level. |
| ptcDistanceSensorControlCapsNone | The distance sensor has no capabilities. |
| ptcDistanceSensorControlCapsRangeFinderEnabled | The distance sensor has a range finder enabled property. |
| ptcDistanceSensorControlCapsSignalLevel | The distance sensor has a signal level. |
The capabilities to check.

### Return Type

True if the distance sensor has the specified capabilities, false if not.


---

## MeasureDistance Method

*Quelle: `PolyScanHeadLib~DistanceSensorControl~MeasureDistance.html` · Polytec PolyScanHead Type Library · DistanceSensorControl Object : MeasureDistance Method*

### Description

Starts a distance measurement.

### Syntax

*Visual Basic:*
```
Public Sub MeasureDistance( _
   ByVal lAvgCount As Long _
)
```

### Parameters

lAvgCount

The number of averages.


---

## Caps Property

*Quelle: `PolyScanHeadLib~DistanceSensorControl~Caps.html` · Polytec PolyScanHead Type Library · DistanceSensorControl Object : Caps Property*

### Description

The capabilities of the distance sensor.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Caps As PTCDistanceSensorControlCaps
```

### Remarks

To check whether the distance sensor has certain capabilities use the HasCap Method.


---

## Connected Property

*Quelle: `PolyScanHeadLib~DistanceSensorControl~Connected.html` · Polytec PolyScanHead Type Library · DistanceSensorControl Object : Connected Property*

### Description

Returns true, if the geometry scan unit is connected.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Connected As Boolean
```


---

## FilterOn Property

*Quelle: `PolyScanHeadLib~DistanceSensorControl~FilterOn.html` · Polytec PolyScanHead Type Library · DistanceSensorControl Object : FilterOn Property*

### Description

Returns true if the filter of the geometry scan unit is switched on.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property FilterOn As Boolean
```


---

## FirmwareVersion Property

*Quelle: `PolyScanHeadLib~DistanceSensorControl~FirmwareVersion.html` · Polytec PolyScanHead Type Library · DistanceSensorControl Object : FirmwareVersion Property*

### Description

The firmware version of the distance sensor.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property FirmwareVersion As String
```


---

## LaserOn Property

*Quelle: `PolyScanHeadLib~DistanceSensorControl~LaserOn.html` · Polytec PolyScanHead Type Library · DistanceSensorControl Object : LaserOn Property*

### Description

Returns true if the geometry laser is on or switches the geometry laser on or off.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property LaserOn As Boolean
```

### Remarks

This property is not available for VibroScan systems. You can check this via HasCap Method passing the value ptcDistanceSensorControlCapsLaserOn.


---

## Name Property

*Quelle: `PolyScanHeadLib~DistanceSensorControl~Name.html` · Polytec PolyScanHead Type Library · DistanceSensorControl Object : Name Property*

### Description

The name of the distance sensor.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Name As String
```


---

## RangeFinderEnabled Property

*Quelle: `PolyScanHeadLib~DistanceSensorControl~RangeFinderEnabled.html` · Polytec PolyScanHead Type Library · DistanceSensorControl Object : RangeFinderEnabled Property*

### Description

Returns or specifies whether the distance sensor laser is active.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property RangeFinderEnabled As Boolean
```


---

## RemoteFilter Property

*Quelle: `PolyScanHeadLib~DistanceSensorControl~RemoteFilter.html` · Polytec PolyScanHead Type Library · DistanceSensorControl Object : RemoteFilter Property*

### Description

Returns true if the filter of the geometry scan unit is remote controlled.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property RemoteFilter As Boolean
```


---

## ScanHeadDevice Property

*Quelle: `PolyScanHeadLib~DistanceSensorControl~ScanHeadDevice.html` · Polytec PolyScanHead Type Library · DistanceSensorControl Object : ScanHeadDevice Property*

### Description

Returns the ScanHeadDevice object.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property ScanHeadDevice As IScanHeadDevice
```


---

## SignalLevel Property

*Quelle: `PolyScanHeadLib~DistanceSensorControl~SignalLevel.html` · Polytec PolyScanHead Type Library · DistanceSensorControl Object : SignalLevel Property*

### Description

Returns the current signal level.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property SignalLevel As Double
```

### Remarks

This property is not available for VibroScan systems. You can check this via HasCap Method passing the value ptcDistanceSensorControlCapsSignalLevel.


---

## SignalLevelThresholdMax Property

*Quelle: `PolyScanHeadLib~DistanceSensorControl~SignalLevelThresholdMax.html` · Polytec PolyScanHead Type Library · DistanceSensorControl Object : SignalLevelThresholdMax Property*

### Description

The maximum threshold for the signal level for a valid distance measurement.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property SignalLevelThresholdMax As Double
```

### Remarks

This property is not available for VibroScan systems. You can check this via HasCap Method passing the value ptcDistanceSensorControlCapsSignalLevel.


---

## SignalLevelThresholdMin Property

*Quelle: `PolyScanHeadLib~DistanceSensorControl~SignalLevelThresholdMin.html` · Polytec PolyScanHead Type Library · DistanceSensorControl Object : SignalLevelThresholdMin Property*

### Description

The minimum threshold for the signal level for a valid distance measurement.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property SignalLevelThresholdMin As Double
```

### Remarks

This property is not available for VibroScan systems. You can check this via HasCap Method passing the value ptcDistanceSensorControlCapsSignalLevel.


---

## Type Property

*Quelle: `PolyScanHeadLib~DistanceSensorControl~Type.html` · Polytec PolyScanHead Type Library · DistanceSensorControl Object : Type Property*

### Description

The type of the distance sensor.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Type As PTCDistanceSensorType
```


---

## UpdateSignalLevel Property

*Quelle: `PolyScanHeadLib~DistanceSensorControl~UpdateSignalLevel.html` · Polytec PolyScanHead Type Library · DistanceSensorControl Object : UpdateSignalLevel Property*

### Description

Returns or specifies whether the signal level is continuously updated.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property UpdateSignalLevel As Boolean
```

### Remarks

This property is not available for VibroScan systems. You can check this via HasCap Method passing the value ptcDistanceSensorControlCapsSignalLevel.
