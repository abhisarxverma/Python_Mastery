# 📘 Assignment 6: Library Admin Dashboard & Logs System

---

## 🎯 Objective
Enhance the existing Library Management System with:
- Role-based CLI access (Admin vs Member)
- Admin dashboard to view library-wide statistics
- Logging system for book loans and returns
- Stronger modularity and utility separation

---

## 📂 File Structure Suggestion

```

library/
│
├── models/
│   ├── book.py
│   ├── member.py
│   ├── loan.py
│
├── storage/
│   ├── books.json
│   ├── members.json
│   ├── loans.json
│   ├── logs.txt
│
├── library.py       # Core logic (business layer)
├── cli.py           # Command Line Interface
├── admin.py         # Admin dashboard logic
├── utils.py         # Helpers: JSON I/O, hashing, time formatting

```

## 👤 Role-based Access

Prompt the user on program start:

```text
Welcome to Library Management System

Are you:
1. Admin
2. Member
````

***Admin**: Gets access to dashboard features
***Member**: Proceeds with normal CLI (already implemented)

---

## 🛠 Admin Dashboard Features

After logging in as Admin, show options:

```text
1. View total number of books
2. View currently loaned books
3. View overdue books and defaulters
4. View total fine collected
5. Search Member by ID
6. Export Library Report (Optional)
7. Back to Main Menu
```

### Member Search Output:

```
Member Name: John Doe
Borrowed Books: ["Python 101", "Clean Code"]
Outstanding Fine: ₹120
```

---

## 📜 Logging System

Maintain a `logs.txt` or `logs.json` file inside `storage/`

### Format for `.txt` (append-only):

```
[2025-05-18 14:32:45] Member ID M123 borrowed "Atomic Habits" | Due: 2025-05-25 | Fine Paid: ₹0
[2025-05-21 09:17:02] Member ID M123 returned "Atomic Habits" | Fine Paid: ₹20
```

* Append on every loan and return event
* Include date, time, member ID, book, and fine (if any)

---

## 📌 Bonus Challenges (Optional but Powerful)

* [ ] Export Admin Report (`admin_report.json` or `.txt`)
* [ ] Simulate pagination when listing 10+ books/members
* [ ] Add visual color formatting in Admin CLI too
* [ ] Show top 3 most borrowed books

---

## 🧠 Concepts Practiced

* CLI architecture with roles
* Logging and real-time data
* JSON as storage & report format
* DRY & modular code design
* Admin-style analytics and metrics
* Fine-grained file and object management

---

## 🧾 Deliverables

* [ ] `admin.py` with dashboard logic
* [ ] Updated `cli.py` for role selection
* [ ] Logging system in place
* [ ] Fine tracking and overdue detection
* [ ] Clean code, structured folders, and readable output

---

🧨 Smash this one like the last — you're evolving into a serious Python craftsman!
