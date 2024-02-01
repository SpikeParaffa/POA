import sys
from exchange.model import MarketOrder
from exchange.utility import settings
from datetime import datetime, timedelta
from dhooks import Webhook, Embed
from loguru import logger
from devtools import pformat
import traceback
import os

logger.remove(0)
logger.add(
    "./log/poa.log",
    rotation="1 days",
    retention="7 days",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
)
logger.add(
    sys.stderr,
    colorize=True,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | <level>{message}</level>",
)

try:
    url = settings.DISCORD_WEBHOOK_URL.replace("discordapp", "discord")
    hook = Webhook(url)
except Exception as e:
    print("웹훅 URL이 유효하지 않습니다: ", settings.DISCORD_WEBHOOK_URL)


'''
    get error from traceback
'''
def get_error(e):
    tb = traceback.extract_tb(e.__traceback__)
    target_folder = os.path.abspath(os.path.dirname(tb[0].filename))
    error_msg = []

    for tb_info in tb:
        # if target_folder in tb_info.filename:
        error_msg.append(f"File {tb_info.filename}, line {tb_info.lineno}, in {tb_info.name}")
        if "raise error." in tb_info.line:
            continue
        error_msg.append(f"  {tb_info.line}")

    error_msg.append(str(e))

    return "\n".join(error_msg)

'''
    get kor_time from utc_time
'''
def parse_time(utc_timestamp):
    timestamp = utc_timestamp + timedelta(hours=9).seconds
    date = datetime.fromtimestamp(timestamp)
    return date.strftime("%y-%m-%d %H:%M:%S")

'''
    log message
'''
def log_message(message="None", embed: Embed = None):
    if hook:
        if embed:
            hook.send(embed=embed)
        else:
            hook.send(message)
        # hook.send(str(message), embed)
    else:
        logger.info(message)
        print(message)

'''
    error log message
'''
def log_error_message(error, name):
    embed = Embed(title=f"{name} 에러", description=f"[{name} 에러가 발생했습니다]\n{error}", color=0xFF0000)
    logger.error(f"{name} [에러가 발생했습니다]\n{error}")
    log_message(embed=embed)

'''
    validation error log message
'''
def log_validation_error_message(msg):
    logger.error(f"검증 오류가 발생했습니다\n{msg}")
    log_message(msg)


'''
    print log message
'''
def print_alert_message(order_info: MarketOrder, result="성공"):
    msg = pformat(order_info.dict(exclude_none=True))

    if result == "성공":
        logger.info(f"주문 {result} 웹훅메세지\n{msg}")
    else:
        logger.error(f"주문 {result} 웹훅메세지\n{msg}")


'''
    alert log message
'''
def log_alert_message(order_info: MarketOrder, result="성공"):
    # discrod
    embed = Embed(
        title=order_info.order_name,
        description="[웹훅 alert_message]",
        color=0xFF0000,
    )
    order_info_dict = order_info.dict(exclude_none=True)
    for key, value in order_info_dict.items():
        embed.add_field(name=key, value=str(value), inline=False)
    log_message(embed=embed)

    # logger
    print_alert_message(order_info, result)
