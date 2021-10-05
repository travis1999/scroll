import scroll
from scroll.base import BaseModel
from scroll.descriptor import PositiveInteger, String, Generic, SizedString, DefaultString, DefaultGeneric, Default
import datetime
from uuid import uuid4
from pprint import pprint


def convert_iso_string(value):
    if isinstance(value, str):
        return datetime.datetime.fromisoformat(value)
    return value


class DefaultPositiveInteger(Default, PositiveInteger):
    pass


class Model(BaseModel):
    """
    A model with a docstring 
        args:
            name: (str) name of the person
            age: (int) age of the person
        Returns:
            (Model) a model with name and age
    """
    
    created_at = DefaultGeneric(datetime.datetime, convert=convert_iso_string, default=datetime.datetime.now)
    modified_at = DefaultGeneric(datetime.datetime, convert=convert_iso_string, default=datetime.datetime.now)
    uuid = DefaultString(default = lambda: str(uuid4()))  
    
    
    @classmethod
    def from_dict(cls, data):
        return cls(**data)


class Person(Model):
    name = String()
    age = PositiveInteger()
    sex = SizedString(maxlen=1)
    
    
class Child(Person):
    parent = String()
    
    
class Master(Model):
    title = String()
    
class MasterChild(Master, Child):
    pass
    
    
t = datetime.datetime.now()



print(Child.__signature__)
pprint(Child.__dict__)

child = Child("Trevor oguna", 12, 'm', parent="oguna", created_at=t)
# print("uiuiui", child.uuid, child.created_at)
child.uuid = "123"
master = MasterChild("Mr", "Trevor oguna", 12, 'm', parent="oguna", created_at=t)
pprint(master.__dict__)
print(Master.from_dict)
