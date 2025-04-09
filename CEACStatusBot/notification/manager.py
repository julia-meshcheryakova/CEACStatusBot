from .handle import NotificationHandle
from CEACStatusBot.request import query_status
from CEACStatusBot.captcha import CaptchaHandle, OnnxCaptchaHandle
import os
import datetime

class NotificationManager():
    def __init__(self,location:str,number:str,passport_number:str,surname:str,captchaHandle:CaptchaHandle=OnnxCaptchaHandle("captcha.onnx")) -> None:
        self.__handleList = []
        self.__location = location
        self.__number = number
        self.__captchaHandle = captchaHandle
        self.__passport_number = passport_number
        self.__surname = surname

    def addHandle(self, notificationHandle:NotificationHandle) -> None:
        self.__handleList.append(notificationHandle)

    def send(self,) -> None:
        res = query_status(self.__location, self.__number, self.__passport_number, self.__surname, self.__captchaHandle)

        last_known_date_str = os.environ.get("LAST_KNOWN_DATE")
        last_known_date = datetime.datetime.strptime(last_known_date_str, "%d-%b-%Y").date() if last_known_date_str else None

        case_updated_date = datetime.datetime.strptime(res['case_last_updated'], "%d-%b-%Y").date()

        # Compare dates instead of strings
        if not last_known_date or case_updated_date > last_known_date:
            print(f"sending notifications (Case updated {case_updated_date} > {last_known_date})")
            for notificationHandle in self.__handleList:
                notificationHandle.send(res)
        else:
            print("no updates after initial submission")

