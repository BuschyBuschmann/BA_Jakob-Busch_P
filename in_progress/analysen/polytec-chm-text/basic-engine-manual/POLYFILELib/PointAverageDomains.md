# POLYFILELib – PointAverageDomains

## PointAverageDomains Collection

*Quelle: `POLYFILELib~PointAverageDomains.html` · Polytec PolyFile Type Library*

### Description

Named and typed collection of the available domains of the point average data.

### Object Model


---

## PointAverageDomains Collection Members

*Quelle: `POLYFILELib~PointAverageDomains_members.html` · Polytec PolyFile Type Library*

### Public Methods

| AddSignal | Adds a user-defined signal with the given description to the Usr or Usr 3D channel. |
|---|---|
| FindSignal | Finds the signal for the given signal description and returns the signal. |

### Public Properties

| Count | Returns the number of items in the PointAverageDomains collection. |
|---|---|
| Exists | Returns True if the item of the given name or type exists in the PointAverageDomains collection. |
| Item | Returns an item of the PointAverageDomains collection. |
| Type | Returns an item of the PointDomains collection. |


---

## AddSignal Method

*Quelle: `POLYFILELib~PointAverageDomains~AddSignal.html` · Polytec PolyFile Type Library · PointAverageDomains Collection : AddSignal Method*

### Description

Adds a user-defined signal with the given description to the Usr or Usr 3D channel.

### Syntax

*Visual Basic:*
```
Public Function AddSignal( _
   ByVal pISignalDescription As ISignalDescription _
) As ISignal5
```

### Parameters

pISignalDescription

The description of the signal to add.

### Return Type

The added signal.

### Remarks

To be able to add a signal to the user channel you have to pass the ptcBuildUser flag of the PTCSignalBuildFlags Enumeration as parameter to the call of the GetPointAverageDomains Method. If the Direction Property of the ResponseDOFs Collection is ptcVector, the signal will be added to the Usr 3D channel. In this case, you have to pass the ptcBuild3d flag in addition to the ptcBuildUser flag. The ChannelName Property of the ResponseDOFs Collection or (for reference signals) of the ReferenceDOFs Collection will be set to Usr or Usr 3D, respectively. The name of the signal (Name Property of the SignalDescription Object) must be different from the names of signals you already have added. To remove a signal use the Remove Method of the Signals Collection.

### Example

This macros adds a new user-defined signal and copies an original average spectrum to the new signal.

- Add Signal (Visual Basic)

```
Option Explicit

Sub Main
    Dim oFile As New PolyFile
    oFile.Readonly = False

    oFile.Open("D:\Temp\Example.svd")

    Dim oPointAverageDomains As PointAverageDomains
    Set oPointAverageDomains = oFile.GetPointAverageDomains(ptcBuildBandData3d)

    Dim oPointAverageDomain As PointAverageDomain
    Set oPointAverageDomain = oPointAverageDomains.Type(ptcDomainSpectrum)

    Dim oDomain As Domain
    Set oDomain = oPointAverageDomain

    Dim oSignal As Signal
    Set oSignal = oDomain.Channels("Vib").Signals("Velocity")

    ' use the signal description and data of an existing, original average spectrum
    Dim oSigDesc As SignalDescription
    Set oSigDesc = oSignal.Description.Clone()

    Dim Data() As Single
    Data = oPointAverageDomain.GetData(oSignal.Displays.Type(ptcDisplayMag), 0)

    ' if this signal exists already as user-defined signal, remove it
    Dim oExistingSignal As Signal
    Set oExistingSignal = oPointAverageDomains.FindSignal(oSigDesc, True)
    If (Not oExistingSignal Is Nothing) Then
        oExistingSignal.Channel.Signals.Remove(oExistingSignal.Name)
    End If

    ' add the new user-defined signal
    Dim oNewSignal As Signal
    Set oNewSignal = oPointAverageDomains.AddSignal(oSigDesc)

    ' copy the original data
    oPointAverageDomain.SetData(oNewSignal, 1, Data)

    oFile.Save()
    oFile.Close()
End Sub
```


---

## FindSignal Method

*Quelle: `POLYFILELib~PointAverageDomains~FindSignal.html` · Polytec PolyFile Type Library · PointAverageDomains Collection : FindSignal Method*

### Description

Finds the signal for the given signal description and returns the signal.

### Syntax

*Visual Basic:*
```
Public Function FindSignal( _
   ByVal pISignalDescription As ISignalDescription, _
   ByVal vbUserSignal As Boolean _
) As ISignal5
```

### Parameters

pISignalDescription

The description of the signal.

vbUserSignal

Specifies whether a user-defined signal or an original signal is searched.

### Return Type

The found Signal Object or nothing, if the signal does not exist.

### Remarks

For an example to use this method, see AddSignal Method.


---

## Count Property

*Quelle: `POLYFILELib~PointAverageDomains~Count.html` · Polytec PolyFile Type Library · PointAverageDomains Collection : Count Property*

### Description

Returns the number of items in the PointAverageDomains collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Count As Long
```


---

## Exists Property

*Quelle: `POLYFILELib~PointAverageDomains~Exists.html` · Polytec PolyFile Type Library · PointAverageDomains Collection : Exists Property*

### Description

Returns True if the item of the given name or type exists in the PointAverageDomains collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Exists( _
   ByVal IndexOrType As Variant _
) As Boolean
```

### Parameters

IndexOrType

Index (string) or type (PTCDomainType) of the PointAverageDomain object.


---

## Item Property

*Quelle: `POLYFILELib~PointAverageDomains~Item.html` · Polytec PolyFile Type Library · PointAverageDomains Collection : Item Property*

### Description

Returns an item of the PointAverageDomains collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Item( _
   ByVal IndexOrName As Variant _
) As PointAverageDomain
```

### Parameters

IndexOrName

Index (integer) or name (string) of the item.

### Return Type

PointAverageDomain object


---

## Type Property

*Quelle: `POLYFILELib~PointAverageDomains~Type.html` · Polytec PolyFile Type Library · PointAverageDomains Collection : Type Property*

### Description

Returns an item of the PointDomains collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Type( _
   ByVal ptcDomainType As PTCDomainType _
) As PointAverageDomain
```

### Parameters

ptcDomainType

| Value | Description |
|---|---|
| ptcDomain3rdOctave | Domain 3rdOctave. |
| ptcDomainAngleSync | Domain synchronized angle (for order analysis, not supported any more). |
| ptcDomainNotAvail | Domain is not available. |
| ptcDomainOrderSpectrum | Domain order spectrum (for order analysis, not supported any more). |
| ptcDomainRMS | Domain RMS. |
| ptcDomainSpectrum | Domain Spectrum. |
| ptcDomainTime | Domain Time. |
Type (PTCDomainType) of the PointAverageDomain.
