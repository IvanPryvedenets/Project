from .models import Basket
from django.contrib import sessions


def context_processor():
    return {"session": sessions}

