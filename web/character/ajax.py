from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from character.models import TagDef, Tag
import ev

def get_settings(request, character):
    """
    Get settings needed for toggles.
    """
    player = ev.search_player(character)[0]
    character = player.character
    my_character = request.user.get_profile().character
    return player, character, my_character

def permissions_check(my_character, target):
    if my_character.player.user.is_staff:
        return True
    if my_character in target.get_alts() or target == my_character:
        return True
    return False

@dajaxice_register
def list_toggle(request, character, listname, elementid, toggle=True):
    """
    Toggle whether or not a user is in one's personal lists.
    """
    result = ""
    dajax = Dajax()
    permitted_lists = {
                        'following': ('Unfollow this character.', 'Follow this character.'),
                        'hiding_from': ('Stop hiding from this character.', 'Hide from this character.'),
                        'ignoring': ('Stop ignoring this character.', 'Ignore this character.')
                      }
    try:
        player, character, my_character = get_settings(request, character)
        mapping = {}
        mapping[True], mapping[False] = permitted_lists[listname]
    except IndexError:
        result = "Could not find player internally."
    except KeyError:
        result = "Not a valid list name."
    if not result:
        status = my_character.check_list(character, listname)
        if toggle:
            my_character.toggle_list(character, not status, listname)
            result = mapping[not status]
        else:
            result = mapping[status]
    dajax.assign(elementid, 'innerHTML', result)
    return dajax.json()

@dajaxice_register
def tags_save(request, character, tag_list):
    """
    Save a player's RP tags.
    """
    result = ""
    dajax = Dajax()
    try:
        player, character, my_character = get_settings(request, character)
        if not permissions_check(my_character, character):
            result = "Permission Denied."
    except IndexError:
        result = "Could not find player internally."
    try:
        tag_list[:]
    except:
        result = "Bad Request."
    if result:
        dajax.assign('#tag_error', 'innerHTML', result)
        return dajax.json()
    print character
    character_tags = character.get_tags(flat=True)
    tags = []
    for tag in tag_list:
        try:
            tags.append(TagDef.objects.get(name=tag))
        except:
            continue
    # Sync lists in a manner which calls the DB the least number of times.
    for tag in character_tags:
        if tag not in tags:
            # Possibility of duplicates. Kill them all.
            doomed_tags = Tag.objects.filter(tag=tag)
            for tag in doomed_tags:
                tag.delete()
    for tag in tags:
        if tag not in character_tags:
            Tag(character=character, tag=tag).save()
    dajax.assign('#tag_error', 'innerHTML', "Saved.")
    return dajax.json()