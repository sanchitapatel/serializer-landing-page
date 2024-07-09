from django.shortcuts import render
from django.http import HttpResponse,JsonResponse

from app.serializers import StudentSerializer
from app.models import Student
from rest_framework.renderers import JSONRenderer
import io
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt


# Create your views here.

def stulist(request):
    stu_list=Student.objects.all()
    print("Query_Set = ",stu_list)
    serializer = StudentSerializer(stu_list,many=True)
    print("Serializer = ",serializer)
    print("Python_data(serializer.data) = ", serializer.data)

    json_data = JSONRenderer().render(serializer.data)
    print("Json_Data =",json_data)
   
    return HttpResponse(json_data,content_type='application/json')
     
    # or

    return JsonResponse(serializer.data,safe=False)

    # safe: A boolean value that indicates whether the data should be serialized safely. 
    # If safe is True, only dict instances will be serialized. If safe is False, any object can be serialized.


def stu_detail(req,pk):
    stu = Student.objects.get(pk=pk)
    print("Query_Set = ",stu)
    #print("Stu_name= ",name)
    # print("Stu_roll= ",user.roll)
    #print("Stu_city= ",city)
    serializer = StudentSerializer(stu)
    print("Serializer = ",serializer)
    print("Python_data(serializer.data) = ", serializer.data)

    json_data = JSONRenderer().render(serializer.data)
    print("Json_data = ",json_data)
    return HttpResponse(json_data,content_type='application/json')
    # when we send json data from views then contet type must be a "application/json" 
    
    # return JsonResponse(serializer.data,safe=False)
    # first argument of JsonResponse should be a dict, otherwise set safe=False
@csrf_exempt
def list(request):
    if request.method =='POST':
        json_data =request.body
        stream =io.BytesIO(json_data)
        python_data=JSONParser().parse(stream)
        serializer =StudentSerializer(data=python_data)
        if serializer.is_valid():
            serializer.save()
            res={'msg':'Data created'}
            json_data=JSONRenderer().render(res)
            return HttpResponse(json_data,content_type='application/json')
            json_data=JSONRenderer().render(serializer.errors)
            return HttpResponse(json_data,content_type='application/json')