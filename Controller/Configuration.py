from Database.Connection import DatabaseConnection, ErrorConnection

class DataManager():
    def __init__(self, column: str, table: str) -> None:
        self.database = DatabaseConnection('Resources/app_data.db')
        self.column = column
        self.table = table
    
    def get_data(self) -> str:
        try:
            query = f'SELECT {self.column} FROM {self.table} WHERE Election = 1'
            self.database.connect()
            result = self.database.query(query)
            self.database.disconnect()
            return result[0][0]
        except ErrorConnection as exception:
            error_code = exception.error_code
            error_description = str(exception)
            raise ErrorDataManager(error_code, error_description)
        except Exception as exception:
            raise ErrorDataManager('ERROR_DataManager_GET', str(exception))
        
    def set_data(self, value: str):
        try:
            query1 = f'UPDATE {self.table} SET Election = 1 WHERE {self.column} = ? AND Election = 0'
            query2 = f'UPDATE {self.table} SET Election = 0 WHERE {self.column} != ? AND Election = 1'
            params = (value,)
            self.database.connect()
            self.database.query(query1, params)
            self.database.query(query2, params)
            self.database.disconnect()
        except ErrorConnection as exception:
            error_code = exception.error_code
            error_description = str(exception)
            raise ErrorDataManager(error_code, error_description)
        except Exception as exception:
            raise ErrorDataManager('ERROR_DataManager_SET', str(exception))

class LanguageManager(DataManager):
    def __init__(self) -> None:
        super().__init__('Language', 'Languages')

    def get_language(self) -> str:
        try:
            return self.get_data()
        except ErrorDataManager as exception:
            raise ErrorDataManager('ERROR_LanguageManager_GET', str(exception))

    def set_language(self, language: str):
        try:
            self.set_data(language)
        except ErrorDataManager as exception:
            raise ErrorDataManager('ERROR_LanguageManager_SET', str(exception))


class ThemeManager(DataManager):
    def __init__(self) -> None:
        super().__init__('Theme', 'Themes')

    def get_theme(self) -> str:
        try:
            return self.get_data()
        except ErrorDataManager as exception:
            raise ErrorDataManager('ERROR_LanguageManager_GET', str(exception))

    def set_theme(self, theme: str):
        try:
            self.set_data(theme)
        except ErrorDataManager as exception:
            raise ErrorDataManager('ERROR_LanguageManager_SET', str(exception))


class ErrorDataManager(Exception):
    def __init__(self, error_code, error_description):
        super().__init__(error_description)
        self.error_code = error_code