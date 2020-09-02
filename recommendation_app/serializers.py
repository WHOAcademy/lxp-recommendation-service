from rest_framework import serializers

# {
#         "id": 1,
#         "title": "Nursing Leadership: Empowering Nurses in Latin America and the Caribbean",
#         "description": "This course aims to empower nurses in Latin America and the Caribbean by enhancing their understanding of nursing leadership and management principles that can be utilized in the practice of nursing.",
#         "duration_seconds": 18000,
#         "creation_date": "2020-07-13T12:45:26.401000Z",
#         "last_mod_date": "2020-08-11T10:38:29Z"
#     },

class RecommendationSerializer(serializers.Serializer):
   """Your data serializer, define your fields here."""
   id = serializers.IntegerField()
   title = serializers.CharField(max_length=200)
   description = serializers.CharField(max_length=500)
   duration_seconds = serializers.IntegerField()
   creation_date = serializers.DateTimeField()
   last_mod_date = serializers.DateTimeField()
