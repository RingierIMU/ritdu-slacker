# ritdu-slacker
pip installable bin to interact with the Ringier SA internal interface for slack.
Provides both CLI and Native python lib functionality.

## Motivation
- Single implementation of a wrapper around our internal slack interface.

## Installation
```bash
$ pip install ritdu-slacker
```

## Usage

### CLI
To send a message to a slack channel from within a thread:
```bash
$ ritdu-slacker message --workspace "${SLACK_WORKSPACE}" --channel "${SLACK_CHANNEL//#}" --text "Update in progress" --thread-uuid "${thread_uuid}" --thread-broadcast
```

To replace a message send a new one with the same message-uuid:
```bash
$ ritdu-slacker message --workspace "${SLACK_WORKSPACE}" --channel "${SLACK_CHANNEL//#}" --text "Update complete!" --message-uuid "${message_uuid}"
```

To send a message and file to a thread in a slack channel:
```bash
$ ritdu-slacker file --workspace "${SLACK_WORKSPACE}" --channel "${SLACK_CHANNEL//#}" --text "Oops!" --file "/tmp/errorlog.txt" --thread-uuid "${thread_uuid}"
```
To send a jsonblob to slack:
```bash
$ ritdu-slacker message --text  '{ "blocks": [ { "type": "section", "text": { "type": "mrkdwn", "text": "Hello, Assistant to the Regional Manager Dwight! *Michael Scott* wants to know where youd like to take the Paper Company investors to dinner tonight.\n\n *Please select a restaurant:*" } }, { "type": "divider" }, { "type": "section", "text": { "type": "mrkdwn", "text": "*Farmhouse aThai Cuisine*\n:star::star::star::star: 1528 reviews\n They do have some vegan options, like the roti and curry, plus they have a ton of salad stuff and noodles can be ordered without meat!! They have something for everyone here" }, "accessory": { "type": "image", "image_url": "https://s3-media3.fl.yelpcdn.com/bphoto/c7ed05m9lC2EmA3Aruue7A/o.jpg", "alt_text": "alt text for image" } }, { "type": "section", "text": { "type": "mrkdwn", "text": "*Kin Khao*\n:star::star::star::star: 1638 reviews\n The sticky rice also goes wonderfully with the caramelized pork belly, which is absolutely melt-in-your-mouth and so soft." }, "accessory": { "type": "image", "image_url": "https://s3-media2.fl.yelpcdn.com/bphoto/korel-1YjNtFtJlMTaC26A/o.jpg", "alt_text": "alt text for image" } }, { "type": "section", "text": { "type": "mrkdwn", "text": "*Ler Ros*\n:star::star::star::star: 2082 reviews\n I would really recommend the  Yum Koh Moo Yang - Spicy lime dressing and roasted quick marinated pork shoulder, basil leaves, chili & rice powder." }, "accessory": { "type": "image", "image_url": "https://s3-media2.fl.yelpcdn.com/bphoto/DawwNigKJ2ckPeDeDM7jAg/o.jpg", "alt_text": "alt text for image" } }, { "type": "divider" } ] }' --command 'SlackJson' --workspace "ringier-southafrica" --channel "pe-test"
```

### Python

```
from ritdu_slacker.api import SlackClient
client = SlackClient()
client.post_message("via python api","ringier-southafrica","#pe-alerts")
{'message_uuid': '9890b802-fac3-4e61-bbe8-b53cc17fc581', 'message_ts': '1677473299.255969', 'thread_uuid': '9890b802-fac3-4e61-bbe8-b53cc17fc581', 'thread_ts': '1677473299.255969', 'channel': 'CV3JFH08J'}
client.post_message(datajson,"ringier-southafrica","pe-test",command="SlackJson")
```

## Development

To setup your development environment:

```
$ make setup-dev
```

Running make on its own generates help documentation:

```
$ make
build                Build the package
check                Check the package
clean                Clean the package
dev                  Setup development environment
format               Format the code
install-prod         Install production dependencies
install              Install all dependencies
lint                 Lint the code
lock                 Update dependency lockfile
publish              Publish the package
test                 Test the package
version              Generate version from GitHub tag
vscode               Update VSCode settings
```

Please read the _Makefile_ to see what each task does.
123
