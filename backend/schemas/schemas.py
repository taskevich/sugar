import datetime

from fastapi import UploadFile
from fastapi.params import File
from pydantic import BaseModel
from typing import Optional, Any, List


class DefaultResponse(BaseModel):
    error: Optional[bool]
    message: Optional[str]
    payload: Optional[Any]


class RequestLogin(BaseModel):
    username: Optional[str]
    password: Optional[str]


class AddScheduleRequest(BaseModel):
    questId: Optional[int] = None
    date: Optional[str]
    isBusy: Optional[bool]


class LinkScheduleRequest(BaseModel):
    questId: Optional[int]
    scheduleId: Optional[int]


class AddServiceRequest(BaseModel):
    questId: Optional[int] = None
    name: Optional[str]
    text: Optional[str]
    price: Optional[int]


class LinkServiceRequest(BaseModel):
    questId: Optional[int]
    serviceId: Optional[int]


class AddQuestRequest(BaseModel):
    name: Optional[str] = "quest"
    slug: Optional[str] = "slug"
    description: Optional[str] = "description"
    myErpId: Optional[Any] = None
    price: Optional[int] = 3000
    hardId: Optional[int] = 1
    horrorId: Optional[int] = 1
    legend: Optional[str] = "legend"
    minPlayers: Optional[int] = 2
    maxPlayers: Optional[int] = 4
    countActors: Optional[int] = 1
    playTime: Optional[int] = 60
    ageLimit: Optional[int] = 18
    isHide: Optional[bool] = False


class AddAndUpdateSchema(BaseModel):
    newQuest: Optional[AddQuestRequest]


class AddBookingRequest(BaseModel):
    name: Optional[str]
    phone: Optional[str]
    pickHorror: Optional[int] = 1
    pickHard: Optional[int] = 1
    pickDate: Optional[int]
    questId: Optional[int]
    pickActors: Optional[int] = 1
    pickPlayers: Optional[int] = 2
    age: Optional[int] = 18
    email: Optional[str] = None
    services: Optional[List[int]] = []


class AddReviewRequest(BaseModel):
    visitor: Optional[str]
    message: Optional[str]
    stars: Optional[int]
    questId: Optional[int] = None


class AddPhotoRequest(BaseModel):
    questId: Optional[int] = None
