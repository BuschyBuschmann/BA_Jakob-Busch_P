# PSV – TimeAcqProperties

## TimeAcqProperties Object

*Quelle: `PSV~TimeAcqProperties.html` · Polytec PSV Type Library*

### Description

The time mode acquisition properties. Item of the AcquisitionProperties collection.


---

## TimeAcqProperties Object Members

*Quelle: `PSV~TimeAcqProperties_members.html` · Polytec PSV Type Library*

### Public Properties

| SampleFrequency | Specifies the sample frequency in Hz. |
|---|---|
| SampleResolution | The time resolution in second. |
| Samples | Specifies the number of samples. |
| SampleTime | The sample time in second. |
| TimeAcqPropertiesValidator | The validator of the time acquisition properties. |


---

## SampleFrequency Property

*Quelle: `PSV~TimeAcqProperties~SampleFrequency.html` · Polytec PSV Type Library · TimeAcqProperties Object : SampleFrequency Property*

### Description

Specifies the sample frequency in Hz.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property SampleFrequency As Double
```


---

## SampleResolution Property

*Quelle: `PSV~TimeAcqProperties~SampleResolution.html` · Polytec PSV Type Library · TimeAcqProperties Object : SampleResolution Property*

### Description

The time resolution in second.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property SampleResolution As Double
```


---

## Samples Property

*Quelle: `PSV~TimeAcqProperties~Samples.html` · Polytec PSV Type Library · TimeAcqProperties Object : Samples Property*

### Description

Specifies the number of samples.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Samples As Long
```


---

## SampleTime Property

*Quelle: `PSV~TimeAcqProperties~SampleTime.html` · Polytec PSV Type Library · TimeAcqProperties Object : SampleTime Property*

### Description

The sample time in second.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property SampleTime As Double
```


---

## TimeAcqPropertiesValidator Property

*Quelle: `PSV~TimeAcqProperties~TimeAcqPropertiesValidator.html` · Polytec PSV Type Library · TimeAcqProperties Object : TimeAcqPropertiesValidator Property*

### Description

The validator of the time acquisition properties.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property TimeAcqPropertiesValidator As TimeAcqPropertiesValidator
```

### Return Type

The time acquisition properties validator.

### Example

This macro validates all supported time-acquisition configurations by iterating through every available sample frequency and sample count combination. For each valid combination it: Sets the sample frequency. Retrieves the valid sample counts for that frequency. Applies the configuration. Starts a single acquisition. Lets the acquisition run for about 2 seconds (20 × 0.1 s), then stops it. Catches and logs any exceptions that occur.

- Example (Visual Basic)

```
'#Language "WWB.NET"

Imports System

Sub Main
  Debug.Clear
  Acquisition.Mode = PTCAcqMode.ptcAcqModeTime

  If (Acquisition.ActiveProperties.HasTimeProperties()) Then
    Dim timeProps As TimeAcqProperties = Acquisition.ActiveProperties.TimeProperties
    Dim timeValidator As TimeAcqPropertiesValidator = timeProps.TimeAcqPropertiesValidator

    Dim sampFreqList As Double() = timeValidator.AvailableSampleFrequencies

    For Each sf As Double In sampFreqList
      timeValidator.SampleFrequency = sf

      Dim samplesList As Integer() = timeValidator.AvailableSamples

      For Each samples As Integer In samplesList
        Debug.WriteLine("Sample Frequency: " + sf.ToString() + " Samples: " + samples.ToString())
        timeValidator.Samples = samples

        Try
          timeProps.TimeAcqPropertiesValidator = timeValidator

          Dim index As Integer = 0

          Acquisition.Start(PTCAcqStartMode.ptcAcqStartSingle)

          While (Acquisition.State <> PTCAcqState.ptcAcqStateStopped)
            If index = 20 Then Acquisition.Stop  ' Stop measurement after 2 s.

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
