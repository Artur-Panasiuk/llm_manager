## Adding new model

Server automatically handles models by classes inherited from BaseModel. When adding new model, create new python file inside /models directory with name that will match class name in it. That name will be used by client when accessing model. Each model has its own python file.

### Structure of example_model.py

Script must import BaseModel from model_base.py, with it create class Example_model(BaseModel). Contents of class must include implementation of loading and prompting the model with latter returning str type value. To work properly, inherited values of model, tokenizer and path to model must be overwritten.