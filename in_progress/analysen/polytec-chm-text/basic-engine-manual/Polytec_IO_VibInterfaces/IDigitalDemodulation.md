# Polytec_IO_VibInterfaces – IDigitalDemodulation

## IDigitalDemodulation Interface

*Quelle: `Polytec_IO_VibInterfaces~IDigitalDemodulation.html` · Polytec IO VibInterfaces Type Library*

### Description

The digital demodulation object gives access to the digital demodulation of the controller.


---

## IDigitalDemodulation Interface Members

*Quelle: `Polytec_IO_VibInterfaces~IDigitalDemodulation_members.html` · Polytec IO VibInterfaces Type Library*

### Public Methods

| SetMode | Sets the digital demodulation mode. |
|---|---|

### Public Properties

| Mode | The digital demodulation mode. |
|---|---|


---

## SetMode Method

*Quelle: `Polytec_IO_VibInterfaces~IDigitalDemodulation~SetMode.html` · Polytec IO VibInterfaces Type Library · IDigitalDemodulation Interface : SetMode Method*

### Description

Sets the digital demodulation mode.

### Syntax

*Visual Basic:*
```
Public Sub SetMode( _
   ByVal parameter As DigitalDemodulationMode _
)
```

### Parameters

parameter

| Value | Description |
|---|---|
| DigitalDemodulationMode_Measurement | The mode is measurement. |
| DigitalDemodulationMode_Reference | The mode is reference. |
The digital demodulation mode.

### Remarks

The reference mode is used by the software to calculate the errors which are caused by the analog components during signal processing.


---

## Mode Property

*Quelle: `Polytec_IO_VibInterfaces~IDigitalDemodulation~Mode.html` · Polytec IO VibInterfaces Type Library · IDigitalDemodulation Interface : Mode Property*

### Description

The digital demodulation mode.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Mode As DigitalDemodulationMode
```

### Remarks

The reference mode is used by the software to calculate the errors which are caused by the analog components during signal processing.
