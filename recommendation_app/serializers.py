from rest_framework import serializers

class RecommendationSerializer(serializers.Serializer):
   """Your data serializer, define your fields here."""
   data = serializers.CharField(max_length=200)
