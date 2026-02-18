from app.database.database_manager import DatabaseManager
from enum import Enum

db = DatabaseManager()

class TableStatus(Enum):
    AVAILABLE = "available"
    OCCUPIED = "occupied"

class Table():
    '''
    Docstring for Table
    '''
    def __init__(self, id: int, table_number: int, status: TableStatus):
        self.id = id
        self.table_number = table_number
        self.status = TableStatus(status)

    def save(self):
        query = "UPDATE tables SET status = %s WHERE id = %s"
        result, text = db.query_tool(query, params=(self.status.value, self.id))
        return result, text
