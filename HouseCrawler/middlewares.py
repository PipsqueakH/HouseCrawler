from scrapy.downloadermiddlewares.retry import RetryMiddleware
from scrapy.utils.response import response_status_message
from time import sleep

class SleepRetryMiddleware(RetryMiddleware):
    def __init__(self, settings):
        RetryMiddleware.__init__(self, settings)

    def process_response(self, request, response, spider):
        if response.status in [301, 302]:
            print('retry ' + response.url)
            sleep(360)  # few minutes
            reason = response_status_message(response.status)
            return self._retry(request, reason, spider) or response

        return super(SleepRetryMiddleware, self).process_response(request, response, spider)
