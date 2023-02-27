import json
from signal import signal, SIGINT
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

    def post_message(
        self,
        text,
        workspace,
        channel,
        thread_uuid=None,
        message_uuid=None,
        message_or_thread_uuid=None,
        thread_broadcast=False,
    ):
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
        response = self.session.post(
            url=url, headers=headers, json=data, timeout=(10, 10)
        ).json()
        return response

    def post_file(
        self,
        file_bytes,
        text,
        workspace,
        channel,
        thread_uuid=None,
        message_uuid=None,
        message_or_thread_uuid=None,
        thread_broadcast=False,
    ):
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
        response = self.session.post(
            url=url, headers=headers, files=files, data=data, timeout=(10, 10)
        ).json()
        return response
