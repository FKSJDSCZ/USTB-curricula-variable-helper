from PySide6.QtCore import QObject, Signal

from view.LoginView import LoginView
from service.LoginService import LoginService


class LoginController(QObject):
	toMainWindow_ = Signal(str)

	def __init__(self, loginView: LoginView, loginService: LoginService):
		super().__init__()
		self.view_: LoginView = loginView
		self.service_: LoginService = loginService

		self._connectionInit()
		self.service_.handleInit()

	def _connectionInit(self) -> None:
		# from view
		self.view_.loginWindow_.getmsgBtn.clicked.connect(self._onGetMsgBtnClicked)
		self.view_.imgRefreshBtn_.clicked.connect(self.service_.handleSmsLogin)
		self.view_.slider_.sliderReleased.connect(lambda: self.service_.checkPuzzle(self.view_.slider_.value()))
		self.view_.loginWindow_.loginBtn.clicked.connect(self._onLoginBtnClicked)
		self.view_.loginWindow_.smsCodeEdit.returnPressed.connect(self._onLoginBtnClicked)
		self.view_.loginWindow_.refreshBtn.clicked.connect(self._onRefreshBtnClicked)

		# from service
		self.service_.initFinished.connect(self._onServiceInited)
		self.service_.qrCodeUpdated.connect(self._onQrCodeUpdated)
		self.service_.imageDataUpdated.connect(self._onImageDataUpdated)
		self.service_.captchaChecked.connect(self._onCaptchaChecked)
		self.service_.btnCooldown.connect(self._onBtnCooldown)
		self.service_.loginSignal.connect(self._onQrLogin)

	def _onGetMsgBtnClicked(self) -> None:
		self.service_.phoneNumber_ = self.view_.loginWindow_.phoneNumberEdit.text().strip()
		if not self.service_.phoneNumber_:
			self.view_.loginWindow_.warningLabel.setText("请输入手机号")
			return
		self.service_.handleSmsLogin()

	def _onLoginBtnClicked(self):
		self.service_.smsCode_ = self.view_.loginWindow_.smsCodeEdit.text()
		self.service_.smsAuthenticate()

	def _onRefreshBtnClicked(self) -> None:
		self.view_.loginWindow_.warningLabel.clear()
		self.service_.handleQrCodeLogin()

	def _onServiceInited(self) -> None:
		self.view_.show()
		self.service_.handleQrCodeLogin()

	def _onQrCodeUpdated(self) -> None:
		self.view_.loginWindow_.qrCodeLabel.setPixmap(self.service_.qrCodePixmap_.scaled(200, 200))

	def _onImageDataUpdated(self) -> None:
		self.view_.updateVerifyImage(self.service_.baseImgData_, self.service_.jigsawImgData_)
		self.view_.showVerifyWindow()

	def _onCaptchaChecked(self, result: bool) -> None:
		if result:
			self.view_.closeVerifyWindow()
		else:
			self.service_.handleSmsLogin()
			self.view_.autoSlideBack()

	def _onBtnCooldown(self, cooldown: int) -> None:
		self.view_.startBtnCooldown(cooldown)

	def _onQrLogin(self, loginState: bool, loginMsg: str) -> None:
		if loginMsg:
			self.view_.loginWindow_.warningLabel.setText(loginMsg)
		if loginState:
			self._goToMainWindow()

	def _goToMainWindow(self) -> None:
		self.view_.close()
		self.toMainWindow_.emit(self.service_.userName_)
