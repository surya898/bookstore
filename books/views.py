from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from books.models import mybooks
from books.serializers import bookserializer,userserializer
from rest_framework.viewsets import ViewSet,ModelViewSet
class mybookView(APIView):
  def get(self,request,*args,**kw):
    qs = mybooks.objects.all()
    serializer = bookserializer(qs,many=True)
    return Response(data=serializer.data)

  def post(self,request,*args,**kw):
    serializer = bookserializer(data=request.data)
    if serializer.is_valid():
      print(serializer.validated_data)
      mybooks.objects.create(**serializer.validated_data)
      return Response(data=serializer.data)
    else:
      return Response(data=serializer.errors)


    
class mybookdetailView(APIView):
  def get(self,request,*args,**kw):
    print(kw)
    id = kw.get('id')
    qs = mybooks.objects.get(id=id)
    serializer = bookserializer(qs)
    return Response(data=serializer.data)
   
  def put(self,request,*args,**kw):
    serializer = bookserializer(data = request.data)
    if serializer.is_valid():
      id = kw.get('id')
      mybooks.objects.filter(id=id).update(**request.data)
      return Response(data=serializer.data)
    else:
      return Response(data=serializer.errors)
   
  def delete(self,request,*args,**kw):
    id = kw.get('id')
    mybooks.objects.filter(id=id).delete()
    return Response(data="successfullt deleted")
  
class userview(ModelViewSet):
    serializer_class = userserializer
    Queryset = User.objects.all()
    
class BookViewSet(ModelViewSet):
    authentication_classes=[BasicAuthentication]
    permission_classes=[IsAuthenticated]
    serializer_class=bookserializer
    queryset=books.objects.all()
    
    @action(methods=['GET'],detail=True)
    def categories(self,request,args,*kw):
        qs=books.objects.value_list('category',flat=True).distinct()
        return Response(data=qs)

    @action(methods=['POST'],detail=True)
    def add_cart(self,request,args,*kw):
        id=kw.get('pk')
        user=request.user
        book=books.objects.get(id=id)
        user.carts_set.create(book=book)
        return Response(data='item successfully added to cart')
    
class cartview(ModelViewSet):
    authentication_classes=[BasicAuthentication]
    permission_classes=[IsAuthenticated]
    queryset=carts.objects.all()
    serializer_class=cartserilizer
    def list(self, request, *args, **kwargs):
        user=request.user
        print(user)
        carts=self.queryset.filter(user=user)
        ser=self.serializer_class(carts,many=True)
        return Response(data=ser.data,status=status.HTTP_200_OK)
   

