# Fire Chicken Context Sensitive Dictation
This repository offers code for overriding the default behavior of the talon community repository context sensitive dictation to make customization easier. It also offers an experimental application specific override for Microsoft Word.

# Settings
user.fire_chicken_context_sensitive_dictation_copy_delay: determines how long in milliseconds to pause before copying text to prevent the scenario of accidentally copying nothing. Default: 200.

user.fire_chicken_context_sensitive_dictation_use_basic_action_recorder_for_context: If nonzero and the basic action recorder is installed (https://github.com/FireChickenProductivity/BAR), it will be used for context information. Every time a basic action other than a text insert action is performed outside of the context grabbing, the context sensitive dictation will have to reassess context manually. Otherwise, it will rely on text insertion information obtained from the basic action recorder for context to the left of the cursor and remember the context to the right of the cursor from the last time it manually grabbed context.

user.fire_chicken_context_sensitive_dictation_ending_delay: determines how long in milliseconds to pause after getting context through peeking manually. Set to 0 by default. This can be useful if the peeking operations happening too quickly before inserting text can cause problems in a given application.

user.fire_chicken_context_sensitive_dictation_select_word_delay: determines how long in milliseconds to pause before selecting a word in the default implementation of the contact sensitive dictation peeking. Set to 0 by default.

user.fire_chicken_context_sensitive_dictation_post_copy_delay: determines how long in milliseconds to pause after copying. Consider increasing this if context sensitive dictation sometimes acts as if it is at the start of a new sentence. Consider setting this to 200 when working with Microsoft Word on windows.

user.fire_chicken_context_sensitive_dictation_mid_peek_delay: determines how long in milliseconds to pause in between manually determining what text is on the left and manually determining what text is on the right.

# Giving Credit
This repository contains some code taken from the talon community repository (https://github.com/talonhub/community/blob/main/LICENSE) distributed under the following license: 
MIT License

Copyright (c) 2021 Jeff Knaus, Ryan Hileman, Zach Dwiel, Michael Arntzenius, and others

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.