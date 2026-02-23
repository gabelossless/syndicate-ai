from tortoise.models import Model
from tortoise import fields
from tortoise import Tortoise, run_async

class User(Model):
    id = fields.IntField(pk=True)
    telegram_id = fields.IntField(unique=True)
    username = fields.CharField(max_length=255, null=True)
    joined_at = fields.DatetimeField(auto_now_add=True)
    is_active = fields.BooleanField(default=True)

class ApiKey(Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField('models.User', related_name='keys')
    exchange_id = fields.CharField(max_length=255)
    encrypted_key = fields.CharField(max_length=255)
    encrypted_secret = fields.CharField(max_length=255)
    label = fields.CharField(max_length=255, default="Main")
    created_at = fields.DatetimeField(auto_now_add=True)

class Trade(Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField('models.User', related_name='trades')
    symbol = fields.CharField(max_length=255)
    side = fields.CharField(max_length=255) # BUY, SELL
    amount = fields.FloatField()
    price = fields.FloatField()
    cost = fields.FloatField() # amount * price
    timestamp = fields.DatetimeField(auto_now_add=True)
    pnl = fields.FloatField(null=True) # Realized PnL
    status = fields.CharField(max_length=255, default="OPEN") # OPEN, CLOSED

class MediaAsset(Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField('models.User', related_name='media')
    title = fields.CharField(max_length=255)
    media_type = fields.CharField(max_length=255, default="audio") # audio, reel, video
    genre = fields.CharField(max_length=255, null=True)
    bpm = fields.IntField(null=True)
    price = fields.FloatField(default=0.0)
    file_path = fields.CharField(max_length=500)
    duration = fields.FloatField(default=0.0) # Length in seconds
    created_at = fields.DatetimeField(auto_now_add=True)

class Play(Model):
    id = fields.IntField(pk=True)
    media = fields.ForeignKeyField('models.MediaAsset', related_name='plays')
    user = fields.ForeignKeyField('models.User', related_name='listens', null=True)
    timestamp = fields.DatetimeField(auto_now_add=True)

class Sale(Model):
    id = fields.IntField(pk=True)
    media = fields.ForeignKeyField('models.MediaAsset', related_name='sales')
    buyer = fields.ForeignKeyField('models.User', related_name='purchases')
    amount = fields.FloatField()
    timestamp = fields.DatetimeField(auto_now_add=True)

class StatDaily(Model):
    id = fields.IntField(pk=True)
    media = fields.ForeignKeyField('models.MediaAsset', related_name='daily_stats')
    date = fields.DateField()
    play_count = fields.IntField(default=0)
    sale_count = fields.IntField(default=0)
    revenue = fields.FloatField(default=0.0)

    class Meta:
        unique_together = (('media', 'date'),)

async def init_db():
    await Tortoise.init(
        db_url='sqlite://syndicate.db',
        modules={'models': ['database.models']}
    )
    # Generate schema is fine for beta, drop handles test resets if needed
    await Tortoise.generate_schemas()
    print("Tortoise-ORM Database Initialized")

if __name__ == "__main__":
    run_async(init_db())
