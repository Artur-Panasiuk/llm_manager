from models.model_base import BaseModel

class Example_Model(BaseModel):
    def __init__(self):
        super().__init__()
        self.path = "Path to model directory"

    def load(self):
        '''
        Set self.tokenizer and self.model
        '''

    def prompt(self, prompt, tokens):
        '''
        Return str type output from model
        '''

    '''
    def clear_memory(self):
        BaseModel has basic implementation of clear_memory which is used everytime model is changed.
        If needed overwrite base function here.
    '''