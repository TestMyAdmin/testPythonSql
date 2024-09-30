from tortoise import Tortoise, fields
from tortoise.models import Model


class Item(Model):
    id = fields.IntField(pk=True)
    col1 = fields.TextField(null=True)
    col2 = fields.TextField(null=True)
    col3 = fields.TextField(null=True)

    class Meta:
        table = "items"


async def init_db():
    await Tortoise.init(
        db_url='sqlite://data.db',
        modules={'models': ['__main__']}
    )
    await Tortoise.generate_schemas()
