"""
Base object class for Winter's Oasis. Contains methods all objects should
have.
"""

from ev import Object

class WOObject(Object):
    """
    Base typeclass for all objects, including characters.
    """
    def check_owner(self, target):
        owner = target.db.owner
        if not owner:
            return False
        return target == owner

    def controls(self, target):
        """
        Checks to see if the user has right to control an object.
        """
        if self.check_owner(target) or self.check_permstring('Superusers'):
            return True
        if target.check_permstring('Superusers'):
            return False
        if target.db.owner and target.db.owner.check_permstring('Immortal') \
        and target.db.protected:
            return False
        if self.check_permstring('Wizards'):
            return True
        return self.access(target, 'control')
