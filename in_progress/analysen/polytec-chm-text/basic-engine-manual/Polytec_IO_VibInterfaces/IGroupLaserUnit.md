# Polytec_IO_VibInterfaces – IGroupLaserUnit

## IGroupLaserUnit Interface

*Quelle: `Polytec_IO_VibInterfaces~IGroupLaserUnit.html` · Polytec IO VibInterfaces Type Library*

### Description

This interface is provided for MPV, e.g. for the case where one laser unit is used for all sensor head lasers of the controller group. Thus, some commands are only available for such unit and are not supported for the individual sensor head laser units.

In particular, please note that this interface is not used to group individual sensor head laser units.

### Object Model


---

## IGroupLaserUnit Interface Members

*Quelle: `Polytec_IO_VibInterfaces~IGroupLaserUnit_members.html` · Polytec IO VibInterfaces Type Library*

### Public Methods

| ReadShifterFrequency | Reads the shifter frequency in Hz from the hardware. |
|---|---|
| ReadShifterOperatingTemperature | Reads the shifter operating temperature in millivolt from the hardware. |
| ReadShifterRFLevel | Reads the shifter RF level from the hardware. |
| SetLaserOn | Switches the laser on or off. |
| SetLaserOperationPointIndex | Sets the laser operation point index. |
| SetPilotLaserModulationOn | Switches the pilot laser modulation on or off. |

### Public Properties

| GroupLaserUnitInfo | Gets information describing the group laser unit. |
|---|---|
| LaserOn | Gets the current activity status of the laser. |
| LaserOperationPointIndex | Gets the zero-based index of the laser operation point. |
| LaserTemperature | Gets the laser temperature in degree Celsius. |
| LaserTemperatureOutOfRange | Gets the Boolean indicating whether the current laser temperature is out of range. |
| LaserWavelengthStable | Gets the Boolean indicating whether the laser wavelength is stable or still stabilizing. |
| PilotLaserModulationOn | Gets the Boolean indicating whether the laser modulation is switched on or off. |


---

## ReadShifterFrequency Method

*Quelle: `Polytec_IO_VibInterfaces~IGroupLaserUnit~ReadShifterFrequency.html` · Polytec IO VibInterfaces Type Library · IGroupLaserUnit Interface : ReadShifterFrequency Method*

### Description

Reads the shifter frequency in Hz from the hardware.

### Syntax

*Visual Basic:*
```
Public Function ReadShifterFrequency() As Long
```

### Return Type

The shifter frequency in Hz.


---

## ReadShifterOperatingTemperature Method

*Quelle: `Polytec_IO_VibInterfaces~IGroupLaserUnit~ReadShifterOperatingTemperature.html` · Polytec IO VibInterfaces Type Library · IGroupLaserUnit Interface : ReadShifterOperatingTemperature Method*

### Description

Reads the shifter operating temperature in millivolt from the hardware.

### Syntax

*Visual Basic:*
```
Public Function ReadShifterOperatingTemperature() As Long
```

### Return Type

The shifter operating temperature in millivolt.


---

## ReadShifterRFLevel Method

*Quelle: `Polytec_IO_VibInterfaces~IGroupLaserUnit~ReadShifterRFLevel.html` · Polytec IO VibInterfaces Type Library · IGroupLaserUnit Interface : ReadShifterRFLevel Method*

### Description

Reads the shifter RF level from the hardware.

### Syntax

*Visual Basic:*
```
Public Function ReadShifterRFLevel() As Long
```

### Return Type

The shifter RF level.


---

## SetLaserOn Method

*Quelle: `Polytec_IO_VibInterfaces~IGroupLaserUnit~SetLaserOn.html` · Polytec IO VibInterfaces Type Library · IGroupLaserUnit Interface : SetLaserOn Method*

### Description

Switches the laser on or off.

### Syntax

*Visual Basic:*
```
Public Sub SetLaserOn( _
   ByVal laserOnParam As Boolean _
)
```

### Parameters

laserOnParam

True to switch on the laser, False to switch it off.


---

## SetLaserOperationPointIndex Method

*Quelle: `Polytec_IO_VibInterfaces~IGroupLaserUnit~SetLaserOperationPointIndex.html` · Polytec IO VibInterfaces Type Library · IGroupLaserUnit Interface : SetLaserOperationPointIndex Method*

### Description

Sets the laser operation point index.

### Syntax

*Visual Basic:*
```
Public Sub SetLaserOperationPointIndex( _
   ByVal operationPointIndexParam As Long _
)
```

### Parameters

operationPointIndexParam

The zero-based index of the laser operation point.


---

## SetPilotLaserModulationOn Method

*Quelle: `Polytec_IO_VibInterfaces~IGroupLaserUnit~SetPilotLaserModulationOn.html` · Polytec IO VibInterfaces Type Library · IGroupLaserUnit Interface : SetPilotLaserModulationOn Method*

### Description

Switches the pilot laser modulation on or off.

### Syntax

*Visual Basic:*
```
Public Sub SetPilotLaserModulationOn( _
   ByVal modulationParam As Boolean _
)
```

### Parameters

modulationParam

True to switch the modulation on, False to switch it off.


---

## GroupLaserUnitInfo Property

*Quelle: `Polytec_IO_VibInterfaces~IGroupLaserUnit~GroupLaserUnitInfo.html` · Polytec IO VibInterfaces Type Library · IGroupLaserUnit Interface : GroupLaserUnitInfo Property*

### Description

Gets information describing the group laser unit.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property GroupLaserUnitInfo As GroupLaserUnitInfo
```

### Return Type

The object holding the information about the group laser unit.


---

## LaserOn Property

*Quelle: `Polytec_IO_VibInterfaces~IGroupLaserUnit~LaserOn.html` · Polytec IO VibInterfaces Type Library · IGroupLaserUnit Interface : LaserOn Property*

### Description

Gets the current activity status of the laser.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property LaserOn As Boolean
```

### Return Type

True if the laser is switched on, False if it is switched off.


---

## LaserOperationPointIndex Property

*Quelle: `Polytec_IO_VibInterfaces~IGroupLaserUnit~LaserOperationPointIndex.html` · Polytec IO VibInterfaces Type Library · IGroupLaserUnit Interface : LaserOperationPointIndex Property*

### Description

Gets the zero-based index of the laser operation point.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property LaserOperationPointIndex As Long
```

### Return Type

The laser operation point index.


---

## LaserTemperature Property

*Quelle: `Polytec_IO_VibInterfaces~IGroupLaserUnit~LaserTemperature.html` · Polytec IO VibInterfaces Type Library · IGroupLaserUnit Interface : LaserTemperature Property*

### Description

Gets the laser temperature in degree Celsius.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property LaserTemperature As Double
```

### Return Type

The laser temperature in degree Celsius.


---

## LaserTemperatureOutOfRange Property

*Quelle: `Polytec_IO_VibInterfaces~IGroupLaserUnit~LaserTemperatureOutOfRange.html` · Polytec IO VibInterfaces Type Library · IGroupLaserUnit Interface : LaserTemperatureOutOfRange Property*

### Description

Gets the Boolean indicating whether the current laser temperature is out of range.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property LaserTemperatureOutOfRange As Boolean
```

### Return Type

True if the laser temperature is out of range, False if it is not.


---

## LaserWavelengthStable Property

*Quelle: `Polytec_IO_VibInterfaces~IGroupLaserUnit~LaserWavelengthStable.html` · Polytec IO VibInterfaces Type Library · IGroupLaserUnit Interface : LaserWavelengthStable Property*

### Description

Gets the Boolean indicating whether the laser wavelength is stable or still stabilizing.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property LaserWavelengthStable As Boolean
```

### Return Type

True if the laser wavelength is stable, False if it is stabilizing.


---

## PilotLaserModulationOn Property

*Quelle: `Polytec_IO_VibInterfaces~IGroupLaserUnit~PilotLaserModulationOn.html` · Polytec IO VibInterfaces Type Library · IGroupLaserUnit Interface : PilotLaserModulationOn Property*

### Description

Gets the Boolean indicating whether the laser modulation is switched on or off.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property PilotLaserModulationOn As Boolean
```

### Return Type

True if the laser modulation is active, False if it is inactive.
