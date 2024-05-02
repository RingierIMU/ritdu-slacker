import json

class MessageFormatter:
    def __init__(self, emoji_map=None):
        if emoji_map is None:
            emoji_map = {
                "INFO": ":information_source:",
                "ERROR": ":exclamation:",
                "WARNING": ":warning:",
                "UNKNOWN": ":question:"
            }
        self.emoji_map = emoji_map

    def init_messages(self, category, title, details):
        emoji = self.emoji_map.get(category.upper(), self.emoji_map["UNKNOWN"])
        blocks = {"blocks": []}
        blocks["blocks"].append({
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": f"{emoji} {title}",
            },
        })
        if isinstance(details, list):
            block_text = "```" + json.dumps(details, indent=2) + "```"
            blocks["blocks"].extend(
                [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": block_text,
                            }
                        }
                ]
            )
        elif isinstance(details, str):
                blocks["blocks"].extend(
                    [
                        {
                            "type": "section",
                            "text": {
                                "type": "mrkdwn",
                                "text": details,
                                }
                            }
                    ]
                )
        return blocks

    def thread_messages(self, details, code=False):
        blocks = {"blocks": []}
        if isinstance(details, list):
            block_text = json.dumps(details, indent=2)
            if code:
                block_text = "```" + block_text + "```"
            blocks["blocks"].extend([
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": block_text,
                    }
                }
            ])
        elif isinstance(details, str):
            blocks["blocks"].extend([
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": details,
                    }
                }
            ])
        return blocks
