# Хакатон Gigachat

## Запуск проекта

``` 
# Копирование переменных окружения
cp .env.example .env 

# Копирование файлов настроек для nginx
rm -rf ./nginx/static && cp -r ./nginx/static_defaults/ ./nginx/static

# Запуск проекта
make dev