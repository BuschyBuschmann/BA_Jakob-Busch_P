# PolyBandsLib – IBandDef

## IBandDef Interface

*Quelle: `PolyBandsLib~IBandDef.html` · Polytec PolyBands Type Library*

### Description

Contains the definition of a single band. Item of the BandDefs Collection.

### Remarks

It is recommended to cast to the BandDef Object.


---

## IBandDef Interface Members

*Quelle: `PolyBandsLib~IBandDef_members.html` · Polytec PolyBands Type Library*

### Public Methods

| Copy | Copies the band definition from the input parameter to this object. |
|---|---|
| IsEqual | Returns true if the input BandDef is equal to this band definition. |

### Public Properties

| Peak | Peak value of a band used for FFT band calculation. |
|---|---|
| Start | Start value of a band. |
| Stop | End value of a band. |


---

## Copy Method

*Quelle: `PolyBandsLib~IBandDef~Copy.html` · Polytec PolyBands Type Library · IBandDef Interface : Copy Method*

### Description

Copies the band definition from the input parameter to this object.

### Syntax

*Visual Basic:*
```
Public Sub Copy( _
   ByVal pIBandDef As IBandDef _
)
```

### Parameters

pIBandDef

The band definition to copy.


---

## IsEqual Method

*Quelle: `PolyBandsLib~IBandDef~IsEqual.html` · Polytec PolyBands Type Library · IBandDef Interface : IsEqual Method*

### Description

Returns true if the input BandDef is equal to this band definition.

### Syntax

*Visual Basic:*
```
Public Function IsEqual( _
   ByVal pIBandDef As IBandDef _
) As Boolean
```

### Parameters

pIBandDef

The band definition to compare with.


---

## Peak Property

*Quelle: `PolyBandsLib~IBandDef~Peak.html` · Polytec PolyBands Type Library · IBandDef Interface : Peak Property*

### Description

Peak value of a band used for FFT band calculation.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Peak As Single
```


---

## Start Property

*Quelle: `PolyBandsLib~IBandDef~Start.html` · Polytec PolyBands Type Library · IBandDef Interface : Start Property*

### Description

Start value of a band.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Start As Single
```


---

## Stop Property

*Quelle: `PolyBandsLib~IBandDef~Stop.html` · Polytec PolyBands Type Library · IBandDef Interface : Stop Property*

### Description

End value of a band.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Stop As Single
```
