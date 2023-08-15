from talon import Context, actions

context = Context()
context.matches = '''
app: Microsoft Word
'''

WORD_LINE_START: str = '\r\n'
WORD_LINE_START_AND_END = '\r\n \r'

@context.action_class('user')
class MicrosoftWordActions:
    def fire_chicken_context_sensitive_dictation_unselect_before(before: str, selected_text: str):
        '''Unselects the text before the cursor for context sensitive dictation in Microsoft Word'''
        actions.edit.left()
        actions.edit.word_right()
    
    def fire_chicken_context_sensitive_dictation_select_before():
        actions.edit.extend_word_left()