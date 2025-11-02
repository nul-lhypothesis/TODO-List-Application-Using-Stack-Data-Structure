import datetime
import json
import os

DATA_FILE = "todo_data.json"

class TODOList:
    """
    Simple TODO List Application using Stack (student-coded).
    Main stacks:
      - self.tasks: list of task dicts (acts as main stack)
      - self.completed_stack: list of completed tasks (for undo)
    """

    def __init__(self, filename=DATA_FILE):
        self.filename = filename
        self.tasks = []
        self.completed_stack = []
        self.next_id = 1
        self.load_tasks()

    def load_tasks(self):
        try:
            if os.path.exists(self.filename):
                with open(self.filename, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.tasks = data.get("tasks", [])
                    self.completed_stack = data.get("completed", [])
                    if self.tasks:
                        self.next_id = max(t["id"] for t in self.tasks) + 1
                print("Loaded existing tasks.")
            else:
                print("No existing tasks found. Starting fresh.")
        except Exception as e:
            print(f"Error loading tasks (file may be corrupted): {e}")
            self.tasks = []
            self.completed_stack = []
            self.next_id = 1

    def save_tasks(self):
        try:
            with open(self.filename, "w", encoding="utf-8") as f:
                json.dump({"tasks": self.tasks, "completed": self.completed_stack}, f, indent=2)
        except Exception as e:
            print(f"Error saving tasks: {e}")

    def reindex_ids(self):
        """Reassign task IDs after deletion"""
        for i, task in enumerate(self.tasks, start=1):
            task["id"] = i
        self.next_id = len(self.tasks) + 1

    @staticmethod
    def now_str():
        return datetime.datetime.now().strftime("%d-%m-%Y %H:%M")

    @staticmethod
    def parse_date_str(date_str):
        try:
            return datetime.datetime.strptime(date_str, "%d-%m-%Y")
        except Exception:
            return datetime.datetime.max

    @staticmethod
    def truncate(text, n=40):
        return text if len(text) <= n else text[:n-3] + "..."

    def display_menu(self):
        print("\n" + "="*50)
        print("          TODO LIST APPLICATION ")
        print("="*50)
        print("1. Add New Task")
        print("2. View All Tasks")
        print("3. Mark Task as Completed")
        print("4. Undo Last Completion")
        print("5. Delete Task")
        print("6. Sort Tasks")
        print("7. Search Tasks")
        print("8. View by Category")
        print("9. View Statistics")
        print("10. Exit")
        print("-"*50)

    def add_task(self):
        print("\n--- Add New Task ---")
        title = input("Enter task title: ").strip()
        if not title:
            print("Task title cannot be empty. Try again.")
            return

        description = input("Enter description (optional): ").strip()

        print("\nPriority (1-High, 2-Medium, 3-Low) [default 2]: ", end="")
        pr = input().strip()
        priority = "High" if pr == "1" else "Low" if pr == "3" else "Medium"

        print("\nCategory (work/personal/study/shopping/other) [default other]: ", end="")
        cat = input().strip().title() or "Other"

        due = input("Due date (DD-MM-YYYY) or leave blank: ").strip()
        if due:
            try:
                datetime.datetime.strptime(due, "%d-%m-%Y")
            except Exception:
                print("Invalid due date format. It will be saved as blank.")
                due = ""

        task = {
            "id": self.next_id,
            "title": title,
            "description": description,
            "priority": priority,
            "category": cat,
            "due_date": due,
            "created_at": self.now_str(),
            "completed": False
        }
        self.tasks.append(task)
        self.next_id += 1
        self.save_tasks()
        print(f"Task '{title}' added (ID {task['id']}).")
        input("Press Enter to continue...")

    def view_tasks(self, tasks=None, header="All Tasks"):
        if tasks is None:
            tasks = self.tasks
        if not tasks:
            print("\nNo tasks to show.")
            return
        print(f"\n--- {header} ---")
        print("ID | Pri | Cat       | Status    | Title")
        print("-"*60)
        for t in tasks:
            status = "Done" if t.get("completed") else "Pending"
            title_display = self.truncate(t.get("title", ""), 38)
            print(f"{t['id']:2} | {t['priority'][0]}   | {t['category'][:9]:9} | {status:9} | {title_display}")
        print("-"*60)

    def complete_task(self):
        if not self.tasks:
            print("\nNo tasks available to complete.")
            return
        self.view_tasks()
        raw = input("Enter Task ID to mark as completed: ").strip()
        if not raw.isdigit():
            print("Enter a numeric ID.")
            return
        tid = int(raw)
        for t in self.tasks:
            if t["id"] == tid:
                if t["completed"]:
                    print("Task already completed.")
                else:
                    self.completed_stack.append(t.copy())
                    t["completed"] = True
                    t["completed_at"] = self.now_str()
                    self.save_tasks()
                    print(f"Task '{t['title']}' marked as completed.")
                input("Press Enter to continue...")
                return
        print("Task ID not found.")

    def undo_last_completion(self):
        if not self.completed_stack:
            print("\nNo completed tasks to undo. Complete a task first.")
            return
        last = self.completed_stack.pop()
        for t in self.tasks:
            if t["id"] == last["id"]:
                t["completed"] = False
                t.pop("completed_at", None)
                self.save_tasks()
                print(f"Undid completion of task '{t['title']}'.")
                input("Press Enter to continue...")
                return
        print("Unexpected: previously completed task not found.")

    def delete_task(self):
        if not self.tasks:
            print("\nNo tasks to delete.")
            return
        self.view_tasks()
        try:
            tid = int(input("Enter Task ID to delete: "))
            for i, t in enumerate(self.tasks):
                if t["id"] == tid:
                    deleted = self.tasks.pop(i)
                    self.completed_stack = [c for c in self.completed_stack if c["title"] != deleted["title"]]
                    self.reindex_ids()   # fixed: reindex IDs
                    self.save_tasks()
                    print(f"Deleted task '{deleted['title']}'.")
                    return
            print("Invalid Task ID.")
        except ValueError:
            print("Enter a valid number.")

    def sort_tasks(self):
        if not self.tasks:
            print("\nNo tasks to sort.")
            return
        print("\nSort by:")
        print("1. Priority (High -> Low)")
        print("2. Due date (earliest first)")
        print("3. Category (A-Z)")
        print("4. Created date (newest first)")
        choice = input("Choice (1-4): ").strip()
        arr = self.tasks.copy()

        n = len(arr)
        for i in range(n):
            for j in range(0, n - i - 1):
                swap = False
                if choice == "1":
                    order = {"High":3, "Medium":2, "Low":1}
                    if order[arr[j]["priority"]] < order[arr[j+1]["priority"]]:
                        swap = True
                elif choice == "2":
                    d1 = self.parse_date_str(arr[j].get("due_date",""))
                    d2 = self.parse_date_str(arr[j+1].get("due_date",""))
                    if d1 > d2:
                        swap = True
                elif choice == "3":
                    if arr[j]["category"].lower() > arr[j+1]["category"].lower():
                        swap = True
                elif choice == "4":
                    try:
                        c1 = datetime.datetime.strptime(arr[j]["created_at"], "%d-%m-%Y %H:%M")
                        c2 = datetime.datetime.strptime(arr[j+1]["created_at"], "%d-%m-%Y %H:%M")
                    except Exception:
                        c1 = c2 = datetime.datetime.min
                    if c1 < c2:
                        swap = True
                if swap:
                    arr[j], arr[j+1] = arr[j+1], arr[j]
        title = {
            "1":"Tasks sorted by Priority",
            "2":"Tasks sorted by Due date",
            "3":"Tasks sorted by Category",
            "4":"Tasks sorted by Created date"
        }.get(choice, "Sorted Tasks")
        self.view_tasks(arr, header=title)

    def search_tasks(self):
        if not self.tasks:
            print("\nNo tasks to search.")
            return
        kw = input("Enter keyword to search (title/description/category): ").strip().lower()
        if not kw:
            print("No keyword entered.")
            return
        found = []
        for t in self.tasks:
            if (kw in t["title"].lower() or
                kw in t.get("description","").lower() or
                kw in t.get("category","").lower()):
                found.append(t)
        self.view_tasks(found, header=f"Search results for '{kw}'")

    def view_by_category(self):
        if not self.tasks:
            print("\nNo tasks to show.")
            return
        groups = {}
        for t in self.tasks:
            cat = t.get("category","Other")
            groups.setdefault(cat, []).append(t)
        for cat, items in groups.items():
            print(f"\n{cat} ({len(items)} tasks):")
            self.view_tasks(items, header=f"{cat} tasks")

    def view_statistics(self):
        if not self.tasks:
            print("\nNo tasks for statistics.")
            return
        total = len(self.tasks)
        completed = sum(1 for t in self.tasks if t.get("completed"))
        pending = total - completed
        high = sum(1 for t in self.tasks if t.get("priority")=="High")
        med = sum(1 for t in self.tasks if t.get("priority")=="Medium")
        low = sum(1 for t in self.tasks if t.get("priority")=="Low")
        rate = (completed / total * 100) if total else 0.0
        print("\n--- Task Statistics ---")
        print(f"Total tasks     : {total}")
        print(f"Completed       : {completed}")
        print(f"Pending         : {pending}")
        print(f"High priority   : {high}")
        print(f"Medium priority : {med}")
        print(f"Low priority    : {low}")
        print(f"Completion rate : {rate:.1f}%")

def main():
    app = TODOList()
    while True:
        app.display_menu()
        choice = input("Enter your choice (1-10): ").strip()
        if not choice:
            print("Please enter a valid option.")
            continue
        if choice == "1":
            app.add_task()
        elif choice == "2":
            app.view_tasks()
            input("Press Enter to continue...")
        elif choice == "3":
            app.complete_task()
        elif choice == "4":
            app.undo_last_completion()
        elif choice == "5":
            app.delete_task()
        elif choice == "6":
            app.sort_tasks()
            input("Press Enter to continue...")
        elif choice == "7":
            app.search_tasks()
            input("Press Enter to continue...")
        elif choice == "8":
            app.view_by_category()
            input("Press Enter to continue...")
        elif choice == "9":
            app.view_statistics()
            input("Press Enter to continue...")
        elif choice == "10":
            print("\nSaving and exiting. Goodbye!")
            app.save_tasks()
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 10.")

if __name__ == "__main__":
    main()



