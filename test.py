# this is the test case of wrapper.

import asyncio
from developer.email import DeveloperEmail
from developer.error import EmailException

async def main():
    dev = DeveloperEmail()
    data = await dev.create_mail()
    print(data)

if __name__ == '__main__':
    asyncio.run(main())