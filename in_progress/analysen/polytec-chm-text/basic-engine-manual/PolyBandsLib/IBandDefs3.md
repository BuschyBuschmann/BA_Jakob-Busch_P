# PolyBandsLib – IBandDefs3

## IBandDefs3 Collection

*Quelle: `PolyBandsLib~IBandDefs3.html` · Polytec PolyBands Type Library*

### Description

Collection of BandDef objects.

### Object Model

### Remarks

It is recommended to cast to the BandDefs Object.


---

## IBandDefs3 Collection Members

*Quelle: `PolyBandsLib~IBandDefs3_members.html` · Polytec PolyBands Type Library*

### Public Methods

| Add | Adds an new band to the collection and returns it. |
|---|---|
| Clear | Removes all items from the collection. |
| Clone | Returns a copy of the BandDefs collection. |
| Copy | Copies all items of the given BandDefs collection to this collection. |
| IsEqual | Returns true when all items of the given BandDefs collection are equal to the items of this collection. |
| Load | Loads the band definition from an ASCII text file. |
| Remove | Removes an item from the collection. |
| SaveAs | Saves all band definitions to an ASCII text file. |

### Public Properties

| Count | The number of items in the collection. |
|---|---|
| HasFreqStep | True if the band definitions contain frequency steps for the PMA software. |
| Item | Returns and item of the collection. |


---

## Add Method

*Quelle: `PolyBandsLib~IBandDefs3~Add.html` · Polytec PolyBands Type Library · IBandDefs3 Collection : Add Method*

### Description

Adds an new band to the collection and returns it.

### Syntax

*Visual Basic:*
```
Public Function Add() As BandDef
```


---

## Clear Method

*Quelle: `PolyBandsLib~IBandDefs3~Clear.html` · Polytec PolyBands Type Library · IBandDefs3 Collection : Clear Method*

### Description

Removes all items from the collection.

### Syntax

*Visual Basic:*
```
Public Sub Clear()
```


---

## Clone Method

*Quelle: `PolyBandsLib~IBandDefs3~Clone.html` · Polytec PolyBands Type Library · IBandDefs3 Collection : Clone Method*

### Description

Returns a copy of the BandDefs collection.

### Syntax

*Visual Basic:*
```
Public Function Clone() As BandDefs
```

### Return Type

The new BandDefs collection.


---

## Copy Method

*Quelle: `PolyBandsLib~IBandDefs3~Copy.html` · Polytec PolyBands Type Library · IBandDefs3 Collection : Copy Method*

### Description

Copies all items of the given BandDefs collection to this collection.

### Syntax

*Visual Basic:*
```
Public Sub Copy( _
   ByVal ppIBandDefs3 As BandDefs _
)
```

### Parameters

ppIBandDefs3

The BandDefs collection to copy the items from.


---

## IsEqual Method

*Quelle: `PolyBandsLib~IBandDefs3~IsEqual.html` · Polytec PolyBands Type Library · IBandDefs3 Collection : IsEqual Method*

### Description

Returns true when all items of the given BandDefs collection are equal to the items of this collection.

### Syntax

*Visual Basic:*
```
Public Function IsEqual( _
   ByVal pIBandDefs As BandDefs _
) As Boolean
```

### Parameters

pIBandDefs

The BandDefs collection to compare this collection with.

### Return Type

True when the number of items is equal and all items have the same properties.


---

## Load Method

*Quelle: `PolyBandsLib~IBandDefs3~Load.html` · Polytec PolyBands Type Library · IBandDefs3 Collection : Load Method*

### Description

Loads the band definition from an ASCII text file.

### Syntax

*Visual Basic:*
```
Public Sub Load( _
   ByVal bstrFileName As String _
)
```

### Parameters

bstrFileName

The name of the text file.


---

## Remove Method

*Quelle: `PolyBandsLib~IBandDefs3~Remove.html` · Polytec PolyBands Type Library · IBandDefs3 Collection : Remove Method*

### Description

Removes an item from the collection.

### Syntax

*Visual Basic:*
```
Public Sub Remove( _
   ByVal lIndex As Long _
)
```

### Parameters

lIndex

The index of the item.


---

## SaveAs Method

*Quelle: `PolyBandsLib~IBandDefs3~SaveAs.html` · Polytec PolyBands Type Library · IBandDefs3 Collection : SaveAs Method*

### Description

Saves all band definitions to an ASCII text file.

### Syntax

*Visual Basic:*
```
Public Sub SaveAs( _
   ByVal bstrFileName As String _
)
```

### Parameters

bstrFileName

The name of the ASCII text file.


---

## Count Property

*Quelle: `PolyBandsLib~IBandDefs3~Count.html` · Polytec PolyBands Type Library · IBandDefs3 Collection : Count Property*

### Description

The number of items in the collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Count As Long
```


---

## HasFreqStep Property

*Quelle: `PolyBandsLib~IBandDefs3~HasFreqStep.html` · Polytec PolyBands Type Library · IBandDefs3 Collection : HasFreqStep Property*

### Description

True if the band definitions contain frequency steps for the PMA software.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property HasFreqStep As Boolean
```


---

## Item Property

*Quelle: `PolyBandsLib~IBandDefs3~Item.html` · Polytec PolyBands Type Library · IBandDefs3 Collection : Item Property*

### Description

Returns and item of the collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Item( _
   ByVal lIndex As Long _
) As BandDef
```

### Parameters

lIndex

The index of the item.
