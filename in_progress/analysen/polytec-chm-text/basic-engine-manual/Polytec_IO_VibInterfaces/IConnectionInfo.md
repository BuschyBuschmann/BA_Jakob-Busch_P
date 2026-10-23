# Polytec_IO_VibInterfaces – IConnectionInfo

## IConnectionInfo Interface

*Quelle: `Polytec_IO_VibInterfaces~IConnectionInfo.html` · Polytec IO VibInterfaces Type Library*

### Description

The information about the connection of the controller.


---

## IConnectionInfo Interface Members

*Quelle: `Polytec_IO_VibInterfaces~IConnectionInfo_members.html` · Polytec IO VibInterfaces Type Library*

### Public Methods

| Clone | Creates and returns a copy of the connection info object. |
|---|---|

### Public Properties

| Address | The address of the connection. |
|---|---|
| Connection | The type of the connection. |
| Mode | The mode of the connection. |
| Simulation | True, if the connection to the controller is simulated. |
| ToString | Returns a string representation of the connection information object. |


---

## Clone Method

*Quelle: `Polytec_IO_VibInterfaces~IConnectionInfo~Clone.html` · Polytec IO VibInterfaces Type Library · IConnectionInfo Interface : Clone Method*

### Description

Creates and returns a copy of the connection info object.

### Syntax

*Visual Basic:*
```
Public Function Clone() As Variant
```


---

## Address Property

*Quelle: `Polytec_IO_VibInterfaces~IConnectionInfo~Address.html` · Polytec IO VibInterfaces Type Library · IConnectionInfo Interface : Address Property*

### Description

The address of the connection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Address As Long
```


---

## Connection Property

*Quelle: `Polytec_IO_VibInterfaces~IConnectionInfo~Connection.html` · Polytec IO VibInterfaces Type Library · IConnectionInfo Interface : Connection Property*

### Description

The type of the connection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Connection As ConnectionType
```


---

## Mode Property

*Quelle: `Polytec_IO_VibInterfaces~IConnectionInfo~Mode.html` · Polytec IO VibInterfaces Type Library · IConnectionInfo Interface : Mode Property*

### Description

The mode of the connection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Mode As ConnectionMode
```

### Remarks

The connection modes other then none are used to specify the measurement mode for the RLV-5000 controller.


---

## Simulation Property

*Quelle: `Polytec_IO_VibInterfaces~IConnectionInfo~Simulation.html` · Polytec IO VibInterfaces Type Library · IConnectionInfo Interface : Simulation Property*

### Description

True, if the connection to the controller is simulated.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Simulation As Boolean
```


---

## ToString Property

*Quelle: `Polytec_IO_VibInterfaces~IConnectionInfo~ToString.html` · Polytec IO VibInterfaces Type Library · IConnectionInfo Interface : ToString Property*

### Description

Returns a string representation of the connection information object.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property ToString As String
```

### Remarks

E.g. "RS232: COM1"
