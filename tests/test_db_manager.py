#TEST
from lib.packages_utility.db_manager import DBManager
from lib.packages_utility.utils import init_settings

import lib.packages_utility.logger  # noqa: F401
import logging

import secrets
dict = {
    "language": "it",
    "wordActivation": "Virgilio",
    "volume": "100.0",
    "city": "Salerno",
    "operation_timeout": "2",
    "dynamic_energy_threshold": "false",
    "energy_threshold": "18",
    "merrosEmail": "email",
    "merrosPassword": "password",
    "temperature": "0.9",
    "max_tokens": "1000",
    "gpt-version": "gpt-3.5-turbo-0613"
}
settings = init_settings(dict)
key = secrets.token_hex(20)
manager = DBManager()
manager.init()
key_id = manager.create_update_user(key,settings=settings)
settings = manager.get_user_settings()
print(settings)
key = manager.get_key()
print(key)
status = manager.get_reminder()
print(type(status))
manager.set_reminder(value=0)
