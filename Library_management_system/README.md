# 📚 Library Management System

## You can refer to the [Last changes file](LAST_CHANGES.md) to get to do next tasks.

## **Module Overview**
A structured implementation of a Library Management System, categorized into key modules.

### **Modules**
#### 1️⃣ **Models.py**
Defines the primary objects used in the library system:
- **Book** 📖
- **Author** ✍️
- **Member** 🧑‍🎓
- **Loan** 🔄

#### 2️⃣ **Services.py**
Contains the **LoanService** class responsible for:
- Creating new loan requests
- Managing book returns

#### 3️⃣ **Catalog.py**
Implements the **LibraryCatalog** for catalog management:
- Adding books & authors
- Searching and filtering catalog entries

#### 4️⃣ **Library.py**
Top-level library operations handled by **Library** class:
- Registering new books
- Processing book loans
- User interaction handling

---