from src.utils.create import create_script

def at_server_start():
    pass
    #create_script("src.utils.gametime.GameTime", obj=None)
def at_servr_stop():
    pass
def at_server_reload():
    pass
# Module containing your custom at_server_start(), at_server_reload() and
# at_server_stop() methods. These methods will be called every time
# the server starts, reloads and resets/stops respectively.
AT_SERVER_STARTSTOP_MODULE = ""