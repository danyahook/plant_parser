from peewee import CharField, Model, SqliteDatabase

db = SqliteDatabase('plants.db')


class PlantNames(Model):
    plant_name = CharField(max_length=256)
    file_name = CharField(max_length=256)

    class Meta:
        database = db
        db_table = 'plant_names'


def create_tables():
    with db:
        db.create_tables([PlantNames])
