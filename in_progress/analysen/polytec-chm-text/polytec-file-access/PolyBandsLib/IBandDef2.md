# PolyBandsLib – IBandDef2

## IBandDef2 Interface

*Quelle: `PolyBandsLib~IBandDef2.html` · Polytec PolyBands Type Library*

### Description

Contains the definition of a single band. Item of the BandDefs Collection.

### Remarks

It is recommended to cast to the BandDef Object.

### Example


---

## IBandDef2 Interface Members

*Quelle: `PolyBandsLib~IBandDef2_members.html` · Polytec PolyBands Type Library*

### Public Methods

| Copy | Copies the band definition from the input parameter to this object. |
|---|---|
| IsEqual | Returns true if the input BandDef is equal to this band definition. |

### Public Properties

| Peak | Peak value of a band used for FFT band calculation. |
|---|---|
| Start | Start value of a band. |
| Step | Frequency steps in a band. Used by the PMA software only. |
| Stop | End value of a band. |


---

## Copy Method

*Quelle: `PolyBandsLib~IBandDef2~Copy.html` · Polytec PolyBands Type Library · IBandDef2 Interface : Copy Method*

### Description

Copies the band definition from the input parameter to this object.

### Syntax

*Visual Basic:*
```
Public Sub Copy( _
   ByVal pIBandDef2 As IBandDef2 _
)
```

### Parameters

pIBandDef2

Source band definition.


---

## IsEqual Method

*Quelle: `PolyBandsLib~IBandDef2~IsEqual.html` · Polytec PolyBands Type Library · IBandDef2 Interface : IsEqual Method*

### Description

Returns true if the input BandDef is equal to this band definition.

### Syntax

*Visual Basic:*
```
Public Function IsEqual( _
   ByVal pIBandDef2 As IBandDef2 _
) As Boolean
```

### Parameters

pIBandDef2

BandDef object to be compared with.


---

## Peak Property

*Quelle: `PolyBandsLib~IBandDef2~Peak.html` · Polytec PolyBands Type Library · IBandDef2 Interface : Peak Property*

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

*Quelle: `PolyBandsLib~IBandDef2~Start.html` · Polytec PolyBands Type Library · IBandDef2 Interface : Start Property*

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

## Step Property

*Quelle: `PolyBandsLib~IBandDef2~Step.html` · Polytec PolyBands Type Library · IBandDef2 Interface : Step Property*

### Description

Frequency steps in a band. Used by the PMA software only.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Step As Single
```


---

## Stop Property

*Quelle: `PolyBandsLib~IBandDef2~Stop.html` · Polytec PolyBands Type Library · IBandDef2 Interface : Stop Property*

### Description

End value of a band.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Stop As Single
```
