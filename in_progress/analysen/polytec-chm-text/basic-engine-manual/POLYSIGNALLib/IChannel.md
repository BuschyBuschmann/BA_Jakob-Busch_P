# POLYSIGNALLib – IChannel

## IChannel Interface

*Quelle: `POLYSIGNALLib~IChannel.html` · Polytec PolySignal Type Library*

### Description

Item of the Channels collection. A channel represents a single acquisition channel (Vib, Ref1, Ref2, Ref3) or a combination of acquisition channels, e.g. Vib & Ref1.

### Object Model

### Remarks

It is recommended to cast to the Channel object.


---

## IChannel Interface Members

*Quelle: `POLYSIGNALLib~IChannel_members.html` · Polytec PolySignal Type Library*

### Public Properties

| Domain | The domain of the channel. |
|---|---|
| Name | The name of the channel. |
| Signals | All available signals of the channel. |


---

## Domain Property

*Quelle: `POLYSIGNALLib~IChannel~Domain.html` · Polytec PolySignal Type Library · IChannel Interface : Domain Property*

### Description

The domain of the channel.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Domain As IDomain
```


---

## Name Property

*Quelle: `POLYSIGNALLib~IChannel~Name.html` · Polytec PolySignal Type Library · IChannel Interface : Name Property*

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

*Quelle: `POLYSIGNALLib~IChannel~Signals.html` · Polytec PolySignal Type Library · IChannel Interface : Signals Property*

### Description

All available signals of the channel.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Signals As ISignals
```
