import os
import torch

from dotenv import load_dotenv
from transformers import AutoModelForCausalLM, AutoTokenizer

load_dotenv(override=True)
hf_token = os.getenv("HF_TOKEN")

tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.2-3B-Instruct", token=hf_token)
model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-3.2-3B-Instruct", token=hf_token)


device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)  # Перемещаем модель на нужное устройство

# Подготовка входного текста
input_text = "Как дела?"
inputs = tokenizer(input_text, return_tensors="pt").to(device)  # Перемещаем входные данные на устройство

# Генерация текста
with torch.no_grad():  # Отключаем градиенты для экономии памяти
    outputs = model.generate(**inputs, max_length=50)  # max_length можно настроить

# Декодирование и вывод результата
generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
print(generated_text)
