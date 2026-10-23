# Polytec_IO_VibInterfaces – IBaseFilterRange

## IBaseFilterRange Interface

*Quelle: `Polytec_IO_VibInterfaces~IBaseFilterRange.html` · Polytec IO VibInterfaces Type Library*

### Description

The base object for the filter ranges. Item of the IBaseFilterRangeCollection.

### Remarks

Depending in the filter type, this object is a IFilterRange object, a IAdaptiveFilterRange object, a ITrackingFilterRange object or a IDCResponseFilterRange object. You can cast to the more specific objects to get more detailed information about the filter range.

### Example

The macro shows how to access all properties of all filter ranges of all filters of the first vibrometer controller.

- Example (Visual Basic)

```
Dim oInfosAcq As InfosAcq
Set oInfosAcq = Acquisition.Infos

Dim oVibrometerGroups As VibrometerGroups
Set oVibrometerGroups = oInfosAcq.Vibrometers
Debug.Print oVibrometerGroups.Count
Debug.Print oVibrometerGroups(1).ControllerInfo.Name

Dim oGroup As IControllerGroup
Set oGroup = oVibrometerGroups(1)

Dim oFilters As IFilterCollection
Set oFilters = oGroup.Filters
Dim oFilter As IFilter
For Each oFilter In oFilters
  Debug.Print "Filter: ";oFilter.Name;vbTab;oFilter.Key
  Dim oBaseFilterRange As Object
  For Each oBaseFilterRange In oFilter.Ranges
    Debug.Print " Range: ";oBaseFilterRange.Name

    Dim oFilterRange As IFilterRange
    Dim oAdaptiveFilterRange As IAdaptiveFilterRange
    Dim oTrackingFilterRange As ITrackingFilterRange

    Select Case oFilter.Key
    Case FilterType_HighPass
      Set oFilterRange = oBaseFilterRange
      Debug.Print "  Cutoff: ";oFilterRange.Cutoff
      Debug.Print "  Passband: ";oFilterRange.Passband
    Case FilterType_LowPass
      Set oFilterRange = oBaseFilterRange
      Debug.Print "  Cutoff: ";oFilterRange.Cutoff
      Debug.Print "  Passband: ";oFilterRange.Passband
    Case FilterType_Tracking
      Set oTrackingFilterRange = oBaseFilterRange
      Debug.Print "  Mode: ";oTrackingFilterRange.Mode
    Case FilterType_Adaptive
      Set oAdaptiveFilterRange = oBaseFilterRange
      Debug.Print "  Scope: ";oAdaptiveFilterRange.Scope
    End Select
  Next
Next
```


---

## IBaseFilterRange Interface Members

*Quelle: `Polytec_IO_VibInterfaces~IBaseFilterRange_members.html` · Polytec IO VibInterfaces Type Library*

### Public Properties

| Name | The name of the filter range. Can be used as an index into the IBaseFilterRangeCollection . |
|---|---|


---

## Name Property

*Quelle: `Polytec_IO_VibInterfaces~IBaseFilterRange~Name.html` · Polytec IO VibInterfaces Type Library · IBaseFilterRange Interface : Name Property*

### Description

The name of the filter range. Can be used as an index into the IBaseFilterRangeCollection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Name As String
```
