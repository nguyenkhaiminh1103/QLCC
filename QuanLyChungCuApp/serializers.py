from rest_framework import serializers
from .models import User, Payment, RelativeAccess

class UserSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['avatar'] = instance.avatar.url if instance.avatar else ''
        return data

    class Meta:
        model = User
        fields = [
            'id', 'username', 'password', 'first_name', 'last_name',
            'phone', 'address', 'role', 'avatar', 'profile_completed'
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(user.password)

        # Nếu tạo mới bằng mật khẩu mặc định -> chưa hoàn tất hồ sơ
        if user.password == 'changeme123':
            user.profile_completed = False

        user.save()
        return user


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
        read_only_fields = ['user', 'timestamp']

class RelativeAccessSerializer(serializers.ModelSerializer):
    class Meta:
        model = RelativeAccess
        fields = '__all__'
        read_only_fields = ['user', 'approved']
