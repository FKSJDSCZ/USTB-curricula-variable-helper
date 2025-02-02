import sys
import requests
import urllib3

from PyQt6.QtWidgets import *

from view.LoginView import LoginView
from view.MainWindowView import MainWindowView
from controller.LoginController import LoginController
from controller.MainWindowController import MainWindowController
from service.LoginService import LoginService
from service.MainWindowService import MainWindowService
from model.LoginModel import LoginModel
from model.MainWindowModel import MainWindowModel

from signals.signal import ToMainWindow

urllib3.disable_warnings()

headers = {
	"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
}

if __name__ == '__main__':
	session = requests.session()
	session.headers = headers
	session.verify = False

	app = QApplication(sys.argv)

	toMainWindow: ToMainWindow = ToMainWindow()

	loginView = LoginView()
	mainWindowView = MainWindowView()

	loginModel = LoginModel()
	mainWindowModel = MainWindowModel()

	loginService = LoginService(session, loginModel)
	mainWindowService = MainWindowService(session, mainWindowModel)

	loginController = LoginController(loginView, loginService, loginModel, toMainWindow)
	mainWindowController = MainWindowController(mainWindowView, mainWindowService, mainWindowModel, toMainWindow)

	loginView.show()

	sys.exit(app.exec())
