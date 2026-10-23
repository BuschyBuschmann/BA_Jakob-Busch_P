# PolyBandsLib – IBandDefs

## IBandDefs Collection

*Quelle: `PolyBandsLib~IBandDefs.html` · Polytec PolyBands Type Library*

### Description

Collection of BandDef objects.

### Object Model

### Remarks

It is recommended to cast to the BandDefs collection.


---

## IBandDefs Collection Members

*Quelle: `PolyBandsLib~IBandDefs_members.html` · Polytec PolyBands Type Library*

### Public Methods

| Add | Adds an new band to the collection and returns it. |
|---|---|
| Clear | Removes all items from the collection. |
| Load | Loads the band definition from an ASCII text file. |
| Remove | Removes an item from the collection. |
| SaveAs | Saves all band definitions to an ASCII text file. |

### Public Properties

| Count | The number of items in the collection. |
|---|---|
| Item | Returns and item of the collection. |


---

## Add Method

*Quelle: `PolyBandsLib~IBandDefs~Add.html` · Polytec PolyBands Type Library · IBandDefs Collection : Add Method*

### Description

Adds an new band to the collection and returns it.

### Syntax

*Visual Basic:*
```
Public Function Add() As IBandDef
```


---

## Clear Method

*Quelle: `PolyBandsLib~IBandDefs~Clear.html` · Polytec PolyBands Type Library · IBandDefs Collection : Clear Method*

### Description

Removes all items from the collection.

### Syntax

*Visual Basic:*
```
Public Sub Clear()
```


---

## Load Method

*Quelle: `PolyBandsLib~IBandDefs~Load.html` · Polytec PolyBands Type Library · IBandDefs Collection : Load Method*

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

*Quelle: `PolyBandsLib~IBandDefs~Remove.html` · Polytec PolyBands Type Library · IBandDefs Collection : Remove Method*

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

*Quelle: `PolyBandsLib~IBandDefs~SaveAs.html` · Polytec PolyBands Type Library · IBandDefs Collection : SaveAs Method*

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

*Quelle: `PolyBandsLib~IBandDefs~Count.html` · Polytec PolyBands Type Library · IBandDefs Collection : Count Property*

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

## Item Property

*Quelle: `PolyBandsLib~IBandDefs~Item.html` · Polytec PolyBands Type Library · IBandDefs Collection : Item Property*

### Description

Returns and item of the collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Item( _
   ByVal lIndex As Long _
) As IBandDef
```

### Parameters

lIndex

The index of the item.
