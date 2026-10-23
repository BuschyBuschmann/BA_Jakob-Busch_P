# PolyBandsLib – BandDef

## BandDef Object

*Quelle: `PolyBandsLib~BandDef.html` · Polytec PolyBands Type Library*

### Description

Contains the definition of a single band. Item of the BandDefs Collection.

### Object Model


---

## BandDef Object Members

*Quelle: `PolyBandsLib~BandDef_members.html` · Polytec PolyBands Type Library*

### Public Methods

| Clone | Returns a copy of the BandDef object. |
|---|---|
| Copy | Copies the band definition from the input parameter to this object. |
| IsEqual | Returns true if the input BandDef is equal to this band definition. |

### Public Properties

| Peak | Peak value of a band used for FFT band calculation. |
|---|---|
| Start | Start value of a band. |
| Step | Frequency steps in a band. Used by the PMA software only. |
| Stop | End value of a band. |


---

## Clone Method

*Quelle: `PolyBandsLib~BandDef~Clone.html` · Polytec PolyBands Type Library · BandDef Object : Clone Method*

### Description

Returns a copy of the BandDef object.

### Syntax

*Visual Basic:*
```
Public Function Clone() As BandDef
```

### Return Type

The new BandDef object.


---

## Copy Method

*Quelle: `PolyBandsLib~BandDef~Copy.html` · Polytec PolyBands Type Library · BandDef Object : Copy Method*

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

*Quelle: `PolyBandsLib~BandDef~IsEqual.html` · Polytec PolyBands Type Library · BandDef Object : IsEqual Method*

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

*Quelle: `PolyBandsLib~BandDef~Peak.html` · Polytec PolyBands Type Library · BandDef Object : Peak Property*

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

*Quelle: `PolyBandsLib~BandDef~Start.html` · Polytec PolyBands Type Library · BandDef Object : Start Property*

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

*Quelle: `PolyBandsLib~BandDef~Step.html` · Polytec PolyBands Type Library · BandDef Object : Step Property*

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

*Quelle: `PolyBandsLib~BandDef~Stop.html` · Polytec PolyBands Type Library · BandDef Object : Stop Property*

### Description

End value of a band.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Stop As Single
```
