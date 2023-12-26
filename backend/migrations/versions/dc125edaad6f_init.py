"""init

Revision ID: dc125edaad6f
Revises: 
Create Date: 2023-08-21 11:06:23.791401

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dc125edaad6f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True, nullable=False),
        sa.Column("username", sa.String(64), unique=True, nullable=False),
        sa.Column("password", sa.String(255), nullable=False)
    )
    op.execute("INSERT INTO users (username, password) VALUES ('admin', 'admin');")

    op.create_table(
        "hards",
        sa.Column("id", sa.Integer, primary_key=True, nullable=False),
        sa.Column("name", sa.String(32), nullable=False, unique=True)
    )
    op.execute("INSERT INTO hards (id, name) VALUES (1, 'Легко'), (2, 'Нормально'), (3, 'Сложно');")

    op.create_table(
        "horrors",
        sa.Column("id", sa.Integer, primary_key=True, nullable=False),
        sa.Column("name", sa.String(32), nullable=False, unique=True)
    )
    op.execute("INSERT INTO horrors (id, name) VALUES (1, 'Не страшно'), (2, 'Мурашки по коже'), (3, 'Спасите меня!!!');")

    op.create_table(
        "quests",
        sa.Column("id", sa.Integer, primary_key=True, nullable=False),
        sa.Column("name", sa.String(64), nullable=False),
        sa.Column("slug", sa.String(64), nullable=False, unique=True),
        sa.Column("description", sa.String(64), nullable=False),
        sa.Column("legend", sa.Text, server_default="Здесь может быть ваша легенда"),
        sa.Column("files", sa.JSON),
        sa.Column("price", sa.Integer, server_default=str(0)),
        sa.Column("min_players", sa.Integer, server_default=str(1), nullable=False),
        sa.Column("max_players", sa.Integer, server_default=str(1), nullable=False),
        sa.Column("count_actors", sa.Integer, server_default=str(1), nullable=False),
        sa.Column("is_hide", sa.Boolean, server_default=str(1)),
        sa.Column("horror_id", sa.Integer, nullable=False),
        sa.Column("hard_id", sa.Integer, nullable=False),
        sa.Column("play_time", sa.Integer, nullable=False, server_default=str(60)),
        sa.Column("age_limit", sa.Integer, server_default=str(18))
    )
    op.create_foreign_key("fk_horror_id", "quests", "horrors", ["horror_id"], ["id"])
    op.create_foreign_key("fk_hard_id", "quests", "hards", ["hard_id"], ["id"])
    op.execute("INSERT INTO quests (name, slug, description, legend, price, min_players, max_players, horror_id, hard_id)"
               " VALUES ('Five Nights at Freddys', 'FNAF', 'Квест Перфоманс', 'В далекой и мрачной пиццерии `Кантринио Карнавалло` царило призрачное молчание. Все было закрыто, кроме одной комнаты, где четыре друга-аниматронника обустраивались для ночного отдыха. Фредди Фазбер, Чика, Бонни и Фокси ожидали следующего дня, чтобы вновь порадовать посетителей пиццерии своими живыми и веселыми выступлениями. Они не знали, что их счастливое время скоро закончится. В тот вечер пиццерию охранял старый Джордж, который долгие годы бодрился о старте каждого нового дня, наблюдая за атмосферой, которую создавали аниматронники. Но Джордж никогда не догадывался о темных силах, скрывающихся в недрах этих кукол. Как только наступила полночь, аниматронники бессчастного охранника Джорджа превратили в свою жертву.Джордж успел нажать тревожную кнопку и приехала группа оперативного реагирования. Сразу, после их захода в пиццерию двери закрылись, а с другой стороны вентиляции послышался леденящий мозг хохот. Ваша задача покончить с этими аниматронниками раз и навсегда, только тогда заблудшие души обретут покой и отпустят вас живыми...'"
               ", 4500, 2, 4, 2, 3);")

    op.create_table(
        "schedules",
        sa.Column("id", sa.Integer, primary_key=True, nullable=False),
        sa.Column("date", sa.DateTime),
        sa.Column("quest_id", sa.Integer),
        sa.Column("is_busy", sa.Boolean, server_default=str(0))
    )
    op.create_foreign_key("fk_quest_id5", "schedules", "quests", ["quest_id"], ["id"])
    op.execute("INSERT INTO schedules (date, quest_id) VALUES ('2023-08-20', 1);")

    op.create_table(
        "visitors",
        sa.Column("id", sa.Integer, primary_key=True, nullable=False),
        sa.Column("name", sa.String(64), nullable=False),
        sa.Column("email", sa.String(64)),
        sa.Column("phone", sa.String(15), nullable=False),
        sa.Column("age", sa.Integer, server_default=str(18))
    )
    op.execute("INSERT INTO visitors (name, email, phone, age) VALUES ('Vadim', 'task@example.com', '11111111111', 19);")
    op.execute("INSERT INTO visitors (name, email, phone, age) VALUES ('Айзек Азимов', 'a.asimov@example.com', '11111111111', 19);")

    op.create_table(
        "orders",
        sa.Column("id", sa.Integer, primary_key=True, nullable=False),
        sa.Column("visitor_id", sa.Integer, nullable=False),
        sa.Column("quest_id", sa.Integer, nullable=False),
        sa.Column("pick_players", sa.Integer, server_default=str(1)),
        sa.Column("pick_actors", sa.Integer, server_default=str(1)),
        sa.Column("pick_hard", sa.Integer, server_default=str(1)),
        sa.Column("pick_horror", sa.Integer, server_default=str(1)),
        sa.Column("pick_date_id", sa.Integer, nullable=False)
    )
    op.create_foreign_key("fk_hard_iddqw", "orders", "hards", ["pick_hard"], ["id"])
    op.create_foreign_key("fk_horror_idddsas", "orders", "horrors", ["pick_horror"], ["id"])
    op.create_foreign_key("fk_pick_date_idd", "orders", "schedules", ["pick_date_id"], ["id"])
    op.execute("INSERT INTO orders (visitor_id, quest_id, pick_players, pick_actors, pick_date_id) VALUES (1, 1, 2, 1, 1);")

    op.create_table(
        "reviews",
        sa.Column("id", sa.Integer, primary_key=True, nullable=False),
        sa.Column("visitor", sa.String, nullable=False),
        sa.Column("message", sa.String(64), nullable=False),
        sa.Column("stars", sa.Text, server_default=str(1)),
        sa.Column("quest_id", sa.Integer, nullable=True)
    )
    op.execute("INSERT INTO reviews (visitor, message, stars) VALUES ('task', 'All right', 5);")
    op.execute("INSERT INTO reviews (visitor, message, stars) VALUES ('Айзек Азимов', 'Роботы атакуют людей!!!', 1);")
    op.create_foreign_key("fk_review_idd1", "reviews", "quests", ["quest_id"], ["id"])

    op.create_table(
        "services",
        sa.Column("id", sa.Integer, primary_key=True, nullable=False),
        sa.Column("name", sa.String(64), nullable=False),
        sa.Column("text", sa.Text, nullable=False),
        sa.Column("price", sa.Integer, server_default=str(0)),
        sa.Column("quest_id", sa.Integer)
    )
    op.create_foreign_key("fk_quest_idddd2", "services", "quests", ["quest_id"], ["id"])
    op.execute("INSERT INTO services (name, text, price, quest_id) VALUES ('Насилие', 'Разрешается избивать игроков', 10000, 1);")


    op.create_table(
        "order_to_service",
        sa.Column("id", sa.Integer, primary_key=True, nullable=False),
        sa.Column("order_id", sa.Integer, nullable=False),
        sa.Column("service_id", sa.Integer, nullable=False)
    )
    op.create_foreign_key("fk_service_iddd3", "order_to_service", "services", ["service_id"], ["id"])
    op.create_foreign_key("fk_order_iddd4", "order_to_service", "orders", ["order_id"], ["id"])


def downgrade() -> None:
    pass
