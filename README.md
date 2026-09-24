# Course Management System

A production-ready **Course Management System** built in **pure Python** to demonstrate the core pillars of **Object-Oriented Programming** and the full **Git / GitHub workflow** (feature branches, meaningful commits, merges and Pull Requests).

> Final OOPs + Git/GitHub mini project — repo: `rajgenai4u/Final-OOPs-Git-GitHub-Mini-Project`

---

## Table of Contents

- [Project Description](#project-description)
- [Architecture & Classes](#architecture--classes)
- [OOP Concepts Demonstrated](#oop-concepts-demonstrated)
- [Installation](#installation)
- [Features](#features)
- [Usage](#usage)
  - [Demo mode](#demo-mode)
  - [Interactive CLI](#interactive-cli)
- [Testing](#testing)
- [Git / GitHub Workflow](#git--github-workflow)
- [Project Structure](#project-structure)

---

## Project Description

The system manages **users** (`Student`s and `Mentor`s), **Courses** and **Enrollments**. It lets you:

- Register students and mentors
- Create courses with a defined capacity
- Enroll / drop students in courses
- Complete an enrollment and grade it
- Query course capacity, enrollment records and users

The codebase is **100% standard-library** (no third-party dependencies), typed, documented and covered by `unittest` tests.

---

## Architecture & Classes

```
course_management/
├── user.py         → User (abstract base class)
├── student.py      → Student (inherits User)
├── mentor.py       → Mentor  (inherits User)
├── course.py       → Course  (+ CourseCapacityError)
├── enrollment.py   → Enrollment
└── __init__.py     → package facade
```

```
                    +----------------------+
                    |        User          |   (ABC — abstract)
                    | -------------------- |
                    | #user_id  _name       |
                    | __email  system_users |
                    | -------------------- |
                    | get_role()  [abstract]|
                    | total_users() [@cls]  |
                    +---------+------------+
                              |
              +--------------+--------------+
              |                             |
    +---------v--------+          +---------v--------+
    |      Student     |          |      Mentor      |
    | ---------------- |          | ---------------- |
    | _enrollments[]   |          | _courses[]       |
    | ---------------- |          | _mentees[]       |
    | enroll()  drop() |          | teach_course()   |
    | courses_taken()  |          | add_mentee()     |
    | from_string()    |          | get_role(): Mentor|
    | get_role():Student|         +----+-------------+
    +---------+--------+              |
              |                       |
   +----------+-----------+           |
   |                    Course <------+  (Mentor assigned to course)
   |   code / title / credits / capacity / mentor
   |   _enrollments[]
   |   add_enrollment() / remove_enrollment() / seats_left()
   |   validate_code()  [@staticmethod]
   |   find_by_code()   [@classmethod]
   +----------+-----------+
              |
              v
   +----------------------+
   |      Enrollment      |
   | -------------------- |
   | _enrollment_id status grade |
   | -------------------- |
   | complete()  cancel() |
   | valid_grade()[@static]|
   | all()/count() [@cls] |
   +----------------------+
```

| Class       | Layer  | Responsibilities                                                      |
|-------------|--------|-----------------------------------------------------------------------|
| `User`      | Base   | Shared identity, property-based encapsulation, abstract `get_role()`  |
| `Student`   | Child  | Enroll / drop courses, track own enrollments, parse from string       |
| `Mentor`    | Child  | Teach courses, guide mentees                                          |
| `Course`    | Domain | Registry of courses, capacity rules, static/class-method lookups      |
| `Enrollment`| Domain | Link Student ↔ Course, status/lifecycle, grade validation             |

---

## OOP Concepts Demonstrated

| Concept         | Where                                                        |
|-----------------|--------------------------------------------------------------|
| **Inheritance** | `Student(User)`, `Mentor(User)`                              |
| **Encapsulation** | Private attributes (`__user_id`, `__code`, `__enrollment_id`) exposed via read-only/validated **properties** |
| **Polymorphism** | `get_role()` overridden per class; `__str__` dispatches by runtime type |
| **Abstraction** | `User` is an `ABC` with abstract `get_role()`                 |
| **Instance methods** | `enroll()`, `drop()`, `complete()`, `cancel()`, `seats_left()` |
| **@staticmethod** | `Course.validate_code()`, `Enrollment.valid_grade()`          |
| **@classmethod** | `Course.find_by_code()`, `Enrollment.all()`, `User.total_users()`, `Student.from_string()` |

---

## Installation

Requirements: **Python 3.8+** (no third-party packages needed).

```bash
git clone git@github.com:rajgenai4u/Final-OOPs-Git-GitHub-Mini-Project.git
cd Final-OOPs-Git-GitHub-Mini-Project

# (optional) create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# run the app
python3 main.py
```

---

## Features

- Abstract, typed domain model with strict input validation
- Property-driven encapsulation (read-only ids, validated emails, capacity, grades)
- Automatic enrollment ids (`ENR-0001`, ...) and a shared course registry
- Capacity enforcement with a domain exception (`CourseCapacityError`)
- Interactive menu **and** a one-shot demo runner
- Polymorphic role/reporting across all user types
- Full standard-library unit test suite

---

## Usage

### Demo mode

Print a narrated walkthrough of every OOP concept:

```bash
python3 main.py        # then select option 9, or:
python3 -c "from main import run_demo; run_demo()"
```

Sample output:

```
============================================================
  COURSE MANAGEMENT SYSTEM - DEMO
============================================================

-- Polymorphism: users speak through their own overridden get_role() --
  Student[S001] Alice Chen <alice@student.edu>
  Mentor[M001] Dr. Ada Lovelace <ada@university.edu>

-- Courses (encapsulated registry + __str__) --
  CS101 - Intro to Programming (4 cr, 0 seat(s) left)
```

### Interactive CLI

```bash
python3 main.py

Course Management System
  1. Add student
  2. Add mentor
  3. Add course
  4. Enroll student
  5. Drop enrollment
  6. Assign grade
  7. List courses
  8. Summary
  9. Run demo
  0. Exit
```

Example session:

```
> 1
Student (id|name|email): S004 | Dave | dave@student.edu
Added: Student[S004] Dave <dave@student.edu>

> 3
Course code (e.g. CS101): CS305
Title: Operating Systems
Credits: 4
Capacity: 25
Added: CS305 - Operating Systems (4 cr, 25 seat(s) left)

> 4
Student id: S004
Course code: CS305
Enrolled: ENR-0001 S004 Dave -> CS305 [active]
```

Programmatic usage:

```python
from course_management import Course, Mentor, Student

course = Course("DS303", "Data Structures", 4, capacity=25)
mentor = Mentor("M001", "Dr. Ada Lovelace", "ada@university.edu", "Algorithms")
mentor.teach_course(course)

alice = Student("S001", "Alice Chen", "alice@student.edu")
enrollment = alice.enroll(course)
enrollment.complete(92)

print(course)                       # DS303 - Data Structures (4 cr, 24 seat(s) left)
print(Course.find_by_code("DS303")) # classmethod lookup
print(Enrollment.all())             # every enrollment record
```

---

## Testing

```bash
python3 -m unittest discover -s tests -v
```

All tests live in `tests/test_course_management.py` and are stdlib `unittest` only.

---

## Git / GitHub Workflow

Development used **feature branches**, atomic commits and Pull Requests merged into `main`:

```
                    main
                     │
   ┌─────────────────┤─────────────────┐
   │                 │                 │
feature/user-    feature/course-    feature/cli-and-
classes   ─┐    enrollment   ─┐    tests        ─┐
   PR #1  ─┘    PR #2   ─────┘    PR #3  ───────┘
         merge        merge            merge
```

Run the tests above in CI locally; contributions follow: `git checkout -b feature/<name>` → commit → push → open a **Pull Request** → review → merge.

---

## Project Structure

```
Final-OOPs-Git-GitHub-Mini-Project/
├── main.py                        # CLI entry point + demo runner
├── README.md                      # this file
├── .gitignore
├── course_management/
│   ├── __init__.py
│   ├── user.py
│   ├── student.py
│   ├── mentor.py
│   ├── course.py
│   └── enrollment.py
└── tests/
    └── test_course_management.py
```

---

## License

MIT — free to use for learning and submission purposes.