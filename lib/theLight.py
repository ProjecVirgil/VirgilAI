import os
import json
import asyncio

from meross_iot.http_api import MerossHttpClient
from meross_iot.manager import MerossManager

from lib.logger import Logger

# ---- This file controll the domotic meross ----


#TODO DA RIVEDERE
current_path = os.getcwd()
file_path = os.path.join(current_path,'setting.json')
#Open file whith key api openai

with open(file_path) as f:
    secrets = json.load(f)
    EMAIL = secrets["merrosEmail"]
    PASSWORD = secrets["merrosPassword"]

logger = Logger()

async def main(status:bool):
    print(logger.Log(" Funzione di turn main"))
    # Setup the HTTP client API from user-password
    http_api_client = await MerossHttpClient.async_from_user_password(email=EMAIL, password=PASSWORD)

    # Setup and start the device manager
    manager = MerossManager(http_client=http_api_client)
    await manager.async_init()

    # Retrieve all the MSS310 devices that are registered on this account
    await manager.async_device_discovery()
    plugs = manager.find_devices(device_type="mss310h")

    if len(plugs) < 1:
        print("No MSS310 plugs found...")
    else:
        # Turn it on channel 0
        # Note that channel argument is optional for MSS310 as they only have one channel
        dev = plugs[0]

        # The first time we play with a device, we must update its status
        await dev.async_update()


        # We can now start playing with that
        if(status):
            print(f"Turning on {dev.name}...")
            await dev.async_turn_on(channel=0)
        else:
            print(f"Turing off {dev.name}")
            await dev.async_turn_off(channel=0)
        
    # Close the manager and logout from http_api
    manager.close()
    await http_api_client.async_logout()

    
def turn(command:str):
    print(logger.Log(" Funzione di turn"))
    
    if("accendi" in command):
        status = True
    elif("spegni" in command):
        status = False
    else:
        print(logger.Log(" Comando non trovato"))
        status =  None
        
    # Create and run a new event loop for this turn() call
    print(logger.Log(" Creazione chiamata"))
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(main(status))
    finally:
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()
