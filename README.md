# GhatGPT навык для Алисы от Яндекса

# Описание

Этот проект добавляет навык для умной колонки Алиса, который позволяет использовать модель языка ChatGPT для генерации текста в ответ на пользовательские запросы. Проект работает через API_KEY, который позволяет взаимодействовать с моделью языка ChatGPT на удаленном сервере.

# Инструкции по установке и использованию

## Установка

* Склонируйте репозиторий на свой компьютер:

      git clone https://github.com/peleccom/chat_gpt_yandex_alice.git

* Получите API_KEY в профиле на сайте openai https://platform.openai.com/account/api-keys

* Сохраните его в .env файле в корне проекта
    OPENAI_API_KEY={YOUR_KEY}

* Запустите проект

      docker-compose up


* Подключите навык к Алисе


## Локальное тестирование

Установите утилиту [alice-nearby](https://github.com/azzzak/alice-nearby)


Запустите ее указав webhook на localhost

    ./alice-nearby --webhook=http://localhost:5000/post --port=3456


Откройте `http://localhost:3456` в браузере

# Ссылки

OpenAI API: https://openai.com/api/

Документация по API Алисы: https://yandex.ru/dev/dialogs/alice/doc/

Руководство по разработке навыков для Алисы: https://yandex.ru/dev/dialogs/alice/doc/quickstart-about.html
