from talon import Module, actions

module = Module()

copy_delay = module.setting(
    'fire_chicken_context_sensitive_dictation_copy_delay',
    type = int,
    default = 200,
    desc = 'How long to pause in milliseconds when copying.'
)

post_copy_delay = module.setting(
    'fire_chicken_context_sensitive_dictation_post_copy_delay',
    type = int,
    default = 0,
    desc = 'How long to pause in milliseconds after copying.'
)

ending_delay = module.setting(
    'fire_chicken_context_sensitive_dictation_ending_delay',
    type = int,
    default = 0,
    desc = 'How long to pause in milliseconds after peeking'
)

select_word_delay = module.setting(
    'fire_chicken_context_sensitive_dictation_select_word_delay',
    type = int,
    default = 0,
    desc = 'How long to pause in milliseconds before word selection in the default fire chicken context sensitive dictation behavior'
)

def wait_copy_delay():
    wait_delay_setting(copy_delay)

def wait_post_copy_delay():
    wait_delay_setting(post_copy_delay)

def wait_ending_delay():
    wait_delay_setting(ending_delay)

def wait_select_word_delay():
    wait_delay_setting(select_word_delay)

def wait_delay_setting(setting):
    delay_amount = setting.get()
    actions.sleep(f'{delay_amount}ms')
