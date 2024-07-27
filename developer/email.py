import time
import aiohttp
import asyncio
from typing import Optional, List, Dict

from .error import EmailException
from .models import CreateEmail, EmailIds, ViewEmail

__all__ = ['DeveloperEmail']


class DeveloperEmail:
    """
    Initialize the DeveloperEmail class.

    Parameters:
    -----------
        version (str):
            The version of the API to use. Default is "v1".
        session (aiohttp.ClientSession):
            An optional aiohttp ClientSession object to reuse. If not provided, a new session will be created.
    """

    def __init__(
        self, version: str = "v1", session: Optional[aiohttp.ClientSession] = None
    ):
        self.base_url = f"https://www.developermail.com/api/{version}"
        self.session = session or aiohttp.ClientSession()

    async def __http_req(
        self,
        method: str,
        url: str,
        headers: Optional[Dict] = None,
        payload: Optional[Dict] = None,
        proxy: Optional[str] = None,
        timeout: Optional[float] = 10.0,
        attempts: Optional[int] = 3,
    ) -> Optional[Dict]:

        if not self.session:
            await DeveloperEmail.new_session


        for attempt in range(attempts):
            try:
                async with self.session.request(
                    method,
                    url,
                    headers=headers,
                    json=payload,
                    proxy=proxy,
                    timeout=timeout,
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get("result")
                    else:
                        continue
            except Exception as e:
                if attempt == attempts - 1:
                    raise EmailException(status=500, message=str(e))
                await asyncio.sleep(1)

        raise EmailException(status=500, message="Failed after multiple attempts")

    async def create_mail(self) -> Optional[CreateEmail]:
        """
        Creates a new mailbox on the DeveloperMail platform.

        Returns:
        --------
        Optional[CreateEmail]
            An optional CreateEmail object containing the details of the newly created mailbox.
            If the request fails, returns None.
        """
        data = await self.__http_req(
            method="PUT",
            url=f"{self.base_url}/mailbox",
            headers={"accept": "application/json"},
        )
        return CreateEmail.from_dict(data)

    async def get_message_ids(
        self, mailbox_name: str, token: str
    ) -> Optional[EmailIds]:
        """
        Retrieves the message IDs of the latest emails in a specified mailbox.

        Parameters:
        -----------
        mailbox_name (str):
            The name of the mailbox to retrieve message IDs from.
        token (str):
            The authentication token for the mailbox.

        Returns:
        --------
        Optional[EmailIds]:
            An optional EmailIds object containing the message IDs of the latest emails.
            If the request fails, returns None.
        """
        headers = {"accept": "application/json", "X-MailboxToken": token}
        data = await self.__http_req(
            method="GET", url=f"{self.base_url}/mailbox/{mailbox_name}", headers=headers
        )
        return EmailIds.from_dict(data)

    async def get_messages(
        self, mailbox_name: str, token: str, message_ids: List[str]
    ) -> Optional[ViewEmail]:
        """
        Retrieves the messages associated with the given message IDs from a specified mailbox.

        Parameters:
        -----------
        mailbox_name (str):
            The name of the mailbox to retrieve messages from.
        token (str):
            The authentication token for the mailbox.
        message_ids (List[str]):
            A list of message IDs to retrieve.

        Returns:
        --------
        Optional[ViewEmail]:
            An optional ViewEmail object containing the retrieved messages.
            If the request fails or no messages are found, returns None.
        """
        headers = {
            "accept": "application/json",
            "X-MailboxToken": token,
            "Content-Type": "application/json",
        }
        data = await self.__http_req(
            method="POST",
            url=f"{self.base_url}/mailbox/{mailbox_name}/messages",
            headers=headers,
            payload={"message_ids": message_ids},
        )
        return ViewEmail.from_dict(data)

    async def wait_for_email(
        self,
        mailbox_name: str,
        token: str,
        timeout: float = 60.0,
        check_interval: int = 5,
    ) -> Optional[ViewEmail]:
        """
        Waits for an email to arrive in a specified mailbox within a given timeout period.

        Parameters:
        -----------
        mailbox_name (str):
            The name of the mailbox to check for incoming emails.
        token (str):
            The authentication token for the mailbox.
        timeout (float, optional):
            The maximum time to wait for an email in seconds. Default is 60.0 seconds.
        check_interval (int, optional):
            The interval at which to check for new emails in seconds. Default is 5 seconds.

        Returns:
        --------
        Optional[ViewEmail]:
            An optional ViewEmail object containing the retrieved email.
            If no email is received within the specified timeout, raises an EmailException.
        """
        start_time = time.time()
        while time.time() - start_time < timeout:
            message_ids = await self.get_message_ids(mailbox_name, token)
            if message_ids and message_ids.mails:
                messages = await self.get_messages(
                    mailbox_name, token, [message_ids.mails[-1].id]
                )
                if messages:
                    return messages
            await asyncio.sleep(check_interval)
        raise EmailException(
            status=None,
            message=f"Could not retrieve any message after {timeout} seconds",
        )

    @property
    async def close(self) -> None:
        """
        A property method to close the aiohttp ClientSession.

        This method is intended to be used as a context manager, allowing the session to be closed
        properly when it is no longer needed.

        Parameters:
        -----------
        None

        Returns:
        --------
        None
            The method does not return any value. It closes the aiohttp ClientSession.
        """
        await self.session.close()

    @property
    async def new_session(self) -> aiohttp.ClientSession:
        """
        A property method to manage the aiohttp ClientSession.
    
        This method ensures that a ClientSession is created when it is accessed for the first time.
        If a ClientSession already exists, it is returned without creating a new one.
    
        Parameters:
        -----------
        None
    
        Returns:
        --------
        aiohttp.ClientSession
            The aiohttp ClientSession object. If a new session is created, it is stored in the instance
            for future use.
        """
        if not self.session:
            self.session = aiohttp.ClientSession()
    
        return self.session
