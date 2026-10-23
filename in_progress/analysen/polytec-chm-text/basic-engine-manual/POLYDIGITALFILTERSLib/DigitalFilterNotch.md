# POLYDIGITALFILTERSLib – DigitalFilterNotch

## DigitalFilterNotch Object

*Quelle: `POLYDIGITALFILTERSLib~DigitalFilterNotch.html` · Polytec PolyDigitalFilters Type Library*

### Description

A notch digital filter.


---

## DigitalFilterNotch Object Members

*Quelle: `POLYDIGITALFILTERSLib~DigitalFilterNotch_members.html` · Polytec PolyDigitalFilters Type Library*

### Public Properties

| CutoffFreq1 | The lower cutoff frequency of the notch. |
|---|---|
| CutoffFreq2 | The upper cutoff frequency of the notch. |
| Name | The name of the digital filter type. |
| Quality | The quality of the digital filter. |
| Type | The type of the digital filter. |


---

## CutoffFreq1 Property

*Quelle: `POLYDIGITALFILTERSLib~DigitalFilterNotch~CutoffFreq1.html` · Polytec PolyDigitalFilters Type Library · DigitalFilterNotch Object : CutoffFreq1 Property*

### Description

The lower cutoff frequency of the notch.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property CutoffFreq1 As Double
```


---

## CutoffFreq2 Property

*Quelle: `POLYDIGITALFILTERSLib~DigitalFilterNotch~CutoffFreq2.html` · Polytec PolyDigitalFilters Type Library · DigitalFilterNotch Object : CutoffFreq2 Property*

### Description

The upper cutoff frequency of the notch.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property CutoffFreq2 As Double
```


---

## Name Property

*Quelle: `POLYDIGITALFILTERSLib~DigitalFilterNotch~Name.html` · Polytec PolyDigitalFilters Type Library · DigitalFilterNotch Object : Name Property*

### Description

The name of the digital filter type.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Name As String
```


---

## Quality Property

*Quelle: `POLYDIGITALFILTERSLib~DigitalFilterNotch~Quality.html` · Polytec PolyDigitalFilters Type Library · DigitalFilterNotch Object : Quality Property*

### Description

The quality of the digital filter.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Quality As PTCDigitalFilterQuality
```


---

## Type Property

*Quelle: `POLYDIGITALFILTERSLib~DigitalFilterNotch~Type.html` · Polytec PolyDigitalFilters Type Library · DigitalFilterNotch Object : Type Property*

### Description

The type of the digital filter.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Type As PTCDigitalFilterType
```

### Example

To find out, what kind of digital filter the ChannelAcqProperties.DigitalFilter Property returns, do the following:

- Work with the DigitalFilter Return Type (Visual Basic)

```
Dim oChannelAcqProps As ChannelAcqProperties

Dim oDigitalFilter As DigitalFilter
oDigitalFilter = oChannelAcqProps.DigitalFilter

Select Case (oDigitalFilter.Type)
Case ptcDigitalFilterLowpass
    Dim oDigitalFilterLowpass As DigitalFilterLowpass
    oDigitalFilterLowpass = oDigitalFilter
    Debug.Print oDigitalFilterLowpass.CutoffFreq
Case ptcDigitalFilterHighpass
    Dim oDigitalFilterHighpass As DigitalFilterHighpass
    oDigitalFilterHighpass = oDigitalFilter
    Debug.Print oDigitalFilterHighpass.CutoffFreq
Case ptcDigitalFilterBandpass
    Dim oDigitalFilterBandpass As DigitalFilterBandpass
    oDigitalFilterBandpass = oDigitalFilter
    Debug.Print oDigitalFilterBandpass.CutoffFreq1
    Debug.Print oDigitalFilterBandpass.CutoffFreq2
Case ptcDigitalFilterNotch
    Dim oDigitalFilterNotch As DigitalFilterNotch
    oDigitalFilterNotch = oDigitalFilter
    Debug.Print oDigitalFilterNotch.CutoffFreq1
    Debug.Print oDigitalFilterNotch.CutoffFreq2
Case ptcDigitalFilterNone
    Dim oDigitalFilterNone As DigitalFilterNone
    oDigitalFilterNone = oDigitalFilter
    Debug.Print oDigitalFilterNone.Name
End Select
```
