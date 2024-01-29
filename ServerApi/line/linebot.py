import json
import re
import uuid

from django.db import transaction
from linebot.v3.webhooks import MessageEvent, TextMessageContent, BeaconEvent
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
    MessagingApi, FlexMessage, FlexContainer, ReplyMessageRequest, TextMessage
)

from InterDiD import settings
from ServerApi.line.linebot_flex_message import image_with_text
from ServerApi.serializer import ArtworksSerializer
from ServerCommon import print_success, print_error
from ServerCommon.models import Users, Beacons, UserGames, Games

# LineConfigurations
configuration = Configuration(
    access_token=settings.LINE_ACCESS_KEY
)
handler = WebhookHandler(settings.LINE_SECRET_KEY)
line_bot_api = MessagingApi(ApiClient(configuration))


def send_message(token, msg):
    line_bot_api.reply_message(
        ReplyMessageRequest(
            reply_token=token,
            messages=[TextMessage(text=msg)]
        )
    )


@handler.add(MessageEvent, message=TextMessageContent)
@transaction.atomic
def handle_message(event, _):
    message = event.message.text
    line_id = event.source.user_id
    reply_token = event.reply_token
    user = Users.objects.get(line_id=line_id)
    # print_warning(event)
    print_success(f'user_id: {user.user_id}, line_id: {line_id}, message: {message}, type: {event.type}')

    if message == 'puzzle':
        try:
            url = f'{settings.APP_HOST}/puzzle?unique_code={user.unique_code}'
            send_message(reply_token, url)
        except Exception as e:
            print_error(e)
    elif message == 'ranking':
        try:
            user_game = UserGames.objects.get(user=user, game_id=Games.objects.get(game_diff_select=1))
            ranking = UserGames.objects.filter(game_id=user_game.game_id, play_date__lt=user_game.play_date).count() + 1
            message = f'難易度為 {user_game.game.game_name}，您的排名為第 {ranking} 名，用時為 {user_game.play_date} 秒'
            send_message(reply_token, message)
        except Exception as e:
            send_message(reply_token, '您還沒有完成遊戲')
            print_error(e)
    else:
        if message.startswith('name:'):
            try:
                name = message.split(':')[1]
                Users.objects.update_or_create(
                    line_id=line_id,
                    defaults={'user_name': name}
                )
                send_message(reply_token, f'您的名字已更改為: {name}')
            except Exception as e:
                print_error(e)
        else:
            send_message(reply_token, '更換名字請輸入: name:你的名字')


@handler.add(BeaconEvent)
@transaction.atomic
def handle_beacon_event(event, _):
    hwid = event.beacon.hwid
    beacon = Beacons.objects.filter(beacon_uuid=hwid).first()

    # 新增用户
    user = Users.objects.filter(line_id=event.source.user_id).first()
    if user:
        if not user.unique_code:
            unique_code = str(uuid.uuid4())
            Users.objects.update_or_create(
                line_id=event.source.user_id,
                defaults={'unique_code': unique_code}
            )
    else:
        unique_code = str(uuid.uuid4())
        Users.objects.create(line_id=event.source.user_id, unique_code=unique_code)

    # 检查 Beacon 是否有关联的 Artworks
    if beacon is None:
        return
    if beacon.artworks is None:
        return

    # 获取 Artworks 的数据
    artworks = beacon.artworks
    serializer = ArtworksSerializer(artworks)

    if len(serializer.data) > 0:
        template = json.loads(image_with_text)
        template["contents"] = []

        # 生成 Flex Message
        for artwork_item in serializer.data['artwork_items']:
            title = re.sub(r'[\x00-\x1F\x7F-\x9F]', '', artwork_item['artwork_item_title'])
            description = re.sub(r'[\x00-\x1F\x7F-\x9F]', '', artwork_item['artwork_item_description'])
            image = f'{settings.APP_HOST}{artwork_item["artwork_item_image"]}'
            action = f'{settings.APP_HOST}?id={artworks.artwork_id}&imageId={artwork_item["artwork_item_id"]}'

            template["contents"].append({
                "type": "bubble",
                "hero": {
                    "type": "image",
                    "url": image,
                    "size": "full",
                    "aspectMode": "fit",
                    "aspectRatio": "1:1",
                    "action": {
                        "type": "uri",
                        "uri": action
                    }
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": title,
                            "weight": "bold",
                            "size": "xl"
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "margin": "lg",
                            "spacing": "sm",
                            "contents": [
                                {
                                    "type": "box",
                                    "layout": "baseline",
                                    "spacing": "sm",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": description,
                                            "wrap": True,
                                            "color": "#666666",
                                            "size": "sm",
                                            "flex": 5
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            })

        # 轉換成 JSON
        json_result = json.dumps(template, ensure_ascii=False)

        # alt_text 顯示在未打開聊天室時的訊息
        flex_message = FlexMessage(
            alt_text=f'{serializer.data["product_title"]}: 點擊查看詳細資訊',
            contents=FlexContainer.from_json(json_result)
        )
        line_bot_api.reply_message(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[flex_message]
            )
        )
        print_success(f'送出成功: {serializer.data["product_title"]}')


class LinebotView(APIView):
    @staticmethod
    @transaction.atomic
    def post(request):
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')
        # 驗證signature
        try:
            handler.handle(body, signature)
        except InvalidSignatureError:
            print_error('Invalid signature.')
            return Response("Invalid signature.", status=status.HTTP_400_BAD_REQUEST)

        return Response('OK', status=status.HTTP_200_OK)
