from telegram import Message
from telegram.ext import filters
import re

class PaymentsFilter(filters.MessageFilter):
    def filter(self, message: Message) -> bool:
        try:
            if re.search('[Pp]+[aymentAYMENT]', message.caption) != None:
                return True
        except TypeError:
            return False
        return False

class AirtimeForCashFilter(filters.MessageFilter):
    def filter(self, message: Message):
        try:
            if re.search('[Aa]irtime to cash', message.caption) != None:
                return True
        except TypeError:
            return False
        return False