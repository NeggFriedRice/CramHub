from main import ma

# Create thread with Marshmallow
class ThreadSchema(ma.Schema):
    class Meta:
        fields = ("id", "category", "title", "date", "description", "link")

thread_schema = ThreadSchema()
threads_schema = ThreadSchema(many=True)