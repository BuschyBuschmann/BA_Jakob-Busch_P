# PolyScanHeadLib – IDistanceSensorControl

## IDistanceSensorControl Interface

*Quelle: `PolyScanHeadLib~IDistanceSensorControl.html` · Polytec PolyScanHead Type Library*

### Description

Controls the distance sensor (geometry scan unit, PSV-A-420, PSV-G-500).

### Object Model

### Remarks

It is recommended to cast to the DistanceSensorControl object.


---

## IDistanceSensorControl Interface Members

*Quelle: `PolyScanHeadLib~IDistanceSensorControl_members.html` · Polytec PolyScanHead Type Library*

### Public Methods

| ConnectSensor | Connects the distance sensor at given RS232 port. |
|---|---|
| ConnectSimulation | Connects the distance sensor simulation for test. |
| Disconnect | Disconnects the geometry scan unit. |
| GetDistance | Returns the measured distance. |
| MeasureDistance | Starts a distance measurement. |

### Public Properties

| Connected | Returns true, if the geometry scan unit is connected. |
|---|---|
| FilterOn | Returns true if the filter of the geometry scan unit is switched on. |
| LaserOn | Returns true if the geometry laser is on or switches the geometry laser on or off. |
| ScanHeadDevice | Returns the ScanHeadDevice object. |
| Type | The type of the distance sensor. |


---

## ConnectSensor Method

*Quelle: `PolyScanHeadLib~IDistanceSensorControl~ConnectSensor.html` · Polytec PolyScanHead Type Library · IDistanceSensorControl Interface : ConnectSensor Method*

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

*Quelle: `PolyScanHeadLib~IDistanceSensorControl~ConnectSimulation.html` · Polytec PolyScanHead Type Library · IDistanceSensorControl Interface : ConnectSimulation Method*

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

*Quelle: `PolyScanHeadLib~IDistanceSensorControl~Disconnect.html` · Polytec PolyScanHead Type Library · IDistanceSensorControl Interface : Disconnect Method*

### Description

Disconnects the geometry scan unit.

### Syntax

*Visual Basic:*
```
Public Sub Disconnect()
```


---

## GetDistance Method

*Quelle: `PolyScanHeadLib~IDistanceSensorControl~GetDistance.html` · Polytec PolyScanHead Type Library · IDistanceSensorControl Interface : GetDistance Method*

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

## MeasureDistance Method

*Quelle: `PolyScanHeadLib~IDistanceSensorControl~MeasureDistance.html` · Polytec PolyScanHead Type Library · IDistanceSensorControl Interface : MeasureDistance Method*

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

## Connected Property

*Quelle: `PolyScanHeadLib~IDistanceSensorControl~Connected.html` · Polytec PolyScanHead Type Library · IDistanceSensorControl Interface : Connected Property*

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

*Quelle: `PolyScanHeadLib~IDistanceSensorControl~FilterOn.html` · Polytec PolyScanHead Type Library · IDistanceSensorControl Interface : FilterOn Property*

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

## LaserOn Property

*Quelle: `PolyScanHeadLib~IDistanceSensorControl~LaserOn.html` · Polytec PolyScanHead Type Library · IDistanceSensorControl Interface : LaserOn Property*

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

## ScanHeadDevice Property

*Quelle: `PolyScanHeadLib~IDistanceSensorControl~ScanHeadDevice.html` · Polytec PolyScanHead Type Library · IDistanceSensorControl Interface : ScanHeadDevice Property*

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

## Type Property

*Quelle: `PolyScanHeadLib~IDistanceSensorControl~Type.html` · Polytec PolyScanHead Type Library · IDistanceSensorControl Interface : Type Property*

### Description

The type of the distance sensor.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Type As PTCDistanceSensorType
```
