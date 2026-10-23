# POLYFILELib – BandDomains

## BandDomains Collection

*Quelle: `POLYFILELib~BandDomains.html` · Polytec PolyFile Type Library*

### Description

Named and typed collection of the available domains of the band data.

### Object Model


---

## BandDomains Collection Members

*Quelle: `POLYFILELib~BandDomains_members.html` · Polytec PolyFile Type Library*

### Public Methods

| AddBand | Adds a user-defined band with the given signal description and band definition to the Signals Collection of the Usr or Usr 3D Channel and returns the newly created DataBand Object and the signal of the band. |
|---|---|
| FindBand | Finds the band with the given signal description and band definition and returns the signal the band belongs to and the DataBand Object of the band. |
| FindSignal | Finds the signal for the given signal description and returns the signal. |
| RemoveBand | Removes the user-defined band with the given definition from the given signal. |

### Public Properties

| Count | Returns the number of items in the BandDomains collection. |
|---|---|
| Exists | Returns True if the item of the given name or type exists in the BandDomains collection. |
| Item | Returns an item of the BandDomains collection. |
| Type | Returns an item of the BandDomains collection. |


---

## AddBand Method

*Quelle: `POLYFILELib~BandDomains~AddBand.html` · Polytec PolyFile Type Library · BandDomains Collection : AddBand Method*

### Description

Adds a user-defined band with the given signal description and band definition to the Signals Collection of the Usr or Usr 3D Channel and returns the newly created DataBand Object and the signal of the band.

### Syntax

*Visual Basic:*
```
Public Function AddBand( _
   ByVal pISignalDescription As ISignalDescription, _
   ByVal pIBandDef As IBandDef3, _
   ByRef ppISignal As ISignal5 _
) As DataBand
```

### Parameters

pISignalDescription

The description of the signal of the band.

pIBandDef

The definition of the band.

ppISignal

The signal of the band. This is an output parameter.

### Return Type

The created DataBand Object.

### Remarks

When a signal with the given signal description does not exist, it is created. Otherwise, the band is added to the signal. In any case, the signal is returned in the signal parameter. The given band definition must be unique for the signal, i.e. the band definition object must not be equal to any other band definition of this signal. To remove an existing band, use the RemoveBand Method.

The value of SignalDescription.XAxis.MaxCount property must be equal to the number of scan points.

### Example

This macro copies an existing original band as a new user-defined band.

- Add Band (Visual Basic)

```
Option Explicit

Sub Main
    Dim oFile As New PolyFile
    oFile.Readonly = False

    oFile.Open("D:\Temp\Example.svd")

    Dim oBandDomains As BandDomains
    Set oBandDomains = oFile.GetBandDomains()

    Dim oBandDomain As BandDomain
    Set oBandDomain = oBandDomains.Type(ptcDomainSpectrum)

    Dim oDomain As Domain
    Set oDomain = oBandDomain

    Dim oSignal As Signal
    Set oSignal = oDomain.Channels("Vib").Signals("Velocity")

    ' use the signal description, band definition and data of an existing, original band
    Dim oSigDesc As SignalDescription
    Set oSigDesc = oSignal.Description.Clone()

    Dim oDataBand As DataBand
    Set oDataBand = oBandDomain.GetDataBands(oSignal)(2)

    Dim oBandDef As BandDef
    Set oBandDef = oDataBand.BandDefinition

    Dim Data() As Single
    Data = oDataBand.GetData(oSignal.Displays.Type(ptcDisplayRealImag), 0)

    ' if this band exists already as user-defined band, remove it
    Dim oExistingSignal As Signal
    Dim oExistingBand As DataBand
    Set oExistingBand = oBandDomains.FindBand(oSigDesc, True, oBandDef, oExistingSignal)
    If (Not oExistingBand Is Nothing) Then
        oBandDomains.RemoveBand(oExistingSignal, oExistingBand.BandDefinition)
    End If

    ' add the new user-defined band
    Dim oBandSignal As Signal
    Dim oNewDataBand As DataBand
    Set oNewDataBand = oBandDomains.AddBand(oSigDesc, oBandDef, oBandSignal)

    ' copy the data of the original band
    oNewDataBand.SetData(oBandSignal, 1, Data)

    oFile.Save()
    oFile.Close()
End Sub
```


---

## FindBand Method

*Quelle: `POLYFILELib~BandDomains~FindBand.html` · Polytec PolyFile Type Library · BandDomains Collection : FindBand Method*

### Description

Finds the band with the given signal description and band definition and returns the signal the band belongs to and the DataBand Object of the band.

### Syntax

*Visual Basic:*
```
Public Function FindBand( _
   ByVal pISignalDescription As ISignalDescription, _
   ByVal vbUserSignal As Boolean, _
   ByVal pIBandDef As IBandDef3, _
   ByRef ppISignal As ISignal5 _
) As DataBand
```

### Parameters

pISignalDescription

The signal description of the band.

vbUserSignal

Specifies whether a user-defined band or an original band is searched.

pIBandDef

The band definition of the band.

ppISignal

The signal the band belongs to or nothing if the band does not exist. This is an output parameter.

### Return Type

The DataBand Object of the band or nothing if the band does not exist.

### Remarks

For an example to use this method, see AddBand Method.


---

## FindSignal Method

*Quelle: `POLYFILELib~BandDomains~FindSignal.html` · Polytec PolyFile Type Library · BandDomains Collection : FindSignal Method*

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


---

## RemoveBand Method

*Quelle: `POLYFILELib~BandDomains~RemoveBand.html` · Polytec PolyFile Type Library · BandDomains Collection : RemoveBand Method*

### Description

Removes the user-defined band with the given definition from the given signal.

### Syntax

*Visual Basic:*
```
Public Sub RemoveBand( _
   ByVal pISignal As ISignal5, _
   ByVal pIBandDef As IBandDef3 _
)
```

### Parameters

pISignal

The signal to remove the band from.

pIBandDef

The definition of the band.

### Remarks

When the last band of the signal is removed, the signal will be removed, too. The signal must be a Signal Object of the Usr or Usr 3D Channel of a BandDomain Object.

For an example to use this method, see AddBand Method.


---

## Count Property

*Quelle: `POLYFILELib~BandDomains~Count.html` · Polytec PolyFile Type Library · BandDomains Collection : Count Property*

### Description

Returns the number of items in the BandDomains collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Count As Long
```


---

## Exists Property

*Quelle: `POLYFILELib~BandDomains~Exists.html` · Polytec PolyFile Type Library · BandDomains Collection : Exists Property*

### Description

Returns True if the item of the given name or type exists in the BandDomains collection.

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

Name (string) or Type (PTCDomainType) of the BandDomain object


---

## Item Property

*Quelle: `POLYFILELib~BandDomains~Item.html` · Polytec PolyFile Type Library · BandDomains Collection : Item Property*

### Description

Returns an item of the BandDomains collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Item( _
   ByVal IndexOrName As Variant _
) As BandDomain
```

### Parameters

IndexOrName

Name (string) or index (integer) of the item.


---

## Type Property

*Quelle: `POLYFILELib~BandDomains~Type.html` · Polytec PolyFile Type Library · BandDomains Collection : Type Property*

### Description

Returns an item of the BandDomains collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Type( _
   ByVal ptcDomainType As PTCDomainType _
) As BandDomain
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
Type of the BandDomain
