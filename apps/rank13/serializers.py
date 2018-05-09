# -*- coding: utf-8 -*-

from rest_framework import serializers
from .models import Rank13Coefficent,Agent,Post,Rank13Demands
class Rank13CoefficentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rank13Coefficent
        fields = "__all__"
class Rank13DemandsSerializer(serializers.ModelSerializer):
    #agent = serializers.StringRelatedField()
    #rank  = serializers.StringRelatedField()
    #post = serializers.CharField()
    class Meta:
        model = Rank13Demands
        fields = "__all__"

class AgentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agent
        fields = ("name",)

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ("name",)