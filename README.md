
# cli-todolist

### A Simple Command-Line Todo List Manager

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue" alt="Python Version">
  <img src="https://img.shields.io/badge/Status-WIP-orange" alt="Project Status">
</p>

---

**cli-todolist** is a simple yet powerful command-line tool for managing your tasks directly from the terminal. With features like task persistence, rich-text formatting, and various task management capabilities, it's a great way to stay productive while practicing your Python skills.

> **Note:** This project was created for learning purposes and is not intended for production use.

---

## Features

- Add, remove, and list tasks.
- Mark tasks as done.
- Edit existing tasks.
- Support for task persistence using **SQLite**.
- Pretty terminal output with **Rich**.
- Sort tasks by different criteria.

---

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/cli-todolist.git
   cd cli-todolist
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the app:
   ```bash
   python todolist.py
   ```

---

## Usage

Here are some examples of how to use `cli-todolist`:

- **Add a task**:
  ```bash
  python todolist.py create "Buy groceries" -d "Get milk and eggs"
  ```

- **List tasks**:
  ```bash
  python todolist.py list --sort title --reversed
  ```

- **Mark a task as done**:
  ```bash
  python todolist.py complete 1
  ```

- **Remove a task**:
  ```bash
  python todolist.py delete 1 --interactive
  ```

- **Edit a task**:
  ```bash
  python todolist.py edit 2 -t "Updated title" -d "Updated description" --completed
  ```

- **For more information check the help command**
    ```bash
    python todolist.py -h
    usage: Todo [-h] {create,delete,complete,list,edit} ...

    A simple Todo list in the CLI

    options:
    -h, --help            show this help message and exit

    General Commands:
    Available Commands

    {create,delete,complete,list,edit}
        create              Create a new Task
        delete              Delete a task
        complete            Mark the Task as Completed
        list                List all current Tasks
        edit                Edit the selected Task (Interactive edit by default if no argument is provided)
    ```

---


## TODO: Improve Functions

### 1. **Improve `get_task_by_id` Function**
- [ ] **Clarify Return Value**  
  - Update docstring to reflect return type (`Task | None`).
  - Ensure `None` is returned consistently for non-existent tasks.

- [ ] **Handle Exceptions**  
  - Catch potential database errors and provide meaningful error messages.

- [ ] **Console Output**  
  - Ensure error messages are properly logged or optionally printed.

### 2. **Improve `get_all_tasks` Function**
- [ ] **Handle Empty Results**  
  - Ensure a meaningful message is returned or logged when no tasks are found.

### 3. **Improve `create_task` Function**
- [ ] **Clarify Return Value**  
  - Return the created `Task` object instead of `True`.

- [ ] **Handle Exceptions**  
  - Roll back the transaction on errors.
  - Provide detailed error messages for debugging.

- [ ] **Optional Console Output**  
  - Ensure `console.print` is optional or configurable.

### 4. **Improve `delete_task` Function**
- [ ] **Return Meaningful Value**  
  - Return `False` explicitly if task deletion fails.

- [ ] **Handle Exceptions**  
  - Roll back the transaction and provide feedback in case of an error.

### 5. **Improve `update_task` Function**
- [ ] **Clarify Return Value**  
  - Return updated `Task` object explicitly.

- [ ] **Handle Exceptions**  
  - Roll back the transaction on failure.

- [ ] **Optional Console Output**  
  - Optionally log or print confirmation of updates.

### 6. **Improve `complete_task` Function**
- [ ] **Clarify Return Value**  
  - Return updated `Task` object for consistency.

- [ ] **Handle Exceptions**  
  - Ensure safe transaction handling.

- [ ] **Optional Console Output**  
  - Ensure output is configurable.

### 7. **Improve `list_tasks` Function**
- [ ] **Handle Empty Results**  
  - Display meaningful messages when no tasks are available.

- [ ] **Table Display Improvements**  
  - Add more formatting options for better visualization.

### 8. **Improve `interactive_edit_task` Function**
- [ ] **Ensure Consistency**  
  - Use updated `Task` objects consistently for confirmation.

- [ ] **Handle Exceptions**  
  - Roll back the transaction on any error.

### 9. **Improve `edit_task` Function**
- [ ] **Return Meaningful Value**  
  - Return the updated `Task` object for consistency.

- [ ] **Handle Exceptions**  
  - Provide robust error handling.

---

## Roadmap

### Completed
- [x] Add tasks
- [x] Remove tasks
- [x] List tasks
- [x] Mark tasks as done
- [x] Prettify the output using **Rich**
- [x] Add support for persistence (SQLite)
- [x] Add support for editing tasks
- [x] Add support for sorting tasks
- [x] Add logging

### In Progress
- [ ] Add tests

### Planned
- [ ] Add support for multiple lists
- [ ] Add support for due dates
- [ ] Add support for priorities
- [ ] Add support for tags
- [ ] Add support for subtasks
- [ ] Add support for recurring tasks
- [ ] Create `setup.py` to install the package
- [ ] Add support for TUI using [**Textual**](https://github.com/Textualize/textual)
- [ ] Add support for GUI using [**DearPyGui**](https://dearpygui.readthedocs.io/en/latest/)

---

## Contributing

Contributions are welcome! If you have suggestions for new features or improvements, feel free to open an issue or submit a pull request.

---

### Acknowledgments

- [**Rich**](https://github.com/Textualize/rich) for beautiful terminal output.
- [**SQLite**](https://www.sqlite.org/index.html) for lightweight persistence.
- [**Textual**](https://github.com/Textualize/textual) and [**DearPyGui**](https://dearpygui.readthedocs.io/en/latest/) for inspiring future UI improvements.
