from talon import clip, actions
from .delay_settings import wait_post_copy_delay

#This is based on the get_selected_text action from the community talon repository located here: 
#https://github.com/talonhub/community
def get_selected_text():
    with clip.revert():
        actions.edit.copy()
        wait_post_copy_delay()
        try:
            result = clip.text()
        except clip.NoChange:
            result = ''
    return result

