# POLYSIGNALLib – IDomains

## IDomains Collection

*Quelle: `POLYSIGNALLib~IDomains.html` · Polytec PolySignal Type Library*

### Description

IDomains Interface

### Object Model

### Remarks

It is recommended to cast to the Domains collection.


---

## IDomains Collection Members

*Quelle: `POLYSIGNALLib~IDomains_members.html` · Polytec PolySignal Type Library*

### Public Properties

| Count | The number of items in the collection. |
|---|---|
| Exists | Returns true if the item with the given name or type exists in the collection. |
| Item | Returns the item with the given name or index. |
| Type | Returns the item with the given domain type. |


---

## Count Property

*Quelle: `POLYSIGNALLib~IDomains~Count.html` · Polytec PolySignal Type Library · IDomains Collection : Count Property*

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

*Quelle: `POLYSIGNALLib~IDomains~Exists.html` · Polytec PolySignal Type Library · IDomains Collection : Exists Property*

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

*Quelle: `POLYSIGNALLib~IDomains~Item.html` · Polytec PolySignal Type Library · IDomains Collection : Item Property*

### Description

Returns the item with the given name or index.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Item( _
   ByVal Index As Variant _
) As IDomain
```

### Parameters

Index

The name or index of the item.


---

## Type Property

*Quelle: `POLYSIGNALLib~IDomains~Type.html` · Polytec PolySignal Type Library · IDomains Collection : Type Property*

### Description

Returns the item with the given domain type.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Type( _
   ByVal eType As PTCDomainType _
) As IDomain
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
