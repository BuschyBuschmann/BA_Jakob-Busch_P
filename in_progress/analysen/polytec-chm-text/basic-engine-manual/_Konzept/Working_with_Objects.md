# _Konzept – Working with Objects

## Working with Objects

*Quelle: `Working with Objects.html` · Basic Engine Manual · Introduction to Automation > Working with Objects*

Once you have referenced a particular object, you use properties and methods to control the characteristics and actions of the object.

#### Accessing Properties

To access a property, you refer to the object and the property name separated by the dot ( . ) operator.

The following code sample accesses the Caption property of a PSV/VibSoft Window object. The active document is referenced by the variable Doc.

*Accessing a Property:*
```
Dim strCap As String
Dim oDoc As VibDocument
Set oDoc = Application.ActiveDocument
Dim oWnd As Window
Set oWnd = oDoc.Windows(1)
strCap = oWnd.Caption
```

#### Invoking Methods

The methods of an object cause an action to occur. For example, a Document object has a Save method that saves it to disk.

To invoke a method, you reference the object, and then the method, separated by a dot ( . ) operator. The following line of sample code saves the active document.

*Save Active Document:*
```
Application.ActiveDocument.SaveAs(MyName.svd)
```

#### Using a Return Value

Some methods return an object. For example, the Add method of the Windows collection returns the Window object. When a method returns an object, you can use the Set statement to save the return value.

*Saving an Object Returned from a Method:*
```
Dim oWnd As Window
Set oWnd = Application.ActiveDocument.Windows.Add()
```

#### Performing a Series of Actions

When you access properties and invoke methods for objects, youll often write a number of code statements that act on the same object.

*Performing Series of Actions:*
```
Dim oSweep As New WaveformSweep
oSweep.StartFrequency = 100.0
oSweep.EndFrequency = 1000.0
oSweep.SweepTime = 1.0
```

To make code easier to read, you can use the With ... End With statement to break up code statements into blocks. This code sample performs the same actions as the previous code, but uses the With ... End With statement.

*Performing a Series of Actions using With ... End With:*
```
Dim oSweep As New WaveformSweep
With oSweep
    .StartFrequency = 100.0
    .EndFrequency = 1000.0
    .SweepTime = 1.0
End With
```

Using the With ... End With statement adds two lines of code, but PSV/VibSoft Basic executes the code in the With ... End With statement more quickly because it evaluates the object only once, rather than three times.

#### Events

Some of the objects defined in the PSV/VibSoft object model define events. These are routines that are called when certain conditions are met or a state changes. To define such a routine you have to declare a global variable of the type of the object decorated with the keyword WithEvents.

*Declaration WithEvents:*
```
Dim WithEvents oAcq As VibSoft.Acquisition
```

 Once in your program you have to initialize the global variable with a valid object, e.g. in Sub Main:

*Set the Object:*
```
Sub Main
    Set oAcq = Application.Acquisition
End Sub
```

 You can now implement the Event routines of this object:

*Event Handlers:*
```
Private Sub oAcq_AcqStateChanged(ByVal acqState As VibSoft.PTCAcqState)
    Debug.Print "AcqState: ";acqState
End Sub
Private Sub oAcq_ScanStateChanged(ByVal scanState As _
            VibSoft.PTCScanState, ByVal scanPoint As Long)
        Debug.Print "ScanState: ";scanState;" ScanPoint: ";scanPoint
End Sub
```

These routines will be called every time the scan state or the acquisition state changes while your macro is running. So you do not have to write a loop where you wait for a measurement stopping but you can use the event routines instead. This is more efficient.
