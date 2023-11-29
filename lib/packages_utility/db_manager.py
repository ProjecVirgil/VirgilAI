import sqlite3


class DBManager:
    """A class for manage the interaction with db."""
    def __init__(self, settings=None) -> None:
        """Initializes the database connection."""
        self.connection = sqlite3.connect('settings.db')
        self.cursor = self.connection.cursor()

    def init(self):
        """Create the database and tables."""
        CT_TABLE_SETTINGS = '''
CREATE TABLE IF NOT EXISTS settings (
    keys_id INTEGER PRIMARY KEY,
    language TEXT,
    wordActivation TEXT,
    volume INTEGER,
    city TEXT,
    operation_timeout INTEGER,
    dynamic_energy_threshold BOOLEAN,
    energy_threshold INTEGER,
    elevenlabs TEXT,
    openAI TEXT,
    merrosEmail TEXT,
    merrosPassword TEXT,
    gpt_version TEXT,
    temperature REAL,
    max_tokens INTEGER,
    created_at TIMESTAMP,
    FOREIGN KEY (keys_id) REFERENCES keys(id)
);
'''
        CT_TABLE_KEYS = '''
    CREATE TABLE IF NOT EXISTS keys (
        id INTEGER PRIMARY KEY,
        key TEXT,
        created_at TIMESTAMP
    );
    '''
        CT_TABLE_REMINDER = '''
    CREATE TABLE IF NOT EXISTS reminder (
        remembered BOOLEAN
    );
    '''
        self.cursor.execute(CT_TABLE_KEYS)
        self.cursor.execute(CT_TABLE_SETTINGS)
        self.cursor.execute(CT_TABLE_REMINDER)

#TEST
manager = DBManager()
manager.init()
