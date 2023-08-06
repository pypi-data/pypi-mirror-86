"""Main entry into script. Global logging settings configured here, including primary sink definitions. Calls the execute function from pyEntrez commandline module.
"""
from pyEntrez.cmdline import execute
from loguru import logger
import os

if __name__ == '__main__':
    """Main sets up loggers using absolute path of installation directory and calls execute.
    """
    logger.opt(colors=True).info("<g>.......pyEntrez started.......</>")
    cwd = os.path.abspath(os.getcwd())
    logPath = os.path.join(cwd,'pyEntrez\\logs\\')
    logger.add(logPath+'out_INFO.log', level="INFO", colorize=False, backtrace=False, diagnose=False, rotation="500 MB", format="{time:YY:MM:DD:HH:mm:ss} |{level} | {message}")
    logger.add(logPath+'out_DEBUG.log', level="DEBUG", colorize=False, backtrace=True, diagnose=True, rotation="500 MB", format="{time:YY:MM:DD:HH:mm:ss} |{level} | {message}")
    logger.debug(logger)
    execute()