# POLYDIGITALFILTERSLib – DigitalFilterHighpass

## DigitalFilterHighpass Object

*Quelle: `POLYDIGITALFILTERSLib~DigitalFilterHighpass.html` · Polytec PolyDigitalFilters Type Library*

### Description

A high pass digital filter.


---

## DigitalFilterHighpass Object Members

*Quelle: `POLYDIGITALFILTERSLib~DigitalFilterHighpass_members.html` · Polytec PolyDigitalFilters Type Library*

### Public Properties

| CutoffFreq | The cutoff frequency of the high pass. |
|---|---|
| Name | The name of the digital filter type. |
| Quality | The quality of the digital filter. |
| Type | The type of the digital filter. |


---

## CutoffFreq Property

*Quelle: `POLYDIGITALFILTERSLib~DigitalFilterHighpass~CutoffFreq.html` · Polytec PolyDigitalFilters Type Library · DigitalFilterHighpass Object : CutoffFreq Property*

### Description

The cutoff frequency of the high pass.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property CutoffFreq As Double
```


---

## Name Property

*Quelle: `POLYDIGITALFILTERSLib~DigitalFilterHighpass~Name.html` · Polytec PolyDigitalFilters Type Library · DigitalFilterHighpass Object : Name Property*

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

*Quelle: `POLYDIGITALFILTERSLib~DigitalFilterHighpass~Quality.html` · Polytec PolyDigitalFilters Type Library · DigitalFilterHighpass Object : Quality Property*

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

*Quelle: `POLYDIGITALFILTERSLib~DigitalFilterHighpass~Type.html` · Polytec PolyDigitalFilters Type Library · DigitalFilterHighpass Object : Type Property*

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
