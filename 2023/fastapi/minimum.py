from pydantic import BaseModel

class CreateRoomRequest(BaseModel):
    live_id: int
    select_difficulty: LiveDifficulty
