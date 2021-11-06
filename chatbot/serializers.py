from .models import intents,intentSamples,responses,responseSamples,conversations,conversationSamples
from rest_framework import serializers


class intentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = intents
        fields = ["id","name"]


class intentSamplesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = intentSamples
        fields = ["id","intent","text","product_ref"]


class responseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = responses
        fields = ["id","name"]


class responseSamplesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = responseSamples
        fields = ["id","response","text"]


class conversationsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = conversations
        fields = ["id","name"]



class conversationSamplesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = conversationSamples
        fields = ["id","conversation","index_ref","intent","response"]
