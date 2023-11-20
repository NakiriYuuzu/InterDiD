import os

from rest_framework import status, permissions
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response

from InterDiD import settings
from ServerApi.serializer import *
from ServerCommon import print_success, print_error
from ServerCommon.models import *


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

        # 檢查是否有 Beacon 正在使用該 Artwork
        if artwork_id and Beacons.objects.filter(artworks__artwork_id=artwork_id).exists():
            return Response({'error': 'Cannot delete artwork as it is currently assigned to a beacon'},
                            status=status.HTTP_400_BAD_REQUEST)

        if artwork_item_id:
            try:
                artwork_item = ArtworkItems.objects.get(artwork_item_id=artwork_item_id)
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
    permission_classes = [permissions.IsAuthenticated]

    @staticmethod
    def get(request):
        beacon_id = request.query_params.get('beacon_id', None)
        if beacon_id:
            beacons = Beacons.objects.filter(beacon_id=beacon_id)
        else:
            beacons = Beacons.objects.all()
        serializer = BeaconsSerializer(beacons, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def post(request):
        artwork_id = request.data.get("artworks", None)  # 默認值為 None
        artwork = None
        if artwork_id:
            try:
                artwork = Artworks.objects.get(pk=artwork_id)
            except Artworks.DoesNotExist:
                return Response({'error': 'Artwork not found'}, status=status.HTTP_404_NOT_FOUND)

        # 驗證是否只有10 個 beacon
        beacons = Beacons.objects.all()
        if len(beacons) >= 10:
            return Response({'error': 'Total Beacon is limited to 10'}, status=status.HTTP_400_BAD_REQUEST)

        print(request.data)
        beacon_data = {
            'beacon_name': request.data.get('beacon_name'),
            'beacon_uuid': request.data.get('beacon_uuid'),
        }
        if not beacon_data['beacon_name'] or not beacon_data['beacon_uuid']:
            return Response({'error': 'Beacon name and uuid are required'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = BeaconsSerializer(data=beacon_data)
        if serializer.is_valid():
            beacon = serializer.save()
            if artwork:  # 只有在 artwork 不為 None 時才保存
                beacon.artworks = artwork
                beacon.save()
            return Response(BeaconsSerializer(beacon).data, status=status.HTTP_201_CREATED)

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
