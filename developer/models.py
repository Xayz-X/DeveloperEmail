from dataclasses import dataclass
from typing import Dict, List, Any

@dataclass(slots=True)
class CreateEmail:
    name: str
    domain: str
    email: str
    token: str
    
    @staticmethod
    def from_dict(data: Dict) -> 'CreateEmail':
        return CreateEmail( 
                           name=data['name'],
                           domain='developermail.com',
                           email=f"{data['name']}@developermail.com",
                           token=data['token'])
        
@dataclass(slots=True)
class Ids:
    id: int

@dataclass(slots=True)
class EmailIds:
    mails: List[Ids] = None

    @staticmethod
    def from_dict(data: List[str]) -> 'EmailIds':
        all_ids = [Ids(id=int(id_str)) for id_str in data]
        return EmailIds(mails=all_ids)

@dataclass(slots=True)
class Email:
    id: int    
    content: Any
    
@dataclass(slots=True)
class ViewEmail:
    mails: List[Email] = None

    @staticmethod
    def from_dict(data: List[dict]) -> 'ViewEmail':
        all_emails = []
        for d in data:
            if 'key' in d and 'value' in d:
                all_emails.append(Email(id=d['key'], content=d['value']))
            else:
                raise ValueError("Invalid format for email data dictionary")
        return ViewEmail(mails=all_emails)