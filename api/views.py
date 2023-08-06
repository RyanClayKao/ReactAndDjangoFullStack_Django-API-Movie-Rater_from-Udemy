from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Movie, Rating
from .serializers import MovieSerializer, RatingSerializer, UserSerializer

# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny, )

class MovieViewSet(viewsets.ModelViewSet):
    serializer_class = MovieSerializer
    queryset = Movie.objects.all()
    authentication_classes = (TokenAuthentication, )
    # 一定要登入才能夠存取使用
    permission_classes = (IsAuthenticated, )
    # 無須驗證即可存取使用
    # permission_classes = (AllowAny, )

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

            stars = request.data['stars']
            print('stars:', stars)

            # 目前這裡會輸出「user: AnonymousUser」，因為並沒有拿到真正登入者的資訊
            # user = request.user
            # print('user:', user)

            # 如上述，因此暫且先 hardcode取得 User資料
            # user = User.objects.get(id=1)
            # print('user:', user.username) # 輸出「uesr: Ryan」 (當時設定的 superuser是 Ryan這個 user)

            # 當request header有附上 Token後，就能透過「authentication_classes = (TokenAuthentication, )」的設定，來取用 user資料
            user = request.user # 能夠成功透過 token解析出 user資料
            print('user:', user) # 輸出「user: Ryan」


            try:
                rating = Rating.objects.get(user=user.id, movie=movie.id)
                rating.stars = stars
                rating.save()

                serializer = RatingSerializer(rating, many=False)
                response = {'message': "Rating updated", 'result': serializer.data}
                return Response(response, status = status.HTTP_200_OK)
            except:
                rating = Rating.objects.create(user=user, movie=movie, stars=stars)
                serializer = RatingSerializer(rating, many=False)
                response = {'message': "Rating created", 'result': serializer.data}
                return Response(response, status = status.HTTP_200_OK)
            
        else:
            response = {'message': "You need to provide stars"}
            return Response(response, status = status.HTTP_400_BAD_REQUEST)
        

class RatingViewSet(viewsets.ModelViewSet):
    serializer_class = RatingSerializer
    queryset = Rating.objects.all()
    authentication_classes = (TokenAuthentication, )
    # 一定要登入才能夠存取使用
    permission_classes = (IsAuthenticated, )

    def update(self, request, *args, **kwargs):
        response = {'message': "You can't update rating like that"}
        return Response(response, status = status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        response = {'message': "You can't create rating like that"}
        return Response(response, status = status.HTTP_400_BAD_REQUEST)