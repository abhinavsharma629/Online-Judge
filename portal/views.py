#IMPORTS
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import SubmissionData, LanguageData, savedCodeData, savedNoteData
from .serializers import SubmissionDataSerializer, LanguageDataSerializer, savedNoteDataSerializer, savedCodeDataSerializer
from django.db.models import Q
from django.http import JsonResponse
from .tasks import submission
from rest_framework.parsers import MultiPartParser
from django.core import serializers
from django.utils import timezone




#Problem Submit And Get Status
class submit(APIView):
    
    #GET
    def get(self, request):
        subId=request.GET.get('subId')
        print(subId)

        #Try if submission Id exists
        try:
            userDetails=SubmissionData.objects.get(submissionId=subId)
        except Exception as e:
            #print(e)
            return Response({"data" :"No Such User Registered"}, status=status.HTTP_404_NOT_FOUND)
        
        if(userDetails.status=="Not Judged"):
            return Response({"data" :"Result Not Generated Yet"}, status=status.HTTP_404_NOT_FOUND)
        else:
            serializer= SubmissionDataSerializer(userDetails)
            userDetails.delete()
            return Response(serializer.data, status=status.HTTP_200_OK)
    
    
    #POST
    parser_classes = (MultiPartParser,)
    def post(self, request, format=None):
        params=request.data
        user=params['user']
        file=params['file']
        print(file)
        c=False
        
        try:
            inputFile=params['inputFile']
            c=True
        except:
            c=False
        
        #print(user, type(user))
        file_ext_check=file.name.split(".")[1]
        #print(file_ext_check)
        if(file_ext_check=='java' or file_ext_check=='c' or file_ext_check=='cpp' or file_ext_check=='py'):
            if(file_ext_check == 'java'):
                language=1
            elif(file_ext_check == 'cpp'):
                language=2
            elif(file_ext_check == 'c'):
                language=3
            elif(file_ext_check == 'py'):
                language=4
            print(language)
            
            stat = submission.delay(language)
            if(c):
                obj,notif=SubmissionData.objects.get_or_create(username=user, problemData=file, inputFile=inputFile, submissionId=stat, status="Not Judged")
            else:
                obj,notif=SubmissionData.objects.get_or_create(username=user, problemData=file, submissionId=stat, status="Not Judged")
            
            if notif is True:
                obj.save()

            return Response({"data": "Submission id is:- "+str(stat)}, status=status.HTTP_201_CREATED)
        else:
            return Response({"data": "Language Not Supported"}, status=status.HTTP_404_NOT_FOUND)
    

@api_view(['GET'])
def getResponse(request):
    obj=SubmissionData.objects.get(submissionId=request.GET.get('subId'))
    while(obj.status=="Not Judged"):
        print("Waiting for judging....")
    return JsonResponse({'url': obj.outputFile.name, "judged": "True"})

#GET Language Syntax params:- probId:- [1-Java, 2- C++, 3- C, 4- Py 3+]
@api_view(['GET'])
def getSyntax(request):

    data=request.GET.get('probId')
    print(data)
    syntaxData=LanguageData.objects.get(languageChoice=data)
    #print(syntaxData)
    #print(syntaxData.languageChoice, syntaxData.problemMandatoryData)
    serializer= LanguageDataSerializer(syntaxData)
    print(serializer.data)
    return Response(serializer.data, status=status.HTTP_200_OK)
    #return JsonResponse({'data':'1'})




#Save And Delete Your Code
class saveDeleteCode(APIView):
    
    #GET
    def get(self, request):
        print(savedCodeData.objects.all())
        data=request.GET.get('codeId')
        print(data)
        try:
            codesData=savedCodeData.objects.get(codeId=data)
            serializer= savedCodeDataSerializer(codesData)
            print(serializer.data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({"data": "No Such Code Present"}, status=status.HTTP_404_NOT_FOUND)


    #POST
    parser_classes = (MultiPartParser,)
    def post(self, request, format=None):
        params=request.data
        #print(data)
        c=0
        for i, j in params.items():
            if(c==0):
                user=params[i]
            else:
                file=params['file']
            c+=1
        
        obj,notif=savedCodeData.objects.get_or_create(username=user, problemData=file, lastUpdated=timezone.now())
        if notif is True:
            obj.save()
            stat=status.HTTP_201_CREATED

        else:
            stat=status.HTTP_203_NOT_CREATED
        
        #To serialize all data of the particular user at once
        serializer = serializers.serialize('json', savedCodeData.objects.all(), fields=('codeId', 'username','problemData', 'createdAt', 'lastUpdated'))
        
        print(serializer)
        return Response(serializer, status=stat)


    #DELETE
    def delete(self, request, format=None):
        params=request.GET
        #print(data)
        
        for i, j in params.items():
            codeId=params[i]
        try:
            obj=savedCodeData.objects.get(codeId=codeId)
            obj.delete()
            stat=status.HTTP_200_OK
        except:
            stat=status.HTTP_404_NOT_FOUND

        #To serialize all data of the particular user at once
        serializer = serializers.serialize('json', savedCodeData.objects.all(), fields=('codeId', 'username','problemData', 'createdAt', 'lastUpdated'))
        
        print(serializer)
        return Response(serializer, status=stat)




#Save And Delete Your Note
class saveDeleteNote(APIView):
    
    #GET
    def get(self, request):

        data=request.GET.get('noteId')
        print(data)
        try:
            notesData=savedNoteData.objects.get(noteId=data)
            serializer= savedNoteDataSerializer(notesData)
            print(serializer.data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({"data": "No Such Note Present"}, status=status.HTTP_404_NOT_FOUND)


    #POST
    parser_classes = (MultiPartParser,)
    def post(self, request, format=None):
        params=request.data
        #print(data)
        c=0
        for i, j in params.items():
            if(c==0):
                user=params[i]
            else:
                file=params['file']
            c+=1

        obj,notif=savedNoteData.objects.get_or_create(username=user, noteData=file, lastUpdated=timezone.now())
        if notif is True:
            obj.save()
            stat=status.HTTP_201_CREATED

        else:
            stat=status.HTTP_203_NOT_CREATED
        
        #To serialize all data of the particular user at once
        serializer = serializers.serialize('json', savedNoteData.objects.all(), fields=('codeId', 'username','noteData', 'createdAt', 'lastUpdated'))
        
        #print(serializer)
        return Response(serializer, status=stat)


    #DELETE
    def delete(self, request, format=None):
        params=request.GET
        #print(data)
        print(params)
        for i, j in params.items():
            noteId=params[i]
        #print(noteId)

        try:
            obj=savedNoteData.objects.get(noteId=noteId)
            obj.delete()
            stat=status.HTTP_200_OK
        except:
            stat=status.HTTP_404_NOT_FOUND

        #To serialize all data of the particular user at once
        serializer = serializers.serialize('json', savedNoteData.objects.all(), fields=('noteId', 'username','noteData', 'createdAt', 'lastUpdated'))
        
        #print(serializer)
        return Response(serializer, status=stat)



#POST
@api_view(['POST'])
def editCode(request):
    parser_classes = (MultiPartParser,)
    
    params=request.data
    user=params['user']
    codeId=params['codeId']
    file=params['file']
    
    try:
        obj=savedCodeData.objects.get(codeId=codeId)
        obj.problemData=file
        obj.lastUpdated=timezone.now()
        obj.save()
        stat=status.HTTP_201_CREATED
    except:
        stat=status.HTTP_404_NOT_FOUND
    
    #To serialize all data of the particular user at once
    serializer = serializers.serialize('json', savedCodeData.objects.all(), fields=('codeId', 'username','problemData', 'createdAt', 'lastUpdated'))
        
    print(serializer)
    return Response(serializer, status=stat)



#POST
@api_view(['POST'])
def editNote(request):
    parser_classes = (MultiPartParser,)
    
    params=request.data
    user=params['user']
    noteId=params['noteId']
    file=params['file']

    try:
        obj=savedNoteData.objects.get(noteId=noteId)
        obj.problemData=file
        obj.lastUpdated=timezone.now()
        obj.save()
        stat=status.HTTP_201_CREATED
    except:
            stat=status.HTTP_404_NOT_FOUND
    
    #To serialize all data of the particular user at once
    serializer = serializers.serialize('json', savedNoteData.objects.all(), fields=('noteId', 'username','noteData', 'createdAt', 'lastUpdated'))
        
    print(serializer)
    return Response(serializer, status=stat)