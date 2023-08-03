from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Movie, Rating
from .serializers import MovieSerializer, RatingSerializer

# Create your views here.
class MovieViewSet(viewsets.ModelViewSet):
    serializer_class = MovieSerializer
    queryset = Movie.objects.all()

    # 備註：需搭配 postman軟體來測試 API
    @action(detail = True, methods=['POST'])
    def rate_movie(self, request, pk=None):
        # 這裡的判斷僅是確認傳來後端時，是否有 stars這個欄位，但不會確認型別、數值範圍等等的，如果要做這些判斷需要再自己寫檢查的邏輯
        if 'stars' in request.data:
            # 印出前端 url中的 pk值 (例如：http://127.0.0.1:8000/api/movies/1/rate_movie/，pk即為 1)
            print('pk:', pk)

            # 使用 pk再去找 movie資料表的資料
            movie = Movie.objects.get(id = pk)
            print("movie's title:", movie.title)

            response = {'message': "it's working"}
            return Response(response, status = status.HTTP_200_OK)
        else:
            response = {'message': "You need to provide stars"}
            return Response(response, status = status.HTTP_400_BAD_REQUEST)
        


class RatingViewSet(viewsets.ModelViewSet):
    serializer_class = RatingSerializer
    queryset = Rating.objects.all()