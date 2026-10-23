# POLYFILELib – LensCalibrations

## LensCalibrations Collection

*Quelle: `POLYFILELib~LensCalibrations.html` · Polytec PolyFile Type Library*

### Description

Collection of LensCalibration objects.

### Object Model

### Remarks

This class can be instantiated using the string "PolyFile.LensCalibrations".

Beginning with the software releases in July 2018, a "lens" is called "objective" in the GUI of the applications.


---

## LensCalibrations Collection Members

*Quelle: `POLYFILELib~LensCalibrations_members.html` · Polytec PolyFile Type Library*

### Public Methods

| Add | Adds a new objective calibration with the given name to the collection and returns the new object. |
|---|---|
| Clear | Clears the collection by removing all objective calibration objects. |
| NameToIndex | Returns the numerical index of the objective calibration with the given name. |
| Remove | Removes an item with the given index or name from the collection. |
| Rename | Renames the objective calibration with the given name to the new name. |

### Public Properties

| Count | Retrieves the number of items in this collection. |
|---|---|
| Exists | Returns true if an item with the given index exists in the collection. |
| Item | Returns an item of the collection. |


---

## Add Method

*Quelle: `POLYFILELib~LensCalibrations~Add.html` · Polytec PolyFile Type Library · LensCalibrations Collection : Add Method*

### Description

Adds a new objective calibration with the given name to the collection and returns the new object.

### Syntax

*Visual Basic:*
```
Public Function Add( _
   ByVal bstrName As String _
) As LensCalibration
```

### Parameters

bstrName

Name of the new objective calibration.

### Return Type

The new objective calibration object.


---

## Clear Method

*Quelle: `POLYFILELib~LensCalibrations~Clear.html` · Polytec PolyFile Type Library · LensCalibrations Collection : Clear Method*

### Description

Clears the collection by removing all objective calibration objects.

### Syntax

*Visual Basic:*
```
Public Sub Clear()
```


---

## NameToIndex Method

*Quelle: `POLYFILELib~LensCalibrations~NameToIndex.html` · Polytec PolyFile Type Library · LensCalibrations Collection : NameToIndex Method*

### Description

Returns the numerical index of the objective calibration with the given name.

### Syntax

*Visual Basic:*
```
Public Function NameToIndex( _
   ByVal bstrName As String _
) As Long
```

### Parameters

bstrName

Name of the item.

### Return Type

The index of the item in the collection.


---

## Remove Method

*Quelle: `POLYFILELib~LensCalibrations~Remove.html` · Polytec PolyFile Type Library · LensCalibrations Collection : Remove Method*

### Description

Removes an item with the given index or name from the collection.

### Syntax

*Visual Basic:*
```
Public Sub Remove( _
   ByVal IndexOrName As Variant _
)
```

### Parameters

IndexOrName

Index (integer) or name (string) of the item.


---

## Rename Method

*Quelle: `POLYFILELib~LensCalibrations~Rename.html` · Polytec PolyFile Type Library · LensCalibrations Collection : Rename Method*

### Description

Renames the objective calibration with the given name to the new name.

### Syntax

*Visual Basic:*
```
Public Sub Rename( _
   ByVal IndexOrName As Variant, _
   ByVal bstrNewName As String _
)
```

### Parameters

IndexOrName

Index (integer) or name (string) of the item.

bstrNewName

The new name of the item.


---

## Count Property

*Quelle: `POLYFILELib~LensCalibrations~Count.html` · Polytec PolyFile Type Library · LensCalibrations Collection : Count Property*

### Description

Retrieves the number of items in this collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Count As Long
```


---

## Exists Property

*Quelle: `POLYFILELib~LensCalibrations~Exists.html` · Polytec PolyFile Type Library · LensCalibrations Collection : Exists Property*

### Description

Returns true if an item with the given index exists in the collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Exists( _
   ByVal IndexOrName As Variant _
) As Boolean
```

### Parameters

IndexOrName

Index (integer) or name (string) of the item.


---

## Item Property

*Quelle: `POLYFILELib~LensCalibrations~Item.html` · Polytec PolyFile Type Library · LensCalibrations Collection : Item Property*

### Description

Returns an item of the collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Item( _
   ByVal IndexOrName As Variant _
) As LensCalibration
```

### Parameters

IndexOrName

Index (integer) or name (string) of the item.

### Return Type

The LensCalibration object.
