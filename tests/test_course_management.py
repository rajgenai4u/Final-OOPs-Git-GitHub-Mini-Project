"""Unit tests for the Course Management System (stdlib unittest only)."""

import unittest

from course_management import (
    Course,
    CourseCapacityError,
    Enrollment,
    Mentor,
    Student,
    User,
)


class UserTests(unittest.TestCase):
    def setUp(self):
        self.student = Student("S001", "Alice Chen", "alice@student.edu")
        self.mentor = Mentor("M001", "Dr. Ada Lovelace", "ada@university.edu", "Algorithms")

    def test_polymorphic_role(self):
        self.assertEqual(self.student.get_role(), "Student")
        self.assertEqual(self.mentor.get_role(), "Mentor")
        self.assertIn("Student[S001]", str(self.student))
        self.assertIn("Mentor[M001]", str(self.mentor))

    def test_user_id_is_read_only(self):
        with self.assertRaises(AttributeError):
            self.student.user_id = "X"

    def test_email_validation(self):
        with self.assertRaises(ValueError):
            self.student.email = "not-an-email"
        self.student.email = "alice@new.edu"
        self.assertEqual(self.student.email, "alice@new.edu")

    def test_total_users_classmethod(self):
        before = User.total_users()
        Student("S900", "Nine", "nine@student.edu")
        self.assertEqual(User.total_users(), before + 1)

    def test_student_from_string_classmethod(self):
        student = Student.from_string("S100 | Zara | zara@student.edu")
        self.assertEqual((student.user_id, student.name, student.email), ("S100", "Zara", "zara@student.edu"))


class CourseTests(unittest.TestCase):
    def setUp(self):
        self.course = Course("CS101", "Intro to Programming", 4, capacity=2)

    def test_staticmethod_validate_code(self):
        self.assertEqual(Course.validate_code("cs101"), "CS101")
        with self.assertRaises(ValueError):
            Course.validate_code("bad")

    def test_classmethod_find_by_code(self):
        same = Course.find_by_code("CS101")
        self.assertIs(same, self.course)
        with self.assertRaises(KeyError):
            Course.find_by_code("ZZZ999")

    def test_capacity_property(self):
        self.course.capacity = 5
        with self.assertRaises(ValueError):
            self.course.capacity = 0
        alice = Student("S001", "Alice", "a@x.edu")
        bob = Student("S002", "Bob", "b@x.edu")
        alice.enroll(self.course)
        bob.enroll(self.course)
        with self.assertRaises(CourseCapacityError):
            self.course.capacity = 1

    def test_full_course(self):
        alice = Student("S001", "Alice", "a@x.edu")
        bob = Student("S002", "Bob", "b@x.edu")
        carol = Student("S003", "Carol", "c@x.edu")
        alice.enroll(self.course)
        bob.enroll(self.course)
        with self.assertRaises(CourseCapacityError):
            carol.enroll(self.course)


class EnrollmentTests(unittest.TestCase):
    def setUp(self):
        self.course = Course("AI404", "Intro to ML", 5, capacity=20)
        self.student = Student("S001", "Alice", "alice@x.edu")

    def test_grade_staticmethod(self):
        self.assertTrue(Enrollment.valid_grade(85))
        self.assertTrue(Enrollment.valid_grade(0))
        self.assertFalse(Enrollment.valid_grade(-1))
        self.assertFalse(Enrollment.valid_grade("A"))

    def test_enroll_complete_and_drop(self):
        enrollment = self.student.enroll(self.course)
        self.assertEqual(enrollment.status, "active")
        enrollment.complete(92)
        self.assertEqual(enrollment.status, "completed")
        self.assertEqual(enrollment.grade, 92)
        with self.assertRaises(ValueError):
            enrollment.complete(150)

        fresh = self.student.enroll(Course("MATH202", "Linear Algebra", 3))
        self.student.drop(fresh.course)
        self.assertEqual(fresh.status, "cancelled")

    def test_classmethod_count(self):
        before = Enrollment.count()
        self.student.enroll(self.course)
        self.assertEqual(Enrollment.count(), before + 1)


if __name__ == "__main__":
    unittest.main()