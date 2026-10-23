# POLYFILELib – SummaryInfo

## SummaryInfo Object

*Quelle: `POLYFILELib~SummaryInfo.html` · Polytec PolyFile Type Library*

### Description

The properties of the summery info are standard properties of a file in the Microsoft® Windows® compound file format. The properties can be displayed in the Windows® explorer.


---

## SummaryInfo Object Members

*Quelle: `POLYFILELib~SummaryInfo_members.html` · Polytec PolyFile Type Library*

### Public Methods

| Save | Commits the changes to the SummaryInfo object to the file. |
|---|---|

### Public Properties

| Author | Specifies the author of the file. |
|---|---|
| Comments | Specifies the comments of the file. |
| Subject | Specifies the subject of the file. |
| Title | Specifies the title of the file. |


---

## Save Method

*Quelle: `POLYFILELib~SummaryInfo~Save.html` · Polytec PolyFile Type Library · SummaryInfo Object : Save Method*

### Description

Commits the changes to the SummaryInfo object to the file.

### Syntax

*Visual Basic:*
```
Public Sub Save()
```


---

## Author Property

*Quelle: `POLYFILELib~SummaryInfo~Author.html` · Polytec PolyFile Type Library · SummaryInfo Object : Author Property*

### Description

Specifies the author of the file.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Author As String
```


---

## Comments Property

*Quelle: `POLYFILELib~SummaryInfo~Comments.html` · Polytec PolyFile Type Library · SummaryInfo Object : Comments Property*

### Description

Specifies the comments of the file.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Comments As String
```


---

## Subject Property

*Quelle: `POLYFILELib~SummaryInfo~Subject.html` · Polytec PolyFile Type Library · SummaryInfo Object : Subject Property*

### Description

Specifies the subject of the file.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Subject As String
```

### Remarks

The subject is used by the MPV/PSV/VibSoft software to store warnings, errors and informational messages that occurred during data taking.


---

## Title Property

*Quelle: `POLYFILELib~SummaryInfo~Title.html` · Polytec PolyFile Type Library · SummaryInfo Object : Title Property*

### Description

Specifies the title of the file.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property Title As String
```
