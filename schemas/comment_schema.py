from main import ma

# Create thread with Marshmallow
class CommentSchema(ma.Schema):
    class Meta:
        fields = ("id", "date", "rating", "review")
