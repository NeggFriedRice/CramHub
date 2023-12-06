from main import ma

# Create thread with Marshmallow
class ThreadSchema(ma.Schema):
    class Meta:
        fields = ("id", "category", "title", "date", "description", "link")
