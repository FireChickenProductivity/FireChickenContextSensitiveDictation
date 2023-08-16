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

should_use_basic_action_recorder_for_context = module.setting(
    'fire_chicken_context_sensitive_dictation_use_basic_action_recorder_for_context',
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
            if not (left or right):
                return None, None
            global stored_context
            if stored_context.has_relevant_before_information() and stored_context.has_relevant_after_information() and should_use_basic_action_recorder_for_context.get():
                return stored_context.get_before(), stored_context.get_after()
            global performing_dictation_peek
            performing_dictation_peek = True
            before, after = None, None
            actions.insert(" ")
            if left:
                if stored_context.has_relevant_before_information() and should_use_basic_action_recorder_for_context.get():
                    before = stored_context.get_before()
                else:
                    actions.user.fire_chicken_context_sensitive_dictation_select_before()
                    wait_copy_delay()
                    selected_text: str = actions.edit.selected_text()
                    before: str = selected_text[:-1]
                    if should_display_debug_output(): print_debug_output(f'Before text is: ({before})')
                    actions.user.fire_chicken_context_sensitive_dictation_unselect_before(before, selected_text)
            if not right:
                actions.key("backspace")  # remove the space
            else:
                actions.user.fire_chicken_context_sensitive_dictation_select_after()
                wait_copy_delay()
                selected_text: str = actions.edit.selected_text()
                after: str = selected_text[1:]
                if should_display_debug_output(): print_debug_output(f'After text is: ({after})')
                actions.user.fire_chicken_context_sensitive_dictation_unselect_after(after, selected_text)
                actions.key("delete")  # remove space
                if should_use_basic_action_recorder_for_context.get() and not stored_context.has_relevant_after_information():
                    stored_context.update_after(after)
            performing_dictation_peek = False
            return before, after

performing_dictation_peek: bool = False

class StoredContext:
    def __init__(self):
        self.stored_before: str = ''
        self.stored_after: str = ''
        self.has_before_information: bool = False
        self.has_after_information: bool = False
    
    def consider_context_irrelevant(self):
        self.has_before_information = False
        self.has_after_information = False
        self.stored_before = ''
        self.stored_after = ''
    
    def update_before(self, before: str):
        if before.isspace():
            self.stored_before += before
        else:
            self.stored_before = before
        self.has_before_information = True
    
    def update_after(self, after: str):
        self.stored_after = after
        self.has_after_information = True
    
    def has_relevant_before_information(self):
        return self.has_before_information
    
    def has_relevant_after_information(self):
        return self.has_after_information
    
    def get_before(self):
        return self.stored_before
    
    def get_after(self):
        return self.stored_after
stored_context = StoredContext()

def on_basic_action(action):
    global stored_context
    if action.get_name() == 'insert':
        inserted_text = action.get_arguments()[0]
        stored_context.update_before(inserted_text)
    else:
        stored_context.consider_context_irrelevant()

module = Module()
@module.action_class
class Actions:
    def fire_chicken_context_sensitive_dictation_select_before():
        '''Selects the text before the cursor for context sensitive dictation'''
        actions.edit.extend_word_left()
        actions.edit.extend_word_left()
    
    def fire_chicken_context_sensitive_dictation_unselect_before(before: str, selected_text: str):
        '''Unselects the text before the cursor for context sensitive dictation'''
        actions.edit.right()

    def fire_chicken_context_sensitive_dictation_select_after():
        '''Selects the text after the cursor for context sensitive dictation'''
        actions.edit.left()
        actions.edit.extend_word_right()
        actions.edit.extend_word_right()
    
    def fire_chicken_context_sensitive_dictation_unselect_after(after: str, selected_text: str):
        '''Unselects the text after the cursor for context sensitive dictation'''
        actions.edit.left()

def print_debug_output(output: str):
    print('ContextSensitiveDictation:', output)

def wait_copy_delay():
    wait_delay_setting(copy_delay)

def wait_delay_setting(setting):
    delay_amount = setting.get()
    actions.sleep(f'{delay_amount}ms')

def should_display_debug_output():
    return debug_mode_setting.get()