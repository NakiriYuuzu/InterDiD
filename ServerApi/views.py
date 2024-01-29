import os

from django.contrib.auth.hashers import make_password
from django.utils import timezone
from rest_framework import status, permissions
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response

from InterDiD import settings
from ServerApi.utils.permission import IsSuperuser
from ServerApi.serializer import *
from ServerCommon import print_success, print_error
from ServerCommon.models import *


class GamesView(APIView):
    """
    使用模型為 Games : ServerCommon.models.Games
    處理遊戲相關的請求，設定難易度，排行榜（通關時間）
    """
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.request.method in ['GET', 'POST']:
            self.permission_classes = [permissions.AllowAny]
        return super(GamesView, self).get_permissions()

    @staticmethod
    def check_required_fields(data, required_fields):
        missing = [field for field in required_fields if field not in data]
        if missing:
            raise ValidationError(f'Missing fields: {missing}')

    @staticmethod
    def get(request):
        types = request.query_params.get('types', None)

        if types == 'setting':
            serializer = GamesSerializer(Games.objects.all(), many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        elif types == 'ranking':
            game_id = request.query_params.get('game_id', None)
            if not game_id:
                game_id = Games.objects.filter(game_diff_select=1)[0].game_id
                game = UserGames.objects.filter(game_id=game_id)
                serializer = UserGamesSerializer(game, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                game = UserGames.objects.filter(game_id=game_id)
                serializer = UserGamesSerializer(game, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)

        elif types == 'select':
            query = Games.objects.filter(game_diff_select=1)
            serializer = GamesSerializer(query, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        else:
            return Response({'error': 'No valid identifier provided'}, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def post(request):
        types = request.data.get('types', None)

        if types == 'setting':
            try:
                required_fields = ['game_name', 'game_diff']
                GamesView.check_required_fields(request.data, required_fields)
                game_name = request.data.get('game_name')
                game_diff = request.data.get('game_diff')

                if game_diff == 1:
                    return Response({'error': 'Game difficulty cannot be set to 1'}, status=status.HTTP_400_BAD_REQUEST)

                game, created = Games.objects.update_or_create(
                    game_name=game_name,
                    defaults={'game_diff': game_diff, 'game_diff_select': 0}
                )
                message = 'Game created successfully' if created else 'Game updated successfully'
                return Response({'message': message}, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        elif types == 'ranking':
            try:
                # 驗證欄位
                required_fields = ['game_id', 'unique_code', 'play_date']
                GamesView.check_required_fields(request.data, required_fields)

                # 取得欄位
                game_id = request.data.get('game_id')
                unique_code = request.data.get('unique_code')
                play_date = request.data.get('play_date')

                # 驗證是否有此用戶
                user = Users.objects.get(unique_code=unique_code)
                if not user:
                    return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

                # 檢查是否有重複的 user_id
                current_selected = UserGames.objects.filter(user_id=user.user_id, game_id=game_id)
                if current_selected:
                    if float(current_selected[0].play_date) > float(play_date):
                        current_selected.update(play_date=play_date)
                else:
                    UserGames.objects.create(user_id=user.user_id, game_id=game_id, play_date=play_date)

                return Response({'message': 'Game ranking successfully'}, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        elif types == 'select':
            try:
                # 驗證欄位
                required_fields = ['game_id']
                GamesView.check_required_fields(request.data, required_fields)

                # 取得欄位
                game_id = request.data.get('game_id')

                # 檢查是否有重複的 game_diff_select = 1
                current_selected = Games.objects.filter(game_diff_select=1)
                if current_selected:
                    current_selected.update(game_diff_select=0)

                # 更新欄位
                Games.objects.filter(game_id=game_id).update(game_diff_select=1)
                return Response({'message': 'Game difficulty successfully'}, status=status.HTTP_201_CREATED)
            except ValidationError as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
            except ValueError:
                return Response({'error': 'Invalid amount value'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'No valid identifier provided'}, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def put(request):
        pass

    @staticmethod
    def delete(request):
        types = request.data.get('types', None)

        if types == 'setting':
            game_id = request.data.get('game_id', None)
            if not game_id:
                return Response({'error': 'Game ID is required'}, status=status.HTTP_400_BAD_REQUEST)
            try:
                game = Games.objects.get(pk=game_id)
                # 檢查是否有 UserGames 正在使用該 Game
                if UserGames.objects.filter(game__game_id=game_id).exists():
                    return Response({'error': 'Cannot delete game as it is currently assigned to a user'},
                                    status=status.HTTP_400_BAD_REQUEST)
                game.delete()
                return Response({'message': 'Game deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'No valid identifier provided'}, status=status.HTTP_400_BAD_REQUEST)


class AccountsView(APIView):
    """
    這個是用於處理 Admin 相關的帳號，使用模型為 Accounts : ServerCommon.models.Accounts
    主要用於管理後台的帳號，包含新增、修改、刪除
    Superuser > Staff > None
    """
    permission_classes = [permissions.IsAuthenticated]

    @staticmethod
    def check_required_fields(data, required_fields):
        missing = [field for field in required_fields if field not in data]
        if missing:
            raise ValidationError(f'Missing fields: {missing}')

    @staticmethod
    def get(request):
        account_id = request.query_params.get('account_id', None)
        serializer = AccountsSerializer(Account.objects.filter(pk=account_id) if account_id else Account.objects.all(),
                                        many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def post(request):
        required_fields = ['amount', 'username']

        if not request.user.is_superuser:
            return Response({'error': 'Only admin can create accounts'}, status=status.HTTP_403_FORBIDDEN)

        try:
            AccountsView.check_required_fields(request.data, required_fields)

            amount = int(request.data['amount'])
            base_username = request.data['username']

            for i in range(1, amount + 1):
                username = f"{base_username}{i}"
                if Account.objects.filter(username=username).exists():
                    continue  # 如果用戶名已存在，則跳過並繼續下一個

                Account.objects.create(
                    username=username,
                    password=make_password(username),  # 設置默認密碼
                    is_staff=request.data.get('is_staff', False),
                    is_active=request.data.get('is_active', True),
                    is_superuser=request.data.get('is_superuser', False)
                )

        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError:
            return Response({'error': 'Invalid amount value'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': f'{amount} accounts created successfully'}, status=status.HTTP_201_CREATED)

    @staticmethod
    def put(request):
        required_fields = ['id']
        try:
            AccountsView.check_required_fields(request.data, required_fields)
            account_id = request.data['id']
            account = Account.objects.get(pk=account_id)

            AccountsView.update_account(request, account)

        except ValidationError as e:
            return Response({'error': e.detail}, status=status.HTTP_400_BAD_REQUEST)
        except Account.DoesNotExist as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)

        return Response({'message': 'Account updated successfully'}, status=status.HTTP_200_OK)

    @staticmethod
    def update_account(request, account):
        if request.data.get('password'):
            if request.user.id == account.id or request.user.is_superuser:
                account.set_password(request.data['password'])
            else:
                raise ValidationError('Only the owner or Admin can change the password')

        if request.user.is_superuser:
            account.is_superuser = request.data.get('is_superuser', account.is_superuser)
            account.is_staff = request.data.get('is_staff', account.is_staff) == 'true'
            account.username = request.data.get('username', account.username)
        else:
            if not request.data.get('username') == account.username:
                return Response({'error': 'Only Admin can change username'}, status=status.HTTP_403_FORBIDDEN)

        account.save()

    @staticmethod
    def delete(request):
        account_id = request.data.get('id')
        if not account_id:
            return Response({'error': 'Username is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = Account.objects.get(pk=account_id)
            user.delete()
        except Account.DoesNotExist:
            return Response({'error': 'Account not found'}, status=status.HTTP_404_NOT_FOUND)

        return Response({'message': 'Account deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


class UsersView(APIView):
    """
    使用模型為 Users : ServerCommon.models.Users
    處理用戶相關的請求 [記錄LineApi的用戶資料]
    """
    permission_classes = [permissions.IsAuthenticated, IsSuperuser]

    @staticmethod
    def get(request):
        today = timezone.now().date()
        users_today = Users.objects.filter(create_at__date=today).count()
        users_month = Users.objects.filter(create_at__month=today.month).count()
        users_total = Users.objects.all().count()
        user_id = request.query_params.get('user_id', None)
        if user_id:
            users = Users.objects.filter(user_id=user_id)
            serializer = UsersSerializer(users, many=True)
            return Response(serializer.field_name, status=status.HTTP_200_OK)
        else:
            data = {
                'users_today': users_today,
                'users_month': users_month,
                'users_total': users_total,
            }
            return Response(data, status=status.HTTP_200_OK)


class ArtworksView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = [permissions.AllowAny]
        return super(ArtworksView, self).get_permissions()

    @staticmethod
    def get(request):
        query = request.query_params.get('query', None)
        artwork_id = request.query_params.get('artwork_id', None)
        artwork_item_id = request.query_params.get('artwork_item_id', None)

        if artwork_item_id:
            artwork_items = ArtworkItems.objects.filter(artwork_item_id=artwork_item_id)
            serializer = ArtworkItemsSerializer(artwork_items, many=True)
        elif artwork_id:
            artworks = Artworks.objects.filter(artwork_id=artwork_id)
            serializer = ArtworksSerializer(artworks, many=True)
        else:
            if query == 'True':
                artworks = Artworks.objects.filter(beacons__isnull=True)
            else:
                artworks = Artworks.objects.all()
            serializer = ArtworksSerializer(artworks, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def post(request):
        # 检查是否提供了 'artworks' 字段
        if 'artworks' not in request.data and 'artwork_product_title' in request.data:
            # 只有 staff 和 superuser 可以创建 Artworks
            if not request.user.is_superuser and not request.user.is_staff:
                return Response({'error': 'Only admin or staff can create artworks'},
                                status=status.HTTP_403_FORBIDDEN)

            # 如果提供了 'artwork_product_title' 而没有提供 'artworks'，则创建新的 Artworks 实例
            artwork_data = {'product_title': request.data['artwork_product_title']}
            artwork_serializer = ArtworksSerializer(data=artwork_data)
            if artwork_serializer.is_valid():
                artwork = artwork_serializer.save()
                request.data['artworks'] = artwork.artwork_id
            else:
                return Response(artwork_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # 现在处理 ArtworkItems 的创建
        serializer = ArtworkItemsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def put(request):
        artwork_id = request.data.get('artwork_id', None)
        artwork_item_id = request.data.get('artwork_item_id', None)

        # 檢查是否是 Superuser 或 Staff
        if not request.user.is_superuser and not request.user.is_staff:
            return Response({'error': 'Only admin or staff can update artworks'}, status=status.HTTP_403_FORBIDDEN)

        if artwork_item_id:
            try:
                artwork_item = ArtworkItems.objects.get(artwork_item_id=artwork_item_id)
                serializer = ArtworkItemsSerializer(artwork_item, data=request.data, partial=True)

                # 先进行数据验证
                if serializer.is_valid():
                    # 如果有新的图片文件上传
                    new_image_file = request.FILES.get('artwork_item_image', None)
                    if new_image_file:
                        # 删除旧图片
                        ArtworksView.delete_image_file(artwork_item.artwork_item_image)

                    # 保存其他字段
                    serializer.save()
                    return Response(serializer.data)

                # 如果验证失败，返回错误
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            except ArtworkItems.DoesNotExist:
                return Response({'error': 'Artwork item not found'}, status=status.HTTP_404_NOT_FOUND)
        elif artwork_id:
            try:
                artwork = Artworks.objects.get(artwork_id=artwork_id)
                serializer = ArtworksSerializer(artwork, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except Artworks.DoesNotExist:
                return Response({'error': 'Artwork not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'error': 'No valid identifier provided'}, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def delete(request):
        artwork_id = request.query_params.get('artwork_id', None)
        artwork_item_id = request.query_params.get('artwork_item_id', None)

        # 檢查是否是 Superuser
        if not request.user.is_superuser:
            return Response({'error': 'Only admin can delete artworks'}, status=status.HTTP_403_FORBIDDEN)

        # 檢查是否有 Beacon 正在使用該 Artwork
        if artwork_id and Beacons.objects.filter(artworks__artwork_id=artwork_id).exists():
            return Response({'error': 'Cannot delete artwork as it is currently assigned to a beacon'},
                            status=status.HTTP_400_BAD_REQUEST)

        if artwork_item_id:
            try:
                artwork_item = ArtworkItems.objects.get(artwork_item_id=artwork_item_id)
                print_error(artwork_item.artworks.artwork_id)
                # 檢查是否只有一個 ArtworkItem
                if Artworks.objects.get(artwork_id=artwork_item.artworks.artwork_id).artwork_items.count() == 1:
                    return Response({'error': 'Cannot delete the only item in an artwork'},
                                    status=status.HTTP_400_BAD_REQUEST)
                # 刪除圖片文件
                ArtworksView.delete_image_file(artwork_item.artwork_item_image)
                artwork_item.delete()
                return Response({'message': 'Artwork item deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
            except ArtworkItems.DoesNotExist:
                return Response({'error': 'Artwork item not found'}, status=status.HTTP_404_NOT_FOUND)
        elif artwork_id:
            try:
                artwork = Artworks.objects.get(artwork_id=artwork_id)
                for item in artwork.artwork_items.all():
                    ArtworksView.delete_image_file(item.artwork_item_image)
                artwork.delete()
                return Response({'message': 'Artwork deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
            except Artworks.DoesNotExist:
                return Response({'error': 'Artwork not found'}, status=status.HTTP_404_NOT_FOUND)

        else:
            return Response({'error': 'No valid identifier provided'}, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def delete_image_file(image_field_file):
        if image_field_file:
            # 从 ImageFieldFile 对象获取文件名
            file_name = image_field_file.name
            # 构建完整的文件路径
            full_path = os.path.join(settings.MEDIA_ROOT, file_name)
            # 检查文件是否存在，并进行删除
            if os.path.exists(full_path):
                os.remove(full_path)
                print_success(f"Deleted Successfully: {full_path}")
            else:
                print_error(f"File Not Found: {full_path}")


class BeaconsView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsSuperuser]

    @staticmethod
    def get(request):
        beacon_id = request.query_params.get('beacon_id', None)
        beacons = Beacons.objects.filter(beacon_id=beacon_id) if beacon_id else Beacons.objects.all()
        serializer = BeaconsSerializer(beacons, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def post(request):
        beacon_data = {
            'beacon_name': request.data.get('beacon_name'),
            'beacon_uuid': request.data.get('beacon_uuid'),
            'artworks': request.data.get("artworks", None)
        }
        if not beacon_data['beacon_name'] or not beacon_data['beacon_uuid']:
            return Response({'error': 'Beacon name and uuid are required'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = BeaconsSerializer(data=beacon_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def put(request):
        beacon_id = request.data.get('beacon_id')
        if beacon_id is None:
            return Response({'error': 'Beacon ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            beacon = Beacons.objects.get(beacon_id=beacon_id)
        except Beacons.DoesNotExist:
            return Response({'error': 'Beacon not found'}, status=status.HTTP_404_NOT_FOUND)

        artwork_id = request.data.get("artworks", None)  # 默認值為 None
        if artwork_id:
            try:
                artwork = Artworks.objects.get(pk=artwork_id)
                beacon.artworks = artwork  # 更新 artwork
            except Artworks.DoesNotExist:
                return Response({'error': 'Artwork not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            beacon.artworks = None  # 將 artwork 設為 None

        serializer = BeaconsSerializer(beacon, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Beacon updated successfully'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def delete(request):
        beacon_id = request.data.get('beacon_id')  # 從請求數據中獲取 beacon_id
        if beacon_id is None:
            return Response({'error': 'Beacon ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            beacon = Beacons.objects.get(beacon_id=beacon_id)
        except Beacons.DoesNotExist:
            return Response({'error': 'Beacon not found'}, status=status.HTTP_404_NOT_FOUND)

        beacon.delete()
        return Response({'message': 'Beacon deleted successfully'}, status=status.HTTP_200_OK)
