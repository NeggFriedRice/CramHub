from main import ma
from marshmallow.validate import Length

# Create user with Marshmallow
class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "password", "email", "cohort")
        password = ma.String(validate=Length(min=6))

user_schema = UserSchema()
users_schema = UserSchema(many=True)