import click
import os
import json
from .api import SlackClient
from .version import __version__
import logging

_tool_name = "ritdu-slacker"  # Try fetch this from pip __main__ instead of repeating.
logger = logging.getLogger()
logger.setLevel(logging.ERROR)
logging.basicConfig(
    format="[%(asctime)s] "
    + _tool_name
    + " [%(levelname)s] %(funcName)s %(lineno)d: %(message)s"
)


class SlackMessageCLI:
    def __init__(self):
        self.sender = SlackClient()

    def version():
        """Return the version of this cli tool"""
        return __version__

    @click.group(help="CLI tool send/update slack messages and send files")
    @click.help_option("--help", "-h")
    @click.version_option(
        prog_name=_tool_name, version=version(), message="%(prog)s, version %(version)s"
    )
    def main():
        pass

    @click.command(
        help="Command to send message, reply to thread or reply and broadcast to thread"
    )
    @click.option("--text", "-m", default=None, required=True, help="text to send")
    @click.option(
        "--workspace", "-w", default=None, required=True, help="slack workspace name"
    )
    @click.option(
        "--channel", "-c", default=None, required=True, help="slack channel name"
    )
    @click.option(
        "--message-uuid",
        "-u",
        default=None,
        required=False,
        help="create/replace existing message",
    )
    @click.option(
        "--thread-uuid",
        "-t",
        default=None,
        required=False,
        help="instantiate thread",
    )
    @click.option(
        "--message-or-thread-uuid",
        "-n",
        default=None,
        required=False,
        help="create or reply to existing thread",
    )
    @click.option(
        "--thread-broadcast",
        "-b",
        is_flag=True,
        help="flag to broadcast message to channel from thread",
    )
    def message(
        text,
        thread_uuid,
        message_uuid,
        message_or_thread_uuid,
        workspace,
        channel,
        thread_broadcast,
    ):
        sender = SlackClient()
        result = sender.post_message(
            text=f"{text}",
            thread_uuid=thread_uuid if thread_uuid else "",
            message_uuid=message_uuid if message_uuid else "",
            message_or_thread_uuid=message_or_thread_uuid
            if message_or_thread_uuid
            else "",
            workspace=workspace,
            channel=channel,
            thread_broadcast=thread_broadcast,
        )
        print(json.dumps(result))

    main.add_command(message)

    @click.command(help="Command to send file to thread")
    @click.option("--debug", is_flag=True, help="Switch to debug logging")
    @click.option("--text", "-m", default=None, required=False, help="text to send")
    @click.option(
        "--workspace", "-w", default=None, required=True, help="slack workspace name"
    )
    @click.option(
        "--channel", "-c", default=None, required=True, help="slack channel name"
    )
    @click.option(
        "--message-uuid",
        "-u",
        default=None,
        required=False,
        help="create/replace existing message",
    )
    @click.option(
        "--thread-uuid",
        "-t",
        default=None,
        required=False,
        help="instantiate thread",
    )
    @click.option(
        "--message-or-thread-uuid",
        "-n",
        default=None,
        required=False,
        help="create or reply to existing thread",
    )
    @click.option(
        "--thread-broadcast",
        "-b",
        is_flag=True,
        help="flag to broadcast message to channel from thread",
    )
    @click.option(
        "--file",
        "-f",
        default=None,
        required=True,
        help="file to send to slack",
    )
    def file(
        debug,
        text,
        thread_uuid,
        message_uuid,
        message_or_thread_uuid,
        workspace,
        channel,
        file,
        thread_broadcast,
    ):
        if debug:
            logger.setLevel(logging.DEBUG)
        logger.debug(f"Send file: {file}")

        file_basename = os.path.basename(file)
        sender = SlackClient()
        with open(file, "rb") as f:
            result = sender.post_file(
                text=f"{text}" if text else f"File: {file_basename}",
                thread_uuid=thread_uuid if thread_uuid else "",
                message_uuid=message_uuid if message_uuid else "",
                message_or_thread_uuid=message_or_thread_uuid
                if message_or_thread_uuid
                else "",
                workspace=workspace,
                channel=channel,
                file_bytes=f,
                thread_broadcast=thread_broadcast,
            )
        print(json.dumps(result))

    main.add_command(file)
