# POLYSIGNALLib – Channel

## Channel Object

*Quelle: `POLYSIGNALLib~Channel.html` · Polytec PolySignal Type Library*

### Description

Item of the Channels collection. A channel represents a single acquisition channel (Vib, Ref1, Ref2, Ref3) or a combination of acquisition channels, e.g. Vib & Ref1.

### Object Model


---

## Channel Object Members

*Quelle: `POLYSIGNALLib~Channel_members.html` · Polytec PolySignal Type Library*

### Public Properties

| Caps | The capabilities of the channel. |
|---|---|
| Domain | The domain of the channel. |
| Name | The name of the channel. |
| Signals | All available signals of the channel. |


---

## Caps Property

*Quelle: `POLYSIGNALLib~Channel~Caps.html` · Polytec PolySignal Type Library · Channel Object : Caps Property*

### Description

The capabilities of the channel.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Caps As PTCChannelCapsType
```


---

## Domain Property

*Quelle: `POLYSIGNALLib~Channel~Domain.html` · Polytec PolySignal Type Library · Channel Object : Domain Property*

### Description

The domain of the channel.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Domain As Domain
```


---

## Name Property

*Quelle: `POLYSIGNALLib~Channel~Name.html` · Polytec PolySignal Type Library · Channel Object : Name Property*

### Description

The name of the channel.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Name As String
```

### Remarks

Can be used as an index into the Channels collection.


---

## Signals Property

*Quelle: `POLYSIGNALLib~Channel~Signals.html` · Polytec PolySignal Type Library · Channel Object : Signals Property*

### Description

All available signals of the channel.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Signals As Signals
```
