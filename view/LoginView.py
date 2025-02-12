from PySide6.QtCore import Qt, QByteArray, QPropertyAnimation, QEasingCurve, QTimer
from PySide6.QtWidgets import QMainWindow, QLabel, QSlider, QPushButton
from PySide6.QtGui import QPixmap, QIcon
from ui.loginUi import Ui_login

PADDING = 10
BASE_IMAGE_WIDTH = 310
BASE_IMAGE_HEIGHT = 155
JIGSAW_IMAGE_WIDTH = 47
JIGSAW_IMAGE_HEIGHT = 155
IMAGE_REFRESH_BUTTON_SIZE = 40


class LoginView(QMainWindow):
	def __init__(self, parent: QMainWindow = None):
		super(LoginView, self).__init__(parent)
		self.loginWindow_ = Ui_login()
		self.loginWindow_.setupUi(self)
		self._initVerifyWindow()

		self.cooldown_: int = 60
		self.timer_: QTimer = QTimer()
		self.timer_.timeout.connect(self._updateBtnCooldown)

	def _initVerifyWindow(self):
		self.verifyWindow_ = QMainWindow(self)
		self.verifyWindow_.setWindowTitle("CAPTCHA")
		self.verifyWindow_.setFixedSize(BASE_IMAGE_WIDTH + 2 * PADDING, BASE_IMAGE_HEIGHT + 5 + JIGSAW_IMAGE_WIDTH + 2 * PADDING)
		self.verifyWindow_.setWindowModality(Qt.WindowModality.WindowModal)

		self.baseImgLabel_ = QLabel(self.verifyWindow_)
		self.baseImgLabel_.setGeometry(PADDING, PADDING, BASE_IMAGE_WIDTH, BASE_IMAGE_HEIGHT)

		self.jigsawImgLabel_ = QLabel(self.verifyWindow_)
		self.jigsawImgLabel_.setGeometry(PADDING, PADDING, JIGSAW_IMAGE_WIDTH, JIGSAW_IMAGE_HEIGHT)

		self.imgRefreshBtn_ = QPushButton(self.verifyWindow_)
		self.imgRefreshBtn_.setGeometry(PADDING + BASE_IMAGE_WIDTH - IMAGE_REFRESH_BUTTON_SIZE, PADDING, IMAGE_REFRESH_BUTTON_SIZE, IMAGE_REFRESH_BUTTON_SIZE)
		self.imgRefreshBtn_.setIcon(QIcon.fromTheme(QIcon.ThemeIcon.ViewRefresh))
		self.imgRefreshBtn_.setStyleSheet("QPushButton { background-color: rgba(0, 0, 0, 0); } ")

		self.slider_ = QSlider(Qt.Orientation.Horizontal, self.verifyWindow_)
		self.slider_.setGeometry(PADDING, PADDING + BASE_IMAGE_HEIGHT + 5, BASE_IMAGE_WIDTH, JIGSAW_IMAGE_WIDTH)
		self.slider_.setRange(0, BASE_IMAGE_WIDTH - JIGSAW_IMAGE_WIDTH)
		self.slider_.setStyleSheet(f"""
			QSlider::groove:horizontal {{
	            height: {JIGSAW_IMAGE_WIDTH}px;
	            background: #e0e0e0;
	            border-radius: 10px;
	        }}
	        QSlider::sub-page:horizontal {{
	            background: #4CAF50;
	            border-radius: 10px;
	        }}
	        QSlider::add-page:horizontal {{
	            background: #e0e0e0;
	            border-radius: 10px;
	        }}
	        QSlider::handle:horizontal {{
	            width: {JIGSAW_IMAGE_WIDTH}px;
	            height: {JIGSAW_IMAGE_WIDTH}px;
	            background: #ffffff;
	            border-radius: 10px;
	        }}
	        QSlider::handle:horizontal:hover {{
			    background: #666;
			}}
		""")
		self.slider_.valueChanged.connect(lambda value: self.jigsawImgLabel_.move(value + PADDING, 10))
		self.slider_.sliderPressed.connect(self._stopAutoSlideBack)

		self.slideBackAnimation_ = QPropertyAnimation(self.slider_, QByteArray(b'value'))
		self.slideBackAnimation_.setEasingCurve(QEasingCurve.Type.Linear)

	def showVerifyWindow(self):
		if self.verifyWindow_.isHidden():
			self.verifyWindow_.show()

	def updateVerifyImage(self, baseImgB64: str, jigsawImgB64: str):
		baseImgPixmap = QPixmap()
		baseImgPixmap.loadFromData(QByteArray.fromBase64(baseImgB64.encode()))
		self.baseImgLabel_.setPixmap(baseImgPixmap)
		puzzleImgPixmap = QPixmap()
		puzzleImgPixmap.loadFromData(QByteArray.fromBase64(jigsawImgB64.encode()))
		self.jigsawImgLabel_.setPixmap(puzzleImgPixmap)

	def autoSlideBack(self):
		if self.slider_.value() == self.slider_.minimum():
			return
		self.slideBackAnimation_.setStartValue(self.slider_.value())
		self.slideBackAnimation_.setEndValue(self.slider_.minimum())
		self.slideBackAnimation_.setDuration((self.slider_.value() - self.slider_.minimum()))
		self.slideBackAnimation_.start()

	def _stopAutoSlideBack(self):
		if self.slideBackAnimation_.state() == QPropertyAnimation.State.Running:
			self.slideBackAnimation_.stop()

	def closeVerifyWindow(self):
		if self.verifyWindow_.isVisible():
			self.verifyWindow_.close()
		self.slider_.setValue(self.slider_.minimum())

	def startBtnCooldown(self, cooldown: int):
		self.loginWindow_.getmsgBtn.setEnabled(False)
		self.cooldown_ = cooldown
		self.timer_.start(1000)

	def _updateBtnCooldown(self):
		self.cooldown_ -= 1
		if self.cooldown_ <= 0:
			self.timer_.stop()
			self.loginWindow_.getmsgBtn.setText("获取验证码")
			self.loginWindow_.getmsgBtn.setEnabled(True)
		else:
			self.loginWindow_.getmsgBtn.setText(f"{self.cooldown_}秒后重发")
