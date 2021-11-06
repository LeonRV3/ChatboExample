from django.contrib import admin
from .models import *

# Register your models here.
admin.register(intents)
admin.register(responses)
admin.register(conversations)
admin.register(intentSamples)
admin.register(responseSamples)
admin.register(conversationSamples)
