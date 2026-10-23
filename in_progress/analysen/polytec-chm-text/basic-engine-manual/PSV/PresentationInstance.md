# PSV – PresentationInstance

## PresentationInstance Object

*Quelle: `PSV~PresentationInstance.html` · Polytec PSV Type Library*

### Description

The PresentationInstance object represents the instance of the PSV application that runs in presentation mode.

### Object Model

### Remarks

This class can be instantiated using the string "PSV.PresentationInstance".

### Example

Regardlesss whether this macro runs in the presentation instance, acquisition instance or in an external automation client, the PSV presentation instance is used to open the specified file.

- Presentation Instance (Visual Basic)

```
Option Explicit

Sub Main
    Dim oPresInstance As New PresentationInstance
    Dim oApp As Application
    Set oApp = oPresInstance.GetApplication(True)
    oApp.Documents.Open("D:\Temp\Scan.svd")
End Sub
```


---

## PresentationInstance Object Members

*Quelle: `PSV~PresentationInstance_members.html` · Polytec PSV Type Library*

### Public Methods

| GetApplication | Gets the application object of the presentation instance. |
|---|---|

### Public Properties

| IsRunning | Returns whether the presentation instance is running. |
|---|---|


---

## GetApplication Method

*Quelle: `PSV~PresentationInstance~GetApplication.html` · Polytec PSV Type Library · PresentationInstance Object : GetApplication Method*

### Description

Gets the application object of the presentation instance.

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

If True, the presentation instance is started, when it is not running already. This can take some time.

lTimeOut

The timeout in ms before the method returns with an error, when the acquisition instance could not be started. When vbCreate is False this parameter has no effect.

### Return Type

The application object of the presentation instance.

### Remarks

When called from the acquisition instance or from an external automation client, the returned application object uses inter-process communication (DCOM) to communicate with the acquisition instance. You can access all methods, properties and sub-objects of the acquisition instance via the returned application object.


---

## IsRunning Property

*Quelle: `PSV~PresentationInstance~IsRunning.html` · Polytec PSV Type Library · PresentationInstance Object : IsRunning Property*

### Description

Returns whether the presentation instance is running.

### Property type

Read-only property

### Syntax

*Visual Basic:*
```
Public Property IsRunning As Boolean
```

### Remarks

If the presentation instance is not running, you can start it by passing True to the vbCreate parameter of the GetApplication Method.
