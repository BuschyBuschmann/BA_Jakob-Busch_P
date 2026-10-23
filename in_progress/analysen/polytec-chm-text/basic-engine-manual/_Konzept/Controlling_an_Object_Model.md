# _Konzept – Controlling an Object Model

## Controlling an Object Model

*Quelle: `Controlling an Object Model.html` · Basic Engine Manual · Introduction to Automation > Controlling an Object Model*

You can use Automation to control the functionality of the objects provided by an application. Automation is an ActiveX service that enables you to integrate applications.

The two key elements in Automation are Automation servers and Automation controllers. An application can serve as an Automation server, an Automation controller, or both.

#### Automation Servers

Automation servers include applications or software components that can be controlled by other applications. The functionality of these components are made accessible as object models to other applications.

Automation servers include PSV, VibSoft, and all of the Microsoft® Office applications.

#### Automation Controllers

Automation controllers include applications or development tools that can control Automation servers with code. Automation controllers access the functionality exposed by Automation servers.

In addition to acting as an Automation server both PSV and VibSoft can also act as Automation controllers. You can use PSV/VibSoft Basic to access the functionality provided by any Automation server. Microsoft® Visual Basic® and some Microsoft® Office applications are also Automation controllers.

#### Navigating an Object Model

To work with a specific object, you must first write code to navigate the object hierarchy. To find and work with a specific object, you write code that navigates the hierarchy by using the dot ( . ) operator. You can refer to an object explicitly by specifying the name of the object you want, or you can refer to an object implicitly by omitting some references and assuming the currently active object.

Sometimes you must reference all objects in a hierarchical path to get to a specific object.
This code sample activates of the first window of the first document and brings it to the front.

*Activating a Windows:*
```
Application.Documents(1).Windows(1).Activate()
```

Sometimes, you don't have to reference the entire object model path to get to a particular object. Depending on which object will be active when the user runs the code, you can omit some object references.

Application has a property that returns the active document or window. For example, the following line of code references the active document:

*Accessing the Active Document:*
```
Application.ActiveDocument
```

To refer to the active window, Application provides the ActiveWindow property.

*Accessing the Active Window:*
```
Application.ActiveWindow
```

A common error when writing Automation code is to assume that the active document is the document you want to reference. If the user changes the active document, and then runs your code, the code may fail or operate incorrectly. If you want to make sure that your code always references a specific document, you should refer to the document explicitly. This ensures that the code will run correctly even if the user changes the active document.
