# POLYPROPERTIESLib – FftAcqPropertiesContainer

## FftAcqPropertiesContainer Object

*Quelle: `POLYPROPERTIESLib~FftAcqPropertiesContainer.html` · Polytec PolyProperties Type Library*

### Description

The FFT acquisition properties. Item of the AcquisitionProperties collection.

### Object Model


---

## FftAcqPropertiesContainer Object Members

*Quelle: `POLYPROPERTIESLib~FftAcqPropertiesContainer_members.html` · Polytec PolyProperties Type Library*

### Public Properties

| Bandwidth | The bandwidth of the FFT in Hz. |
|---|---|
| EndFrequency | The end frequency of the FFT in Hz. |
| FftAcqPropertiesValidator | The validator of the FFT acquisition properties. |
| Lines | The number of FFT lines. |
| Overlap | The overlap of the FFT in percent. |
| SampleFrequency | The sample frequency of the FFT in Hz. |
| SampleResolution | The frequency resolution of the FFT in Hz. |
| Samples | The number of samples used for the FFT. |
| SampleTime | The sample time of the FFT. |
| StartFrequency | The start frequency of the FFT. |


---

## Bandwidth Property

*Quelle: `POLYPROPERTIESLib~FftAcqPropertiesContainer~Bandwidth.html` · Polytec PolyProperties Type Library · FftAcqPropertiesContainer Object : Bandwidth Property*

### Description

The bandwidth of the FFT in Hz.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Bandwidth As Double
```


---

## EndFrequency Property

*Quelle: `POLYPROPERTIESLib~FftAcqPropertiesContainer~EndFrequency.html` · Polytec PolyProperties Type Library · FftAcqPropertiesContainer Object : EndFrequency Property*

### Description

The end frequency of the FFT in Hz.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property EndFrequency As Double
```


---

## FftAcqPropertiesValidator Property

*Quelle: `POLYPROPERTIESLib~FftAcqPropertiesContainer~FftAcqPropertiesValidator.html` · Polytec PolyProperties Type Library · FftAcqPropertiesContainer Object : FftAcqPropertiesValidator Property*

### Description

The validator of the FFT acquisition properties.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property FftAcqPropertiesValidator As IFftAcqPropertiesValidator
```

### Example

This macro validates and tests all available FFT acquisition configurations. It iterates through every supported bandwidth and line setting, configures a valid frequency range for each combination, applies the settings, and performs a short FFT measurement. Any invalid or unsupported configuration is caught and reported in the debug output.

- FFT Validator Example (Visual Basic)

```
#Language "WWB.NET"

Imports System

Sub Main
  Debug.Clear
  Acquisition.Mode = PTCAcqMode.ptcAcqModeFft
  If (Acquisition.ActiveProperties.HasFftProperties()) Then
    Dim fftProps As FftAcqProperties = Acquisition.ActiveProperties.FftProperties
    Dim fftValidator As FftAcqPropertiesValidator = fftProps.FftAcqPropertiesValidator

    Dim bandwidthList As Double() = fftValidator.AvailableBandwidths
    For Each bw As Double In bandwidthList
      fftValidator.Bandwidth = bw

      Dim startFreq As Double
      Dim endFreq As Double
      fftValidator.GetMinMaxFrequencyRange(startFreq, endFreq)
      Dim quater As Double = (endFreq - startFreq) / 4.0
      fftValidator.StartFrequency = quater * 2
      fftValidator.EndFrequency = quater * 3

      Dim linesList As Integer() = fftValidator.AvailableLines
      For Each lines As Integer In linesList
        Debug.WriteLine("Bandwidth: " + bw.ToString() + " Lines: " + lines.ToString())
        fftValidator.Lines = lines

        Try
          fftProps.FftAcqPropertiesValidator = fftValidator

          Dim index As Integer = 0
          Acquisition.Start(PTCAcqStartMode.ptcAcqStartSingle)
          While (Acquisition.State <> PTCAcqState.ptcAcqStateStopped)
            If index = 20 Then Acquisition.Stop ' Stop measurement after 2 s.
            Wait 0.1
            index += 1
          End While
        Catch oExc As Exception
          Debug.Print oExc.Message
        End Try
      Next
    Next
  End If
End Sub
```


---

## Lines Property

*Quelle: `POLYPROPERTIESLib~FftAcqPropertiesContainer~Lines.html` · Polytec PolyProperties Type Library · FftAcqPropertiesContainer Object : Lines Property*

### Description

The number of FFT lines.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Lines As Long
```


---

## Overlap Property

*Quelle: `POLYPROPERTIESLib~FftAcqPropertiesContainer~Overlap.html` · Polytec PolyProperties Type Library · FftAcqPropertiesContainer Object : Overlap Property*

### Description

The overlap of the FFT in percent.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Overlap As Long
```


---

## SampleFrequency Property

*Quelle: `POLYPROPERTIESLib~FftAcqPropertiesContainer~SampleFrequency.html` · Polytec PolyProperties Type Library · FftAcqPropertiesContainer Object : SampleFrequency Property*

### Description

The sample frequency of the FFT in Hz.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property SampleFrequency As Double
```


---

## SampleResolution Property

*Quelle: `POLYPROPERTIESLib~FftAcqPropertiesContainer~SampleResolution.html` · Polytec PolyProperties Type Library · FftAcqPropertiesContainer Object : SampleResolution Property*

### Description

The frequency resolution of the FFT in Hz.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property SampleResolution As Double
```


---

## Samples Property

*Quelle: `POLYPROPERTIESLib~FftAcqPropertiesContainer~Samples.html` · Polytec PolyProperties Type Library · FftAcqPropertiesContainer Object : Samples Property*

### Description

The number of samples used for the FFT.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Samples As Long
```

### Remarks

Setting the property is only supported for acquisition mode MultiFrame.


---

## SampleTime Property

*Quelle: `POLYPROPERTIESLib~FftAcqPropertiesContainer~SampleTime.html` · Polytec PolyProperties Type Library · FftAcqPropertiesContainer Object : SampleTime Property*

### Description

The sample time of the FFT.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property SampleTime As Double
```


---

## StartFrequency Property

*Quelle: `POLYPROPERTIESLib~FftAcqPropertiesContainer~StartFrequency.html` · Polytec PolyProperties Type Library · FftAcqPropertiesContainer Object : StartFrequency Property*

### Description

The start frequency of the FFT.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property StartFrequency As Double
```
