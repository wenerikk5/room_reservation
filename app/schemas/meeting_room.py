from pydantic import BaseModel, Field, validator


class MeetingRoomBase(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=100)
    description: str | None


class MeetingRoomCreate(MeetingRoomBase):
    name: str = Field(..., min_length=1, max_length=100)


class MeetingRoomUpdate(MeetingRoomBase):
    pass

    @validator('name')
    def name_cant_be_null(cls, value: str):
        if value is None:
            raise ValueError('Имя не может быть пустым!')
        return value


class MeetingRoomDB(MeetingRoomBase):
    id: int

    class Config:
        orm_mode = True
