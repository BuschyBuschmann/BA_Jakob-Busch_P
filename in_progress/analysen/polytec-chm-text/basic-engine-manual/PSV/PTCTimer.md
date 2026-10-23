# PSV – PTCTimer

## PTCTimer Object

*Quelle: `PSV~PTCTimer.html` · Polytec PSV Type Library*

### Description

The PTCTimer object can be used to perform periodic tasks.

### Remarks

This class can be instantiated using the string "Psv.PTCTimer".


---

## PTCTimer Object Members

*Quelle: `PSV~PTCTimer_members.html` · Polytec PSV Type Library*

### Public Properties

| Interval | Specifies the interval between two timer events in ms. |
|---|---|

### Events

| Timer | The timer event occurs after each completed timer interval . |
|---|---|


---

## Interval Property

*Quelle: `PSV~PTCTimer~Interval.html` · Polytec PSV Type Library · PTCTimer Object : Interval Property*

### Description

Specifies the interval between two timer events in ms.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Interval As Long
```

### Remarks

If the value is 0, the timer is disabled.


---

## Timer Event

*Quelle: `PSV~PTCTimer~Timer_EV.html` · Polytec PSV Type Library · PTCTimer Object : Timer Event*

### Description

The timer event occurs after each completed timer interval.

### Syntax

*Visual Basic:*
```
Public Event Timer()
```
