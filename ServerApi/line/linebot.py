from django.db import transaction
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from linebot.v3 import (
    WebhookHandler,
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi
)

# LineConfigurations
configuration = Configuration(
    access_token='BHu8wZ/6u7BSSRNOIJjkH2WcVRcGThJmAGSyYnOpHUKLMTMZ7OMf3LNmSff5m9emb2JXke4o50KEgCfblJqaBsTgEe'
                 '/VfRFeEorfR2Hd8w3HlktyazGJzXrwgw5+0aZJgX5MQ51mND80p2fG2eqX3AdB04t89/1O/w1cDnyilFU='
)
handler = WebhookHandler('3e03ed5ebb5a6598ab290f478591a1a8')
line_bot_api = MessagingApi(ApiClient(configuration))


# @handler.add(MessageEvent, message=TextMessageContent)
# @transaction.atomic
# def handle_message(event):
#     flex_message = FlexMessage(
#         alt_text=event.message.text,
#         contents=FlexContainer.from_json(image_with_text)
#     )
#     line_bot_api.reply_message(
#         ReplyMessageRequest(
#             reply_token=event.reply_token,
#             messages=[flex_message]
#         )
#     )
#
#
# @handler.add(BeaconEvent)
# @transaction.atomic
# def handle_beacon_event(event, _):
#     hwid = event.beacon.hwid
#
#     # 检查是否有匹配的事件
#     if len(serializer.data) > 0:
#         # 获取第一个匹配的事件的数据
#         first_event = serializer.data[0]
#
#         # 提取特定字段
#         event_name = first_event.get('event_name', 'N/A')
#         event_url = first_event.get('event_url', 'N/A')
#
#         # 检查用户是否存在
#         user = Users.objects.filter(line_id=event.source.user_id).first()
#         if user:
#             if not user.unique_code:
#                 unique_code = str(uuid.uuid4())
#                 Users.objects.update_or_create(
#                     line_id=event.source.user_id,
#                     defaults={'unique_code': unique_code}
#                 )
#             else:
#                 unique_code = user.unique_code
#         else:
#             unique_code = str(uuid.uuid4())
#             Users.objects.create(line_id=event.source.user_id, unique_code=unique_code)
#
#         # 构建回复消息
#         msg = f'{event_name}: {event_url}?unique_id={unique_code}'
#
#         line_bot_api.reply_message(
#             ReplyMessageRequest(
#                 reply_token=event.reply_token,
#                 messages=[TextMessage(text=msg)]
#             )
#         )
#     else:
#         pass


class LinebotView(APIView):
    @staticmethod
    @transaction.atomic
    def post(request):
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')
        print("\033[93m", body, end="\033[0m \n")

        # 驗證signature
        try:
            handler.handle(body, signature)
        except InvalidSignatureError:
            return Response("Invalid signature.", status=status.HTTP_400_BAD_REQUEST)

        return Response('OK', status=status.HTTP_200_OK)
