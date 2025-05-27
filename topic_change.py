# Script to notify about topic changes


IMPORT_OK = True

try:
    import weechat
except ImportError:
    print('This script must be run under WeeChat.')
    print('Get WeeChat now at: https://weechat.org/')
    IMPORT_OK = False


def print_hook_cb(data, buffer, date, tags, displayed, highlight, prefix, message):
            weechat.prnt(topicbuffer, message)
            weechat.command(topicbuffer, "/buffer set hotlist 3")
            return weechat.WEECHAT_RC_OK

def topic_buffer_input_cb(data, buffer, input_data):
    return weechat.WEECHAT_RC_OK

def topic_buffer_close_cb(data, buffer):
    return weechat.WEECHAT_RC_OK


if __name__ == '__main__' and IMPORT_OK:
    # Register the script
    weechat.register("topic_notifier", "Viceroy", "1.0", "GPL3", "Topic Change Notifier", "", "")
    # create buffer
    topicbuffer = weechat.buffer_new("TOPIC", "topic_buffer_input_cb", "", "topic_buffer_close_cb", "")
    weechat.buffer_set(topicbuffer, "localvar_set_no_log", "1") # don't log

    weechat.prnt(topicbuffer, "Initialized Topic relay script")

    # Hook the print hook
    weechat.hook_print("", "irc_topic", "", 1, "print_hook_cb", "")
