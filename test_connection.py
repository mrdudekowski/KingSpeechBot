from google.oauth2 import service_account
from googleapiclient.discovery import build

# Если вы изменяете эти области, удалите файл token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

def main():
    try:
        # Создаем учетные данные из Service Account
        creds = service_account.Credentials.from_service_account_file(
            'service-account.json',  # Имя файла с ключом Service Account
            scopes=SCOPES
        )

        # Создаем сервис
        service = build('sheets', 'v4', credentials=creds)
        print("Успешно подключено к Google Sheets API!")
        
        # ID таблицы
        SPREADSHEET_ID = '14uUOXdoxXLGZuFOiF9YaFxlblQF9NE8C2IKpSF7eXrI'
        
        # Пробуем получить данные
        result = service.spreadsheets().values().get(
            spreadsheetId=SPREADSHEET_ID,
            range='Лист1!A1:A1'
        ).execute()
        
        print("Успешно получены данные из таблицы!")
        print("Результат:", result)
        
    except Exception as e:
        print("Произошла ошибка:", str(e))

if __name__ == '__main__':
    main() 