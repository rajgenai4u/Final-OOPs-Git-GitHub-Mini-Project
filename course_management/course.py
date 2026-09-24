"""Course class demonstrating static/class methods, encapsulation and a registry."""

import re


class CourseCapacityError(Exception):
    """Raised when a course has no free seats."""


class Course:
    """A course offered by the system.

    Demonstrates:
        - @staticmethod : ``validate_code`` helper.
        - @classmethod  : ``find_by_code`` over a shared registry.
        - Encapsulation : private ``__code`` exposed read-only via a property.
        - Instances     : enrolment/Drop logic as instance methods.
    """

    _registry = {}

    def __init__(self, code, title, credits, capacity=30, mentor=None):
        code = Course.validate_code(code)
        self.__code = code
        self._title = title
        self._credits = credits
        self._capacity = capacity
        self._mentor = None
        self._enrollments = []
        Course._registry[code] = self
        if mentor is not None:
            self.mentor = mentor

    @property
    def code(self):
        return self.__code

    @property
    def title(self):
        return self._title

    @property
    def credits(self):
        return self._credits

    @property
    def capacity(self):
        return self._capacity

    @capacity.setter
    def capacity(self, value):
        if not isinstance(value, int) or value <= 0:
            raise ValueError("Capacity must be a positive integer.")
        if value < len(self._enrollments):
            raise CourseCapacityError(
                f"Cannot shrink {self.__code} below its {len(self._enrollments)} enrolments."
            )
        self._capacity = value

    @property
    def mentor(self):
        return self._mentor

    @mentor.setter
    def mentor(self, mentor):
        from .mentor import Mentor

        if mentor is not None and not isinstance(mentor, Mentor):
            raise TypeError("Course mentor must be a Mentor instance or None.")
        self._mentor = mentor

    @property
    def enrollments(self):
        return list(self._enrollments)

    def add_enrollment(self, enrollment):
        if len(self._enrollments) >= self._capacity:
            raise CourseCapacityError(f"Course {self.__code} is full.")
        if any(e.student is enrollment.student for e in self._enrollments):
            raise ValueError(f"{enrollment.student.name} is already enrolled in {self.__code}.")
        self._enrollments.append(enrollment)

    def remove_enrollment(self, enrollment):
        try:
            self._enrollments.remove(enrollment)
        except ValueError:
            raise ValueError(f"Enrollment {enrollment.enrollment_id} not found in {self.__code}.")

    def enrolled_students(self):
        """Return students with an active enrollment in this course."""
        return [e.student for e in self._enrollments if e.status == "active"]

    def seats_left(self):
        active = len(self.enrolled_students())
        return max(0, self._capacity - active)

    def __str__(self):
        return f"{self.__code} - {self._title} ({self._credits} cr, {self.seats_left()} seat(s) left)"

    @staticmethod
    def validate_code(code):
        """Staticmethod: ensure ``code`` matches a format like ``CS101``."""
        if not isinstance(code, str) or not re.fullmatch(r"[A-Za-z]{2,4}\d{3}", code):
            raise ValueError(f"Invalid course code {code!r}; use a format like 'CS101'.")
        return code.upper()

    @classmethod
    def find_by_code(cls, code):
        """Classmethod: look up a course from the shared registry."""
        code = cls.validate_code(code)
        if code not in cls._registry:
            raise KeyError(f"No course registered with code {code}.")
        return cls._registry[code]