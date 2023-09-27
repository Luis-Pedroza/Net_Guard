# ***************************************************
# FILE: Configuration.py
#
# DESCRIPTION:
# The provided code defines several classes related to managing
# and retrieving data from a database, specifically for language
# and theme settings.
#
# AUTHOR:  Luis Pedroza
# CREATED: 22/09/2023 (dd/mm/yyyy)
# ******************* ********************************

from Database.Connection import DatabaseConnection, ErrorConnection


class DataManager():
    '''
    A base class for managing data retrieval and manipulation in the application's database.

    Attributes:
        database (DatabaseConnection): Manages the connection to the database.
        column (str): The database column to interact with.
        table (str): The database table to interact with.

    Methods:
        __init__(self, column: str, table: str)
            Initializes the DataManager class with the specified column and table.

        get_data(self) -> str
            Retrieves data from the specified column and table in the database.

        set_data(self, value: str)
            Sets data in the specified column and table in the database.

    '''
    def __init__(self, column: str, table: str) -> None:
        self.database = DatabaseConnection('Resources/app_data.db')
        self.column = column
        self.table = table

    def get_data(self) -> str:
        '''
        Retrieves data from the specified column and table in the database.

        Args:
            None

        Returns:
            str: The data retrieved from the database.

        Raises:
            ErrorDataManager: If there is an issue with the data retrieval.

        Example Usage:
            data_manager = DataManager('Language', 'Languages')
            language = data_manager.get_data()

        '''
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
        '''
        Sets data in the specified column and table in the database.

        Args:
            value (str): The data value to be set in the database.

        Returns:
            None

        Raises:
            ErrorDataManager: If there is an issue with setting the data.

        Example Usage:
            data_manager = DataManager('Language', 'Languages')
            data_manager.set_data('en')

        '''
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
    '''
    A class for managing language-related data in the application's database.

    Inherits from DataManager.

    Methods:
        __init__(self)
            Initializes the LanguageManager class with the appropriate column and table.

        get_language(self) -> str
            Retrieves the selected language from the database.

        set_language(self, language: str)
            Sets the selected language in the database.

    '''
    def __init__(self) -> None:
        super().__init__('Language', 'Languages')

    def get_language(self) -> str:
        '''
        Retrieves the selected language from the database.

        Args:
            None

        Returns:
            str: The selected language.

        Raises:
            ErrorDataManager: If there is an issue with data retrieval.

        Example Usage:
            language_manager = LanguageManager()
            language = language_manager.get_language()

        '''
        try:
            return self.get_data()
        except ErrorDataManager as exception:
            raise ErrorDataManager('ERROR_LanguageManager_GET', str(exception))

    def set_language(self, language: str):
        '''
        Sets the selected language in the database.

        Args:
            language (str): The language code to set.

        Returns:
            None

        Raises:
            ErrorDataManager: If there is an issue with setting the language.

        Example Usage:
            language_manager = LanguageManager()
            language_manager.set_language('en')

        '''
        try:
            self.set_data(language)
        except ErrorDataManager as exception:
            raise ErrorDataManager('ERROR_LanguageManager_SET', str(exception))


class ThemeManager(DataManager):
    '''
    A class for managing theme-related data in the application's database.

    Inherits from DataManager.

    Methods:
        __init__(self)
            Initializes the ThemeManager class with the appropriate column and table.

        get_theme(self) -> str
            Retrieves the selected theme from the database.

        set_theme(self, theme: str)
            Sets the selected theme in the database.

    '''
    def __init__(self) -> None:
        super().__init__('Theme', 'Themes')

    def get_theme(self) -> str:
        '''
        Retrieves the selected theme from the database.

        Args:
            None

        Returns:
            str: The selected theme.

        Raises:
            ErrorDataManager: If there is an issue with data retrieval.

        Example Usage:
            theme_manager = ThemeManager()
            theme = theme_manager.get_theme()

        '''
        try:
            return self.get_data()
        except ErrorDataManager as exception:
            raise ErrorDataManager('ERROR_LanguageManager_GET', str(exception))

    def set_theme(self, theme: str):
        '''
        Sets the selected theme in the database.

        Args:
            theme (str): The theme name to set.

        Returns:
            None

        Raises:
            ErrorDataManager: If there is an issue with setting the theme.

        Example Usage:
            theme_manager = ThemeManager()
            theme_manager.set_theme('DarkTheme')

        '''
        try:
            self.set_data(theme)
        except ErrorDataManager as exception:
            raise ErrorDataManager('ERROR_LanguageManager_SET', str(exception))


class ErrorDataManager(Exception):
    def __init__(self, error_code, error_description):
        super().__init__(error_description)
        self.error_code = error_code
