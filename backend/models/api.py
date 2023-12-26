import os

from typing import Tuple
from .models import Session, Quests, Visitors, Users, Orders, Services, Hard, Horror, Schedules, OrderToService, \
    Reviews, Gallery


def get_user(session: Session, username: str) -> Users | tuple[bool, str]:
    try:
        user = session.query(Users).filter(Users.username == username).first()
        if user:
            return user
        return True, "Пользователь не найден"
    except Exception as ex:
        return True, str(ex)


def get_schedules(session: Session) -> Schedules | tuple[bool, str]:
    try:
        return session.query(Schedules).all()
    except Exception as ex:
        return True, str(ex)


def link_schedule(session: Session, quest_id: int, schedule_id: int) -> Schedules | tuple[bool, str]:
    try:
        quest = session.query(Quests).get(quest_id)
        schedule = session.query(Schedules).get(schedule_id)
        if quest and schedule:
            if schedule.quest_id is not None:
                return True, "You can't link already linked schedule"

            schedule.quest_id = quest.id
            session.commit()
            return schedule
        return True, "Quest or schedule not found"
    except Exception as ex:
        return True, str(ex)


def get_photos_from_gallery(session: Session, is_main: bool, quest_id: int = None) -> list[Gallery] | tuple[bool, str]:
    try:
        if quest_id:
            stmt = session.query(Gallery).filter(Gallery.quest_id == quest_id, Gallery.is_main == is_main)
        else:
            stmt = session.query(Gallery).filter(Gallery.is_main == is_main)
        return stmt.all()
    except Exception as ex:
        return True, str(ex)


def add_photo_to_gallery(session: Session, photo: str, is_main: bool, quest_id: int = None) -> Gallery | tuple[bool, str]:
    try:
        gallery = Gallery(
            photo=photo,
            quest_id=quest_id,
            is_main=is_main
        )
        session.add(gallery)
        session.commit()
        return gallery
    except Exception as ex:
        return True, str(ex)


def unlink_schedule(session: Session, schedule_id: int) -> Schedules | tuple[bool, str]:
    try:
        schedule = session.query(Schedules).get(schedule_id)
        if not schedule:
            return True, "Quest or schedule not found"

        if schedule.quest_id:
            schedule.quest_id = None
            session.commit()
            return schedule
        return True, "Schedule is not linked to anyone"
    except Exception as ex:
        return True, str(ex)


def add_schedule(session: Session, request) -> Schedules | tuple[bool, str]:
    try:
        if request.questId is not None and not session.query(Quests).get(request.questId):
            return True, "Schedule can't be added. Quest not exists"

        schedule = Schedules(
            quest_id=request.questId,
            date=request.date,
            is_busy=request.isBusy
        )
        session.add(schedule)
        session.commit()
        return schedule
    except Exception as ex:
        return True, str(ex)


def delete_schedule(session: Session, id: int) -> bool | tuple[bool, str]:
    try:
        schedule = session.query(Schedules).get(id)
        if schedule:
            session.delete(schedule)
            session.commit()
            return True
        return True, "Schedule is not exists"
    except Exception as ex:
        return True, str(ex)


def get_service(session: Session):
    try:
        return session.query(Services).all()
    except Exception as ex:
        return True, str(ex)


def add_service(session: Session, data) -> Services | tuple[bool, str]:
    try:
        new_service = Services(
            name=data.name,
            text=data.text,
            price=data.price,
            quest_id=data.questId
        )
        session.add(new_service)
        session.commit()
        return new_service
    except Exception as ex:
        return True, str(ex)


def link_services(session: Session, quest_id: int, service_id: int) -> bool | tuple[bool, str]:
    try:
        quest = session.query(Quests).get(quest_id)
        service = session.query(Services).get(service_id)
        if quest and service:
            if service.quest_id is not None:
                return True, "Service already linked to quest"

            service.quest_id = quest.id
            session.commit()
            return True
        return True, "Quest or service not exists"
    except Exception as ex:
        return True, str(ex)


def unlink_services(session: Session, service_id: int) -> bool | tuple[bool, str]:
    try:
        service = session.query(Services).get(service_id)
        if not service:
            return True, "Quest or service not exists"

        if service and service.quest_id:
            service.quest_id = None
            session.commit()
            return True
        return True, "Service is not linked to anyone"
    except Exception as ex:
        return True, str(ex)


def delete_service(session: Session, id: int) -> bool | tuple[bool, str]:
    try:
        service = session.query(Services).get(id)
        if service:
            session.delete(service)
            session.commit()
            return True
        return True, "Service not found"
    except Exception as ex:
        return True, str(ex)


def get_schedule_by_quest_id(session: Session, id: int):
    try:
        return session.query(Schedules).filter(Schedules.quest_id == id).all()
    except Exception as ex:
        return True, str(ex)


def get_service_by_quest_id(session: Session, id: int):
    try:
        services = session.query(Services).filter(Services.quest_id == id).all()
        return services
    except Exception as ex:
        return True, str(ex)


def _get_quest_by_id(session: Session, id: int):
    try:
        return session.query(Quests).get(id)
    except Exception as ex:
        return True, str(ex)


def get_quest_by_slug(session: Session, slug: str) -> Quests | tuple[bool, str]:
    try:
        quest = session.query(Quests).filter(Quests.slug == slug).first()
        if quest:
            return quest
        return True, "Квест не найден"
    except Exception as ex:
        return True, str(ex)


def add_booking(session: Session, visitor_data) -> Orders | tuple[bool, str]:
    try:
        visitor = session.query(Visitors).filter(Visitors.phone == visitor_data.phone).first()

        if not visitor:
            visitor = Visitors(
                name=visitor_data.name,
                email=visitor_data.email,
                phone=visitor_data.phone,
                age=visitor_data.age
            )
            session.add(visitor)

        order = Orders(
            visitor_id=visitor.id,
            quest_id=visitor_data.questId,
            pick_hard=visitor_data.pickHard,
            pick_horror=visitor_data.pickHorror,
            pick_players=visitor_data.pickPlayers,
            pick_actors=visitor_data.pickActors,
            pick_date_id=visitor_data.pickDate
        )
        session.add(order)

        if visitor_data and visitor_data.services:
            for service in visitor_data.services:
                session.add(OrderToService(
                    order_id=order.id,
                    service_id=service
                ))
        session.commit()
        return order
    except Exception as ex:
        return True, str(ex)


def get_reviews(session: Session, quest_id: int):
    try:
        reviews = session.query(Reviews).filter(Reviews.quest_id == quest_id).all()
        return reviews
    except Exception as ex:
        return True, str(ex)


def get_all_hards(session: Session) -> list[any] | tuple[bool, str]:
    try:
        return session.query(Hard).all()
    except Exception as ex:
        return True, str(ex)


def get_all_horrors(session: Session) -> list[any] | tuple[bool, str]:
    try:
        return session.query(Horror).all()
    except Exception as ex:
        return True, str(ex)


def get_all_quests(session: Session, is_user: bool = False) -> list[any] | tuple[bool, str]:
    try:
        if is_user:
            condition = Quests.is_hide == False
            return session.query(Quests).filter(condition).all()
        else:
            return session.query(Quests).all()
    except Exception as ex:
        return True, str(ex)


def get_all_visitors(session: Session) -> list[Visitors] | tuple[bool, str]:
    try:
        return session.query(Visitors, Orders).filter(Visitors.id == Orders.visitor_id).all()
    except Exception as ex:
        return True, str(ex)


def add_quest(session: Session, data) -> Quests | tuple[bool, str]:
    try:
        new = Quests(
            name=data.name,
            slug=data.slug,
            description=data.description if data.description else "Здесь может быть ваше описание",
            legend=data.legend,
            price=data.price,
            min_players=data.minPlayers,
            max_players=data.maxPlayers,
            count_actors=data.countActors,
            hard_id=data.hardId,
            horror_id=data.horrorId,
            play_time=data.playTime,
            is_hide=data.isHide,
            my_erp_id=data.myErpId if data.myErpId else None,
        )
        session.add(new)
        session.commit()
        return new
    except Exception as ex:
        return True, str(ex)


def remove_quest(session: Session, id: int) -> bool | tuple[bool, str]:
    try:
        quest = session.query(Quests).get(id)
        quest_photos = session.query(Gallery).filter(Gallery.quest_id == id).all()
        services = session.query(Services).filter(Services.quest_id == id).all()
        if quest:
            for q in quest_photos:
                session.delete(q)

            for s in services:
                session.delete(s)

            session.delete(quest)
            session.commit()
            return True
        return True, "Квест не найден"
    except Exception as ex:
        return True, str(ex)


def get_hards(session: Session) -> list[any] | tuple[bool, str]:
    try:
        return session.query(Hard).all()
    except Exception as ex:
        return True, str(ex)


def add_hards(session: Session, name: str) -> Hard | tuple[bool, str]:
    try:
        hard = session.query(Hard).filter(Hard.name == name).first()
        if not hard:
            new = Hard(name=name)
            session.add(new)
            session.commit()
            return new
        return True, "Сложность уже существует"
    except Exception as ex:
        return True, str(ex)


def get_horrors(session: Session) -> list[any] | tuple[bool, str]:
    try:
        return session.query(Horror).all()
    except Exception as ex:
        return True, str(ex)


def add_horrors(session: Session, name: str) -> Horror | tuple[bool, str]:
    try:
        horror = session.query(Horror).filter(Horror.name == name).first()
        if not horror:
            new = Horror(name=name)
            session.add(new)
            session.commit()
            return new
        return True, "Страх уже существует"
    except Exception as ex:
        return True, str(ex)


def delete_hards(session: Session, id: int):
    try:
        hard = session.query(Hard).get(id)
        if hard:
            session.delete(hard)
            session.commit()
            return True
        return True, "Сложность не существует"
    except Exception as ex:
        return True, str(ex)


def delete_horrors(session: Session, id: int):
    try:
        horror = session.query(Horror).get(id)
        if horror:
            session.delete(horror)
            session.commit()
            return True
        return True, "Страх не существует"
    except Exception as ex:
        return True, str(ex)


def delete_photo(session: Session, id: int) -> bool | tuple[bool, str]:
    try:
        photo = session.query(Gallery).get(id)
        if photo:
            if os.path.exists(photo.photo):
                os.remove(photo.photo)

            session.delete(photo)
            session.commit()
            return True
        return True, "Фото не найдено"
    except Exception as ex:
        return True, str(ex)


def hide_quest(session: Session, id: int) -> bool | tuple[bool, str]:
    try:
        quest: Quests = session.query(Quests).get(id)
        if quest.is_hide:
            quest.is_hide = False
        else:
            quest.is_hide = True
        session.commit()
        return True
    except Exception as ex:
        return True, str(ex)


def update_quest(session: Session, data, id: int) -> bool | tuple[bool, str]:
    try:
        if not data.myErpId:
            my_erp_id = None
        else:
            my_erp_id = int(data.myErpId)

        quest: Quests = session.query(Quests).get(id)

        if quest:
            quest.name = data.name,
            quest.slug = data.slug,
            quest.description = data.description,
            quest.legend = data.legend,
            quest.price = data.price,
            quest.min_players = data.minPlayers,
            quest.max_players = data.maxPlayers,
            quest.count_actors = data.countActors,
            quest.hard_id = data.hardId,
            quest.horror_id = data.horrorId,
            quest.play_time = data.playTime,
            quest.is_hide = data.isHide
            quest.age_limit = data.ageLimit
            quest.my_erp_id = my_erp_id
            session.commit()
            return quest
        return True, "Квест не найден"
    except Exception as ex:
        return True, str(ex)


def get_all_reviews(session: Session, quest_id: int):
    try:
        if quest_id is not None:
            return session.query(Reviews).filter(Reviews.quest_id == quest_id).all()
        else:
            return session.query(Reviews).all()
    except Exception as ex:
        return True, str(ex)


def add_review(session: Session, data):
    try:
        review = Reviews(
            visitor=data.visitor,
            message=data.message,
            stars=data.stars,
            quest_id=data.questId
        )
        session.add(review)
        session.commit()
        return review
    except Exception as ex:
        return True, str(ex)


def delete_review(session: Session, id: int):
    try:
        review = session.query(Reviews).get(id)
        if review:
            session.delete(review)
            session.commit()
            return True
        return False, "Отзыв не найден"
    except Exception as ex:
        return True, str(ex)
