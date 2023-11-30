"""Now Virgil support only one key and the db manager is project for manage only one key.

Returns:
     _type_: _description_
"""
from datetime import datetime
import sqlite3
import logging
from lib import Settings

import lib.packages_utility.logger  # noqa: F401
import contextlib

class DBManager:
    """A class for manage the interaction with db."""
    def __init__(self) -> None:
        """Initializes the database connection."""
        self.connection = sqlite3.connect('settings.db')
        self.cursor = self.connection.cursor()
    def init(self):
        """Create the database and tables."""
        ct_table_settings = '''
CREATE TABLE IF NOT EXISTS settings (
    keys_id INTEGER PRIMARY KEY CHECK (keys_id = 1),
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
    last_access TIMESTAMP,
    FOREIGN KEY (keys_id) REFERENCES keys(id)
);
'''
        ct_table_keys = '''
    CREATE TABLE IF NOT EXISTS keys (
        id INTEGER PRIMARY KEY CHECK (id = 1),
        key TEXT UNIQUE,
        last_access TIMESTAMP
    );
    '''
        ct_table_reminder = '''
    CREATE TABLE IF NOT EXISTS reminder (
        id INTEGER PRIMARY KEY CHECK (id = 1),
        remembered BOOLEAN UNIQUE
    );
    '''
        self.cursor.execute(ct_table_keys)
        self.cursor.execute(ct_table_settings)

        self.cursor.execute(ct_table_reminder)
        with contextlib.suppress(sqlite3.IntegrityError):
            self.cursor.execute('INSERT INTO reminder(remembered) VALUES (?)',(0,))
        self.connection.commit()


    def create_update_user(self,key:str,settings:Settings) -> int:
        """Insert a new user in the tables.

        Args:
            key (_type_): _description_
            settings (_type_): _description_
        """
        current_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        query = '''
        INSERT INTO keys (key, last_access) VALUES(?, ?)
        ON CONFLICT(key) DO UPDATE SET last_access = excluded.last_access;
        '''
        key_id  = 1
        try:
            self.cursor.execute(query, (key, current_timestamp))
            key_id = self.cursor.lastrowid
            self.connection.commit()
        except sqlite3.IntegrityError:
            pass

        query = '''
        INSERT INTO settings (
            keys_id,
            language,
            wordActivation,
            volume,
            city,
            operation_timeout,
            dynamic_energy_threshold,
            energy_threshold,
            elevenlabs,
            openAI,
            merrosEmail,
            merrosPassword,
            gpt_version,
            temperature,
            max_tokens,
            last_access
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(keys_id) DO UPDATE SET
            language = excluded.language,
            wordActivation = excluded.wordActivation,
            volume = excluded.volume,
            city = excluded.city,
            operation_timeout = excluded.operation_timeout,
            dynamic_energy_threshold = excluded.dynamic_energy_threshold,
            energy_threshold = excluded.energy_threshold,
            elevenlabs = excluded.elevenlabs,
            openAI = excluded.openAI,
            merrosEmail = excluded.merrosEmail,
            merrosPassword = excluded.merrosPassword,
            gpt_version = excluded.gpt_version,
            temperature = excluded.temperature,
            max_tokens = excluded.max_tokens,
            last_access = excluded.last_access;
        '''
        self.cursor.execute(query, (1, settings.language, settings.word_activation, settings.volume, settings.city, settings.operation_timeout, settings.dynamic_energy_threshold, settings.energy_threshold, settings.elevenlabs, settings.openai, settings.merros_email, settings.merros_password, settings.gpt_version, settings.temperature, settings.max_tokens, current_timestamp))
        self.connection.commit()
        return key_id

    def get_user_settings(self, key: int = 1):
        """Get user data from the database.

        Args:
            key (int): For now are every 1
        """
        try:
            query = '''SELECT * FROM settings WHERE keys_id = ?'''
            self.cursor.execute(query, (key,))
            settings_row = self.cursor.fetchone()
            if settings_row:
                column_names = ["keys_id", "language", "wordActivation", "volume", "city", "operation_timeout", "dynamic_energy_threshold", "energy_threshold", "elevenlabs", "openAI", "merrosEmail", "merrosPassword", "gpt_version", "temperature", "max_tokens", "created_at"]
                settings_dict = dict(zip(column_names, settings_row))
                return settings_dict
        except sqlite3.Error as e:
            logging.error(f"Error during the get of the settings: {e}")

    def get_key(self,id:int = 1):
        """Get a specific key from the database.

        Args:
            id (int, optional): _description_. Defaults to 1.

        Returns:
            _type_: _description_
        """
        try:
            query =''' SELECT * FROM keys WHERE id = ?'''
            self.cursor.execute(query,(id,))
            key_row = self.cursor.fetchone()
            if key_row:
                return key_row[1]
        except sqlite3.Error as e:
            logging.error(f"Error during the get of key: {e}")

    def get_reminder(self,id = 1):
        """Get reminders for the client.

        Args:
            id (int, optional): _description_. Defaults to 1.

        Returns:
            _type_: _description_
        """
        try:
            query =''' SELECT * FROM reminder WHERE rowid  = ?'''
            self.cursor.execute(query,(id,))
            status = self.cursor.fetchone()
        except sqlite3.Error as e:
            logging.error(f"Error during the get of reminder: {e}")
        if status:
            return status[1]

    def set_reminder(self, id:int = 1,value:int = 0):
        """Update the 'remembered' value in the reminder table for id 1.

        Args:
            id (bool): The new value to set for 'remembered'.
            value (int): The value to modify
        """
        try:
            query = "UPDATE reminder SET remembered = ? WHERE id = ?"
            self.cursor.execute(query, (value,id))
            self.connection.commit()
        except sqlite3.Error as e:
            logging.error(f"Error during the update of reminder: {e}")
