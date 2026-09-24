"""Course Management System (OOPs + Git/GitHub mini project).

A clean, dependency-free package that demonstrates the core pillars of
object-oriented programming in Python: inheritance, encapsulation,
polymorphism, abstraction, instance methods, @staticmethod and @classmethod.
"""

from .user import User
from .student import Student
from .mentor import Mentor
from .course import Course, CourseCapacityError
from .enrollment import Enrollment

__all__ = [
    "User",
    "Student",
    "Mentor",
    "Course",
    "CourseCapacityError",
    "Enrollment",
]

__version__ = "1.0.0"