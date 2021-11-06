from django.contrib.auth.models import PermissionsMixin
from django.http import response
from django.http.response import JsonResponse
from django.utils.translation import templatize
from django.views.generic import TemplateView
from django.http import HttpResponse
from django import http
from django.shortcuts import render
from rest_framework import views, viewsets,permissions

from .models import intentSamples,intents,conversationSamples,conversations,responseSamples,responses,trainingModels
from .serializers import intentSerializer,intentSamplesSerializer,conversationSamplesSerializer,conversationsSerializer,responseSamplesSerializer,responseSerializer
from django.core import serializers
import json



# Create your views here.
class intentViewSet(viewsets.ModelViewSet):
    queryset = intents.objects.all()
    serializer_class = intentSerializer

class intentSamplesViewSet(viewsets.ModelViewSet):
    queryset = intentSamples.objects.all()
    serializer_class = intentSamplesSerializer

class responseViewSet(viewsets.ModelViewSet):
    queryset = responses.objects.all()
    serializer_class = responseSerializer

class responseSamplesViewSet(viewsets.ModelViewSet):
    queryset = responseSamples.objects.all()
    serializer_class = responseSamplesSerializer

class conversationViewSet(viewsets.ModelViewSet):
    queryset = conversations.objects.all()
    serializer_class = conversationsSerializer

class conversationSamplesViewSet(viewsets.ModelViewSet):
    queryset = conversationSamples.objects.all()
    serializer_class = conversationSamplesSerializer

#######-----------------------------------------------------------------
#######--------------CHATBOT ML
#######-----------------------------------------------------------------

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from django.core.files.base import File
from django.http import HttpResponse,JsonResponse
from random import randint
import os
import numpy as np
import pickle

from random import shuffle
import yaml

class testModel(TemplateView):
    def get(self,request):
        HttpResponse("path on service",200)

    def post(self,request):
        json_req = json.loads(request.body)
        model = trainingModels.objects.filter(active=True).first()

        X_train_counts = pickle.loads(model.fileCountVect.read())
        X_train_tfidf =pickle.loads(model.fileFitTransform.read())
        clf = pickle.loads(model.fileModel.read())

        X_new_counts = X_train_counts.transform([json_req["text"]])
        X_new_tfidf = X_train_tfidf.transform(X_new_counts)
        predicted = [item for item in clf.predict(X_new_tfidf)][0]
        text = intents.objects.filter(id = predicted).first().name
        response_id = conversationSamples.objects.filter(intent__pk=predicted).first().response.id
        response = [instance for instance in responseSamples.objects.filter(response=response_id)]
        response = response[randint(0,len(response)-1)].text
        return JsonResponse({"usr_msg_type":text,"bot_msg":response})

class activateModel(TemplateView):
    def get(self,request):
        return HttpResponse("path on service",200)
    
    def post(self,request):
        json_req = json.loads(request.body)
        objects = trainingModels.objects.all()
        for instance in objects:
            if(int(json_req['id'])==instance.id):
                instance.active = bool(json_req["status"])
                instance.save()
                return HttpResponse(f"(id:{instance.id}) - instance of MODELS updated to active:{instance.active}",200)
            else:
                instance.active = False
                instance.save()
        return HttpResponse("done",200)


class trainModel(TemplateView):
    def get(self,request):
        return HttpResponse("path on service",200)

    def put(self,request):
        try:
                
            json_req = json.loads(request.body) 
            intent_names = [(instance.__dict__['name'],instance.__dict__['id']) for instance in intents.objects.all()]
            data = [(instance.text,instance.intent.id) for instance in intentSamples.objects.all()]
            shuffle(data)
            train    = data[:int(len(data)*0.85)]
            validate = data[int(len(data)*0.85):]
            print(f"len train : {len(train)}\t len validate : {len(validate)}")
            count_vect = CountVectorizer()
            X_train_counts = count_vect.fit_transform([item[0] for item in train])
            tfidf_transformer = TfidfTransformer()
            X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)

            if(json_req["model_type"]=='knn'):
                CLASSIFIER = KNeighborsClassifier(n_neighbors=int(len(intent_names)) )
                clf = CLASSIFIER.fit(X_train_tfidf,[item[1] for item in train])
            elif(json_req["model_type"]=='tree'):
                CLASSIFIER = DecisionTreeClassifier(random_state=0)
                clf = CLASSIFIER.fit(X_train_tfidf,[item[1] for item in train])
            elif(json_req["model_type"]=='NN'):
                CLASSIFIER = MLPClassifier(hidden_layer_sizes=(100,50,25,),random_state=1, max_iter=300)
                clf = CLASSIFIER.fit(X_train_tfidf,[item[1] for item in train])
            else:
                return HttpResponse("ERROR: not valid body",403)

            with open(os.path.dirname(os.path.abspath(__file__))+"/tempModels/CountVect.pickle",'wb') as file:
                pickle.dump(count_vect,file)
            with open(os.path.dirname(os.path.abspath(__file__))+"/tempModels/tfidfTransformer.pickle",'wb') as file:
                pickle.dump(tfidf_transformer,file)
            with open(os.path.dirname(os.path.abspath(__file__))+"/tempModels/Classifier.pickle",'wb') as file:
                pickle.dump(clf,file)
                
            _MODEL = trainingModels()
            with open(os.path.dirname(os.path.abspath(__file__))+"/tempModels/CountVect.pickle",'rb') as file:
                _MODEL.fileCountVect.save(os.path.dirname(os.path.abspath(__file__))+"/tempModels/CountVect_DB.pickle",File(file))

            with open(os.path.dirname(os.path.abspath(__file__))+"/tempModels/tfidfTransformer.pickle",'rb') as file:
                _MODEL.fileFitTransform.save(os.path.dirname(os.path.abspath(__file__))+"/tempModels/tfidfTransformer_DB.pickle",File(file))

            with open(os.path.dirname(os.path.abspath(__file__))+"/tempModels/Classifier.pickle",'rb') as file:
                _MODEL.fileModel.save(os.path.dirname(os.path.abspath(__file__))+"/tempModels/Classifier_DB.pickle",File(file))

            X_new_counts = count_vect.transform([item[0] for item in train])
            X_new_tfidf = tfidf_transformer.transform(X_new_counts)
            predicted = clf.predict(X_new_tfidf)

            _MODEL.acc_train = float(np.mean(predicted == [item[1] for item in train])*100)

            X_new_counts = count_vect.transform([item[0] for item in validate])
            X_new_tfidf = tfidf_transformer.transform(X_new_counts)
            predicted = clf.predict(X_new_tfidf)

            _MODEL.acc_validate = float(np.mean(predicted == [item[1] for item in validate])*100)
            _MODEL.save()
            return HttpResponse("model trained with: "+json_req["model_type"]+f"|\taccTrain: {_MODEL.acc_train}\taccValidate: {_MODEL.acc_validate}",200)
        except Exception as e:
            return HttpResponse("Error:"+str(e),500)

# class trainModel(TemplateView):
#     pass