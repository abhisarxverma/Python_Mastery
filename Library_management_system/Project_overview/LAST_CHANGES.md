# LAST CHANGES
***Things I worked on last time.***

- Implemented the absolute import system in all python files
- Made the Library_management_system directory a package using the __init__.py
- Made the Commandline and the models also a package to be imported and used anywhere in system
- Separated the admin commandline and the member commandline and merged them in the cli.py
- Separated all the models in separate files
- put the log file in the Log folder
- When i made the directory the packages, the paths of the jsons stopped working, I fixed that
- Putting the book and the author object in different files is causing the circular import cause both need other for initialization, that's why i put them in single book file, cause they will often be used together.

**THANK TO PROGRAMMING, THAT CLI IS WORKING (I am Atheist and I believe that programming is only god)**

## NEXT TASKS
***Need to do next***

- Make a new command line interface logic for the admin analysis things like to see the stats
- Need to implement that before loaning a book, we are checking that loan limit is not reached, but we also have to check that the member has any fine payment left
- In the admin analysis file, I have to implement one feature as of now that show the most borrowed 3 books
- Create a new data structure for the stats storage for every entity.
- Need to replace at every place where I am raising a exception for the checking, to the logging for the better debugging and also to include in that the file name and the function name