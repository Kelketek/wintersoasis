from django.contrib.auth.models import User
from selectable.base import ModelLookup
from selectable.registry import registry, LookupAlreadyRegistered

class UserLookup(ModelLookup):
    model = User
    search_fields = ('username__icontains', )

try:
    registry.register(UserLookup)
except LookupAlreadyRegistered:
    pass
