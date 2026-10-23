# POLYPROPERTIESLib – IAcquisitionProperties

## IAcquisitionProperties Collection

*Quelle: `POLYPROPERTIESLib~IAcquisitionProperties.html` · Polytec PolyProperties Type Library*

### Description

Collection of objects of different types representing the respective acquisition properties.

### Remarks

It is recommended to cast to the AcquisitionPropertiesContainer object.


---

## IAcquisitionProperties Collection Members

*Quelle: `POLYPROPERTIESLib~IAcquisitionProperties_members.html` · Polytec PolyProperties Type Library*

### Public Properties

| Count | Returns the number of AcquisitionProperty objects in this collection. |
|---|---|
| Item | Returns a specific AcquisitionProperty object of this collection. |


---

## Count Property

*Quelle: `POLYPROPERTIESLib~IAcquisitionProperties~Count.html` · Polytec PolyProperties Type Library · IAcquisitionProperties Collection : Count Property*

### Description

Returns the number of AcquisitionProperty objects in this collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Count As Long
```


---

## Item Property

*Quelle: `POLYPROPERTIESLib~IAcquisitionProperties~Item.html` · Polytec PolyProperties Type Library · IAcquisitionProperties Collection : Item Property*

### Description

Returns a specific AcquisitionProperty object of this collection.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property Item( _
   ByVal PTCAcqPropertiesType As PTCAcqPropertiesType _
) As Object
```

### Parameters

PTCAcqPropertiesType

| Value | Description |
|---|---|
| ptcAcqPropertiesTypeAverage | Averaging properties |
| ptcAcqPropertiesTypeChannels | Channel properties |
| ptcAcqPropertiesTypeFastScans | FastScans properties |
| ptcAcqPropertiesTypeFft | FFT properties |
| ptcAcqPropertiesTypeFrontEnd | Front End properties |
| ptcAcqPropertiesTypeGeneral | General properties |
| ptcAcqPropertiesTypeGenerators | Generators properties |
| ptcAcqPropertiesTypeMultiFrame | MultiFrame properties |
| ptcAcqPropertiesTypeSignalEnhancement | Signal enhancement properties |
| ptcAcqPropertiesTypeTime | Time properties |
| ptcAcqPropertiesTypeTrigger | Trigger properties |
| ptcAcqPropertiesTypeVibrometers | Vibrometer properties |
| ptcAcqPropertiesTypeZoomFft | Zoom-FFT properties |
The type of the acquisition properties.

### Remarks

If the corresponding object is not present in the collection, Nothing is returned.
