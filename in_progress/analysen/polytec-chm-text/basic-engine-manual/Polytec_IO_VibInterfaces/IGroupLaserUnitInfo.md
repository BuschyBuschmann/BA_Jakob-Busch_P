# Polytec_IO_VibInterfaces – IGroupLaserUnitInfo

## IGroupLaserUnitInfo Interface

*Quelle: `Polytec_IO_VibInterfaces~IGroupLaserUnitInfo.html` · Polytec IO VibInterfaces Type Library*

### Description

Provides summary information about the group laser unit.


---

## IGroupLaserUnitInfo Interface Members

*Quelle: `Polytec_IO_VibInterfaces~IGroupLaserUnitInfo_members.html` · Polytec IO VibInterfaces Type Library*

### Public Methods

| HasCap | Returns True if and only if the specified capability is available. |
|---|---|

### Public Properties

| Caps | Gets the group laser unit capabilities. |
|---|---|
| MaxLaserOperationPointIndex | Gets the laser operating point index maximum. |
| MinLaserOperationPointIndex | Gets the laser operating point index minimum. |


---

## HasCap Method

*Quelle: `Polytec_IO_VibInterfaces~IGroupLaserUnitInfo~HasCap.html` · Polytec IO VibInterfaces Type Library · IGroupLaserUnitInfo Interface : HasCap Method*

### Description

Returns True if and only if the specified capability is available.

### Syntax

*Visual Basic:*
```
Public Function HasCap( _
   ByVal cap As GroupLaserUnitCaps _
) As Boolean
```

### Parameters

cap

| Value | Description |
|---|---|
| GroupLaserUnitCaps_LaserOperationPoint | The capability that the laser operation point can be changed. |
| GroupLaserUnitCaps_LaserShutter | The capability that the laser unit can be switched on and off. |
| GroupLaserUnitCaps_LaserTemperature | The capability that the laser temperature can be queried. |
| GroupLaserUnitCaps_LaserTemperatureOutOfRange | The capability that it can be queried whether the laser temperature is out of range. |
| GroupLaserUnitCaps_LaserWavelengthStabilization | The capability that it can be queried whether the laser wavelength is stable or still stabilizing. |
| GroupLaserUnitCaps_None | None of the capabilities is available. |
| GroupLaserUnitCaps_PilotLaserModulation | The capability that the pilot laser modulation can be switched on and off. |
| GroupLaserUnitCaps_PilotLaserShutter | The capability that the pilot laser unit can be switched on and off. |
| GroupLaserUnitCaps_ShifterFrequency | The capability that the shifter frequency can be queried. |
| GroupLaserUnitCaps_ShifterOperatingTemperature | The capability that the shifter operating temperature can be queried. |
| GroupLaserUnitCaps_ShifterRFLevel | The capability that the shifter RF level can be queried. |
The capability to query.

### Return Type

True if the specified capability is supported.


---

## Caps Property

*Quelle: `Polytec_IO_VibInterfaces~IGroupLaserUnitInfo~Caps.html` · Polytec IO VibInterfaces Type Library · IGroupLaserUnitInfo Interface : Caps Property*

### Description

Gets the group laser unit capabilities.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Caps As GroupLaserUnitCaps
```

### Return Type

The capabilities.


---

## MaxLaserOperationPointIndex Property

*Quelle: `Polytec_IO_VibInterfaces~IGroupLaserUnitInfo~MaxLaserOperationPointIndex.html` · Polytec IO VibInterfaces Type Library · IGroupLaserUnitInfo Interface : MaxLaserOperationPointIndex Property*

### Description

Gets the laser operating point index maximum.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property MaxLaserOperationPointIndex As Long
```

### Return Type

The laser operating point index maximum.


---

## MinLaserOperationPointIndex Property

*Quelle: `Polytec_IO_VibInterfaces~IGroupLaserUnitInfo~MinLaserOperationPointIndex.html` · Polytec IO VibInterfaces Type Library · IGroupLaserUnitInfo Interface : MinLaserOperationPointIndex Property*

### Description

Gets the laser operating point index minimum.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property MinLaserOperationPointIndex As Long
```

### Return Type

The laser operating point index minimum.
