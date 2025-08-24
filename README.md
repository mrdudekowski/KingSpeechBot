# KingSpeech Bot 🤖

Telegram бот для автоматизации лидогенерации школы английского языка KingSpeech.

## 🚀 Быстрый деплой

### Railway (Рекомендуется - Бесплатно)

1. **Fork этого репозитория** на GitHub
2. **Перейдите на [Railway](https://railway.app/)**
3. **Нажмите "Deploy from GitHub repo"**
4. **Выберите ваш форк**
5. **Добавьте переменные окружения:**
   ```
   TELEGRAM_BOT_TOKEN=ваш_токен_бота
   SPREADSHEET_ID=ваш_spreadsheet_id
   ```
6. **Загрузите service-account.json** в разделе "Variables"
7. **Нажмите "Deploy"**

### Render (Альтернатива - Бесплатно)

1. **Fork этого репозитория** на GitHub
2. **Перейдите на [Render](https://render.com/)**
3. **Создайте новый Web Service**
4. **Подключите ваш GitHub репозиторий**
5. **Настройте переменные окружения**
6. **Нажмите "Create Web Service"**

## 📋 Требования

- Python 3.8+
- Telegram Bot Token
- Google Sheets API credentials
- Google Spreadsheet ID

## 🔧 Локальная установка

```bash
# Клонировать репозиторий
git clone https://github.com/your-username/kingspeech-bot.git
cd kingspeech-bot

# Установить зависимости
pip install -r requirements.txt

# Настроить переменные окружения
cp .env.example .env
# Отредактировать .env файл

# Запустить бота
python kingspeech_bot.py
```

## 📁 Структура проекта

```
kingspeech-bot/
├── dialogs/                 # Диалоги бота
│   ├── __init__.py         # Управление диалогами
│   └── main_survey.py      # Основной опрос
├── services/               # Сервисы
│   ├── dialog_manager.py   # Управление диалогами
│   ├── sheets_service.py   # Google Sheets интеграция
│   ├── cached_sheets_service.py  # Кэшированная версия
│   ├── localization_service.py   # Локализация
│   └── validators.py       # Валидация
├── locales/                # Локализация
│   ├── ru.json            # Русский
│   ├── en.json            # Английский
│   └── zh.json            # Китайский
├── kingspeech_bot.py      # Главный файл бота
├── config.py              # Конфигурация
├── requirements.txt       # Зависимости
└── Dockerfile            # Docker конфигурация
```

## 🔑 Настройка переменных окружения

Создайте файл `.env` со следующими переменными:

```env
TELEGRAM_BOT_TOKEN=ваш_токен_бота
SPREADSHEET_ID=ваш_spreadsheet_id
GOOGLE_APPLICATION_CREDENTIALS=service-account.json
```

## 📊 Функциональность

- ✅ 7-шаговый опрос с прогресс-баром
- ✅ Автоматическое создание листов Google Sheets по месяцам
- ✅ Обработка контактов через Telegram API
- ✅ Мультиязычная поддержка (русский/английский)
- ✅ Валидация данных и обработка ошибок
- ✅ Модульная архитектура

## 🧪 Тестирование

```bash
# Запустить тесты
pytest tests/

# Проверить покрытие
pytest --cov=.
```

## 📈 Мониторинг

- **Логи**: Доступны в консоли платформы деплоя
- **Статус**: Проверяйте через Telegram Bot API
- **Google Sheets**: Мониторинг через Google Sheets API

## 🔒 Безопасность

- Все токены хранятся в переменных окружения
- Валидация всех входных данных
- Rate limiting для защиты от спама
- Безопасная обработка контактов

## 📞 Поддержка

Если у вас возникли вопросы:
1. Проверьте логи в консоли платформы
2. Убедитесь, что все переменные окружения настроены
3. Проверьте права доступа к Google Sheets

## 📄 Лицензия

MIT License

---

**Создано для KingSpeech** 🎓 