# POLYWAVEFORMSLib – WaveformUserDefined

## WaveformUserDefined Object

*Quelle: `POLYWAVEFORMSLib~WaveformUserDefined.html` · Polytec PolyWaveforms Type Library*

### Description

The user-defined waveform.

### Remarks

This class can be instantiated using the string "PolyWaveforms.WaveformUserDefined".


---

## WaveformUserDefined Object Members

*Quelle: `POLYWAVEFORMSLib~WaveformUserDefined_members.html` · Polytec PolyWaveforms Type Library*

### Public Methods

| Load | Loads the user-defined waveform from the specified file. |
|---|---|

### Public Properties

| Frequency | The frequency of the waveform in Hz. |
|---|---|
| Name | The name of the waveform. |
| Type | The type of the waveform. |
| WaveformData | The waveform data of the user-defined waveform. |


---

## Load Method

*Quelle: `POLYWAVEFORMSLib~WaveformUserDefined~Load.html` · Polytec PolyWaveforms Type Library · WaveformUserDefined Object : Load Method*

### Description

Loads the user-defined waveform from the specified file.

### Syntax

*Visual Basic:*
```
Public Sub Load( _
   ByVal bstrFileName As String _
)
```

### Parameters

bstrFileName

The filename of the user-defined waveform.


---

## Frequency Property

*Quelle: `POLYWAVEFORMSLib~WaveformUserDefined~Frequency.html` · Polytec PolyWaveforms Type Library · WaveformUserDefined Object : Frequency Property*

### Description

The frequency of the waveform in Hz.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Frequency As Double
```


---

## Name Property

*Quelle: `POLYWAVEFORMSLib~WaveformUserDefined~Name.html` · Polytec PolyWaveforms Type Library · WaveformUserDefined Object : Name Property*

### Description

The name of the waveform.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Name As String
```


---

## Type Property

*Quelle: `POLYWAVEFORMSLib~WaveformUserDefined~Type.html` · Polytec PolyWaveforms Type Library · WaveformUserDefined Object : Type Property*

### Description

The type of the waveform.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Type As PTCWaveformType
```


---

## WaveformData Property

*Quelle: `POLYWAVEFORMSLib~WaveformUserDefined~WaveformData.html` · Polytec PolyWaveforms Type Library · WaveformUserDefined Object : WaveformData Property*

### Description

The waveform data of the user-defined waveform.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property WaveformData As Double()
```

### Return Type

One-dimensional, zero-based array of doubles.

### Example
