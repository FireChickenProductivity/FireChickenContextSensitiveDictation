from talon import Module, Context, actions
from typing import Optional

module = Module()
module.tag('fire_chicken_context_sensitive_dictation', desc = 'Enables fire chicken context sensitive dictation')

copy_delay = module.setting(
    'fire_chicken_context_sensitive_dictation_copy_delay',
    type = int,
    default = 200,
    desc = 'How long to pause in milliseconds when copying.'
)

debug_mode_setting = module.setting(
    'fire_chicken_context_sensitive_dictation_print_debug_output',
    type = int,
    default = 0,
    desc = 'If nonzero, debug information is printed to the console'
)

standard_override_context = Context()
standard_override_context.matches = r'''
tag: user.fire_chicken_context_sensitive_dictation
'''
#This is based on the dictation_peek action from the community talon repository located here: 
#https://github.com/talonhub/community
@standard_override_context.action_class('user')
class ContextSensitiveDictationActions:
        def dictation_peek(left: bool, right: bool) -> tuple[Optional[str], Optional[str]]:
            """
            Gets text around the cursor to inform auto-spacing and -capitalization.
            Returns (before, after), where `before` is some text before the cursor,
            and `after` some text after it. Results are not guaranteed; `before`
            and/or `after` may be None, indicating no information. If `before` is
            the empty string, this means there is nothing before the cursor (we are
            at the beginning of the document); likewise for `after`.

            To optimize performance, pass `left = False` if you won't need
            `before`, and `right = False` if you won't need `after`.

            dictation_peek() is intended for use before inserting text, so it may
            delete any currently selected text.
            """
            if not (left or right):
                return None, None
            before, after = None, None
            actions.insert(" ")
            if left:
                actions.edit.extend_word_left()
                actions.edit.extend_word_left()
                wait_copy_delay()
                before: str = actions.edit.selected_text()[:-1]
                if should_display_debug_output(): print_debug_output(f'Before text is: ({before})')
                actions.edit.right()
            if not right:
                actions.key("backspace")  # remove the space
            else:
                actions.edit.left()
                actions.edit.extend_word_right()
                actions.edit.extend_word_right()
                wait_copy_delay()
                after: str = actions.edit.selected_text()[1:]
                if should_display_debug_output(): print_debug_output(f'After text is: ({after})')
                actions.edit.left()
                actions.key("delete")  # remove space
            return before, after

def print_debug_output(output: str):
    print('ContextSensitiveDictation:', output)

def wait_copy_delay():
    wait_delay_setting(copy_delay)

def wait_delay_setting(setting):
    delay_amount = setting.get()
    actions.sleep(f'{delay_amount}ms')

def should_display_debug_output():
    return debug_mode_setting.get()