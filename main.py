import logging
import time
from multiprocessing import Process
from subprocess import Popen, PIPE
import platform

OS = platform.system()

def setup_logger(name, log_file, level=logging.INFO):
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    return logger


ping_log = setup_logger(name='ping_log', log_file="./ping_log.log")
app_log = setup_logger(name='app_log', log_file="./app_log")


def ping_mon(count: int, host: str):
    if OS == "Windows":
        proc = Popen(["ping", "-n", str(count), host], stdout=PIPE)
    else:
        proc = Popen(["ping", "-c", str(count), host], stdout=PIPE)
    output = proc.communicate()
    ping_data = f"Ping to {host} "
    for item in output:
        try:
            status = str(item, encoding='utf-8')
            if OS == "Windows":
                status = status.split('\r')
            else:
                status = status.split('\n')
            app_log.info(f'Ping Status: {status}')
            app_log.info(f'Ping Status length: {len(status)}')
        except TypeError as e:
            app_log.info(e)
    for item in status:
        if "packet loss" or "loss" in item:
            item = item.lstrip('\n')
            item = item.rstrip('\n')
            ping_data += item + " "
        if "round-trip" or "Average" in item:
            item = item.lstrip('\n')
            item = item.rstrip('\n')
            ping_data += item

    ping_log.info(ping_data)


def start_ping_mon(host, duration: int = 10):
    while duration > 0:
        star_time = int(time.time())
        ping_mon(count=4, host=host)
        end_time = int(time.time())
        time_spent = end_time - star_time
        duration = duration - time_spent


if __name__ == '__main__':
    host = input("What ip would you like to monitor:")
    duration = int(input("For how many seconds would you like to monitor:"))
    p = Process(target=start_ping_mon, args=(host, duration,))
    p.start()
    print(f"monitoring {host} for {duration} check ping_log.log for details")
