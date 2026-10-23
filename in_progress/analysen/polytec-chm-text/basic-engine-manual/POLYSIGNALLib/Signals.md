# POLYSIGNALLib – Signals

## Signals Collection

*Quelle: `POLYSIGNALLib~Signals.html` · Polytec PolySignal Type Library*

### Description

Named collection of the available signals of a Channel.

### Object Model

### Remarks

To add a user-defined signal to the signals collection of the Usr or Usr 3D channel see the AddBand Method of the BandDomains Object, the AddSignal Method of the PointDomains Object, or the AddSignal Method of the PointAverageDomains Object.


---

## Signals Collection Members

*Quelle: `POLYSIGNALLib~Signals_members.html` · Polytec PolySignal Type Library*

### Public Methods

| Remove | Removes a user signal from the collection. |
|---|---|
| Update | Updates the signal description of a user signal. |

### Public Properties

| Count | The number of items in the collection. |
|---|---|
| Exists | Returns true if the item with the given index or name exists in the collection. |
| Item | Returns an item of the collection with the given index or name. |
| PreferredItem | Returns the signal that is preferred for display in the analyzer. |


---

## Remove Method

*Quelle: `POLYSIGNALLib~Signals~Remove.html` · Polytec PolySignal Type Library · Signals Collection : Remove Method*

### Description

Removes a user signal from the collection.

### Syntax

*Visual Basic:*
```
Public Sub Remove( _
   ByVal vtIndex As Variant _
)
```

### Parameters

vtIndex

The index or name of the signal.

### Remarks

You can remove signals from the Usr or Usr 3D channel only. To add a signal see the AddBand Method of the BandDomains Object, the AddSignal Method of the PointDomains Object, or the AddSignal Method of the PointAverageDomains Object.


---

## Update Method

*Quelle: `POLYSIGNALLib~Signals~Update.html` · Polytec PolySignal Type Library · Signals Collection : Update Method*

### Description

Updates the signal description of a user signal.

### Syntax

*Visual Basic:*
```
Public Sub Update( _
   ByVal vtIndex As Variant, _
   ByVal pISignalDescription As SignalDescription _
)
```

### Parameters

vtIndex

The name or index of the user signal.

pISignalDescription

The new description of the signal.

### Remarks

You can call this method only for signals in the Usr or Usr 3D channel. The properties you can update are limited. E.g. you must not change a property that changes the number of data values the signal has. You can change the name of the signal if the new name does not exist already.


---

## Count Property

*Quelle: `POLYSIGNALLib~Signals~Count.html` · Polytec PolySignal Type Library · Signals Collection : Count Property*

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

*Quelle: `POLYSIGNALLib~Signals~Exists.html` · Polytec PolySignal Type Library · Signals Collection : Exists Property*

### Description

Returns true if the item with the given index or name exists in the collection.

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

The index or name of the item.


---

## Item Property

*Quelle: `POLYSIGNALLib~Signals~Item.html` · Polytec PolySignal Type Library · Signals Collection : Item Property*

### Description

Returns an item of the collection with the given index or name.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Item( _
   ByVal Index As Variant _
) As Signal
```

### Parameters

Index

The index or name of the item.


---

## PreferredItem Property

*Quelle: `POLYSIGNALLib~Signals~PreferredItem.html` · Polytec PolySignal Type Library · Signals Collection : PreferredItem Property*

### Description

Returns the signal that is preferred for display in the analyzer.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property PreferredItem As Signal
```
