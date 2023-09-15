from Database.Connection import DatabaseConnection


class LanguageManager():
    def __init__(self) -> None:
        self.database = DatabaseConnection('Resources/app_data.db')

    def get_language(self):
        query = 'SELECT Language FROM Languages WHERE Election = 1'
        self.database.connect()
        language = self.database.query(query)
        self.database.disconnect()
        return language[0][0]
    
    def set_language(self, language: str):
        query1 = 'UPDATE Languages SET Election = 1 WHERE Language = ? AND Election = 0'
        query2 = 'UPDATE Languages SET Election = 0 WHERE Language != ? AND Election = 1'
        params = (language,)
        self.database.connect()
        self.database.query(query1, params)
        self.database.query(query2, params)
        self.database.disconnect()