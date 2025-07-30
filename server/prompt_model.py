import torch

def prompt_qwen(tokenizer, model, user_input):
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    model = model.to(device)
    model.eval()

    prompt = f"<|user|>\n{user_input}\n<|assistant|>"
    inputs = tokenizer(prompt, return_tensors="pt")
    inputs = {k: v.to(device) for k, v in inputs.items()}

    outputs = model.generate(
        **inputs,
        max_new_tokens=512,
        do_sample=False
    )

    response = tokenizer.decode(outputs[0], skip_special_tokens=False)
    return response

def prompt_llama(tokenizer, model, user_input):
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    model = model.to(device)
    model.eval()

    prompt = f"[INST] {user_input} [/INST]"
    inputs = tokenizer(prompt, return_tensors="pt")
    inputs = {k: v.to(device) for k, v in inputs.items()}

    outputs = model.generate(
        **inputs,
        max_new_tokens=512,
        do_sample=False
    )

    response = tokenizer.decode(outputs[0], skip_special_tokens=False)
    return response