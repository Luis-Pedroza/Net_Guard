from Database.Connection import DatabaseConnection, ErrorConnection


class LanguageManager():
    '''
    A class for managing language settings and interactions with the database.

    Attributes:
        database (DatabaseConnection): Manages the connection to the database.

    Methods:
        __init__(self)
            Initializes the LanguageManager class. It sets up the database connection.

        get_language(self) -> str
            Retrieves the currently selected language from the database.

        set_language(self, language: str)
            Sets the selected language in the database.

    '''
    def __init__(self) -> None:
        self.database = DatabaseConnection('Resources/app_data.db')

    def get_language(self) -> str:
        '''
        Retrieves the currently selected language from the database.

        Args:
            None

        Returns:
            str: The currently selected language.

        Raises:
            Exception: If there is an issue with the database query.

        Example Usage:
            lang_manager = LanguageManager()
            current_language = lang_manager.get_language()

        '''
        try:
            query = 'SELECT Language FROM Languages WHERE Election = 1'
            self.database.connect()
            language = self.database.query(query)
            self.database.disconnect()
            return language[0][0]
        except ErrorConnection as exception:
            error_code = exception.error_code
            error_description = str(exception)
            raise ErrorLanguage(error_code, error_description)
        except Exception as exception:
            raise ErrorLanguage('ERROR_LanguageManager_GET', str(exception))

    def set_language(self, language: str):
        '''
        Sets the selected language in the database.

        Args:
            language (str): The language to set.

        Returns:
            None

        Raises:
            Exception: If there is an issue with the database query.

        Example Usage:
            lang_manager = LanguageManager()
            lang_manager.set_language('en')

        '''
        try:
            query1 = 'UPDATE Languages SET Election = 1 WHERE Language = ? AND Election = 0'
            query2 = 'UPDATE Languages SET Election = 0 WHERE Language != ? AND Election = 1'
            params = (language,)
            self.database.connect()
            self.database.query(query1, params)
            self.database.query(query2, params)
            self.database.disconnect()
        except ErrorConnection as exception:
            error_code = exception.error_code
            error_description = str(exception)
            raise ErrorLanguage(error_code, error_description)
        except Exception as exception:
            raise ErrorLanguage('ERROR_LanguageManager_SET', str(exception))


class ThemeManager():
    '''
    A class for managing language settings and interactions with the database.

    Attributes:
        database (DatabaseConnection): Manages the connection to the database.

    Methods:
        __init__(self)
            Initializes the LanguageManager class. It sets up the database connection.

        get_language(self) -> str
            Retrieves the currently selected language from the database.

        set_language(self, language: str)
            Sets the selected language in the database.

    '''
    def __init__(self) -> None:
        self.database = DatabaseConnection('Resources/app_data.db')

    def get_theme(self) -> str:
        '''
        Retrieves the currently selected language from the database.

        Args:
            None

        Returns:
            str: The currently selected language.

        Raises:
            Exception: If there is an issue with the database query.

        Example Usage:
            lang_manager = ThemeManager()
            current_language = lang_manager.get_language()

        '''
        try:
            query = 'SELECT Theme FROM Themes WHERE Election = 1'
            self.database.connect()
            language = self.database.query(query)
            self.database.disconnect()
            return language[0][0]
        except ErrorConnection as exception:
            error_code = exception.error_code
            error_description = str(exception)
            raise ErrorLanguage(error_code, error_description)
        except Exception as exception:
            raise ErrorLanguage('ERROR_ThemeManager_GET', str(exception))

    def set_theme(self, theme: str):
        '''
        Sets the selected language in the database.

        Args:
            language (str): The language to set.

        Returns:
            None

        Raises:
            Exception: If there is an issue with the database query.

        Example Usage:
            lang_manager = ThemeManager()
            lang_manager.set_language('en')

        '''
        try:
            query1 = 'UPDATE Themes SET Election = 1 WHERE Theme = ? AND Election = 0'
            query2 = 'UPDATE Themes SET Election = 0 WHERE Theme != ? AND Election = 1'
            params = (theme,)
            self.database.connect()
            self.database.query(query1, params)
            self.database.query(query2, params)
            self.database.disconnect()
        except ErrorConnection as exception:
            error_code = exception.error_code
            error_description = str(exception)
            raise ErrorLanguage(error_code, error_description)
        except Exception as exception:
            raise ErrorLanguage('ERROR_ThemeManager_SET', str(exception))


class ErrorLanguage(Exception):
    def __init__(self, error_code, error_description):
        super().__init__(error_description)
        self.error_code = error_code