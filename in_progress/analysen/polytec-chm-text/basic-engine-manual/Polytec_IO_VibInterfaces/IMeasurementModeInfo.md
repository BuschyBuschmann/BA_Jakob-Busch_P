# Polytec_IO_VibInterfaces – IMeasurementModeInfo

## IMeasurementModeInfo Interface

*Quelle: `Polytec_IO_VibInterfaces~IMeasurementModeInfo.html` · Polytec IO VibInterfaces Type Library*

### Description

The information about the measurement mode of the controller.


---

## IMeasurementModeInfo Interface Members

*Quelle: `Polytec_IO_VibInterfaces~IMeasurementModeInfo_members.html` · Polytec IO VibInterfaces Type Library*

### Public Methods

| HasCap | Returns true when the measurement mode of the controller has the given capability. |
|---|---|

### Public Properties

| Caps | The capabilities of the measurement mode of the controller. |
|---|---|
| Mode | The measurement mode of the controller. |


---

## HasCap Method

*Quelle: `Polytec_IO_VibInterfaces~IMeasurementModeInfo~HasCap.html` · Polytec IO VibInterfaces Type Library · IMeasurementModeInfo Interface : HasCap Method*

### Description

Returns true when the measurement mode of the controller has the given capability.

### Syntax

*Visual Basic:*
```
Public Function HasCap( _
   ByVal cap As MeasurementModeCaps _
) As Boolean
```

### Parameters

cap

| Value | Description |
|---|---|
| MeasurementModeCaps_None | The measurement mode has no capabilities. |
| MeasurementModeCaps_Rotation | The measurement mode can be rotation. |
| MeasurementModeCaps_Translation | The measurement mode can be translation. |
The capability of the measurement mode.


---

## Caps Property

*Quelle: `Polytec_IO_VibInterfaces~IMeasurementModeInfo~Caps.html` · Polytec IO VibInterfaces Type Library · IMeasurementModeInfo Interface : Caps Property*

### Description

The capabilities of the measurement mode of the controller.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Caps As MeasurementModeCaps
```


---

## Mode Property

*Quelle: `Polytec_IO_VibInterfaces~IMeasurementModeInfo~Mode.html` · Polytec IO VibInterfaces Type Library · IMeasurementModeInfo Interface : Mode Property*

### Description

The measurement mode of the controller.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Mode As MeasurementModeType
```
