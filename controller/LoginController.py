from view.LoginView import LoginView
from service.LoginService import LoginService
from model.LoginModel import LoginModel
from signals.signal import ToMainWindow


class LoginController:
	def __init__(self, loginView: LoginView, loginService: LoginService, loginModel: LoginModel,
	             toMainWindow: ToMainWindow):
		self.view_: LoginView = loginView
		self.service_: LoginService = loginService
		self.model_: LoginModel = loginModel
		self.toMainWindow_: ToMainWindow = toMainWindow

		self._connectionInit()
		self._onRefreshBtnClicked()

	def _connectionInit(self) -> None:
		# from view
		self.view_.loginBtn_.clicked.connect(self._onLoginBtnClicked)
		self.view_.userPasswordEdit_.returnPressed.connect(self._onLoginBtnClicked)
		self.view_.refreshBtn_.clicked.connect(self._onRefreshBtnClicked)

		# inside service
		self.service_.qrManager_.finished.connect(self.service_.qrCodeLoginAuth)

		# from service
		self.service_.qrLogin_.qrLoginSignal_.connect(self._onQrLogin)

	def _onLoginBtnClicked(self) -> None:
		self.view_.warningLabel_.setText("登录中...")
		self.model_.userAccount_ = self.view_.userAccountEdit_.text()
		self.model_.userPassword_ = self.view_.userPasswordEdit_.text()

		loginState, loginMsg = self.service_.passwordLoginAuth()
		self.view_.warningLabel_.setText(loginMsg)
		if loginState:
			self._goToMainWindow()

	def _onRefreshBtnClicked(self) -> None:
		self.view_.warningLabel_.clear()
		self.service_.getQrCode()
		self.view_.qrCodeLabel_.setPixmap(self.model_.qrCodePixmap_.scaled(200, 200))

	def _onQrLogin(self, loginState: bool, loginMsg: str) -> None:
		if loginMsg:
			self.view_.warningLabel_.setText(loginMsg)
		if loginState:
			self._goToMainWindow()

	def _goToMainWindow(self) -> None:
		self.view_.close()
		self.toMainWindow_.toMainWindowSignal_.emit(self.model_.userAccount_)
