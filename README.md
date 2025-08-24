# KingSpeech Bot 🤖

Telegram бот для автоматизации лидогенерации школы английского языка KingSpeech.

## 🚀 Быстрый деплой

### Render (Рекомендуется - Бесплатно)

1. **Fork этого репозитория** на GitHub
2. **Перейдите на [Render](https://render.com/)**
3. **Создайте новый Web Service**
4. **Подключите ваш GitHub репозиторий**
5. **Настройте переменные окружения:**
   ```
   TELEGRAM_BOT_TOKEN=ваш_токен_бота
   SPREADSHEET_ID=ваш_spreadsheet_id
   ```
6. **Загрузите service-account.json** в разделе "Secret Files"
7. **Нажмите "Create Web Service"**

## 📋 Требования

- Python 3.8+
- Telegram Bot Token
- Google Sheets API credentials
- Google Spreadsheet ID

## 🔧 Локальная установка

```bash
# Клонировать репозиторий
git clone https://github.com/mrdudekowski/KingSpeechBot.git
cd KingSpeechBot

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
KingSpeechBot/
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
├── Dockerfile            # Docker конфигурация
└── render.yaml           # Render конфигурация
```

## 🔑 Настройка переменных окружения

Создайте файл `.env` со следующими переменными:

```env
# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN=ваш_токен_бота
MANAGER_CHAT_ID=ваш_manager_chat_id

# Google Sheets Configuration
SPREADSHEET_ID=ваш_spreadsheet_id
SHEET_NAME=KingSpeechLeads

# Leads Bot Configuration (для пересылки лидов в @kingspeechassistbot)
LEADS_BOT_TOKEN=токен_бота_kingspeechassistbot
LEADS_BOT_CHAT_ID=chat_id_для_отправки_лидов
```

### Настройка пересылки лидов

1. **Получите токен бота @kingspeechassistbot** от @BotFather
2. **Получите Chat ID** куда отправлять лиды (может быть личный чат с ботом или группа)
3. **Добавьте переменные в .env:**
   - `LEADS_BOT_TOKEN` - токен бота @kingspeechassistbot
   - `LEADS_BOT_CHAT_ID` - ID чата для отправки лидов

## 📊 Функциональность

- ✅ 7-шаговый опрос с прогресс-баром
- ✅ Автоматическое создание листов Google Sheets по месяцам
- ✅ **Пересылка лидов в Telegram бота @kingspeechassistbot**
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
- **Health Check**: `https://your-app-name.onrender.com/health`

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