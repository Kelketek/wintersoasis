"""
Base object class for Winter's Oasis. Contains methods all objects should
have.
"""

from ev import Object

class WOObject(Object):
    def check_owner(self, target):
        owner = target.db.owner
        if not owner:
            return False
        return person == owner
