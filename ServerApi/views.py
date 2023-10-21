from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from ServerApi.serializer import *
from ServerCommon.models import *


class ArtworksView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @staticmethod
    def get(request):
        query = request.query_params.get('query', None)
        artwork_id = request.query_params.get('artwork_id', None)
        if artwork_id:
            artworks = Artworks.objects.filter(artwork_id=artwork_id)
        else:
            if query == 'True':
                artworks = Artworks.objects.filter(beacons__isnull=True)
            else:
                artworks = Artworks.objects.all()
        serializer = ArtworksSerializer(artworks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


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
