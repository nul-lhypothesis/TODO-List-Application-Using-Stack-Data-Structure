# 📝 TODO List Application

This project is a Python-based TODO List Application which helps users organize their daily tasks efficiently by using a stack-based structure - allowing them to add, view, complete, undo, delete, sort, and search tasks, all through a simple console interface.

---

## 💡 Introduction

The TODO List Application is designed to make everyday task management easier and more structured.  
It uses the stack data structure (LIFO) to handle adding and undoing tasks and stores all task information - such as title, category, priority, and completion status - in a JSON file for persistence.  
This project helped me understand how data structures and file handling can be applied together in a real-world scenario.

---

## ⚙️ Features

- Add new tasks with details like title, description, priority, category, and due date  
- View all tasks in a neatly formatted list  
- Mark tasks as completed or undo the most recent completion (LIFO behavior)  
- Delete specific tasks by ID with automatic reindexing  
- Sort tasks by priority, due date, category, or creation date using Bubble Sort  
- Search for tasks by keyword using Linear Search
- View tasks grouped by category  
- See task statistics like total, completed, and pending counts  

---

## 🧠 Concepts Used

- **Stack Data Structure** – Used for managing and undoing task operations  
- **File Handling & JSON** – To save and reload tasks each time the program runs  
- **Sorting (Bubble Sort)** – For arranging tasks by various criteria  
- **Searching (Linear Search)** – For quick keyword-based lookup  
- **Object-Oriented Programming (OOP)** – Encapsulated in a single class structure  
- **Lists & Dictionaries** – For efficient data storage and modification  
- **Error Handling** – To prevent crashes and guide the user properly  

---

## 🔄 How It Works

1. When the program starts, it checks if the data file (`todo_data.json`) exists and loads previous tasks if found.  
2. The main menu appears with options from **1 to 10**, covering all operations.  
3. Based on user input, it performs actions like adding, viewing, sorting, or undoing tasks.  
4. Every change is automatically saved back to the JSON file.  
5. On exiting, it displays “Saving and exiting. Goodbye!” and safely stores all updates.

---

## 🖥️ Output Overview

- The main menu displays all available operations clearly.  
- Tasks are shown in a tabular format with columns for ID, priority, category, status, and title.  
- Completion status updates to “Done” once a task is finished.  
- Sorting and searching provide filtered and organized results.  
- Statistics summarize task progress and priorities.  
- The `todo_data.json` file is automatically updated after every change.

---

## 🙏 Acknowledgement

This project was created as part of my internship to apply Python concepts in a real use case. It helped me understand how stack operations, file handling, and object-oriented logic work together in a functional program. The process involved gradual testing and debugging to make it consistent and error-free.

---

## 🧾 References

- [Python Official Documentation](https://docs.python.org/3/)  
- [W3Schools Python Tutorials](https://www.w3schools.com/python/)  
- [GeeksforGeeks – Python Programming Language](https://www.geeksforgeeks.org/python-programming-language/)    
- College Notes and internship resources 

---

## 👩‍💻 Submitted By

**Meenakshi T.S**  
B.Tech Computer Engineering, GCET  
Developed during MyJobGrow Internship  

---

View Project Repository: (https://github.com/nul-lhypothesis/TODO-List-Application-Using-Stack-Data-Structure)

---
