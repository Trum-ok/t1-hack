import os
import sys

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from extractors import KnowledgeBaseBuilder
from dotenv import load_dotenv

load_dotenv()

# База знаний
knowledge_base = {
  "documents": [
    {
      "id": 1,
      "title": "Процесс разработки программного обеспечения",
      "content": "Наш процесс разработки программного обеспечения состоит из нескольких фаз:" \
      "планирование, анализ требований, проектирование, кодирование, тестирование и поддержка."
    },
    {
      "id": 2,
      "title": "Политика безопасности",
      "content": "Политика безопасности компании направлена на защиту информации и данных наших" \
      "клиентов. Все сотрудники обязаны соблюдать принципы безопасности."
    },
    {
      "id": 3,
      "title": "Описание продукта",
      "content": "Наш продукт — это облачная платформа для управления проектами, которая позволяет командам эффективно организовывать свою работу."
    },
    {
      "id": 4,
      "title": "Техническая документация",
      "content": "В нашей технической документации мы подробно описываем все API-интерфейсы, которые предоставляет наша платформа."
    }
  ]
}


def create_input_for_rag(query, knowledge_base):
    # Извлекаем текст из базы знаний
    context = " ".join([doc['content'] for doc in knowledge_base['documents']])
    input_text = f"Query: {query} Context: {context}"
    return input_text


kb_builder = KnowledgeBaseBuilder()
kb_builder.process_and_index("faiss/test.json", 'file')

# Пример: сохранение индекса
n = kb_builder.save_index()
print(n)

# Пример: выполнение поиска
query = "У вас есть документация?"
distances, indices = kb_builder.search(query)

print("Результаты поиска:")
print(f"Дистанции: {distances}")
print(f"Индексы: {indices}")
