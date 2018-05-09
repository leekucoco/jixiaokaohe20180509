from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from datetime import datetime
# from .models import UserFav
from .models import UserUploadBaseFiles
# from goods.serializers import GoodsSerializer


# class UserFavDetailSerializer(serializers.ModelSerializer):
#     goods = GoodsSerializer()
#
#     class Meta:
#         model = UserFav
#         fields = ("goods", "id")
#
#
# class UserFavSerializer(serializers.ModelSerializer):
#     user = serializers.HiddenField(
#         default=serializers.CurrentUserDefault()
#     )
#
#     class Meta:
#         model = UserFav
#         validators = [
#             UniqueTogetherValidator(
#                 queryset=UserFav.objects.all(),
#                 fields=('user', 'goods'),
#                 message="已经收藏"
#             )
#         ]
#
#         fields = ("user", "goods", "id")
#
#
# class LeavingMessageSerializer(serializers.ModelSerializer):
#     user = serializers.HiddenField(
#         default=serializers.CurrentUserDefault()
#     )
#     add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')
#     class Meta:
#         model = UserLeavingMessage
#         fields = ("user", "message_type", "subject", "message", "file", "id" ,"add_time")

class UploadFilesSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')
    update_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')
    filename = serializers.CharField(read_only=True,)
    def create(self, validated_data):
        user = self.context["request"].user
        filename = validated_data["file"].name
        validated_data["filename"] = filename
        existed = UserUploadBaseFiles.objects.filter(user=user,filename=filename)
        if existed:
            # existed.save()
            # existed.message = validated_data["message"]
            # existed.save()
            existed[0].update_time = datetime.now()
            existed[0].save()
            return existed[0]
        else:
            existed = UserUploadBaseFiles.objects.create(**validated_data)

            return existed
    class Meta:
        model = UserUploadBaseFiles
        fields = "__all__"

# class AddressSerializer(serializers.ModelSerializer):
#     user = serializers.HiddenField(
#         default=serializers.CurrentUserDefault()
#     )
#     add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')
#
#     class Meta:
#         model = UserAddress
#         fields = ("id", "user", "province", "city", "district", "address", "signer_name", "add_time", "signer_mobile")

