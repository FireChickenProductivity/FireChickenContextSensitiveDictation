from .basic_action_recorder_interface import get_text_from_insert_action

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
    
    def update_before(self, action):
        before: str = get_text_from_insert_action(action)
        if StoredContext._new_before_context_information_is_inadequate(before):
            self.stored_before += before
        else:
            self.stored_before = before
        self.has_before_information = True
    
    @staticmethod
    def _new_before_context_information_is_inadequate(before: str) -> bool:
        return before.isspace() or len(before) <= 1 or not before[0].isspace()
    
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
    
    def get_context_information(self):
        return self.get_before(), self.get_after()
