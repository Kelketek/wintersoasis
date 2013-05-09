"""
These commands are used for building in a user-content driven
environment.
"""

from ev import Command as BaseCommand
from ev import default_cmds
from ev import utils

Cmd = default_cmds.MuxCommand

class Create(Cmd):
    """
    @create - create new objects

    Usage:
      @create[/drop] objname[;alias;alias...][:type]

    switch:
       drop - automatically drop the new object into your current location (this is not echoed)
              this also sets the new object's home to the current location rather than to you.

    Create a new object. If a type is given, the object is created as
    that type. If no type is specified, a normal object is created.

    For example, if one wanted to create an object called 'Great Sword', they could type:

       @create Great Sword; : examples.red_button.RedButton
 
    """
    key = "@create"
    locks = "cmd:perm(create) or perm(Builders)"
    help_category = "Building"

    def func(self):
        """
        Creates the object.
        """

        caller = self.caller

        if not self.args:
            caller.msg("Usage: @create[/drop] objectname[;alias;alias...][:type]")
            return

        # create the objects
        for objdef in self.lhs_objs:
            string = ""
            name = objdef['name']
            aliases = objdef['aliases']
            typeclass = objdef['option']

            # create object (if not a valid typeclass, the default
            # object typeclass will automatically be used)
            lockstring = "control:id(%s);examine:perm(Builders);delete:id(%s) or perm(Wizards);get:all()" % (caller.id, caller.id)
            obj = create.create_object(typeclass, name, caller,
                                       home=caller, aliases=aliases, locks=lockstring, report_to=caller)
            if not obj:
                continue
            if aliases:
                string = "You create a new %s: %s (aliases: %s)."
                string = string % (obj.typeclass.typename, obj.name, ", ".join(aliases))
            else:
                string = "You create a new %s: %s."
                string = string % (obj.typeclass.typename, obj.name)
            # set a default desc
            if not obj.db.desc:
                obj.db.desc = "You see nothing special."
            if 'drop' in self.switches:
                if caller.location:
                    obj.home = caller.location
                    obj.move_to(caller.location, quiet=True)
        if string:
           caller.msg(string)
