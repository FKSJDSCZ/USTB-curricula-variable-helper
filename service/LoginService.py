import sys
import time
import requests
import urllib3
import json

from lxml import etree
from urllib import parse
from io import BytesIO
from requests import Session
from PyQt6.QtNetwork import *
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import QUrl

from model.LoginModel import LoginModel
from signals.signal import QrLogin
from utils.Functions import *

rootDomain = "https://jwgl.ustb.edu.cn"
authDomain = "https://sis.ustb.edu.cn"


class LoginService:
	def __init__(self, session: Session, loginModel: LoginModel):
		self.session_: Session = session
		self.model_: LoginModel = loginModel

		self.qrLogin_: QrLogin = QrLogin()

		self.qrManager_: QNetworkAccessManager = QNetworkAccessManager(None)

	def passwordLoginAuth(self) -> tuple[bool, str]:
		if not self.model_.userAccount_:
			return False, "用户名为空"
		if not self.model_.userPassword_:
			return False, "密码为空"
		if self._sendLoginRequest():
			return True, "登录成功"
		else:
			return False, "用户名或密码错误"

	def _sendLoginRequest(self) -> bool:
		encodedAc = encrypt(self.model_.userAccount_)
		encodedPwd = encrypt(self.model_.userPassword_)

		loginUrl = rootDomain + "/xk/LoginToXk"
		loginData = {"userAccount": self.model_.userAccount_,
		             "userPassword": "",
		             "encoded": f"{encodedAc}%%%{encodedPwd}"}
		loginReq = self.session_.post(url=loginUrl, data=loginData)
		loginHtml = etree.HTML(loginReq.text, etree.HTMLParser())
		errorInfo = loginHtml.xpath("//span[@class='input_li']")
		return len(errorInfo) == 0

	def qrCodeLoginAuth(self, response: QNetworkReply) -> None:
		resBytes = response.readAll()
		resDict = json.loads(str(resBytes.data(), 'utf-8'))
		if resDict["state"] == 101:
			self.qrLogin_.qrLoginSignal_.emit(False, str())
			self._sendCheckStateRequest()
		elif resDict["state"] == 102:
			self.qrLogin_.qrLoginSignal_.emit(False, "已扫码，请确认")
			self._sendCheckStateRequest()
		elif resDict["state"] == 103:
			self.qrLogin_.qrLoginSignal_.emit(False, "session id已失效，请刷新")
		elif resDict["state"] == 104:
			self.qrLogin_.qrLoginSignal_.emit(False, "二维码已失效，请刷新")
		else:
			loginUrl = rootDomain + "/glht/Logon.do"
			loginParams = {
				"method": "weCharLogin",
				"appid": self.model_.appId_,
				"auth_code": resDict["data"],
				"rand_token": self.model_.token_
			}
			self.session_.get(url=loginUrl, params=loginParams)
			self.qrLogin_.qrLoginSignal_.emit(True, "登录中...")

	def getQrCode(self) -> None:
		self.session_.get(url=rootDomain)

		tokenUrl = rootDomain + "/glht/Logon.do?method=randToken"
		tokenReq = self.session_.post(url=tokenUrl)
		tokenDict = tokenReq.json()
		self.model_.token_ = tokenDict["rand_token"]
		self.model_.appId_ = tokenDict["appid"]

		qrCodeUrl = authDomain + "/connect/qrpage"
		qrCodeParams = {
			"appid": self.model_.appId_,
			"return_url": "https://jwgl.ustb.edu.cn/glht/Logon.do?method=weCharLogin",
			"rand_token": self.model_.token_,
			"embed_flag": "1"
		}
		qrCodeReq = self.session_.get(url=qrCodeUrl, params=qrCodeParams)
		qrCodeHtml = etree.HTML(qrCodeReq.text, etree.HTMLParser())
		qrCodeLink = authDomain + qrCodeHtml.xpath("//img/@src")[0]
		self.model_.sid_ = parse.parse_qs(parse.urlparse(qrCodeLink).query)["sid"][0]

		qrCodeData = requests.get(url=qrCodeLink).content
		self.model_.qrCodePixmap_.loadFromData(BytesIO(qrCodeData).read())

		self._sendCheckStateRequest()

	def _sendCheckStateRequest(self) -> None:
		checkStateUrl = f"{authDomain}/connect/state?sid={self.model_.sid_}"
		stateReq = QNetworkRequest(QUrl(checkStateUrl))
		self.qrManager_.get(stateReq)
