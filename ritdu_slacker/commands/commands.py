import base64
import logging, click, click_log, json
import requests, json, click, logging, os
from requests import Session
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


class SlackClient:
    def __init__(self):
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.ERROR)

    def requests_retry_session(
        self,
        retries=5,
        backoff_factor=0.5,
        status_forcelist=(500, 502, 504),
        session=None,
    ) -> Session:
        session = session or requests.Session()
        retry = Retry(
            total=retries,
            read=retries,
            connect=retries,
            backoff_factor=backoff_factor,
            status_forcelist=status_forcelist,
        )
        adapter = HTTPAdapter(max_retries=retry)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        return session

    def post_message_to_slack(
        self,
        text,
        thread_uuid,
        message_uuid,
        message_or_thread_uuid,
        workspace,
        channel,
        thread_broadcast=False,
    ) -> dict:
        return (
            self.requests_retry_session()
            .post(
                url="https://slacker.cube-services.net/api/message-template",
                headers={"Content-Type": "application/json"},
                json={
                    "command": "SimpleMessage",
                    "workspace": workspace,
                    "channel": channel,
                    "message_uuid": message_uuid,
                    "thread_uuid": thread_uuid,
                    "message_or_thread_uuid": message_or_thread_uuid,
                    "thread_broadcast": thread_broadcast,
                    "message": text,
                    "fallback_message": text,
                },
                timeout=(10, 10),
            )
            .json()
        )

    def post_file_to_slack(
        self,
        text,
        thread_uuid,
        message_uuid,
        message_or_thread_uuid,
        workspace,
        channel,
        file_bytes,
        thread_broadcast=False,
    ) -> dict:
        return (
            self.requests_retry_session()
            .post(
                url="https://slacker.cube-services.net/api/message-template",
                headers={
                    "Accept": "application/json",
                },
                files={"file": file_bytes},
                data={
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
                },
                timeout=(10, 10),
            )
            .json()
        )


class SlackCLI:
    def __init__(self):
        self.client = SlackClient()
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.ERROR)

    @click.group(help="CLI tool send/update slack messages and send files")
    @click.help_option("--help", "-h")
    def main(self):
        pass

    @click.command(
        help="Command to send message, reply to thread or reply and broadcast to thread"
    )
    @click.option("--debug", is_flag=True, help="Switch to debug logging")
    @click.option("--text", "-m", default=None, required=True, help="text to send")
    @click.option(
        "--workspace",
        "-w",
        default=None,
        required=True,
        help="slack workspace name",
    )
