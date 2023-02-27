from .cli import SlackMessageCLI
from signal import signal, SIGINT
from sys import exit
import logging

_tool_name = "ritdu-slacker"
logger = logging.getLogger()
logger.setLevel(logging.ERROR)
logging.basicConfig(
    format="[%(asctime)s] "
    + _tool_name
    + " [%(levelname)s] %(funcName)s %(lineno)d: %(message)s"
)


def sigint_handler(signal_received, frame):
    """Handle SIGINT or CTRL-C and exit gracefully"""
    logger.warning("SIGINT or CTRL-C detected. Exiting gracefully")
    exit(0)


def main():
    cli = SlackMessageCLI()
    cli.main()


if __name__ == "__main__":
    signal(SIGINT, sigint_handler)
    main()
