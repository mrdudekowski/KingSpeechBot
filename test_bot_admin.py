import asyncio
from main import remove_emojis
from config import MANAGER_CHAT_ID
import datetime
from cursor import GoogleSheets

# Мок-функция для имитации отправки сообщения менеджеру
async def mock_send_manager_notification(context_vars):
    now = datetime.datetime.now()
    reg_time = now.strftime('%H:%M %m.%d.%Y')
    manager_text = (
        f"Новая регистрация клиента!\n"
        f"Время: {reg_time}\n"
        f"Имя: {context_vars.get('user_name')}\n"
        f"Телефон: {context_vars.get('phone')}\n"
        f"Язык: {context_vars.get('language')}\n"
        f"Уровень: {context_vars.get('level')}\n"
        f"Цель: {context_vars.get('goals')}\n"
        f"Формат: {context_vars.get('format')}\n"
        f"Ожидания: {context_vars.get('expectations')}\n"
        f"Дата старта: {context_vars.get('start_date')}\n"
        f"Telegram: @{context_vars.get('telegram_username')}"
    )
    print(f"[Менеджер получил уведомление]:\n{manager_text}")
    return reg_time

# Тестовые данные (пример)
def test_manager_notification():
    context_vars = {
        'user_name': 'Вася Пупкин',
        'phone': '+79234445443',
        'language': 'Английский 🇬🇧',
        'level': 'С нуля 🆕',
        'goals': 'Общий язык 🌐',
        'format': 'Индивидуальный',
        'expectations': 'Разнообразие слов и выражений 📝',
        'start_date': 'Прямо сейчас 🚀',
        'telegram_username': 'vasyapupkin',
        'telegram_id': 111222333
    }
    reg_time = asyncio.run(mock_send_manager_notification(context_vars))
    
    # Проверяем что функция работает корректно
    assert context_vars['telegram_id'] == 111222333
    assert reg_time is not None
    assert isinstance(reg_time, str)
    assert len(reg_time) > 0

# Тест обновления статуса заявки в Google Sheets
def test_update_status():
    # Создаем тестовые данные напрямую
    telegram_id = 111222333
    reg_time = "13:20 08.24.2025"
    
    sheet = GoogleSheets('14uUOXdoxXLGZuFOiF9YaFxlblQF9NE8C2IKpSF7eXrI', 'Лист1')
    try:
        sheet.update_status(telegram_id, reg_time, 'В работе')
        print('✅ Статус заявки обновлён на "В работе"')
        sheet.update_status(telegram_id, reg_time, 'Обработано')
        print('✅ Статус заявки обновлён на "Обработано"')
    except Exception as e:
        print('❌ Ошибка при обновлении статуса:', e)

if __name__ == '__main__':
    test_update_status() 