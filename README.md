
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

## TODO: Improve Functions

### 1. **Improve `get_task_by_id` Function**
- [x] **Clarify Return Value**  
  - Update docstring to reflect return type (`Task | None`).
  - Ensure `None` is returned consistently for non-existent tasks.

- [x] **Handle Exceptions**  
  - Catch potential database errors and provide meaningful error messages.

- [x] **Console Output**  
  - Ensure error messages are properly logged or optionally printed.

### 2. **Improve `get_all_tasks` Function**
- [x] **Handle Empty Results**  
  - Ensure a meaningful message is returned or logged when no tasks are found.

### 3. **Improve `create_task` Function**
- [x] **Clarify Return Value**  
  - Return the created `Task` object instead of `True`.

- [x] **Handle Exceptions**  
  - Roll back the transaction on errors.
  - Provide detailed error messages for debugging.

### 4. **Improve `delete_task` Function**
- [x] **Handle Exceptions**  
  - Roll back the transaction and provide feedback in case of an error.

### 5. **Improve `update_task` Function**
- [x] **Clarify Return Value**  
  - Return updated `Task` object explicitly.

- [x] **Handle Exceptions**  
  - Roll back the transaction on failure.

### 6. **Improve `complete_task` Function**
- [x] **Clarify Return Value**  
  - Return updated `Task` object for consistency.

- [x] **Handle Exceptions**  
  - Ensure safe transaction handling.

### 7. **Improve `list_tasks` Function**
- [ ] **Table Display Improvements**  
  - Add more formatting options for better visualization.

### 8. **Improve `interactive_edit_task` Function**
- [x] **Ensure Consistency**  
  - Use updated `Task` objects consistently for confirmation.

- [x] **Handle Exceptions**  
  - Roll back the transaction on any error.

### 9. **Improve `edit_task` Function**
- [x] **Return Meaningful Value**  
  - Return the updated `Task` object for consistency.
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
