import torch
from transformers import pipeline

model_id = "meta-llama/Llama-3.2-3B-Instruct"
pipe = pipeline(
    "text-generation",
    model=model_id,
    torch_dtype=torch.bfloat16,
    device_map="auto",
)

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
    outputs = pipe(
    messages,
    max_new_tokens=256,
)
    return outputs[0]["generated_text"][-1]

if __name__ == "__main__":
    # Пример входных данных
    error_id = "000bd884-acb9-481b-9f83-4f200da02dbd"
    ip = "192.168.1.78"
    timestamp = "2024-10-23 03:05:08"
    error_details = '{"error": "Error 500"}'
    code = 500
    comment = "Internal Server Error: The server has encountered a situation it doesnt know how to handle."

    # Определяем ответственного
    responsible = determine_responsible(error_id, ip, timestamp, error_details, code, comment)
    print("Generated Response:")
    print(responsible)