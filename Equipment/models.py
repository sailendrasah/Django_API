from mongoengine import Document, StringField,IntField,BooleanField

class userRegister(Document):
    name = StringField(required=True)
    email = StringField(required=True, unique=True)
    password = StringField(required=True)
    phone = StringField(required=True)
    role = StringField(required = True,choice =['USER','EQUIPMENT_OWNER'],default ='')
    otp = IntField()
    is_verified = BooleanField(default=False)