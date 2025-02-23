import json
import re

from lxml import etree
from urllib.parse import urlparse, parse_qs
from PySide6.QtCore import Signal, QObject
from PySide6.QtGui import QPixmap
from PySide6.QtNetwork import QNetworkRequest, QNetworkReply

from entity.NetworkAccessManager import NetworkAccessManager

rootDomain = "https://jwgl.ustb.edu.cn"
ssoAuthDomain = "https://sso.ustb.edu.cn"
sisAuthDomain = "https://sis.ustb.edu.cn"


class LoginService(QObject):
	initFinished = Signal()
	qrCodeUpdated = Signal()
	imageDataUpdated = Signal()
	captchaChecked = Signal(bool)
	btnCooldown = Signal(int)
	loginSignal = Signal(bool, str)

	def __init__(self, manager: NetworkAccessManager):
		super().__init__()
		self.userName_: str = str()
		self.phoneNumber_: str = str()
		self.smsCode_: str = str()
		self.lck_: str = str()
		self.entityId_: str = str()
		self.qrToken_: str = str()
		self.appId_: str = str()
		self.sessionId_: str = str()
		self.smsToken_: str = str()
		self.baseImgData_: str = str()
		self.jigsawImgData_: str = str()
		self.authChainCodes_: dict = dict()
		self.qrCodePixmap_: QPixmap = QPixmap()
		self.lastQrStateQuery_: QNetworkReply = None
		self.manager_: NetworkAccessManager = manager

	def handleInit(self):
		"""step 0: get lck & entityId"""
		self.manager_.get(
			f"{ssoAuthDomain}/idp/authCenter/authenticate",
			self._setLck,
			{
				"response_type": "code",
				"client_id": "NS2022062",
				"state": "test",
				"redirect_uri": "https://jwgl.ustb.edu.cn/glht/Logon.do?method=weCharLogin",
			},
			False,
		)

	def _setLck(self, reply: QNetworkReply):
		"""step 1: set lck & entityId & query authenticate methods"""
		redirectUrl = reply.header(QNetworkRequest.KnownHeaders.LocationHeader).toString()
		redirectParams = parse_qs(urlparse(redirectUrl).fragment.split("?")[1])

		self.lck_ = redirectParams["lck"][0]
		self.entityId_ = redirectParams["entityId"][0]
		self.initFinished.emit()

		self.manager_.post(
			f"{ssoAuthDomain}/idp/authn/queryAuthMethods",
			self._setAuthMethods,
			None,
			{
				"lck": self.lck_,
				"entityId": self.entityId_,
			}
		)
		reply.deleteLater()

	def _setAuthMethods(self, reply: QNetworkReply):
		"""step 2: set authenticate chain codes and module code"""
		resData = json.loads(reply.readAll().data().decode())
		if resData["code"] == 200:
			for dataDict in resData["data"]:
				self.authChainCodes_[dataDict["moduleCode"]] = dataDict["authChainCode"]
		else:
			self.loginSignal.emit(False, resData["message"])

		reply.deleteLater()

	def handleQrCodeLogin(self) -> None:
		"""step 0: get appId & randomToken"""
		if self.lastQrStateQuery_:
			self.lastQrStateQuery_.finished.disconnect()
			self.lastQrStateQuery_.abort()
			self.lastQrStateQuery_.deleteLater()
			self.lastQrStateQuery_ = None
		self.manager_.post(
			f"{ssoAuthDomain}/idp/authn/getMicroQr",
			self._getQrCodeLink,
			None,
			{
				"lck": self.lck_,
				"entityId": self.entityId_,
			},
		)

	def _getQrCodeLink(self, reply: QNetworkReply) -> None:
		"""step 1: get Qr code link"""
		resData = json.loads(reply.readAll().data().decode())
		self.appId_ = resData["data"]["appId"]
		returnUrl = resData["data"]["returnUrl"]
		getQrCodeUrl = resData["data"]["url"]
		self.qrToken_ = resData["data"]["randomToken"]

		self.manager_.get(
			getQrCodeUrl,
			self._getQrCodeData,
			{
				"appid": self.appId_,
				"return_url": returnUrl,
				"rand_token": self.qrToken_,
				"embed_flag": 1
			},
		)
		reply.deleteLater()

	def _getQrCodeData(self, reply: QNetworkReply) -> None:
		"""step 2: get Qr Code image data"""
		qrCodeHtml: etree._Element = etree.HTML(reply.readAll().data().decode(), etree.HTMLParser())
		qrCodeLink = sisAuthDomain + qrCodeHtml.xpath("//img/@src")[0]
		qrCodeLinkParams = parse_qs(urlparse(qrCodeLink).query)
		self.sessionId_ = qrCodeLinkParams["sid"][0]

		self.manager_.get(
			qrCodeLink,
			self._queryQrState,
		)
		reply.deleteLater()

	def _queryQrState(self, reply: QNetworkReply) -> None:
		"""step 3: load Qr Code data & query Qr code state"""
		self.qrCodePixmap_.loadFromData(reply.readAll())
		self.qrCodeUpdated.emit()

		self._sendCheckStateRequest()
		reply.deleteLater()

	def _sendCheckStateRequest(self):
		self.lastQrStateQuery_ = self.manager_.get(
			f"{sisAuthDomain}/connect/state",
			self._qrAuthenticate,
			{
				"sid": self.sessionId_
			},
		)

	def _qrAuthenticate(self, reply: QNetworkReply) -> None:
		"""step 4: check Qr code state & authenticate"""
		if parse_qs(urlparse(reply.request().url().toString()).query)["sid"][0] == self.sessionId_:
			resData = json.loads(reply.readAll().data().decode())
			if resData["code"] == 1:
				self.manager_.get(
					f"{ssoAuthDomain}/idp/authCenter/authenticateByLck",
					self._sendLoginRequest,
					{
						"thirdPartyAuthCode": "microQr",
						"lck": self.lck_,
						"appid": self.appId_,
						"auth_code": resData["data"],
						"rand_token": self.qrToken_,
					}
				)
				self.loginSignal.emit(False, "登录中...")
			elif resData["code"] == 2:
				emitMsg = ("企业" if resData["data"] == "WxWork" else str()) + "微信已扫码，请确认"
				self.loginSignal.emit(False, emitMsg)
				self._sendCheckStateRequest()
			elif resData["code"] == 3 or resData["code"] > 200:
				self.loginSignal.emit(False, "二维码已失效，请刷新")
			elif resData["code"] == 4:
				self.loginSignal.emit(False, str())
				self._sendCheckStateRequest()
			elif resData["code"] == 0:
				self.loginSignal.emit(False, "请求状态异常")
			elif resData["code"] == 101:
				self.loginSignal.emit(False, "请求的方法不被允许")
			elif resData["code"] == 102:
				self.loginSignal.emit(False, "请求不合法")
			else:
				self.loginSignal.emit(False, resData["message"])
		self.lastQrStateQuery_ = None
		reply.deleteLater()

	def _sendLoginRequest(self, reply: QNetworkReply) -> None:
		"""step 5: ready to login"""
		authHtml: etree._Element = etree.HTML(reply.readAll().data().decode(), etree.HTMLParser())
		authCode = authHtml.xpath("//input[@id='code']/@value")[0]
		state = authHtml.xpath("//input[@id='state']/@value")[0]

		self.manager_.get(
			f"{rootDomain}/glht/Logon.do",
			self._login,
			{
				"method": "weCharLogin",
				"code": authCode,
				"state": state,
			}
		)
		reply.deleteLater()

	def _login(self, reply: QNetworkReply) -> None:
		"""step 6: ready to switch view"""
		homepageHtml: etree._Element = etree.HTML(reply.readAll().data().decode(), etree.HTMLParser())
		scripts = homepageHtml.xpath("//script[@type='text/javascript']/text()")
		for script in scripts:
			match = re.findall(r"var\s+userid\s*=\s*['\"](.*?)['\"]", script)
			if match:
				self.userName_ = match[0]
				break
		self.loginSignal.emit(True, str())
		reply.deleteLater()

	def handleSmsLogin(self) -> None:
		"""step 0: get CAPTCHA block puzzle"""
		self.manager_.get(
			f"{ssoAuthDomain}/idp/captcha/getBlockPuzzle",
			self._setBlockPuzzle
		)

	def _setBlockPuzzle(self, reply: QNetworkReply) -> None:
		"""step 1: set block puzzle"""
		resData = json.loads(reply.readAll().data().decode())
		if resData["code"] == "200":
			self.smsToken_ = resData["data"]["token"]
			self.baseImgData_ = resData["data"]["originalImageBase64"]
			self.jigsawImgData_ = resData["data"]["jigsawImageBase64"]
			self.imageDataUpdated.emit()
		else:
			self.loginSignal.emit(False, resData["message"])
		reply.deleteLater()

	def checkPuzzle(self, value: int) -> None:
		"""step 2: check block puzzle & send message if CAPTCHA passed"""
		self.manager_.post(
			f"{ssoAuthDomain}/idp/authn/sendSmsMsg",
			self._getMsg,
			None,
			{
				"loginName": self.phoneNumber_,
				"pointJson": json.dumps({"x": value, "y": 5}),
				"token": self.smsToken_,
				"lck": self.lck_,
			}
		)

	def _getMsg(self, reply: QNetworkReply) -> None:
		"""step 3: process CAPTCHA result"""
		resData = json.loads(reply.readAll().data().decode())
		if resData["code"] == "200":
			self.captchaChecked.emit(True)
			self.loginSignal.emit(False, resData["data"]["msg"])
			self.btnCooldown.emit(int(resData["data"]["coolingTime"]))
		elif resData["code"] == "5054":
			self.captchaChecked.emit(False)
		else:
			self.captchaChecked.emit(True)
			self.loginSignal.emit(False, resData["message"])
		reply.deleteLater()

	def smsAuthenticate(self) -> None:
		"""step 4: verify SMS code & get login link"""
		self.manager_.post(
			f"{ssoAuthDomain}/idp/authn/authExecute",
			self._getLoginLink,
			None,
			{
				"authModuleCode": "userAndSms",
				"authChainCode": self.authChainCodes_["userAndSms"],
				"entityId": self.entityId_,
				"requestType": "chain_type",
				"lck": self.lck_,
				"authPara":
					{
						"loginName": self.phoneNumber_,
						"smsCode": self.smsCode_,
						"verifyCode": ""
					}
			}
		)

	def _getLoginLink(self, reply: QNetworkReply) -> None:
		"""step 5: get login link"""
		resData = json.loads(reply.readAll().data().decode())
		if resData["code"] == 200:
			self.userName_ = resData["userName"]
			self.manager_.post(
				f"{ssoAuthDomain}/idp/authCenter/authnEngine",
				self._sendLoginRequest,
				{"locale": "zh-CN"},
				{"loginToken": resData["loginToken"]},
				"application/x-www-form-urlencoded"
			)
			self.loginSignal.emit(False, "登录中...")
		else:
			self.loginSignal.emit(False, resData["message"])
		reply.deleteLater()
