from fastapi import APIRouter

from . import attendance
from . import laid
from . import student

__all__ = [
    "attendance",
    "laid",
    "student",
]