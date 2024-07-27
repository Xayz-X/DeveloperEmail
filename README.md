# DeveloperEmail API Wrapper

The `DeveloperEmail` class provides an asynchronous interface to interact with the DeveloperEmail API. This library allows you to create email mailboxes, retrieve message IDs, and fetch email messages, making it easy to manage and automate email interactions.

## Features

- Create new email mailboxes.
- Retrieve message IDs from a mailbox.
- Fetch email messages by ID.
- Wait for new emails to arrive in a mailbox.

## Installation

To use the `DeveloperEmail` API wrapper, you need to have Python installed on your system. You can install the required packages using `pip`:

```bash
pip install aiohttp
```

## Usage

Here is a basic example of how to use the `DeveloperEmail` class:
```python
import asyncio
from developer.email import DeveloperEmail

async def main():
    developer_email = DeveloperEmail()
    mailbox = await developer_email.create_mail()
    print(f"Created mailbox: {mailbox.email}")

if __name__ == "__main__":
    asyncio.run(main())

```

