"""

Lockfuncs module template

Copy this module one level up, to gamesrc/conf/, name it what
you will and edit it to your liking.

Then add the new module's path to the end of the tuple
defined in settings.LOCK_FUNC_MODULES.

All functions defined globally in this module are assumed to be
available for use in lockstrings to determine access. See
http://code.google.com/p/evennia/wiki/Locks

A lock function is always called with two arguments, accessing_obj and
accessed_obj, followed by any number of arguments. All possible
arguments should be handled (excess ones calling magic (*args,
**kwargs) to avoid errors). The lock function should handle all
eventual tracebacks by logging the error and returning False.

See many more examples of lock functions in src.locks.lockfuncs.

"""

def semi_approved(accessing_obj, accessed_obj, *args, **kwargs):
    return accessing_obj.db.approvers
