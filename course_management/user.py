"""Base User class demonstrating abstraction, encapsulation and class attributes."""

from abc import ABC, abstractmethod


class User(ABC):
    """Abstract base class for every user of the Course Management System.

    Demonstrates:
        - Abstraction     : subclass responsibility via the abstract ``get_role``.
        - Encapsulation   : private attributes exposed through properties.
        - Class variables : ``system_users`` counts created users across the app.
    """

    system_users = 0

    def __init__(self, user_id, name, email):
        self.__user_id = str(user_id)
        self._name = name
        self.__email = email
        User.system_users += 1

    @property
    def user_id(self):
        """Read-only identifier of the user."""
        return self.__user_id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Name must be a non-empty string.")
        self._name = value.strip()

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, value):
        if "@" not in value or "." not in value.split("@")[-1]:
            raise ValueError(f"Invalid email address: {value!r}")
        self.__email = value

    @abstractmethod
    def get_role(self):
        """Return the role of this user. Overridden by every subclass."""

    def __str__(self):
        return f"{self.get_role()}[{self.user_id}] {self.name} <{self.email}>"

    @classmethod
    def total_users(cls):
        """Classmethod: total number of users created so far."""
        return cls.system_users