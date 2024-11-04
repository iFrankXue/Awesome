# utils.py

import uuid
from django.http import Http404

def validate_uuid(pk):
    try:
        uuid.UUID(pk, version=4)
    except ValueError:
        raise Http404("Invalid UUID")