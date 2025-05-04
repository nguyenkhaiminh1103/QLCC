from rest_framework import viewsets, status, permissions, parsers
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import User, Payment, RelativeAccess
from .serializers import UserSerializer, PaymentSerializer, RelativeAccessSerializer
from rest_framework.permissions import IsAdminUser
from QuanLyChungCuApp import serializers

class UserViewSet(viewsets.ViewSet):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
    parser_classes = [parsers.MultiPartParser]

    def get_permissions(self):
        if self.action == 'create':
            return [IsAdminUser()]  # Chỉ admin được phép tạo user
        return super().get_permissions()

    def create(self, request):
        """Quản trị viên tạo tài khoản cư dân"""
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(self.serializer_class(user).data, status=status.HTTP_201_CREATED)

    @action(methods=['get', 'patch'], url_path='current-user', detail=False,
            permission_classes=[permissions.IsAuthenticated])
    def get_current_user(self, request):
        user = request.user

        if request.method == 'PATCH':
            data = request.data

            for field in ['first_name', 'last_name', 'phone', 'address', 'avatar']:
                if field in data:
                    setattr(user, field, data[field])

            if 'password' in data:
                user.set_password(data['password'])

            # Kiểm tra điều kiện hoàn tất hồ sơ
            if user.avatar and not user.check_password('changeme123'):
                user.profile_completed = True
            else:
                user.profile_completed = False

            user.save()

        return Response(self.serializer_class(user).data)

    @action(methods=['patch'], detail=True, permission_classes=[permissions.IsAdminUser])
    def deactivate(self, request, pk=None):
        user = self.get_object()
        user.is_active = False
        user.save()
        return Response({'message': 'Tài khoản đã bị khóa.'})


from rest_framework.exceptions import PermissionDenied

class ProtectedViewSet(viewsets.ViewSet):
    def list(self, request):
        if not request.user.is_staff and not request.user.profile_completed:
            raise PermissionDenied("Bạn cần đổi mật khẩu và tải lên ảnh đại diện để sử dụng hệ thống.")
        # Cho phép nếu đủ điều kiện



class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    parser_classes = [parsers.MultiPartParser]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Payment.objects.all()
        return Payment.objects.filter(user=user)

class RelativeAccessViewSet(viewsets.ModelViewSet):
    serializer_class = RelativeAccessSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return RelativeAccess.objects.all()
        return RelativeAccess.objects.filter(user=user)
