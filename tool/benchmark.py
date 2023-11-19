"""Tool for measuring the resource utilization of a software program."""
import colorama
import psutil
import argparse
import time
import sys
from colorama import Fore, Style

result = {
    "max_mem_percent":0,
    "max_mem_mb":0,
    "max_cpu":0,
    "average_cpu" : [],
    "average_mem_percent" : [],
    "average_mem_mb" : [],
}

time_start = 0
time_end = 0

BANNER = Fore.CYAN + '''
______                     _     ___  ___              _
| ___ \                   | |    |  \/  |             | |
| |_/ /  ___  _ __    ___ | |__  | .  . |  __ _  _ __ | | __
| ___ \ / _ \| '_ \  / __|| '_ \ | |\/| | / _` || '__|| |/ /
| |_/ /|  __/| | | || (__ | | | || |  | || (_| || |   |   < 
\____/  \___||_| |_| \___||_| |_|\_|  |_/ \__,_||_|   |_|\_\

'''

def show_result(pid):
    """Show result in console."""
    print(f'''

---- [FINAL RESULS] ----

Pid: {pid}

Max cpu used: {result["max_cpu"]:.2f}%
Max ram used: {result["max_mem_percent"]:.2f}%
Max ram used: {int(result["max_mem_mb"])}mb

Average cpu used: {(sum(result["average_cpu"]) / len(result["average_cpu"])):.2f}%
Average ram used: {(sum(result["average_mem_percent"]) / len(result["average_mem_percent"])):.2f}%
Average ram used: {int(sum(result["average_mem_mb"]) / len(result["average_mem_mb"]))}MB

Benchmark duration: {formated_time(time_end - time_start)}.
''')

def formated_time(seconds:float) -> str:
    """Formats seconds into hh:mm:ss format.

    Args:
        seconds (float): The seconds of execution

    Returns:
        str: _description_
    """
    MAX = 60  # noqa: N806
    if seconds > MAX:
        minuts = seconds / 60
        if minuts > MAX:
            hours = minuts / 60
            return f'{int(hours)}h {int(minuts - (MAX * int(hours)))}m and {int(seconds - (MAX * int(minuts)))}s'
        else:
            return f'{int(minuts)}m and {int(seconds - (MAX * int(minuts)))}s'
    else:
        return f'{int(seconds)}s'

def get_bar(value_percent:int,bars:int):
    """Get bar for progress bar.

    Args:
        value_percent (int): _description_
        bars (int): _description_
    """
    value_bar  = '█' * int(value_percent * bars) + '-' * (bars - int(value_percent * bars))
    return value_bar

def update_max(key: str, value: float) -> None:
    """Aggiorna i valori nel dizionario 'result'."""
    if(result[key] < value):
        result[key] = value
def update_average(key:str,value:float) -> None:
    """Aggiorna la media dei valori del dizionario 'result'."""
    support = result[key]
    support.append(value)
    result[key] = support

def get_color(value):
    """Get color based on the value.

    Args:
        value (_type_): _description_

    Returns:
        _type_: _description_
    """
    medium = 40
    high = 80

    if value > medium:
        return Style.BRIGHT + Fore.YELLOW
    elif value > high:
        return  Style.BRIGHT + Fore.RED
    else:
        return Style.BRIGHT + Fore.GREEN


def display_usage(cpu_usage:int,mem_usage_percent:int,mem_usage_mb:int,bars = 50) -> None:
    """Display the usage of CPU and memory of a precis process.

    Args:
        cpu_usage (int): Percent of CPU usage
        mem_usage_percent (int): Percent of memory
        mem_usage_mb (int): Number of memory in MB
        bars (int, optional): The number of bars MAX. Defaults to 50.
    """
    cpu_percent = (cpu_usage / 100.0)
    mem_percent = (mem_usage_percent / 100.0)

    update_max("max_cpu",cpu_percent)
    update_max("max_mem_mb",mem_usage_mb)
    update_max("max_mem_percent",mem_percent)

    update_average("average_cpu",cpu_percent)
    update_average("average_mem_mb",mem_usage_mb - 60)
    update_average("average_mem_percent",mem_percent)

    color_cpu = get_color(cpu_percent)
    color_mem = get_color(mem_percent)

    print(Style.BRIGHT + Fore.WHITE + "\rCPU Usage:" + color_cpu + f" |{get_bar(cpu_percent,bars)}| {cpu_usage:.2f}% ",end="", flush=True)
    print(Style.BRIGHT + Fore.WHITE + "MEM Usage:" + color_mem + f"|{get_bar(mem_percent,bars)}| {mem_usage_percent:.2f}% MB: {int(mem_usage_mb)-60} ",end="\r", flush=True)


def main(process):
    """Main function that will be executed when running this script directly from command line.

    Args:
        process (Process): The process with the PID
    """
    number_divisor = (1024 ** 2)
    global time_end  # noqa: PLW0603

    while True:
        try:
            ram_usage_bytes = process.memory_info().rss
            total_memory = psutil.virtual_memory().total
            ram_usage_percent = (ram_usage_bytes / total_memory) * 100
        except  psutil.NoSuchProcess:
            time_end = time.time()
            show_result(process.pid)
            sys.exit("\nThe process was unexpectedly interrupted")
        display_usage(process.cpu_percent(),ram_usage_percent,ram_usage_bytes / number_divisor,30)
        time.sleep(0.5)

if __name__ == "__main__":
    colorama.init(autoreset=True)
    print(BANNER,flush=True)

    parser = argparse.ArgumentParser()
    parser.add_argument("pid", help="Pid of process")
    args = parser.parse_args()
    try:
        process = psutil.Process(int(args.pid))
    except psutil.NoSuchProcess:
        sys.exit('No such process')
    try:
        time_start  = time.time()
        main(process)
    except  KeyboardInterrupt:
        time_end = time.time()
        show_result(args.pid)
        sys.exit(0)
