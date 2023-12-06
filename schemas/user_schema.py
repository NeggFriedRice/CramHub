from main import ma

# Create user with Marshmallow
class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "email", "cohort")

user_schema = UserSchema()
users_schema = UserSchema(many=True)