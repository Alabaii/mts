from transformers import AutoModelForCausalLM, AutoTokenizer

model_name = "Qwen/Qwen2.5-Coder-1.5B-Instruct"

model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype="auto",
    device_map="auto"
)
tokenizer = AutoTokenizer.from_pretrained(model_name)

def determine_responsible(error_id, ip, timestamp, error_details, code, comment):
    error_data = {
        "error_id": error_id,
        "ip": ip,
        "timestamp": timestamp,
        "error_details": error_details,
        "code": code,
        "comment": comment
    }
# Текст для генерации
    input_text =  f"""
    Error Report:
    - Error ID: {error_id}
    - IP Address: {ip}
    - Timestamp: {timestamp}
    - Error Details: {error_details}
    - HTTP Status Code: {code}
    - Server Comment: {comment}

    Instructions:
    Based on the comment and HTTP status code, determine which team or person might be responsible.
    Use the HTTP status code and error description to infer the type of issue (e.g., network, application, database).
    give the answer in words, who is to blame? ind the culprit among the front development team, backend developer or someone else
"""

    messages = [
    {"role": "system", "content": "you are a helper for delegating mistakes"},
    {"role": "user", "content": input_text}
]
    text = tokenizer.apply_chat_template(
    messages,
    tokenize=False,
    add_generation_prompt=True
)
    model_inputs = tokenizer([text], return_tensors="pt").to(model.device)

    generated_ids = model.generate(
    **model_inputs,
    max_new_tokens=512
)
    generated_ids = [
    output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
]

    response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
    return response
# Пример использования функции
if __name__ == "__main__":
    # Пример входных данных
    error_id = "000bd884-acb9-481b-9f83-4f200da02dbd"
    ip = "192.168.1.78"
    timestamp = "2024-10-23 03:05:08"
    error_details = '{"error": "Error 404"}'
    code = 404
    comment = "Not Found: The server can not find the requested resource."

    # Определяем ответственного
    responsible = determine_responsible(error_id, ip, timestamp, error_details, code, comment)
    print("Generated Response:")
    print(responsible)