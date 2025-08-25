# KingSpeech Bot 🤖

Telegram бот для автоматизации лидогенерации школы английского языка KingSpeech.

## 🌐 Интеграция с сайтом (Веб-хук)

### Настройка веб-хука для приема заявок с сайта

1. **Запустите веб-хук сервер:**
   ```bash
   python webhook_handler.py
   ```

2. **Настройте переменные окружения для веб-хука:**
   ```env
   WEBHOOK_SECRET=ваш_секретный_ключ
   WEBHOOK_PORT=5000
   ```

3. **Интегрируйте форму на сайте:**
   - Скопируйте код из `landing-integration-example.js`
   - Настройте URL веб-хука и секретный ключ
   - Добавьте JavaScript на ваш landing page

4. **Пример HTML формы:**
   ```html
   <form id="contact-form">
       <input type="text" name="name" placeholder="Ваше имя" required>
       <input type="tel" name="phone" placeholder="Телефон" required>
       <select name="level">
           <option value="">Выберите уровень</option>
           <option value="Начинающий">Начинающий</option>
           <option value="Средний">Средний</option>
           <option value="Продвинутый">Продвинутый</option>
       </select>
       <button type="submit">Отправить заявку</button>
   </form>
   ```

### Преимущества интеграции:
- ✅ **Единая система** для лидов с бота и сайта
- ✅ **Автоматическая отправка** в Telegram чат
- ✅ **Сохранение в Google Sheets** с пометкой источника
- ✅ **Безопасность** через секретный ключ
- ✅ **Простая интеграция** с любым сайтом

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

# Workgroup Chat Configuration (для пересылки лидов в чат рабочей группы)
WORKGROUP_CHAT_ID=chat_id_рабочей_группы

# Webhook Configuration (для интеграции с сайтом)
WEBHOOK_SECRET=ваш_секретный_ключ_для_вебхука
WEBHOOK_PORT=5000
```

### Настройка пересылки лидов в чат рабочей группы

1. **Добавьте бота в чат рабочей группы** и сделайте его администратором
2. **Получите Chat ID рабочей группы** одним из способов:
   - Отправьте сообщение в группу и перешлите его боту @userinfobot
   - Или используйте @RawDataBot для получения информации о чате
3. **Добавьте переменную в .env:**
   - `WORKGROUP_CHAT_ID` - ID чата рабочей группы (например: -1001234567890)

## 📊 Функциональность

- ✅ 7-шаговый опрос с прогресс-баром
- ✅ Автоматическое создание листов Google Sheets по месяцам
- ✅ **Пересылка лидов в чат рабочей группы**
- ✅ **Веб-хук для интеграции с сайтом** (новое!)
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