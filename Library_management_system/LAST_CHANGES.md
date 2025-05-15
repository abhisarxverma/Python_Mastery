# LAST CHANGES
Things I worked on last time.

- Separated the import and the export and the make objects helper functions in the separate files
- Moved the make object functions to the object class method.
- Fixed the Circular import Error i got which happens when we try to import a file which itself have the import statement for the file in which we are importing in first place.

## NEXT TASKS
Need to do next

- Current scenario of the system is bad, the command line is not working, fully somethings are working, but not everything, need to write tests also to test everything.
- To make the objects, I need to have access to the library's data like authors and books and members, but doing that is causing the Circular Import, need to fix this.
- I Have to make a clean diagram of the current scenario of the system modules to fix the circula import and make the system more clear
- Need to make the methods and functions to save the books written by corresponding author, which I don't have now.
- Code some more functions to make the system up and running.