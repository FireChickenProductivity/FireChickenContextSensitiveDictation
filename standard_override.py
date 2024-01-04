from talon import Module, Context, actions, app, settings
from typing import Optional
from .stored_context import StoredContext
from .basic_action_recorder_interface import register_basic_action_recorder_callback_function, unregister_basic_action_recorder_callback_function, action_is_inserting_text
from .delay_settings import wait_select_word_delay, wait_copy_delay, wait_ending_delay, wait_post_copy_delay, wait_mid_peek_delay
from .clipboard import get_selected_text

module = Module()
module.tag('fire_chicken_context_sensitive_dictation', desc = 'Enables fire chicken context sensitive dictation')

debug_mode_setting_setting_name = 'fire_chicken_context_sensitive_dictation_print_debug_output'
debug_mode_setting = 'user.' + debug_mode_setting_setting_name
module.setting(
    debug_mode_setting_setting_name,
    type = int,
    default = 0,
    desc = 'If nonzero, debug information is printed to the console'
)

should_use_basic_action_recorder_for_context_setting_name = 'fire_chicken_context_sensitive_dictation_use_basic_action_recorder_for_context'
should_use_basic_action_recorder_for_context = 'user.' + should_use_basic_action_recorder_for_context_setting_name
module.setting(
    should_use_basic_action_recorder_for_context_setting_name,
    type = int,
    default = 0,
    desc = 'If nonzero and the basic action recorder is installed, fire chicken context sensitive dictation uses it for context information when the user has not used a non insert action'
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
            if context_is_not_needed(left, right): return None, None
            global stored_context
            if can_rely_on_stored_context(stored_context): return stored_context.get_context_information()
            global performing_dictation_peek
            performing_dictation_peek = True
            before, after = actions.user.fire_chicken_context_sensitive_dictation_perform_manual_peek(left, right)
            performing_dictation_peek = False
            if should_update_stored_after_context(right): stored_context.update_after(after)
            wait_ending_delay()
            return before, after
        
def context_is_not_needed(left: bool, right: bool) -> bool:
    return not (left or right)

def can_rely_on_stored_context(stored_context):
    return stored_context.has_relevant_before_information() and stored_context.has_relevant_after_information() and settings.get(should_use_basic_action_recorder_for_context)

def should_update_stored_after_context(right: bool):
    return right and settings.get(should_use_basic_action_recorder_for_context)

performing_dictation_peek: bool = False
stored_context = StoredContext()

def on_basic_action(action):
    if should_update_context_information():
        update_context_information(action)

def should_update_context_information() -> bool:
    global performing_dictation_peek
    return settings.get(should_use_basic_action_recorder_for_context) and not performing_dictation_peek

def update_context_information(action):
    global stored_context
    if action_is_inserting_text(action):
        stored_context.update_before(action)
    else:
        stored_context.consider_context_irrelevant()

module = Module()
@module.action_class
class Actions:
    def fire_chicken_context_sensitive_dictation_perform_manual_peek(left: bool, right: bool) -> tuple[Optional[str], Optional[str]]:
        '''Performs the manual peek for fire chicken context sensitive dictation'''
        before, after = None, None
        actions.user.fire_chicken_context_sensitive_dictation_perform_before_peek_setup(left, right)
        if left:
            before = actions.user.fire_chicken_context_sensitive_dictation_perform_peek_left()
        wait_mid_peek_delay()
        if right:
            after = actions.user.fire_chicken_context_sensitive_dictation_perform_manual_peek_right()
        actions.user.fire_chicken_context_sensitive_dictation_perform_after_peek_cleanup(left, right, before, after)
        return before, after
    
    def fire_chicken_context_sensitive_dictation_perform_before_peek_setup(left: bool, right: bool):
        '''Performs the initial setup for the fire chicken context sensitive dictation peaking'''
        actions.insert(" ")
    
    def fire_chicken_context_sensitive_dictation_perform_after_peek_cleanup(left: bool, right: bool, before: Optional[str], after: Optional[str]):
        '''Performs the cleanup for the fire chicken context sensitive dictation peaking'''
        if right:
            actions.key("delete")  # remove space
        else:
            actions.key("backspace")  # remove the space
    
    def fire_chicken_context_sensitive_dictation_perform_peek_left() -> str:
        '''Performs the left peek for fire chicken context sensitive dictation'''
        global stored_context
        if can_rely_on_stored_before_context(stored_context):
            before = stored_context.get_before()
        else:
            before = actions.user.fire_chicken_context_sensitive_dictation_perform_manual_peek_left()
        return before
        
    def fire_chicken_context_sensitive_dictation_perform_manual_peek_left() -> str:
        '''Performs the manual left peek for fire chicken context sensitive dictation'''
        actions.user.fire_chicken_context_sensitive_dictation_select_before()
        wait_copy_delay()
        selected_text: str = get_selected_text()
        before: str = selected_text[:-1]
        if should_display_debug_output(): print_debug_output(f'Before text is: ({before})')
        actions.user.fire_chicken_context_sensitive_dictation_unselect_before(before, selected_text)
        return before

    def fire_chicken_context_sensitive_dictation_perform_manual_peek_right() -> str:
        '''Performs the manual right peek for fire chicken context sensitive dictation'''
        actions.user.fire_chicken_context_sensitive_dictation_select_after()
        wait_copy_delay()
        selected_text: str = actions.edit.selected_text()
        wait_post_copy_delay()
        after: str = selected_text[1:]
        if should_display_debug_output(): print_debug_output(f'After text is: ({after})')
        actions.user.fire_chicken_context_sensitive_dictation_unselect_after(after, selected_text)
        return after

    def fire_chicken_context_sensitive_dictation_select_before():
        '''Selects the text before the cursor for context sensitive dictation'''
        wait_select_word_delay()
        actions.edit.extend_word_left()
        wait_select_word_delay()
        actions.edit.extend_word_left()
    
    def fire_chicken_context_sensitive_dictation_unselect_before(before: str, selected_text: str):
        '''Unselects the text before the cursor for context sensitive dictation'''
        actions.edit.right()

    def fire_chicken_context_sensitive_dictation_select_after():
        '''Selects the text after the cursor for context sensitive dictation'''
        actions.edit.left()
        wait_select_word_delay()
        actions.edit.extend_word_right()
        wait_select_word_delay()
        actions.edit.extend_word_right()
    
    def fire_chicken_context_sensitive_dictation_unselect_after(after: str, selected_text: str):
        '''Unselects the text after the cursor for context sensitive dictation'''
        actions.edit.left()

def print_debug_output(output: str):
    print('ContextSensitiveDictation:', output)

def should_display_debug_output():
    return settings.get(debug_mode_setting)

def can_rely_on_stored_before_context(stored_context):
    return stored_context.has_relevant_before_information() and settings.get(should_use_basic_action_recorder_for_context)

def setup():
    handle_should_use_basic_action_recorder_for_context_setting_change(settings.get(should_use_basic_action_recorder_for_context))

def handle_should_use_basic_action_recorder_for_context_setting_change(new_value):
    if new_value: register_basic_action_recorder_callback_function(on_basic_action)
    else: unregister_basic_action_recorder_callback_function()
    stored_context.consider_context_irrelevant()

settings.register('user.fire_chicken_context_sensitive_dictation_use_basic_action_recorder_for_context', handle_should_use_basic_action_recorder_for_context_setting_change)

app.register('ready', setup)