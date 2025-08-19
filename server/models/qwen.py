import torch
from models.model_base import BaseModel
from transformers import AutoTokenizer, AutoModelForCausalLM


class Qwen(BaseModel):
    def __init__(self):
        super().__init__()
        self.path = "C:/Users/Artur/.cache/huggingface/hub/models--Qwen--Qwen2.5-Coder-3B"

    def load(self):
        self.tokenizer = AutoTokenizer.from_pretrained(self.path, trust_remote_code=False)
        self.model = AutoModelForCausalLM.from_pretrained(self.path, trust_remote_code=False)

    def prompt(self, prompt, tokens):
        device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        self.model = self.model.to(device)
        self.model.eval()

        inputs = self.tokenizer(prompt, return_tensors="pt")
        inputs = {k: v.to(device) for k, v in inputs.items()}

        outputs = self.model.generate(
            **inputs,
            max_new_tokens=tokens,
            do_sample=False
        )

        response = self.tokenizer.decode(outputs[0], skip_special_tokens=False)
        return response