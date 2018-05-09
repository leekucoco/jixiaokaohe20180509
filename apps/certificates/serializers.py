# -*- coding: utf-8 -*-

from rest_framework import serializers

from datetime import datetime,date
from .models import Cerficates,IndexUserCertificate
class CerficateSerializer(serializers.ModelSerializer):
    # certificate_user= serializers.HyperlinkedRelatedField(
    #     many=True,
    #     read_only=True,
    #     view_name='indexusercertificate-detail'
    # )
    class Meta:
        model = Cerficates
        fields = ("id", 'name','score',)

class IndexUserCertificateSerializer(serializers.ModelSerializer):
    certificate = serializers.StringRelatedField()
    certificatemanager = serializers.HyperlinkedIdentityField(
        # read_only=True,
         view_name='indexusercertificate-detail'

    )
    name = serializers.SerializerMethodField()
    score = serializers.SerializerMethodField()
    add_time = serializers.DateTimeField(read_only=True)
    class Meta:
        model = IndexUserCertificate
        fields = ("id","user", "certificate", "name","score","image","certificatemanager","add_time")
    def get_name(self,obj):
        return obj.certificate.name
    def get_score(self,obj):
        return obj.certificate.score
class IndexUserCertificateSerializer2(serializers.ModelSerializer):
    add_time = serializers.DateTimeField(read_only=True)
    class Meta:
        model = IndexUserCertificate
        fields = ("user", "certificate", "image","add_time")
    def update(self, instance, validated_data):
        instance.update_time = datetime.now()
        instance.save()
        return instance
