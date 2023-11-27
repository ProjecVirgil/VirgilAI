"""File for the configuration of the other classes."""
from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class Settings:
    """Settings dataclass for the application.

    This is a singleton object that holds all of our
    settings and can be accessed anywhere in the app through this single instance.
    """
    # ******************** Setting ********************
    language: str
    word_activation: str
    volume: str
    city: str
    operation_timeout: str
    dynamic_energy_threshold: str
    energy_threshold: str
    elevenlabs: str
    openai: str
    merros_email: str
    merros_password: str
    gpt_version:str
    temperature: str
    max_tokens: str

    # ******************** Script language ********************
    # ----- Calendar -----
    phrase_calendar: str
    split_calendar: str
    months_calendar: str
    week_calendar: str
    words_meaning_tomorrow: str
    words_meaning_after_tomorrow: str
    words_meaning_yesterday: str
    words_meaning_today: str
    # ----- Choose command -----
    split_command: str
    # ----- Time -----
    phrase_time: str
    split_time: str
    # ----- Process -----
    prompt: str
    # ----- Events -----
    phrase_events: str
    # ----- Outputs -----
    phrase_output: str
    split_output: str
    # ----- News -----
    synonyms_news: str
    # ----- Wheather -----
    phrase_wheather: str
    split_wheather: str
    wwc_wheather: str
    word_meaning_tomorrow_wheather: str
    # ----- MediaPlayer -----
    synonyms_mediaplayer: str
