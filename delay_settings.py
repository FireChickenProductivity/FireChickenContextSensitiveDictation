from talon import Module, actions, settings

module = Module()

copy_delay_setting_name = 'fire_chicken_context_sensitive_dictation_copy_delay'
copy_delay = 'user.' + copy_delay_setting_name
module.setting(
    copy_delay_setting_name,
    type = int,
    default = 200,
    desc = 'How long to pause in milliseconds when copying.'
)

post_copy_delay_setting_name = 'fire_chicken_context_sensitive_dictation_post_copy_delay'
post_copy_delay = 'user.' + post_copy_delay_setting_name
module.setting(
    post_copy_delay_setting_name,
    type = int,
    default = 0,
    desc = 'How long to pause in milliseconds after copying.'
)

ending_delay_setting_name = 'fire_chicken_context_sensitive_dictation_ending_delay'
ending_delay = 'user.' + ending_delay_setting_name
module.setting(
    ending_delay_setting_name,
    type = int,
    default = 0,
    desc = 'How long to pause in milliseconds after peeking'
)

select_word_delay_setting_name = 'fire_chicken_context_sensitive_dictation_select_word_delay'
select_word_delay = 'user.' + select_word_delay_setting_name
module.setting(
    select_word_delay_setting_name,
    type = int,
    default = 0,
    desc = 'How long to pause in milliseconds before word selection in the default fire chicken context sensitive dictation behavior'
)

mid_peek_delay_setting_name = 'fire_chicken_context_sensitive_dictation_mid_peek_delay'
mid_peek_delay = 'user.' + mid_peek_delay_setting_name
module.setting(
    mid_peek_delay_setting_name,
    type = int,
    default = 0,
    desc = 'How long to pause in milliseconds in between the left and right peeks'
)

def wait_copy_delay():
    wait_delay_setting(copy_delay)

def wait_post_copy_delay():
    wait_delay_setting(post_copy_delay)

def wait_ending_delay():
    wait_delay_setting(ending_delay)

def wait_mid_peek_delay():
    wait_delay_setting(mid_peek_delay)

def wait_select_word_delay():
    wait_delay_setting(select_word_delay)

def wait_delay_setting(setting):
    delay_amount = settings.get(setting)
    actions.sleep(f'{delay_amount}ms')
