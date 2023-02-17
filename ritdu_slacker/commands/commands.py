import base64
import logging, json
import requests
from requests import Session
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


class SlackClient:
    def __init__(self, retries=5, backoff_factor=0.5, status_forcelist=(500, 502, 504)):
        self.retries = retries
        self.backoff_factor = backoff_factor
        self.status_forcelist = status_forcelist
        self.session = Session()
        self.retry = Retry(
            total=self.retries,
            read=self.retries,
            connect=self.retries,
            backoff_factor=self.backoff_factor,
            status_forcelist=self.status_forcelist,
        )
        self.adapter = HTTPAdapter(max_retries=self.retry)
        self.session.mount("http://", self.adapter)
        self.session.mount("https://", self.adapter)

    def post_message(self, text, workspace, channel, thread_uuid=None, message_uuid=None, message_or_thread_uuid=None, thread_broadcast=False):
        url = "https://slacker.cube-services.net/api/message-template"
        headers = {"Content-Type": "application/json"}
        data = {
            "command": "SimpleMessage",
            "workspace": workspace,
            "channel": channel,
            "message_uuid": message_uuid,
            "thread_uuid": thread_uuid,
            "message_or_thread_uuid": message_or_thread_uuid,
            "thread_broadcast": thread_broadcast,
            "message": text,
            "fallback_message": text,
        }
        response = self.session.post(url=url, headers=headers, json=data, timeout=(10, 10)).json()
        return response

    def post_file(self, file_bytes, text, workspace, channel, thread_uuid=None, message_uuid=None, message_or_thread_uuid=None, thread_broadcast=False):
        url = "https://slacker.cube-services.net/api/message-template"
        headers = {"Accept": "application/json"}
        files = {"file": file_bytes}
        data = {
            "json": json.dumps(
                {
                    "command": "SimpleMessage",
                    "workspace": workspace,
                    "channel": channel,
                    "message_uuid": message_uuid,
                    "thread_uuid": thread_uuid,
                    "message_or_thread_uuid": message_or_thread_uuid,
                    "thread_broadcast": thread_broadcast,
                    "message": text,
                    "fallback_message": text,
                }
            )
        }
        response = self.session.post(url=url, headers=headers, files=files, data=data, timeout=(10, 10)).json()
        return response


import click
@click.group(help="CLI tool to send/update Slack messages and send files")
@click.help_option("--help", "-h")
@click.option("--debug", is_flag=True, help="Switch to debug logging")
@click.option("--workspace", "-w", default=None, required=True, help="Slack workspace name")
@click.option("--channel", "-c", default=None, required=True, help="Slack channel name")
@click.pass_context
def main(ctx, debug, workspace, channel):
    if debug:
        logger.setLevel(logging.DEBUG)
    ctx.obj = SlackClient(workspace=workspace, channel=channel)


@main.command(help="Command to send message, reply to thread or reply and broadcast to thread")
@click.option("--text", "-m", default=None, required=True, help="Text to send")
@click.option("--thread-uuid", "-t", default=None, required=False, help="Instantiate thread")
@click.option("--message-uuid", "-u", default=None, required=False, help="Create/replace existing message")
@click.option("--message-or-thread-uuid", "-n", default=None, required=False, help="Create or reply to existing thread")
@click.option("--thread-broadcast", "-b", is_flag=True, help="Flag to broadcast message to channel from thread")
@click.pass_obj
def message(slack_client, text, thread_uuid, message_uuid, message_or_thread_uuid, thread_broadcast):
    result = slack_client.send_message(text, thread_uuid, message_uuid, message_or_thread_uuid, thread_broadcast)
    print(json.dumps(result))
