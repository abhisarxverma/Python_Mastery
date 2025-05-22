# LAST CHANGES
***Things I worked on last time.***

- Removed the pay fine feature temporarily
- Made the fine system that everytime the data is imported, the member's fine will be calculated again by the loans 
- And that's why they have to pay fine while returning the book itself
- Completed the admin command line iterface
- Implemented the Logging system for the new loan and the loan return

## NEXT TASKS
***Need to do next***

- Neet to put the admin command line and the member command line into separate files
- And merge them in single cli file
- Make a new command line interface logic for the admin analysis things like to see the stats
- Need to implement that before loaning a book, we are checking that loan limit is not reached, but we also have to check that the member has any fine payment left
- In the admin analysis file, I have to implement one feature as of now that show the most borrowed 3 books
- Create a new data structure for the stats storage for every entity.