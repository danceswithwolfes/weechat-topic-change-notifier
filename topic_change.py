import weechat
import re

# Script to notify about topic changes

SCRIPT_NAME = "topic_change_notify"
SCRIPT_AUTHOR = "Viceroy (modified by Termin8or)"
SCRIPT_VERSION = "1.1"
SCRIPT_LICENSE = "GPL3"
SCRIPT_DESC = "Topic Change Notifier - Reformats topic change messages"

# Compile regex patterns once for efficiency
# Pattern for topic change from "old" to "new"
# Example: User has changed topic for #DEVELOPMENT from "testing" to "testing in progress"
PATTERN_OLD_NEW = re.compile(
    r'^(.*?) has changed topic for (#[^ ]+) from "(.*?)" to "(.*?)"$', 
    re.IGNORECASE
)

# Pattern for topic set to "new" (no old topic mentioned explicitly in this format)
# Example: user has changed topic for #DEVELOPMENT to "testing"
PATTERN_NEW_ONLY = re.compile(
    r'^(.*?) has changed topic for (#[^ ]+) to "(.*?)"$', 
    re.IGNORECASE
)

def print_hook_cb(data, buffer, date, tags, displayed, highlight, prefix, message):
    topic_buffer_ptr = data 
    
    if not topic_buffer_ptr:
        # This should not happen if the script initializes correctly
        return weechat.WEECHAT_RC_OK

    formatted_message_lines = []
    match_old_new = PATTERN_OLD_NEW.match(message)

    if match_old_new:
        user = match_old_new.group(1).strip()
        channel = match_old_new.group(2).strip()
        old_topic = match_old_new.group(3).strip()
        new_topic = match_old_new.group(4).strip()
        
        formatted_message_lines.append(f"{user} has changed topic for {channel}")
        formatted_message_lines.append(f"old: {old_topic}")
        formatted_message_lines.append(f"new: {new_topic}")
    else:
        match_new_only = PATTERN_NEW_ONLY.match(message)
        if match_new_only:
            user = match_new_only.group(1).strip()
            channel = match_new_only.group(2).strip()
            new_topic = match_new_only.group(3).strip()
            
            formatted_message_lines.append(f"{user} has changed topic for {channel}")
            formatted_message_lines.append(f"new: {new_topic}")
        else:
            # Fallback: If no specific pattern matched, print the original message
            formatted_message_lines.append(message)

    # Print the formatted lines to the TOPIC buffer
    for line in formatted_message_lines:
        weechat.prnt(topic_buffer_ptr, line)

    # Set hotlist for the TOPIC buffer
    weechat.command(topic_buffer_ptr, "/buffer set hotlist 3")
    
    return weechat.WEECHAT_RC_OK

def topic_buffer_input_cb(data, buffer, input_data):
    return weechat.WEECHAT_RC_OK

def topic_buffer_close_cb(data, buffer):
    """Callback for when the TOPIC buffer is closed."""
    # weechat.prnt("", f"{SCRIPT_NAME}: TOPIC buffer closed.")
    return weechat.WEECHAT_RC_OK

if __name__ == '__main__':
    weechat.register(SCRIPT_NAME, SCRIPT_AUTHOR, SCRIPT_VERSION, SCRIPT_LICENSE, SCRIPT_DESC, "", "")
    
    topic_buffer = weechat.buffer_new("TOPIC", "topic_buffer_input_cb", "", "topic_buffer_close_cb", "")
    
    if topic_buffer:
        # Set the buffer to not log to WeeChat's main log file
        weechat.buffer_set(topic_buffer, "localvar_set_no_log", "1")
        
        weechat.prnt("", f"Initialized {SCRIPT_DESC} script (version {SCRIPT_VERSION})")
        
        weechat.hook_print("",
                           "irc_topic",
                           "",
                           1,
                           "print_hook_cb",
                           topic_buffer)
    else:
        weechat.prnt("", f"Error: Could not create TOPIC buffer for {SCRIPT_NAME}. Script will not function correctly.")

