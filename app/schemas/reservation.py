from pydantic import BaseModel, validator, root_validator, Extra, Field

from datetime import datetime, timedelta


FROM_TIME = (datetime.now() + timedelta(minutes=10)) \
    .isoformat(timespec='minutes')
TO_TIME = (datetime.now() + timedelta(hours=1)) \
    .isoformat(timespec='minutes')


class ReservationBase(BaseModel):
    from_reserve: datetime = Field(..., example=FROM_TIME)
    to_reserve: datetime = Field(..., example=TO_TIME)

    class Config:
        extra = Extra.forbid


class ReservationUpdate(ReservationBase):

    @validator('from_reserve')
    def check_from_reserve_later_than_now(cls, value: datetime):
        if value < datetime.now():
            raise ValueError('Время начала не должно быть меньше'
                             'текущего времени')
        return value

    @root_validator(skip_on_failure=True)
    def check_from_reserve_before_to_reserve(cls, values):
        if values['from_reserve'] >= values['to_reserve']:
            raise ValueError('Время начала не должно быть позже'
                             'времени окончания')
        return values


class ReservationCreate(ReservationUpdate):
    meetingroom_id: int


class ReservationDB(ReservationBase):
    id: int
    meetingroom_id: int
    user_id: int | None

    class Config:
        orm_mode = True
