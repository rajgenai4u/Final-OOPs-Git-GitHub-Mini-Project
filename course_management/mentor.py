"""Mentor class demonstrating inheritance and polymorphic behaviour."""

from .user import User


class Mentor(User):
    """A mentor who teaches courses and guides students."""

    def __init__(self, mentor_id, name, email, specialization):
        super().__init__(mentor_id, name, email)
        self._specialization = specialization
        self._courses = []
        self._mentees = []

    @property
    def specialization(self):
        return self._specialization

    def teach_course(self, course):
        """Instance method: assign this mentor to ``course``."""
        if course in self._courses:
            raise ValueError(f"{self.name} already teaches {course.code}")
        course.mentor = self
        self._courses.append(course)
        return course

    def add_mentee(self, student):
        """Instance method: add a student under this mentor's guidance."""
        if student not in self._mentees:
            self._mentees.append(student)

    def list_courses(self):
        return list(self._courses)

    def list_mentees(self):
        return list(self._mentees)

    def get_role(self):
        return "Mentor"