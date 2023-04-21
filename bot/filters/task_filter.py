from telegram.ext import filters
import re

class TaskFilter(filters.MessageFilter):
    def filter(self, message):
        print(re.search('[Tt]+[askASK]{3}', message.text))
        return False