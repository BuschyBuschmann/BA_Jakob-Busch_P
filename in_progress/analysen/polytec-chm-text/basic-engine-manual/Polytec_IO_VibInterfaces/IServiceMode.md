# Polytec_IO_VibInterfaces – IServiceMode

## IServiceMode Interface

*Quelle: `Polytec_IO_VibInterfaces~IServiceMode.html` · Polytec IO VibInterfaces Type Library*

### Description

The service mode object allows to control and access the service mode of the vibrometer controller.


---

## IServiceMode Interface Members

*Quelle: `Polytec_IO_VibInterfaces~IServiceMode_members.html` · Polytec IO VibInterfaces Type Library*

### Public Methods

| HasCap | Returns true, if the service mode has the given capability. |
|---|---|
| Update | Updates the service mode status. |

### Public Properties

| Caps | The capabilities of the service mode. |
|---|---|
| Temperature | The current internal temperature of the connected laser vibrometer in degree Celsius. |
| TemperatureState | The current state of the internal temperature of the connected laser vibrometer. |
| TestSignal | The current state of the test signal. |


---

## HasCap Method

*Quelle: `Polytec_IO_VibInterfaces~IServiceMode~HasCap.html` · Polytec IO VibInterfaces Type Library · IServiceMode Interface : HasCap Method*

### Description

Returns true, if the service mode has the given capability.

### Syntax

*Visual Basic:*
```
Public Function HasCap( _
   ByVal cap As ServiceCaps _
) As Boolean
```

### Parameters

cap

| Value | Description |
|---|---|
| ServiceCaps_None | The service mode has no capabilities. |
| ServiceCaps_Temperature | The service mode can monitor the temperature. |
| ServiceCaps_TestSignals | The service mode can generate a test signal. |
The capability of the service mode.


---

## Update Method

*Quelle: `Polytec_IO_VibInterfaces~IServiceMode~Update.html` · Polytec IO VibInterfaces Type Library · IServiceMode Interface : Update Method*

### Description

Updates the service mode status.

### Syntax

*Visual Basic:*
```
Public Sub Update()
```

### Remarks

The service mode status is updated periodically. By calling this method you can force an update.


---

## Caps Property

*Quelle: `Polytec_IO_VibInterfaces~IServiceMode~Caps.html` · Polytec IO VibInterfaces Type Library · IServiceMode Interface : Caps Property*

### Description

The capabilities of the service mode.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Caps As ServiceCaps
```


---

## Temperature Property

*Quelle: `Polytec_IO_VibInterfaces~IServiceMode~Temperature.html` · Polytec IO VibInterfaces Type Library · IServiceMode Interface : Temperature Property*

### Description

The current internal temperature of the connected laser vibrometer in degree Celsius.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Temperature As Double
```

### Example


---

## TemperatureState Property

*Quelle: `Polytec_IO_VibInterfaces~IServiceMode~TemperatureState.html` · Polytec IO VibInterfaces Type Library · IServiceMode Interface : TemperatureState Property*

### Description

The current state of the internal temperature of the connected laser vibrometer.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property TemperatureState As ServiceTemperatureState
```


---

## TestSignal Property

*Quelle: `Polytec_IO_VibInterfaces~IServiceMode~TestSignal.html` · Polytec IO VibInterfaces Type Library · IServiceMode Interface : TestSignal Property*

### Description

The current state of the test signal.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property TestSignal As ServiceTestSignal
```

### Remarks

The test signals are only required for service and diagnostic purposes. Only persons which are authorized by Polytec are allowed to use these signals.
