from main import ma

# Create thread with Marshmallow
class CommentSchema(ma.Schema):
    class Meta:
        fields = ("date", "rating", "review")

comment_schema = CommentSchema()
comments_schema = CommentSchema(many=True)