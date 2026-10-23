# POLYFILELib – Version

## Version Object

*Quelle: `POLYFILELib~Version.html` · Polytec PolyFile Type Library*

### Description

The version object contains properties for general version information of the file.


---

## Version Object Members

*Quelle: `POLYFILELib~Version_members.html` · Polytec PolyFile Type Library*

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
| ProgramVersionBuild | Specifies the build number part of the program version. |
| ProgramVersionMajor | Specifies the major version number part of the program version. |
| ProgramVersionMinor | Specifies the minor version number part of the program version. |
| ProgramVersionRevision | Specifies the revision number part of the program version. |
| ProgramVersionString | Specifies the program version as string. |


---

## Save Method

*Quelle: `POLYFILELib~Version~Save.html` · Polytec PolyFile Type Library · Version Object : Save Method*

### Description

Commits the changes to the Version object to the file.

### Syntax

*Visual Basic:*
```
Public Sub Save()
```


---

## FileID Property

*Quelle: `POLYFILELib~Version~FileID.html` · Polytec PolyFile Type Library · Version Object : FileID Property*

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

*Quelle: `POLYFILELib~Version~FileTime.html` · Polytec PolyFile Type Library · Version Object : FileTime Property*

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

*Quelle: `POLYFILELib~Version~FileVersion.html` · Polytec PolyFile Type Library · Version Object : FileVersion Property*

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

*Quelle: `POLYFILELib~Version~ProgramID.html` · Polytec PolyFile Type Library · Version Object : ProgramID Property*

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

*Quelle: `POLYFILELib~Version~ProgramVersion.html` · Polytec PolyFile Type Library · Version Object : ProgramVersion Property*

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


---

## ProgramVersionBuild Property

*Quelle: `POLYFILELib~Version~ProgramVersionBuild.html` · Polytec PolyFile Type Library · Version Object : ProgramVersionBuild Property*

### Description

Specifies the build number part of the program version.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property ProgramVersionBuild As Long
```


---

## ProgramVersionMajor Property

*Quelle: `POLYFILELib~Version~ProgramVersionMajor.html` · Polytec PolyFile Type Library · Version Object : ProgramVersionMajor Property*

### Description

Specifies the major version number part of the program version.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property ProgramVersionMajor As Long
```


---

## ProgramVersionMinor Property

*Quelle: `POLYFILELib~Version~ProgramVersionMinor.html` · Polytec PolyFile Type Library · Version Object : ProgramVersionMinor Property*

### Description

Specifies the minor version number part of the program version.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property ProgramVersionMinor As Long
```


---

## ProgramVersionRevision Property

*Quelle: `POLYFILELib~Version~ProgramVersionRevision.html` · Polytec PolyFile Type Library · Version Object : ProgramVersionRevision Property*

### Description

Specifies the revision number part of the program version.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property ProgramVersionRevision As Long
```


---

## ProgramVersionString Property

*Quelle: `POLYFILELib~Version~ProgramVersionString.html` · Polytec PolyFile Type Library · Version Object : ProgramVersionString Property*

### Description

Specifies the program version as string.

### Property type

Read-write property

### Syntax

*Visual Basic:*
```
Public Property ProgramVersionString As String
```
