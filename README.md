This is a very basic [maubot](https://github.com/maubot/maubot) plugin that writes the messages it receives to a file.

Use case: using Matrix for note-taking.
You send quick notes to the bot's account, it persists them.

Messages are appended to a file at a configured path.
They're prepended with a timestamp; the format is currently hardcoded.

Attachments, both encrypted and unencrypted, are supported.
The decrypted attachment is stored in a configured directory; the filename is a UUID and a file extension guessed based on mimetype.
A message is appended to the main file linking to the attachment using markdown syntax (image links are used for images; normal links are used for all other files).

You can and probably should configure it to only record messages from specific users.
No attempt is made to protect from markdown injection attacks.

# Installation

- [Setup maubot](https://docs.mau.fi/maubot/usage/setup/index.html)
- Clone this repo and [use `mbc build -u`](https://docs.mau.fi/maubot/usage/cli/build.html) to build the plugin
- [Create a client and an instance](https://docs.mau.fi/maubot/usage/basic.html)
- Update the configuration; see [base-config.yaml](base-config.yaml) for documentation of the available options
