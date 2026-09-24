"""Interactive CLI for the Course Management System."""

from course_management import Course, CourseCapacityError, Enrollment, Mentor, Student, User


def run_demo():
    """Seed sample data and walk through the OOP concepts end to end."""
    courses = [
        Course("CS101", "Intro to Programming", 4, capacity=2),
        Course("MATH202", "Linear Algebra", 3, capacity=30),
        Course("DS303", "Data Structures", 4, capacity=25),
        Course("AI404", "Intro to Machine Learning", 5, capacity=20),
    ]

    mentor = Mentor("M001", "Dr. Ada Lovelace", "ada@university.edu", "Algorithms")
    mentor.teach_course(courses[0])
    mentor.teach_course(courses[2])

    students = [
        Student.from_string("S001 | Alice Chen | alice@student.edu"),
        Student("S002", "Bob Marin", "bob@student.edu"),
        Student("S003", "Cara Dias", "cara@student.edu"),
    ]

    enrollments = [
        students[0].enroll(courses[0]),
        students[1].enroll(courses[0]),
        students[1].enroll(courses[1]),
        students[2].enroll(courses[3]),
    ]
    for s in students[:2]:
        mentor.add_mentee(s)

    enrollments[0].complete(92)
    enrollments[1].complete(78)

    print("=" * 60)
    print("  COURSE MANAGEMENT SYSTEM - DEMO")
    print("=" * 60)

    print("\n-- Polymorphism: users speak through their own overridden get_role() --")
    for user in students + [mentor]:
        print(" ", user)

    print("\n-- Courses (encapsulated registry + __str__) --")
    for course in courses:
        print(" ", course)

    print("\n-- Course looked up through a classmethod: Course.find_by_code('DS303') --")
    print(" ", Course.find_by_code("DS303"))

    print("\n-- Staticmethod validation: Course.validate_code('CS101'/'nope') --")
    print("   valid:  ", Course.validate_code("cs101"))
    try:
        Course.validate_code("nope")
    except ValueError as exc:
        print("   invalid:", exc)

    print("\n-- Enrollments --")
    for enrollment in Enrollment.all():
        print(" ", enrollment)

    print(f"\n-- Class level summaries --")
    print(f"   Users created      : {User.total_users()}")
    print(f"   Enrollments created: {Enrollment.count()}")

    print("\n-- Capacity encapsulated via properties --")
    try:
        courses[0].capacity = 1
    except CourseCapacityError as exc:
        print("   ", exc)

    print("\n-- Staticmethod grade check: Enrollment.valid_grade --")
    print("   85 ->", Enrollment.valid_grade(85), "| 'A' ->", Enrollment.valid_grade("A"))
    print("\nDemo finished.")


def read_course(db, prompt="Course code"):
    return Course.find_by_code(input(f"{prompt}: ").strip())


def read_student(db, prompt="Student id"):
    student_id = input(f"{prompt}: ").strip()
    for student in db["students"]:
        if student.user_id == student_id:
            return student
    raise ValueError(f"No student with id {student_id}.")


def interactive_menu():
    db = {"students": [], "mentors": [], "courses": []}

    def add_student():
        student = Student.from_string(input("Student (id|name|email): ").strip())
        db["students"].append(student)
        print("Added:", student)

    def add_mentor():
        mentor = Mentor(
            input("Mentor id: ").strip(),
            input("Mentor name: ").strip(),
            input("Mentor email: ").strip(),
            input("Specialization: ").strip(),
        )
        db["mentors"].append(mentor)
        print("Added:", mentor)

    def add_course():
        course = Course(
            input("Course code (e.g. CS101): ").strip(),
            input("Title: ").strip(),
            int(input("Credits: ").strip()),
            capacity=int(input("Capacity: ").strip() or 30),
        )
        db["courses"].append(course)
        print("Added:", course)

    def enroll():
        student = read_student(db)
        course = read_course(db)
        enrollment = student.enroll(course)
        print("Enrolled:", enrollment)

    def drop():
        student = read_student(db)
        course = read_course(db)
        print("Dropped:", student.drop(course))

    def grade():
        enrollment_id = input("Enrollment id: ").strip()
        enrollment = next(e for e in Enrollment.all() if e.enrollment_id == enrollment_id)
        enrollment.complete(float(input("Grade (0-100): ").strip()))
        print("Updated:", enrollment)

    def list_courses():
        for course in db["courses"]:
            print(" ", course)
            for student in course.enrolled_students():
                print("      -", student.name)

    def summary():
        print(f"Users={User.total_users()} "
              f"Students={len(db['students'])} Mentors={len(db['mentors'])} "
              f"Courses={len(db['courses'])} Enrollments={Enrollment.count()}")

    actions = {
        "1": ("Add student", add_student),
        "2": ("Add mentor", add_mentor),
        "3": ("Add course", add_course),
        "4": ("Enroll student", enroll),
        "5": ("Drop enrollment", drop),
        "6": ("Assign grade", grade),
        "7": ("List courses", list_courses),
        "8": ("Summary", summary),
        "9": ("Run demo", run_demo),
    }

    while True:
        print("\nCourse Management System")
        for key, (label, _) in actions.items():
            print(f"  {key}. {label}")
        print("  0. Exit")
        choice = input("> ").strip()
        if choice == "0":
            print("Goodbye!")
            break
        action = actions.get(choice)
        if not action:
            print("Unknown option.")
            continue
        try:
            action[1]()
        except (ValueError, TypeError, KeyError, CourseCapacityError) as exc:
            print(f"Error: {exc}")


if __name__ == "__main__":
    interactive_menu()