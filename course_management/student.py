"""Student class demonstrating inheritance and instance behaviour."""

from .user import User


class Student(User):
    """A student who can enrol in courses.

    Demonstrates inheritance from ``User`` and polymorphic ``get_role``.
    """

    def __init__(self, student_id, name, email):
        super().__init__(student_id, name, email)
        self._enrollments = []

    @property
    def enrollments(self):
        return list(self._enrollments)

    def enroll(self, course):
        """Instance method: register this student for ``course``."""
        from .enrollment import Enrollment

        enrollment = Enrollment(self, course)
        self._enrollments.append(enrollment)
        course.add_enrollment(enrollment)
        return enrollment

    def drop(self, course):
        """Instance method: cancel the active enrollment in ``course``."""
        for enrollment in self._enrollments:
            if enrollment.course is course and enrollment.status == "active":
                course.remove_enrollment(enrollment)
                self._enrollments.remove(enrollment)
                enrollment.cancel()
                return enrollment
        raise ValueError(f"{self.name} is not actively enrolled in {course.code}")

    def courses_taken(self):
        """Return the list of courses this student is actively enrolled in."""
        return [e.course for e in self._enrollments if e.status == "active"]

    def get_role(self):
        return "Student"

    @classmethod
    def from_string(cls, data):
        """Classmethod: build a Student from a ``"id|name|email"`` string."""
        parts = [part.strip() for part in str(data).split("|")]
        if len(parts) != 3:
            raise ValueError(f"Expected 'id|name|email', got {data!r}")
        return cls(parts[0], parts[1], parts[2])