from talon import actions

REGISTRATION_NAME: str = 'FireChickenContextSensitiveDictation'
def register_basic_action_recorder_callback_function(function):
    try: actions.user.basic_action_recorder_register_callback_function_with_name(function, REGISTRATION_NAME)
    except: print('Fire Chicken Context Sensitive Dictation: The BAR must be installed to use basic action recording for context.')

def unregister_basic_action_recorder_callback_function():
    try: actions.user.basic_action_recorder_unregister_callback_function_with_name(REGISTRATION_NAME)
    except: print('Fire Chicken Context Sensitive Dictation: The BAR must be installed to use basic action recording for context.')

def action_is_inserting_text(action) -> bool:
    return action.get_name() == 'insert'

def get_text_from_insert_action(action) -> str:
    return action.get_arguments()[0]