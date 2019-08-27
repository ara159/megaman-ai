from datetime import datetime

logger = open(".megaman_ai.log", "a")

def info(texto):
    logger.write("{} - {}\n".format(datetime.now().isoformat(), texto))

def close():
    logger.close()