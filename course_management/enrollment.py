"""Enrollment class linking a Student to a Course."""

from itertools import count


class Enrollment:
    """A single enrolment record between a student and a course."""

    _sequence = count(1)
    _registry = {}

    def __init__(self, student, course):
        self.__enrollment_id = f"ENR-{next(Enrollment._sequence):04d}"
        self._student = student
        self._course = course
        self._status = "active"
        self._grade = None
        Enrollment._registry[self.__enrollment_id] = self

    @property
    def enrollment_id(self):
        return self.__enrollment_id

    @property
    def student(self):
        return self._student

    @property
    def course(self):
        return self._course

    @property
    def status(self):
        return self._status

    @property
    def grade(self):
        return self._grade

    def complete(self, grade):
        """Instance method: mark the course complete with a grade."""
        if not Enrollment.valid_grade(grade):
            raise ValueError(f"Grade must be between 0 and 100, got {grade!r}.")
        self._grade = grade
        self._status = "completed"

    def cancel(self):
        """Instance method: cancel an active enrollment."""
        if self._status != "active":
            raise ValueError(f"Enrollment {self.enrollment_id} is already {self._status}.")
        self._status = "cancelled"

    def __str__(self):
        grade = f", grade {self._grade}" if self._grade is not None else ""
        return f"{self.enrollment_id} {self.student.name} -> {self.course.code} [{self._status}{grade}]"

    @staticmethod
    def valid_grade(grade):
        """Staticmethod: a grade is valid when it is a number in [0, 100]."""
        return isinstance(grade, (int, float)) and 0 <= grade <= 100

    @classmethod
    def all(cls):
        """Classmethod: all enrollment records, newest first."""
        return list(cls._registry.values())[::-1]

    @classmethod
    def count(cls):
        """Classmethod: total number of enrollment records."""
        return len(cls._registry)