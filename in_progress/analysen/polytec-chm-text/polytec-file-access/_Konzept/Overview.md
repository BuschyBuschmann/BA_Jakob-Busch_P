# _Konzept – Overview

## Overview

*Quelle: `Overview.html` · Object Model Reference*

#### What is Polytec File Access?

Polytec File Access is a collection of Objects written according to the standard Component Object Model (COM) of Microsoft®. Polytec File Access exposes its functionality by a hierarchy of classes with methods and properties. These methods and properties allow access to most of the information that is stored in -

- PSV measurement files (single point and scan data)

- MPV measurement files (multipoint data and raw data)

- VibSoft measurement files

- PSV settings files

- MPV settings files

- VibSoft settings files

As COM is a binary standard you can use any programming language that allows access to COM objects with Polytec File Access, e.g. Visual Basic® Scripting edition, Visual Basic® for Applications, Delphi, Visual C++® etc. You can also use the built in Basic Engine of PSV and VibSoft. To demonstrate the use of Polytec File Access we provide examples written in Visual Basic® for Applications (Microsoft® Excel and PSV/VibSoft) and Visual C++®, see section Examples.

#### Intended Audience

This manual and Polytec File Access are intended for programmers who have experience in any of the above-mentioned languages and the access to COM objects. For those developers Polytec File Access provides an easy and efficient way to access the data stored in Polytecs proprietary file formats used by MPV, PSV, and VibSoft. Programmers not familiar with COM might want to read the section Introduction to Automation in the Basic Engine Manual help file provided with MPV, PSV, and VibSoft.

#### Quick Start

To install the software proceed as follows:

- Switch on your workstation and log on with administrator rights. See your operating system manual how to do this.

- Install Polytec File Access as described in the File File Access\Release Notes.doc on your Polytec File Access CD.

In your installation directory (the default path is C:\Program Files\Polytec\File Access) you will find a directory Examples. Those examples are described in section Examples. Choose one and run it (see section Examples how to do this).

Select a MPV, PSV, or VibSoft data file and see how the example accesses the data and the information stored in the file.
