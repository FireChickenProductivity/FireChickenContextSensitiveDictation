from talon import clip, actions
from .delay_settings import wait_post_copy_delay

def get_selected_text():
    with clip.revert():
        actions.edit.copy()
        wait_post_copy_delay()
        try:
            result = clip.text()
        except clip.NoChange:
            result = ''
    return result

