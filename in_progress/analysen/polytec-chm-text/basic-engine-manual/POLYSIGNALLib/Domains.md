# POLYSIGNALLib – Domains

## Domains Collection

*Quelle: `POLYSIGNALLib~Domains.html` · Polytec PolySignal Type Library*

### Description

The typed and named collection of the domains.

### Object Model


---

## Domains Collection Members

*Quelle: `POLYSIGNALLib~Domains_members.html` · Polytec PolySignal Type Library*

### Public Properties

| Count | The number of items in the collection. |
|---|---|
| Exists | Returns true if the item with the given name or type exists in the collection. |
| Item | Returns the item with the given name or index. |
| Type | Returns the item with the given domain type. |


---

## Count Property

*Quelle: `POLYSIGNALLib~Domains~Count.html` · Polytec PolySignal Type Library · Domains Collection : Count Property*

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

*Quelle: `POLYSIGNALLib~Domains~Exists.html` · Polytec PolySignal Type Library · Domains Collection : Exists Property*

### Description

Returns true if the item with the given name or type exists in the collection.

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

The name or type of the domain.


---

## Item Property

*Quelle: `POLYSIGNALLib~Domains~Item.html` · Polytec PolySignal Type Library · Domains Collection : Item Property*

### Description

Returns the item with the given name or index.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Item( _
   ByVal Index As Variant _
) As Domain
```

### Parameters

Index

The name or index of the item.


---

## Type Property

*Quelle: `POLYSIGNALLib~Domains~Type.html` · Polytec PolySignal Type Library · Domains Collection : Type Property*

### Description

Returns the item with the given domain type.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Type( _
   ByVal eType As PTCDomainType _
) As Domain
```

### Parameters

eType

| Value | Description |
|---|---|
| ptcDomain3rdOctave | Domain 3rdOctave. |
| ptcDomainAngleSync | Domain synchronized angle (for order analysis, not supported any more). |
| ptcDomainNotAvail | Domain is not available. |
| ptcDomainOrderSpectrum | Domain order spectrum (for order analysis, not supported any more). |
| ptcDomainRMS | Domain RMS. |
| ptcDomainSpectrum | Domain Spectrum. |
| ptcDomainTime | Domain Time. |
The type of the domain.
