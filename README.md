# Хакатон Gigachat

Проект представляет собой виртуального помощника по адаптации новых сотрудников в компании. Помощник в основе своей использует GigaChat, чтобы предоставить информацию и задания на различных этапах адаптации. Проект включает в себя обработку данных, ретривал информации и построение конечной системы.

## Основной функционал
- ***Интерактивные инструкции***;
- ***Задачи и цели Onboarding'а***;
- ***Чат-Поддержка в реальном времени***;
- ***Оценка прогресса и обратная связь***;
- ***Аналитика Использования***.

## Контекст ассистена
Для формирования контекста с учетом QA в проекте использовались эмбеддинги из сета данных следующего формата:
question: Неструктурированный запрос или обычный вопрос.
context: Релевантный этому вопросу параграф из базы знаний (пассаж).
Для поддержания контекста и улучшения производительности системы был внедрен ансамбль ретриверов, представленный моделями:
TFIDFRetriever: Модель, основанная на методе TF-IDF (Term Frequency-Inverse Document Frequency), который оценивает важность слова в контексте документа.
EmbedchainRetriever: Модель, предоставляющая эмбеддинги для вопросов и контекстов, обеспечивая более глубокое понимание семантики запросов и пассажей.
ElasticSearchBM25Retriever: Модель, использующая алгоритм BM25 в Elasticsearch для эффективного поиска релевантных документов.

## Стек проекта
- Backend
    - ![Python/FastAPI](https://img.shields.io/badge/fastapi-109989?style=for-the-badge&logo=FASTAPI&logoColor=white): Веб-фреймворк для разработки быстрых API на основе языка Python.
    - ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white): Реляционная база данных для хранения структурированных данных.
    - ![Elasticsearch](https://img.shields.io/badge/Elastic_Search-005571?style=for-the-badge&logo=elasticsearch&logoColor=white): Поисковый и аналитический движок для обработки и анализа больших объемов данных.
- Data Processing
    - ![Airflow](https://img.shields.io/badge/Airflow-017CEE?style=for-the-badge&logo=Apache%20Airflow&logoColor=white): Платформа управления потоками данных с открытым исходным кодом.
    - gigachain: Библиотека для создания и использования языковых моделей.
    - faiss-cpu: Библиотека для эффективного поиска по векторам.
    - sentence-transformers: Модели для преобразования текстовых данных в векторы.
    - sentencepiece: Инструмент для токенизации текста.
- Text Retrieval
    - rank_bm25: Библиотека для ранжирования документов по их релевантности к запросу.
- Data Management
    - datasets: Библиотека для управления и работе с различными датасетами.

## Запуск проекта

``` 
# Копирование переменных окружения
cp .env.example .env 

# Копирование файлов настроек для nginx
rm -rf ./nginx/static && cp -r ./nginx/static_defaults/ ./nginx/static

# Запуск проекта
make dev
```

## Полезные ссылки
- [UserFlow](https://miro.com/app/board/uXjVNHqnQEs=/?share_link_id=661963652395)
- [Design](https://www.figma.com/file/lpEJl9nvFcWcO0RXV49V6s/GigaChat?type=design&node-id=0-1&mode=design)
- [Презентация](https://drive.google.com/drive/folders/1RyQes6j32EB0TZiysGlvVfHsikXHn-Mt?usp=sharing)
