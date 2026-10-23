# _Konzept – Operating on Combined Files

## Operating on Combined Files

*Quelle: `Operating on Combined Files.html` · Basic Engine Manual · The PSV/VibSoft Object Model > Operating on Combined Files*

A combined file is the combination of a series of 3D measurements each saved as an individual PSV scanning file (.svd). Individual files can be either copied to the main combined file storage or linked to it. Files of this type have also the .svd extension. It can also contain another combined file as a contained file. It uses Infos from the active file, which is the first contained file for the current implementation.

The following code creates a new combined file with three single .svd files. The first single file is added as a copy and the other two as links. If a file is linked to a combined file with a relative path (i.e. .\, ..\ etc.), then it has also to be copied if the combined file is copied to another location.

*Creating a combined file:*
```
Dim oPolyFile As New PolyFile
oPolyFile.ReadOnly = False
oPolyFile.FileName = "D:\Examples\CombinedFile.svd"
Dim oContainedFiles As ContainedFiles
Set oContainedFiles = oPolyFile.ContainedFiles
oContainedFiles.Add("D:\Examples\X.svd", ptcContainedCopy)
oContainedFiles.Add("D:\Examples\Y.svd", ptcContainedLink)
oContainedFiles.Add("..\Z.svd", ptcContainedLink) ' relative path
oPolyFile.Save()
oPolyFile.Close()
```

The single measurement files can be accessed through the ContainedFiles collection of the PolyFile. Its a collection of all the individual files as ContainedFile objects. ContainedFile has a File property which returns the underlying PolyFile object for the single file.

*Opening a combined file and accessing the individual contained files:*
```
Dim oPolyFile As New PolyFile
oPolyFile.Open("D:\Examples\CombinedFile.svd")
Dim oContainedFile As ContainedFile
For Each oContainedFile In oPolyFile.ContainedFiles
 Debug.Print oContainedFile.Name ' Name used to include it
 Debug.Print oContainedFile.File.FileName ' absolute path
Next
```
