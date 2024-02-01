from fastapi.exception_handlers import (
    request_validation_exception_handler,
)
from pprint import pprint
from fastapi import FastAPI, Request, status
from fastapi.responses import ORJSONResponse
from fastapi.exceptions import RequestValidationError
import httpx
from exchange.utility import (
    settings,
    log_order_message,
    log_alert_message,
    print_alert_message,
    log_order_error_message,
    log_validation_error_message,
    log_error_message,
    log_message,
)
import traceback
from exchange import get_exchange, log_message, db, settings, get_bot
import ipaddress
import os

whitelist = ["52.89.214.238", "34.212.75.30", "54.218.53.128", "52.32.178.7", "127.0.0.1"]
whitelist = whitelist + settings.WHITELIST


VERSION = "0.1.0"
app = FastAPI(default_response_class=ORJSONResponse)


'''s
    starup and shutdown
'''
@app.on_event("startup")
async def startup():
    log_message(f"POTATOBOT 실행 완료! - 버전:{VERSION}")

@app.on_event("shutdown")
async def shutdown():
    db.close()


'''
    http whitelist ips
'''
@app.middleware("http")
async def whitelist_middleware(request: Request, call_next):
    try:
        if request.client.host not in whitelist and not ipaddress.ip_address(request.client.host).is_private:
            msg = f"{request.client.host}는 안됩니다"
            print(msg)
            return ORJSONResponse(status_code=status.HTTP_403_FORBIDDEN, content=f"{request.client.host}는 허용되지 않습니다")
    except:
        log_error_message(traceback.format_exc(), "미들웨어 에러")
    else:
        response = await call_next(request)
        return response

'''
    exception handler
'''
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    msgs = [f"[에러{index+1}] " + f"{error.get('msg')} \n{error.get('loc')}" for index, error in enumerate(exc.errors())]
    message = "[Error]\n"
    for msg in msgs:
        message = message + msg + "\n"

    log_validation_error_message(f"{message}\n {exc.body}")
    return await request_validation_exception_handler(request, exc)


'''
    get current ip
'''
@app.get("/ip")
async def get_ip():
    data = httpx.get("https://ipv4.jsonip.com").json()["ip"]
    log_message(data)


'''
    get health check
'''
@app.get("/health")
async def welcome():
    return "check"


### func. log
def log(exchange_name, result, order_info):
    log_order_message(exchange_name, result, order_info)
    print_alert_message(order_info)

### func. error log 
def log_error(error_message, order_info):
    log_order_error_message(error_message, order_info)
    log_alert_message(order_info, "실패")

### func. get error from traceback
def get_error(e):
    tb = traceback.extract_tb(e.__traceback__)
    target_folder = os.path.abspath(os.path.dirname(tb[0].filename))
    error_msg = []

    for tb_info in tb:
        # if target_folder in tb_info.filename:
        error_msg.append(f"File {tb_info.filename}, line {tb_info.lineno}, in {tb_info.name}")
        error_msg.append(f"  {tb_info.line}")

    error_msg.append(str(e))

    return error_msg