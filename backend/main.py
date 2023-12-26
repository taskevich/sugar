import io
import os
import shutil
import jwt
import re
import uuid

from PIL import Image
from fastapi import FastAPI, HTTPException, Depends, status, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.params import File
from fastapi.security import HTTPAuthorizationCredentials
from fastapi.responses import FileResponse
from datetime import datetime, timedelta
from starlette.responses import Response, StreamingResponse
from auth import CustomHTTPBearer, ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM
from schemas.schemas import DefaultResponse, RequestLogin, AddScheduleRequest, LinkScheduleRequest, AddServiceRequest, \
    LinkServiceRequest, AddBookingRequest, AddReviewRequest, AddAndUpdateSchema, AddQuestRequest
from models.api import get_all_quests, add_quest, remove_quest, hide_quest, update_quest, get_user, get_quest_by_slug, \
    add_booking, get_all_visitors, get_service_by_quest_id, get_schedule_by_quest_id, get_schedules, link_schedule, \
    add_schedule, delete_schedule, get_service, add_service, link_services, delete_service, \
    unlink_services, unlink_schedule, get_reviews, get_all_reviews, add_review, delete_review, get_photos_from_gallery, \
    add_photo_to_gallery, get_all_hards, get_all_horrors, delete_photo, _get_quest_by_id
from models.models import SessionManager, Quests

app = FastAPI()

security = CustomHTTPBearer()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def upload_photo_process(session, is_main, quest_id, file):
    photo = os.path.join("uploads", str(uuid.uuid4()))
    with open(photo, 'wb') as image:
        shutil.copyfileobj(file.file, image)

    result = add_photo_to_gallery(session, photo, is_main, quest_id)
    return photo


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = decoded_token.get("username")
        if username:
            return decoded_token
    except jwt.exceptions.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )


@app.get("/get_quests", response_model=DefaultResponse, tags=["API", "Пользователь"])
def _get_quests():
    """ Пользовательский маршрут получения квестов """
    with SessionManager() as session:
        quests = get_all_quests(session, is_user=True)
        if not isinstance(quests, tuple):
            return DefaultResponse(error=False, message="OK", payload=[quest.as_dict() for quest in quests])
        return DefaultResponse(error=quests[0], message=quests[1], payload=None)


@app.get("/get_quest/{slug}", response_model=DefaultResponse, tags=["API", "Пользователь"])
def _get_quest(slug: str):
    with SessionManager() as session:
        quest = get_quest_by_slug(session, slug)
        if not isinstance(quest, tuple):
            services = get_service_by_quest_id(session, quest.id)

            if isinstance(services, tuple):
                return DefaultResponse(error=services[0], message=services[1], payload=None)

            schedules = get_schedule_by_quest_id(session, quest.id)
            if isinstance(schedules, tuple):
                return DefaultResponse(error=schedules[0], message=schedules[1], payload=None)

            reviews = get_reviews(session, quest.id)
            if isinstance(schedules, tuple):
                return DefaultResponse(error=reviews[0], message=reviews[1], payload=None)

            result = {"quest": quest.as_dict(), "services": [service.as_dict() for service in services],
                      "schedules": [schedule.as_dict() for schedule in schedules],
                      "reviews": [review.as_dict() for review in reviews]}
            return DefaultResponse(error=False, message="OK", payload=result)
        return DefaultResponse(error=quest[0], message=quest[1], payload=None)


@app.get("/get_image", tags=["API", "Пользователь"])
def get_image(image_path: str):
    if os.path.exists(image_path):
        img = Image.open(image_path)
        img = img.convert("RGB")
        img_byte_array = io.BytesIO()
        img.save(img_byte_array, format="JPEG")
        img_byte_array.seek(0)

        try:
            return StreamingResponse(io.BytesIO(img_byte_array.getvalue()), media_type="image/jpeg")
        except:
            return DefaultResponse(error=True, message="Недопустимый формат файла", payload=None)
    else:
        return DefaultResponse(error=True, message="Изображение не найдено", payload=None)


@app.get("/get_photos", response_model=DefaultResponse, tags=["API", "Пользователь"])
def get_photos(quest_id: int = None, is_main: bool = False):
    with SessionManager() as session:
        photos = get_photos_from_gallery(session, is_main, quest_id)
        if not isinstance(photos, tuple):
            return DefaultResponse(error=False, message="OK", payload=[{photo.id: photo.photo} for photo in photos])
        return DefaultResponse(error=photos[0], message=photos[1], payload=None)


@app.delete("/admin/remove_photo/{photo_id}")
def remove_photo(photo_id: int, current_user: dict = Depends(get_current_user)):
    with SessionManager() as session:
        result = delete_photo(session, photo_id)
        if not isinstance(result, tuple):
            return DefaultResponse(error=False, message="OK", payload=None)
        return DefaultResponse(error=result[0], message=result[1], payload=None)


@app.post("/add_photo", response_model=DefaultResponse, tags=["API", "Админ"])
def add_photo(file: UploadFile = File(...), quest_id: int = None, is_main: bool = False, current_user: dict = Depends(get_current_user)):
    with SessionManager() as session:
        result = upload_photo_process(session, is_main, quest_id, file)
        if not isinstance(result, tuple):
            return DefaultResponse(error=False, message="Фотография добавлена.", payload=result)
        return DefaultResponse(error=result[0], message=result[1], payload=None)


@app.post("/add_booking", response_model=DefaultResponse, tags=["API", "Пользователь"])
async def _add_booking(request: AddBookingRequest):
    """ Пользовательский маршрут бронирования """
    with SessionManager() as session:
        order = add_booking(session, request)
        if not isinstance(order, tuple):
            return DefaultResponse(error=False, message="OK", payload=None)
        return DefaultResponse(error=order[0], message=order[1], payload=None)


@app.get("/", response_model=DefaultResponse, tags=["API", "Главная"])
def root():
    """ Админский маршрут """
    return DefaultResponse(error=False, message="OK", payload={"Created by": "Brick Studio"})


@app.post("/admin/login", response_model=DefaultResponse, tags=["API", "Авторизация"])
async def login(request: RequestLogin, response: Response):
    """ Маршрут авторизации """
    with SessionManager() as session:

        username = request.username
        password = request.password

        user = get_user(session, username)

        if isinstance(user, tuple):
            return {"error": user[0], "message": user[1], "payload": []}
        elif user:
            if username == user.username and user.password == password:
                token = create_access_token(user.as_dict())
                response.set_cookie("access_token_cookie", token, httponly=True)
                return DefaultResponse(error=False, message="OK", payload=token)
            else:
                return DefaultResponse(error=True, message="Неверный логин или пароль", payload=None)

        return DefaultResponse(error=True, message="Пользователь не найден", payload=None)


@app.get("/admin/get_schedules", response_model=DefaultResponse, tags=["API", "Расписание"])
async def _get_schedules(current_user: dict = Depends(get_current_user)):
    with SessionManager() as session:
        schedules = get_schedules(session)
        if not isinstance(schedules, tuple):
            return DefaultResponse(error=False, message="OK", payload=[schedule.as_dict() for schedule in schedules])
        return DefaultResponse(error=schedules[0], message=schedules[1], payload=None)


@app.post("/admin/add_schedules", response_model=DefaultResponse, tags=["API", "Расписание"])
async def _add_schedules(request: AddScheduleRequest, current_user: dict = Depends(get_current_user)):
    with SessionManager() as session:
        new_schedule = add_schedule(session, request)
        if not isinstance(new_schedule, tuple):
            return DefaultResponse(error=False, message="OK", payload=new_schedule.as_dict())
        return DefaultResponse(error=new_schedule[0], message=new_schedule[1], payload=None)


@app.post("/admin/link_schedules", response_model=DefaultResponse, tags=["API", "Расписание"])
async def _link_schedule(request: LinkScheduleRequest, current_user: dict = Depends(get_current_user)):
    with SessionManager() as session:
        schedule = link_schedule(session, request.questId, request.scheduleId)
        if not isinstance(schedule, tuple):
            return DefaultResponse(error=False, message="OK", payload=schedule.as_dict())
        return DefaultResponse(error=schedule[0], message=schedule[1], payload=None)


@app.post("/admin/unlink_schedules/{id}", response_model=DefaultResponse, tags=["API", "Расписание"])
async def _unlink_schedule(id: int, current_user: dict = Depends(get_current_user)):
    with SessionManager() as session:
        unlinked = unlink_schedule(session, id)
        if not isinstance(unlinked, tuple):
            return DefaultResponse(error=False, message="OK", payload=None)
        return DefaultResponse(error=unlinked[0], message=unlinked[1], payload=None)


@app.delete("/admin/delete_schedule/{id}", response_model=DefaultResponse, tags=["API", "Расписание"])
async def _delete_schedule(id: int, current_user: dict = Depends(get_current_user)):
    with SessionManager() as session:
        del_schedule = delete_schedule(session, id)
        if not isinstance(delete_schedule, tuple):
            return DefaultResponse(error=False, message="OK", payload=None)
        return DefaultResponse(error=del_schedule[0], message=del_schedule[1], payload=None)


@app.post("/admin/add_services", response_model=DefaultResponse, tags=["API", "Услуги"])
async def _add_service(request: AddServiceRequest, current_user: dict = Depends(get_current_user)):
    with SessionManager() as session:
        service = add_service(session, request)
        if not isinstance(service, tuple):
            return DefaultResponse(error=False, message="OK", payload=service.as_dict())
        return DefaultResponse(error=service[0], message=service[1], payload=None)


@app.get("/admin/get_services", response_model=DefaultResponse, tags=["API", "Услуги"])
async def _get_services(current_user: dict = Depends(get_current_user)):
    with SessionManager() as session:
        services = get_service(session)
        if not isinstance(services, tuple):
            return DefaultResponse(error=False, message="OK", payload=[service.as_dict() for service in services])
        return DefaultResponse(error=services[0], message=services[1], payload=None)


@app.post("/admin/link_service", response_model=DefaultResponse, tags=["API", "Услуги"])
async def _link_service(request: LinkServiceRequest, current_user: dict = Depends(get_current_user)):
    with SessionManager() as session:
        is_linked = link_services(session, request.questId, request.serviceId)
        if not isinstance(is_linked, tuple):
            return DefaultResponse(error=False, message="OK", payload=None)
        return DefaultResponse(error=is_linked[0], message=is_linked[1], payload=None)


@app.post("/admin/unlink_service/{id}", response_model=DefaultResponse, tags=["API", "Услуги"])
async def unlink_service(id: int, current_user: dict = Depends(get_current_user)):
    with SessionManager() as session:
        unlinked = unlink_services(session, id)
        if not isinstance(unlinked, tuple):
            return DefaultResponse(error=False, message="OK", payload=None)
        return DefaultResponse(error=unlinked[0], message=unlinked[1], payload=None)


@app.delete("/admin/delete_service/{id}", response_model=DefaultResponse, tags=["API", "Услуги"])
async def _delete_service(id: int, current_user: dict = Depends(get_current_user)):
    with SessionManager() as session:
        is_deleted = delete_service(session, id)
        if not isinstance(is_deleted, tuple):
            return DefaultResponse(error=False, message="OK", payload=None)
        return DefaultResponse(error=is_deleted[0], message=is_deleted[1], payload=None)


@app.get("/admin/panel", response_model=DefaultResponse, tags=["API", "Квесты"])
async def panel(current_user: dict = Depends(get_current_user)):
    """ Маршрут панели, возвращает все квесты и информацию о посетителях """
    with (SessionManager() as session):
        quests = get_all_quests(session)
        visitors = get_all_visitors(session)
        hards = get_all_hards(session)
        horrors = get_all_horrors(session)

        if (not isinstance(quests, tuple) and not isinstance(visitors, tuple) and
                not isinstance(hards, tuple) and not isinstance(horrors, tuple)):
            visitors_collection = []

            for visitor, order in visitors:
                visitor_dict = next((v for v in visitors_collection if v["id"] == visitor.id), None)

                if visitor_dict is None:
                    visitor_dict = visitor.as_dict()
                    visitor_dict["orders"] = []

                    visitors_collection.append(visitor_dict)

                visitor_dict["orders"].append(order.as_dict())

            result = {
                "quests": [quest.as_dict() for quest in quests],
                "visitors": visitors_collection,
                "hards": [{hard.id: hard.name} for hard in hards],
                "horrors": [{horror.id: horror.name} for horror in horrors],
            }
            return DefaultResponse(error=False, message="OK", payload=result)
        elif isinstance(visitors, tuple):
            return DefaultResponse(error=visitors[0], message=visitors[1], payload=None)
        elif isinstance(hards, tuple):
            return DefaultResponse(error=hards[0], message=hards[1], payload=None)
        elif isinstance(horrors, tuple):
            return DefaultResponse(error=horrors[0], message=horrors[1], payload=None)
        else:
            return DefaultResponse(error=quests[0], message=quests[1], payload=None)


@app.post("/admin/panel/set_photo", response_model=DefaultResponse, tags=["API", "Квесты"])
async def set_photo(quest_id: int, file: UploadFile = File(...), current_user: dict = Depends(get_current_user)):
    with SessionManager() as session:
        photo = os.path.join("uploads", re.sub("\s+", "", file.filename))
        with open(photo, 'wb') as image:
            shutil.copyfileobj(file.file, image)

        quest = _get_quest_by_id(session, quest_id)
        if isinstance(quest, Quests):
            # res = add_photo_to_gallery(session, photo, False, quest_id)
            quest.files = {0: photo}
            session.commit()
            return DefaultResponse(error=False, message="OK", payload=quest.id)
        return DefaultResponse(error=True, message="Квест не найден", payload=None)


@app.post("/admin/panel/add", response_model=DefaultResponse, tags=["API", "Квесты"])
async def _add_quest(request: AddQuestRequest, current_user: dict = Depends(get_current_user)):
    """ Маршрут добавления квеста """
    with SessionManager() as session:
        new = add_quest(session, request)
        if not isinstance(new, tuple):
            return DefaultResponse(error=False, message="OK", payload=new.id)
        return DefaultResponse(error=new[0], message=new[1], payload=None)


@app.delete("/admin/panel/remove/{id}", response_model=DefaultResponse, tags=["API", "Квесты"])
async def _remove_quest(id: int, current_user: dict = Depends(get_current_user)):
    """ Маршрут удаления квеста """
    with SessionManager() as session:
        res = remove_quest(session, id)
        if not isinstance(res, tuple):
            return DefaultResponse(error=False, message="OK", payload=None)
        return DefaultResponse(error=res[0], message=res[1], payload=None)


@app.post("/admin/panel/hide/{id}", response_model=DefaultResponse, tags=["API", "Квесты"])
async def _hide_quest(id: int, current_user: dict = Depends(get_current_user)):
    """ Маршрут скрытия квеста """
    with SessionManager() as session:
        res = hide_quest(session, id)
        if not isinstance(res, tuple):
            return DefaultResponse(error=False, message="OK", payload=None)
        return DefaultResponse(error=res[0], message=res[1], payload=None)


@app.post("/admin/panel/update/{id}", response_model=DefaultResponse, tags=["API", "Квесты"])
async def _update_quest(request: AddQuestRequest, id: int, current_user: dict = Depends(get_current_user)):
    """ Маршрут обновления квеста """
    with SessionManager() as session:
        res = update_quest(session, request, id)

        if isinstance(res, Quests):
            return DefaultResponse(error=False, message="OK", payload=res.id)
        return DefaultResponse(error=res[0], message=res[1], payload=None)


@app.post("/admin/get_reviews", response_model=DefaultResponse, tags=["API", "Отзывы"])
async def _get_reviews(quest_id: int = None):
    with SessionManager() as session:
        reviews = get_all_reviews(session, quest_id)
        if not isinstance(reviews, tuple):
            return DefaultResponse(error=False, message="OK", payload=[review.as_dict() for review in reviews])
        return DefaultResponse(error=reviews[0], message=reviews[1], payload=None)


@app.post("/admin/reviews/add", response_model=DefaultResponse, tags=["API", "Отзывы"])
async def _add_reviews(request: AddReviewRequest, current_user: dict = Depends(get_current_user)):
    with SessionManager() as session:
        review = add_review(session, request)
        if not isinstance(review, tuple):
            return DefaultResponse(error=False, message="OK", payload=review.as_dict())
        return DefaultResponse(error=review[0], message=review[1], payload=None)


@app.delete("/admin/reviews/delete/{id}", tags=["API", "Отзывы"])
async def _delete_review(id: int, current_user: dict = Depends(get_current_user)):
    with SessionManager() as session:
        was_deleted = delete_review(session, id)
        if not isinstance(was_deleted, tuple):
            return DefaultResponse(error=False, message="OK", payload=None)
        return DefaultResponse(error=was_deleted[0], message=was_deleted[1], payload=None)
