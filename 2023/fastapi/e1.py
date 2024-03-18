from pydantic import BaseModel
from enum import IntEnum

class Choice(IntEnum):
    a = 1
    b = 2

class Item(BaseModel, strict=True):
    id: int
    choice: Choice

item = Item(id=42, choice=Choice.b)

print(item.model_validate(item.model_dump()))  # works
print(item.model_validate_json(item.model_dump_json()))  # works

print(f"{item.model_dump()=}")
print(f"{item.model_dump(mode='json')=}")

print(item.model_validate(item.model_dump(mode="json"))) # doesn't work
