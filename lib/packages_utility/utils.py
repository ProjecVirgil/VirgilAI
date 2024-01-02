"""File with some utils function."""
# ruff: noqa
import json
import re
from math import sin, cos, sqrt, atan2, radians

from geopy.geocoders import Nominatim
from lib import Settings


# ---- This file convert all the number in word ----

# Because the ElevenLabs TTS read the number only in english

class Utils:
    """A class with utils function."""

    def __init__(self) -> None:
        """Init the logger class."""

    def count_number(self, command) -> int:
        """Count how many numbers are there in a string.

        Args:
            command (str): input sentence

        Returns:
            int: The number of numbers in the input sentence
        """
        if not isinstance(command, str):
            command = " ".join(command)
        number_find = re.findall(r'\d+', command)
        return len(number_find)

    def get_coordinates(self, city_name: str) -> tuple:
        """Get coordinates from city name.

        Args:
            city_name (str): _description_

        Returns:
            tuple: The lat and long of a city
        """
        geolocator = Nominatim(user_agent="VirgilAI")
        location = geolocator.geocode(city_name)

        if location:
            return location.latitude, location.longitude

        return None, None

    def haversine_distance(self, coord1: tuple, coord2: tuple) -> float:
        """Haversine distance between two points on earth.

        Args:
            coord1 (tuple): Cordinate of first point (lat and lon)
            coord2 (tuple): Cordinate of second point (lat and lon)

        Returns:
            float: distance
        """
        radius_earth = 6371  # Radius of Earth in kilometers
        lat1, lon1 = coord1
        lat2, lon2 = coord2

        # Conversion to radians
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

        # Haversine formula
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        distance = radius_earth * c

        return distance

    def number_to_word(self, number) -> str:
        """Convert a number into words.

        Args:
            number (_type_): the number to convert

        Returns:
            str: the number converted in word
        """
        number = int(number)
        words_up_to_vents = [
            "zero", "uno", "due", "tre", "quattro", "cinque", "sei", "sette",
            "otto", "nove", "dieci", "undici", "dodici", "tredici", "quattordici",
            "quindici", "sedici", "diciassette", "diciotto", "diciannove", "venti"
        ]

        word_dozens = [
            "", "", "venti", "trenta", "quaranta", "cinquanta",
            "sessanta", "settanta", "ottanta", "novanta"
        ]

        word_hundreds = [
            "", "cento", "duecento", "trecento", "quattrocento",
            "cinquecento", "seicento", "settecento", "ottocento", "novecento"
        ]

        def convert_under_1000(number):
            """Convert under 1000.

            Args:
                number (int): The number under 1000

            Returns:
                str: the number under 1000 converted
            """
            if 0 <= number <= 999:
                if number < 21:
                    return words_up_to_vents[number]
                if number < 100:
                    dozen = number // 10
                    unit = number % 10
                    if unit in (1, 8):
                        word_dozen = word_dozens[dozen][:-1]
                    else:
                        word_dozen = word_dozens[dozen]
                    if dozen == 1 and unit == 0:
                        return "dieci"
                    if dozen == 8 and unit == 0:
                        return "ottanta"
                    return word_dozen + words_up_to_vents[unit]

                hundred = number // 100
                remainder = number % 100
                if remainder == 0:
                    return word_hundreds[hundred]
                return word_hundreds[hundred] + convert_under_1000(remainder)

        if 0 <= number <= 9999:
            if number < 1000:
                return convert_under_1000(number)

            thousands = number // 1000
            remainder = number % 1000
            result = ""
            if thousands == 1:
                result += "mille"
            else:
                result += words_up_to_vents[thousands] + "mila"
            if remainder > 0:
                if remainder < 100:
                    result += "e"
                result += convert_under_1000(remainder)
            return result
        return "Unmanaged number"


def init_settings(settings_json,user_key) -> Settings:
    """Initialize settings for all the modules.

    Returns:
        Settings: Dataclasses
    """
    language = settings_json["language"]
    prompt= '''
You are a virtual assistant who speaks only {language}, writes numbers in letters and is called Virgil. You are able to do exactly these things:
- Create a timer
- Tell the time right now
- Know the latest news
- Change the audio volume
- The outside temperature
- Interact with home automation
- Know what time it is
- Remember my schedule
- Play music from YouTube
- And you can do many other things, such as create an exercise plan, a diet and anything else a user may ask.
 When they ask you what you can do, explain these points with examples:
- Virgil sets a 10-minute timer
- Virgil What's the weather like today?
- Virgil sets the volume to 10%
- Virgil tells me the latest news
- Virgil what's the temperature?

 If I ask you questions related to any of the above commands and you can't answer me, tell me to try pronouncing the command and use the examples I listed above.
- Ready to pretend to be Virgil? Answer yes if you understand, and from now on when I ask you a question, answer me as if I were a virtual assistant.

TOOLS:
------

Assistant has access to the following tools:

> Wikipedia: A wrapper around Wikipedia. Useful for when you need to answer general questions about people, places, companies, facts, historical events, or other subjects. Input should be a search query.

To use a tool, please use the following format:

```
Thought: Do I need to use a tool? Yes
Action: the action to take, should be one of [Wikipedia]
Action Input: the input to the action
Observation: the result of the action
```

When you have a response to say to the Human, or if you do not need to use a tool, you MUST use the format:

```
Thought: Do I need to use a tool? No
AI: [your response here]
```

Begin!

Previous conversation history:
{chat_history}

New input: {input}
{agent_scratchpad}
'''
    
    with open(f'lang/{language}/{language}.json', encoding="utf8") as file_scripts:
            # INIT FILE
            script = json.load(file_scripts)
            script_calendar = script["calendar"]
            script_command = script["command"]
            script_time = script["time"]
            script_events = script["events"]
            script_output = script["outputs"]
            script_news = script["news"]
            script_weather = script["weather"]
            script_mediaplayer = script["mediaplayer"]
            return Settings(
                key_user=user_key,
                language=language,
                word_activation=settings_json["wordActivation"].lower(),
                volume=settings_json["volume"],
                city=settings_json["city"],
                operation_timeout=settings_json["operation_timeout"],
                dynamic_energy_threshold=settings_json["dynamic_energy_threshold"],
                energy_threshold=settings_json["energy_threshold"],
                elevenlabs=settings_json["elevenlabs"],
                openai=settings_json["openAI"],
                merros_email=settings_json["merrosEmail"],
                merros_password=settings_json["merrosPassword"],
                temperature=settings_json["temperature"],
                gpt_version= settings_json["gpt-version"],
                max_tokens=settings_json["max_tokens"],
                phrase_calendar=script_calendar["phrase"],
                split_calendar=script_calendar["split"],
                months_calendar=script_calendar["month"],
                week_calendar=script_calendar["week"],
                words_meaning_tomorrow=script_calendar["words_meaning_tomorrow"],
                words_meaning_after_tomorrow=script_calendar["words_meaning_after_tomorrow"],
                words_meaning_yesterday=script_calendar["words_meaning_yesterday"],
                words_meaning_today=script_calendar["words_meaning_today"],
                split_command=script_command["split"],
                phrase_time=script_time["phrase"],
                split_time=script_time["split"],
                phrase_events=script_events["phrase"],
                phrase_output=script_output["phrase"],
                split_output=script_output["split"],
                prompt=prompt,
                synonyms_news=script_news["synonyms"],
                phrase_weather=script_weather["phrase"],
                split_weather=script_weather["split"],
                wwc_weather=script_weather["WWC"],
                word_meaning_tomorrow_weather=script_weather["word_meaning_tomorrow"],
                synonyms_mediaplayer=script_mediaplayer["synonyms"]
            )
