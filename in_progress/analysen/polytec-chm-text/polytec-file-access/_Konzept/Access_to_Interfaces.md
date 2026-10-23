# _Konzept – Access to Interfaces

## Access to Interfaces

*Quelle: `Access to Interfaces.html` · Object Model Reference*

Every object consists of one or more interfaces. Properties and methods in an object are defined in interfaces. By convention the names of interfaces start with the uppercase letter I. By default the object returns one interface, almost always the most important and the newest one. In some programming languages like Visual Basic and C# this default interface has the same name as the object without the leading I. Most often you work with the default interface and need not to know about the other interfaces an object might offer. Nevertheless, there are situations where you have to know about and work with interfaces:

#### Versioning

The MPV/PSV/VibSoft and Polytec File Access object model evolves over time. New objects are added and existing objects are enhanced by new functionality, i.e. by additional properties and methods. To keep backward compatibility with existing applications, we do not change existing interfaces but create new versions of interfaces. These new interface versions become the new default interfaces of the respective objects. If you work with default interfaces in your source code (which is recommended) you will automatically gain access to the new properties and methods.

*Working with Default Interfaces (VB):*
```

' working with an explicit version of PolyFile
' this interface will not change over time
Dim oPolyFile8 As IPolyFile8
Set oPolyFile8 = New PolyFile
' the Create method is not available in this interface
' working with the default interface of PolyFile
' this interface will be extended and changed over time
Dim oPolyFile As PolyFile
Set oPolyFile = New PolyFile
oPolyFile.ReadOnly = False
' the Create method is available in the current version of PolyFile
oPolyFile.Create("D:\Temp\File.svd", ptcCreateAlways)
```

*Working with Default Interfaces (C#):*
```

// working with an explicit version of PolyFile
// this interface will not change over time
IPolyFile8 polyFile8;
polyFile8 = new PolyFileClass();
// the Create method is not available in this interface
// working with the default interface of PolyFile
// this interface will be extended and changed over time
PolyFile polyFile;
polyFile = new PolyFileClass();
polyFile.ReadOnly = false;
// the Create method is available in the current version of PolyFile
polyFile.Create(@"D:\Temp\File.svd", PTCCreateFlags.ptcCreateAlways);
```

In an object model as large as that of MPV/PSV/VibSoft and Polytec File Access it is not always possible to keep all references to interfaces up to date. Therefore, methods and properties might return an earlier version of an interface than the version of the default interface. In this case the interface listed in the documentation has the leading uppercase letter I, otherwise the name of the default interface (i.e. the object name without the leading I) is listed. We recommend to cast to and work with the default interface in these cases. How to cast depends on the programming language. In Visual Basic you simply declare a variable with the type of the default interface and assign the older interface with the Set command.

*Cast to the Default Interface (VB):*
```

Dim oPolyFile As PolyFile
Set oPolyFile = New PolyFile
' open a combined file
oPolyFile.Open("D:\Temp\fussball_b.svd")
' the following is not possible, because the File property returns an IPolyFile8 interface
' IPolyFile8 has no CurrentFileVersionNumber property
Debug.Print Hex$(oPolyFile.ContainedFiles(1).File.CurrentFileVersionNumber) ' will not run
' therefore implicitly cast to the default interface first
Dim oContainedFile As PolyFile
Set oContainedFile = oPolyFile.ContainedFiles(1).File
Debug.Print Hex$(oContainedFile.CurrentFileVersionNumber)
oPolyFile.Close()
```

 In C# you have to cast explicitly using the cast operator with the name of the default interface.

*Cast to the Default Interface (C#):*
```

PolyFile polyFile = new PolyFileClass();
// open a combined file
polyFile.Open(@"D:\Temp\fussball_b.svd");
// the following is not possible, because the File property returns an IPolyFile8 interface
// IPolyFile8 has no CurrentFileVersionNumber property
// the following line will not compile
Console.WriteLine("{0:X}", polyFile.ContainedFiles[1].File.CurrentFileVersionNumber);
// therefore explicitly cast to the default interface first
PolyFile combinedFile = (PolyFile)polyFile.ContainedFiles[1].File;
Console.WriteLine("{0:X}", combinedFile.CurrentFileVersionNumber);
polyFile.Close();
```

#### Common Interfaces for Different Objects

Another application of interfaces is the use of a common interface that is implemented by a number of different objects. One example of this technique is the IWaveform interface. This interface is the type that is returned and accepted by the Waveform propertyof the generator acquisition properties. The interface is implemented by all waveforms that are supported by the generators of a MPV, PSV, or VibSoft system. Therefore you can create any of the waveform objects listed in the documentation of the IWaveform interface and pass this object to the waveform property. The default interface of the waveform object is implicitly casted to IWaveform. To retrieve the full information about the waveform that is returned by the waveform property you have to cast to the default interface of the corresponding waveform object. See the example given in the documentation of the Waveform property on how to do this.

#### Early Binding and Late Binding

The examples given in this section use early binding to access the properties and methods of an object. In this case variables are evaluated during compile time, and you will get a compile error if you want to access a property or method not exposed by the default interface. In late binding, where a variable is declared as an object or a variant (typeless), an interface retrieval is not necessary. Its done internally by the scripting runtime. Nevertheless, we recommend to use early binding in all cases.
