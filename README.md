This is a very basic [maubot](https://github.com/maubot/maubot) plugin that writes the messages it receives to a file.

Use case: using Matrix for note-taking.
You send quick notes to the bot's account, it persists them.

Currently it only handles text messages.
They're appended to a file at a configured path.
Messages are prepended with a timestamp; the format is currently hardcoded.

You can and probably should configure it to only record messages from specific users.

# Installation

- [Setup maubot](https://docs.mau.fi/maubot/usage/setup/index.html)
- Clone this repo and [use `mbc build -u`](https://docs.mau.fi/maubot/usage/cli/build.html) to build the plugin
- [Create a client and an instance](https://docs.mau.fi/maubot/usage/basic.html)
- Update the configuration; see [base-config.yaml](base-config.yaml) for documentation of the available options
