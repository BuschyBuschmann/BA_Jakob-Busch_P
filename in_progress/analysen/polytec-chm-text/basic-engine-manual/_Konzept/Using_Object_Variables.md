# _Konzept – Using Object Variables

## Using Object Variables

*Quelle: `Using Object Variables.html` · Basic Engine Manual · Introduction to Automation > Using Object Variables*

You can use object variables to reference an object anywhere in the hierarchy of an object model. If you want to reference the same object in more than one place in your code, you can set an object variable, and then use the variable repeatedly. This approach is more efficient than referencing the entire hierarchy each time you want to refer to the object.

To use an object variable, you first declare the variable, and then use the Set statement to assign the variable to a specific object. The following code sample declares an object variable, and then sets the variable to a document.

*Printing the Name of a Document:*
```
Dim oDoc As VibDocument
Set oDoc = Application.ActiveDocument
Debug.Print oDoc.Name
```

#### Declaring an Object Variable

You can declare a variable with a specific object type (the object class). This is referred to as early binding. Or, you can use the generic Object data type to declare a variable, which is referred to as late binding.

#### Setting an Object Variable

After you declare an object variable, you use the Set statement to assign the variable to a specific object.

*Setting an Object Variable:*
```
Dim oDoc As VibDocument
Set oDoc = Application.ActiveDocument
```

#### Determining Whether an Object Variable Is Set

You can use the Nothing keyword to determine whether an object variable has been set to an object.

*Determining Whether an Object Variable is Set:*
```
 Dim oDoc As VibDocument
 Set oDoc = Application.ActiveDocument
 Dim oProps As Object
 Set oProps = oDoc.AcquisitionProperties(ptcAcqPropertiesTypeMultiFrame)
 If oProps Is Nothing Then
      MsgBox "No MultiFrame Properties", vbOkOnly
 End If
```

You can set an object variable to Nothing to clear the reference. When object variables that refer to the object are set to Nothing, the associated memory and system resources will be released.

This line of sample code sets the object variable oProps to Nothing.

*Set Object Variable to Nothing:*
```
Set oProps = Nothing
```
