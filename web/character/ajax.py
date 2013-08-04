from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
import ev
from game.gamesrc.oasis.lib.oasis import get_full_taglist
from src.typeclasses.models import Tag


def get_settings(request, character):
    """
    Get settings needed for toggles.
    """
    player = ev.search_player(character)[0]
    character = player.db.avatar
    my_character = request.user.db.avatar
    return player, character, my_character

def permissions_check(my_character, target):
    if my_character.db.spirit.is_staff:
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
                        'watching': ('Watch this character.', 'Unwatch this character.'),
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
    print "CHARACTER TAGS: %s" % character_tags
    possible_tags = get_full_taglist()
    print "POSSIBLE TAGS: %s" % possible_tags
    print "PREPROCESSED TAG LIST: %s" % tag_list
    tag_list = Tag.objects.in_bulk(tag_list).values()
    print "TAG LIST: %s" % tag_list
    # Make sure someone doesn't hack up our other tags.
    tags = [tag for tag in tag_list if tag in possible_tags]

    for tag in character_tags:
        if tag not in tags:
            print "Removing %s" % tag
            category = tag.db_category.replace('object_','')
            character.tags.remove(tag.db_key, category=category)
    for tag in tags:
        if tag not in character_tags:
            print "Adding %s" % tag
            category = tag.db_category.replace('object_','')
            character.tags.add(tag.db_key, category=category)
    dajax.assign('#tag_error', 'innerHTML', "Saved.")
    return dajax.json()
