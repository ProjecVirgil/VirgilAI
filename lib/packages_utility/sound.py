"""File so manage the audio and the STT."""
import os

import gtts
from pygame.mixer import music
from elevenlabs import generate, save, api

from lib.packages_utility.logger import logging
from lib.packages_utility.utils import Utils

# ---- This file make the TTS ----
class Audio:
    """A class for manage the audio in Virgil."""

    def __init__(self, volume, elevenlabs, language):
        """Init the settings for the audio class.

        Args:
            volume (str): the volume of audio
            elevenlabs (str): the key of elevenlabs API
            language (str): the language of Virgil
        """
        self.volume = volume
        self.api_key = elevenlabs
        self.language = language
        self.utils = Utils()

        self.MAX = 1.0
        self.MIN = 0.1

    def change(self, command: str) -> str:
        """Change the volume of Virgil.

        Args:
            command (str): The input sentence

        Returns:
            str: Final message after change the volume
        """
        if self.utils.count_number(command) >= 1:
            def search_volume(command):
                return [x for x in command if x.isdigit()]
            self.volume = int(search_volume(command)[0])
        else:
            logging.error("Sorry there was an error request the command with an appropriate value"),
            self.create(file=True, namefile="ErrorValueVirgil")
            return "104"
        try:
            self.volume = int(self.volume) / 100
            if self.volume < self.MIN or self.volume > self.MAX:
                return "104"
            return str(self.volume)
        except ValueError:
            logging.error("Sorry there was an error request the command with an appropriate value"),
            self.create(file=True, namefile="ErrorValueVirgil")
            return "104"

    def create(self, text: str = "", file: bool = False, namefile: str = "") -> None:
        """Create a mp3 or wav file with text from tts.

        Args:
            text (str, optional): the text to transform in audio. Defaults to "".
            file (bool, optional): is a file? Defaults to False.
            namefile (str, optional): the file to play Defaults to "".
        """
        music.unload()
        if music.get_volume != float(self.volume):
            music.set_volume(float(self.volume))
            if file:
                logging.info(f"File reproduce: {namefile}")
                file = os.path.join(f"assets/audio/{self.language}/{namefile}.mp3")
                music.load(file)
                music.play()
                return
            try:
                sound = generate(
                    api_key=self.api_key,
                    text=text,
                    voice="Antoni",
                    model='eleven_multilingual_v1'
                )
                save(sound, 'audio.mp3')
            except api.error.APIError:
                logging.warning(
                    " Google text to speech has started the cause could be a missing valid key or the end of the elevenLabs plan if you are aware of this you can ignore the message")
                sound = gtts.gTTS(text, lang=self.language)
                sound.save("audio.mp3")

        file = os.path.join("audio.mp3")
        music.load(file)
        music.play()
