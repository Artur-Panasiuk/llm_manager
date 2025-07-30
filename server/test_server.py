import time
from prompt_model import prompt_llama, prompt_qwen
from db_connector import fetch_pending_prompt, update_response
from model_handler import load_model_and_tokenizer, load_models_config, get_model_by_id, clear_memory


def main():
    models = load_models_config()
    model_info, tokenizer, model = None, None, None
    current_model_id = None

    try:
        print("Server listening...")
        while True:
            task = fetch_pending_prompt()
            if task:
                prompt = task["prompt"]
                model_id = task.get("model_id", 1)
                doc_id = task["_id"]
                print(f"📥 Prompt (model {model_id}): {prompt}")

                if model_id != current_model_id:
                    print("Changing model")
                    clear_memory(model, tokenizer)
                    model_info = get_model_by_id(models, model_id)
                    tokenizer, model = load_model_and_tokenizer(model_info["path"])
                    current_model_id = model_id

                if model_info["type"] == "qwen":
                    response = prompt_qwen(tokenizer, model, prompt)
                elif model_info["type"] == "llama":
                    response = prompt_llama(tokenizer, model, prompt)
                else:
                    response = "model err"

                update_response(doc_id, response)
                print("Answer send\n")

            time.sleep(2)
    finally:
        clear_memory(model, tokenizer)
        print("memory cleaned")

if __name__ == "__main__":
    main()
