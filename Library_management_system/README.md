# 📚 Library Management System

## You can refer to the [Last changes file](LAST_CHANGES.md) to get current scenario of the system.

## **Module Overview**
A structured implementation of a Library Management System, categorized into key modules.

### **Models**
#### 1️⃣ **Models.py**
Defines the primary objects used in the library system:
- **Book** 📖
- **Author** ✍️
- **Member** 🧑‍🎓
- **Loan** 🔄

#### 2️⃣ **LoanService.py**
Contains the **LoanService** class responsible for:
- Creating new loan requests
- Managing book returns

#### 3️⃣ **CatalogService.py**
Implements the **CatalogService** for catalog management:
- Adding books & authors
- Searching and filtering catalog entries

#### 4️⃣ **MemberService.py**
Deals with all the functions and methods that relate to members in the library:
- Register new member
- Find member

#### 5️⃣ **DataService.py**
Deals with Saving and Importing the data from the data files:
- Import Members
- Import Loans
- Export Books
- Export Members

#### 4️⃣ **Library.py**
Top-level library operations handled by **Library** class:
Integrates all the service classes and then do the library operations from top level:
- Cataloging new book
- Registering new member
- Loan book
---