# POLYFILELib – IVersion2

## IVersion2 Interface

*Quelle: `POLYFILELib~IVersion2.html` · Polytec PolyFile Type Library*

### Description

IVersion2 Interface

### Remarks

It is recommended to cast to the Version Object.


---

## IVersion2 Interface Members

*Quelle: `POLYFILELib~IVersion2_members.html` · Polytec PolyFile Type Library*

### Public Methods

| Save | Commits the changes to the Version object to the file. |
|---|---|

### Public Properties

| FileID | Specifies the file type. |
|---|---|
| FileTime | Specifies the creation time of the file (time of measurement). |
| FileVersion | Specifies the file version as hexadecimal number. |
| ProgramID | Specifies the program type that generated the file. |
| ProgramVersion | Specifies the program version as a hexadecimal value. |


---

## Save Method

*Quelle: `POLYFILELib~IVersion2~Save.html` · Polytec PolyFile Type Library · IVersion2 Interface : Save Method*

### Description

Commits the changes to the Version object to the file.

### Syntax

*Visual Basic:*
```
Public Sub Save()
```


---

## FileID Property

*Quelle: `POLYFILELib~IVersion2~FileID.html` · Polytec PolyFile Type Library · IVersion2 Interface : FileID Property*

### Description

Specifies the file type.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property FileID As PTCFileID
```


---

## FileTime Property

*Quelle: `POLYFILELib~IVersion2~FileTime.html` · Polytec PolyFile Type Library · IVersion2 Interface : FileTime Property*

### Description

Specifies the creation time of the file (time of measurement).

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property FileTime As Date
```


---

## FileVersion Property

*Quelle: `POLYFILELib~IVersion2~FileVersion.html` · Polytec PolyFile Type Library · IVersion2 Interface : FileVersion Property*

### Description

Specifies the file version as hexadecimal number.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property FileVersion As Long
```

### Return Type

The file version is returned in hexadecimal format. E.g. means a value of 0x860 that the file version is 8.6.


---

## ProgramID Property

*Quelle: `POLYFILELib~IVersion2~ProgramID.html` · Polytec PolyFile Type Library · IVersion2 Interface : ProgramID Property*

### Description

Specifies the program type that generated the file.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property ProgramID As PTCProgramID
```


---

## ProgramVersion Property

*Quelle: `POLYFILELib~IVersion2~ProgramVersion.html` · Polytec PolyFile Type Library · IVersion2 Interface : ProgramVersion Property*

### Description

Specifies the program version as a hexadecimal value.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property ProgramVersion As Long
```

### Return Type

The program version is returned in hexadecimal format. E.g. means a value of 0x8600 that the program version is 8.6.

### Example
