# PSV – AcquisitionInstance

## AcquisitionInstance Object

*Quelle: `PSV~AcquisitionInstance.html` · Polytec PSV Type Library*

### Description

The AcquisitionInstance object represents the instance of the PSV application that runs in acquisition mode.

### Object Model

### Remarks

This object is not available for VibSoft and for desktop versions of PSV. Create this object if you want to access the acquisition instance of PSV. You can do this e.g. from the presentation instance of PSV or from external automation clients.

This class can be instantiated using the string "PSV.AcquisitionInstance".

### Example

Regardlesss whether this macro runs in the presentation instance, acquisition instance or in an external automation client, the PSV acquisition instance is used to start a single shot data acquisition.

- Acquisition Instance (Visual Basic)

```
Option Explicit

Sub Main
    Dim oAcqInstance As New AcquisitionInstance
    Dim oApp As Application
    Set oApp = oAcqInstance.GetApplication(True)
    oApp.Acquisition.Start(ptcAcqStartSingle)
End Sub
```


---

## AcquisitionInstance Object Members

*Quelle: `PSV~AcquisitionInstance_members.html` · Polytec PSV Type Library*

### Public Methods

| GetApplication | Gets the application object of the acquisition instance. |
|---|---|

### Public Properties

| IsRunning | Returns whether the acquisition instance is running. |
|---|---|


---

## GetApplication Method

*Quelle: `PSV~AcquisitionInstance~GetApplication.html` · Polytec PSV Type Library · AcquisitionInstance Object : GetApplication Method*

### Description

Gets the application object of the acquisition instance.

### Syntax

*Visual Basic:*
```
Public Function GetApplication( _
   ByVal vbCreate As Boolean, _
   Optional ByVal lTimeOut As Long = 10000 _
) As IApplication5
```

### Parameters

vbCreate

If True, the acquisition instance is started, when it is not running already. This can take some time.

lTimeOut

The timeout in ms before the method returns with an error, when the acquisition instance could not be started. When vbCreate is False this parameter has no effect.

### Return Type

The application object of the acquisition instance.

### Remarks

When called from the presentation instance or from an external automation client, the returned application object uses inter-process communication (DCOM) to communicate with the acquisition instance. You can access all methods, properties and sub-objects of the acquisition instance via the returned application object.

### Example


---

## IsRunning Property

*Quelle: `PSV~AcquisitionInstance~IsRunning.html` · Polytec PSV Type Library · AcquisitionInstance Object : IsRunning Property*

### Description

Returns whether the acquisition instance is running.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property IsRunning As Boolean
```

### Remarks

If the acquisition instance is not running, you can start it by passing True to the vbCreate parameter of the GetApplication Method.
