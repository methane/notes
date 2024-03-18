from fastapi import FastAPI, Body
from pydantic import BaseModel, ConfigDict
from enum import IntEnum


app = FastAPI()


class Color(IntEnum):
    blue = 1
    red = 2


class Item(BaseModel):
    name: str
    color: Color
    model_config = ConfigDict(strict=True)


@app.post("/item")
async def create_item(item: Item = Body()):
    print(item)
    return {}

if __name__ == '__main__':
    # print(repr(Item.model_validate_json('{"name":"cup", "color": 1}')))
    print(Item.model_validate_json('{"name":"cup", "color": 1}'))

