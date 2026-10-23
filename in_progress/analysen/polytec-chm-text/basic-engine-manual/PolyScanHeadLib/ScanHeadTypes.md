# PolyScanHeadLib – ScanHeadTypes

## ScanHeadTypes Collection

*Quelle: `PolyScanHeadLib~ScanHeadTypes.html` · Polytec PolyScanHead Type Library*

### Description

The named and typed collection of the available scanning head types.

### Object Model


---

## ScanHeadTypes Collection Members

*Quelle: `PolyScanHeadLib~ScanHeadTypes_members.html` · Polytec PolyScanHead Type Library*

### Public Methods

| Init | Initializes the scanning head types collection. |
|---|---|

### Public Properties

| ActiveScanHeadType | The active scanning head type. |
|---|---|
| Count | The number of items in the collection. |
| Exists | Returns true if an item with the given index exists in the collection. |
| Item | Returns the item with the given index from the collection. |
| Type | Returns the item with the given type from the collection. |


---

## Init Method

*Quelle: `PolyScanHeadLib~ScanHeadTypes~Init.html` · Polytec PolyScanHead Type Library · ScanHeadTypes Collection : Init Method*

### Description

Initializes the scanning head types collection.

### Syntax

*Visual Basic:*
```
Public Sub Init( _
   ByVal pVal As IFrontEnd _
)
```

### Parameters

pVal

The interface to the front end that is used to control the scanning heads.


---

## ActiveScanHeadType Property

*Quelle: `PolyScanHeadLib~ScanHeadTypes~ActiveScanHeadType.html` · Polytec PolyScanHead Type Library · ScanHeadTypes Collection : ActiveScanHeadType Property*

### Description

The active scanning head type.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property ActiveScanHeadType As ScanHeadType
```


---

## Count Property

*Quelle: `PolyScanHeadLib~ScanHeadTypes~Count.html` · Polytec PolyScanHead Type Library · ScanHeadTypes Collection : Count Property*

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

## Exists Property

*Quelle: `PolyScanHeadLib~ScanHeadTypes~Exists.html` · Polytec PolyScanHead Type Library · ScanHeadTypes Collection : Exists Property*

### Description

Returns true if an item with the given index exists in the collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Exists( _
   ByVal Index As Variant _
) As Boolean
```

### Parameters

Index

Name or type of the item.


---

## Item Property

*Quelle: `PolyScanHeadLib~ScanHeadTypes~Item.html` · Polytec PolyScanHead Type Library · ScanHeadTypes Collection : Item Property*

### Description

Returns the item with the given index from the collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Item( _
   ByVal vtIndex As Variant _
) As ScanHeadType
```

### Parameters

vtIndex

The index or name of the given item.


---

## Type Property

*Quelle: `PolyScanHeadLib~ScanHeadTypes~Type.html` · Polytec PolyScanHead Type Library · ScanHeadTypes Collection : Type Property*

### Description

Returns the item with the given type from the collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Type( _
   ByVal PTCScanHeadType As PTCScanHeadType _
) As ScanHeadType
```

### Parameters

PTCScanHeadType

| Value | Description |
|---|---|
| ptcScanHeadTypeMPVI800 | MPV-I-800 |
| ptcScanHeadTypeMSAI100 | MSA-I-100 |
| ptcScanHeadTypeMSAI400 | MSA-I-400 |
| ptcScanHeadTypeMSAI500 | MSA-I-500 |
| ptcScanHeadTypeMSAI600 | MSA-I-600 |
| ptcScanHeadTypeMSAI620 | MSA-I-620 |
| ptcScanHeadTypeMSAI630 | MSA-I-630 |
| ptcScanHeadTypeMSAI650 | MSA-I-650 |
| ptcScanHeadTypeMSV | MSV, ID not used anymore |
| ptcScanHeadTypeMSV_NTSC | MSV NTSC, ID not used anymore |
| ptcScanHeadTypeNone | No scanning head |
| ptcScanHeadTypeOFV040 | OFV040, ID not used anymore |
| ptcScanHeadTypeOFV048Down | OFV048 Down, ID not used anymore |
| ptcScanHeadTypeOFV048Front | OFV048 Front, ID not used anymore |
| ptcScanHeadTypeOFV050 | OFV050, ID not used anymore |
| ptcScanHeadTypeOFV055 | OFV055, ID not used anymore |
| ptcScanHeadTypeOFV055F | OFV055F, ID not used anymore |
| ptcScanHeadTypeOFV056 | OFV056, ID not used anymore |
| ptcScanHeadTypeOFV534 | OFV-534 |
| ptcScanHeadTypePSV500 | PSV-I-500, PSV-I-520, PSV-I-560, or PSV-I-570 |
| ptcScanHeadTypePSV6xx | PSV-I-680 or PSV-I-690 |
| ptcScanHeadTypePSVI400_LR | PSV-I-400 LR with OFV-505 |
| ptcScanHeadTypePSVI400_MR | PSV-I-400 MR with OFV-505 |
| ptcScanHeadTypePSVI7xx | VibroScan PSV-I-730 or PSV-I-780 |
| ptcScanHeadTypeUHF120 | UHF-I-120 |
| ptcScanHeadTypeVFX_I_130 | VFX-I-130 |
| ptcScanHeadTypeVIO_I_130 | VIO-I-130 |
| ptcScanHeadTypeVPI | VPI, ID not used anymore |
The type of the item.
