import json
import re

from lxml import etree
from urllib.parse import urlencode, urlparse, parse_qs
from PySide6.QtCore import QUrl, QUrlQuery, QByteArray, QTimer
from PySide6.QtNetwork import *
from PySide6.QtGui import QStandardItem

from model.MainWindowModel import MainWindowModel
from signals.signal import DataUpdateSignals
from entity.Class import Class, ExtensionClass

rootDomain = "https://jwgl.ustb.edu.cn"


class MainWindowService:
	def __init__(self, mainWindowModel: MainWindowModel):
		super().__init__()
		self.model_: MainWindowModel = mainWindowModel
		self.manager_: QNetworkAccessManager = QNetworkAccessManager()
		self.dataUpdate_: DataUpdateSignals = DataUpdateSignals()
		self.timer_: QTimer = QTimer()

	def get(self, url: str, callBack, params: dict[str, str] = None, save: bool = False, *other) -> None:
		paramStr = str()
		if params:
			paramStr = "?" + urlencode(params)
		qurl = QUrl(url + paramStr)
		reply = self.manager_.get(QNetworkRequest(qurl))
		reply.finished.connect(lambda: callBack(reply, *other))
		if save:
			self.model_.autoReplyList_.append(reply)

	def post(self, url: str, callBack, params: dict[str, str] = None, data: dict[str, str] = None):
		paramStr = str()
		if params:
			paramStr = "?" + urlencode(params)
		request = QNetworkRequest(QUrl(url + paramStr))
		request.setHeader(QNetworkRequest.KnownHeaders.ContentTypeHeader, "application/json")

		query = QUrlQuery()
		if data:
			for key, value in data:
				query.addQueryItem(key, value)
		data_ = QByteArray(query.toString().encode())

		reply = self.manager_.post(request, data_)
		reply.finished.connect(lambda: callBack(reply))

	def getEpochList(self) -> None:
		# get epoch selection page
		getEpochUrl = rootDomain + "/xsxk/xsxkzx_index"
		self.get(url=getEpochUrl, callBack=self._handleGetEpochRes)

	def _handleGetEpochRes(self, getEpochReply: QNetworkReply) -> None:
		epochHtml = etree.HTML(getEpochReply.readAll().data().decode(), etree.HTMLParser())
		tableRows = epochHtml.xpath("//tr")
		for i in range(1, len(tableRows)):
			unitList = tableRows[i].xpath(".//td")
			self.model_.epochTimeList_.append(unitList[1].text)
			self.model_.epochCodeList_.append(unitList[3].xpath("./a/@onclick")[0][6:-3])

		self.dataUpdate_.updateEpochTime_.emit()
		getEpochReply.deleteLater()

	def getTypeList(self) -> None:
		# choose epoch & get course type selection page
		getTypeUrl = rootDomain + "/xsxk/xsxkzx_zy"
		getTypeParams = {
			"glyxk": "1",
			"jx0502zbid": self.model_.epochCodeList_[self.model_.currentEpochIndex_],
			"isgld": "null"
		}
		self.post(getTypeUrl, self._handleGetTypeRes, getTypeParams)

	def _handleGetTypeRes(self, getTypeReply: QNetworkReply):
		# parse type name & url
		typeHtml = etree.HTML(getTypeReply.readAll().data().decode(), etree.HTMLParser())
		self.model_.typeNameList_ = typeHtml.xpath("//li/a/text()")
		self.model_.typeUrlList_ = typeHtml.xpath("//li/a/@href")

		self.dataUpdate_.updateTypeName_.emit()
		getTypeReply.deleteLater()

	def getTypeData(self, count: int) -> None:
		# course select
		if self.model_.currentTypeIndex_ != count - 1:
			urlToParse = self.model_.typeUrlList_[self.model_.currentTypeIndex_]
			typeParams = parse_qs(urlparse(urlToParse).query)
			self.model_.type_ = typeParams["type"][0]
			self.model_.opener_ = typeParams["opener"][0]
		# class table log query
		else:
			self.model_.type_ = ""
			self.model_.opener_ = ""

	def getCourseData(self) -> None:
		# get course data
		getCourseUrl = rootDomain + self.model_.typeUrlList_[self.model_.currentTypeIndex_]
		self.get(url=getCourseUrl, callBack=self._handleCourseDataRes)

	def _handleCourseDataRes(self, getCourseReply: QNetworkReply) -> None:
		courseHtml = etree.HTML(getCourseReply.readAll().data().decode(), etree.HTMLParser())
		self.model_.courseTableRows_ = courseHtml.xpath("//tr")
		tableHeader = self.model_.courseTableRows_[0].xpath(".//th/text()")[1:]

		# set course data to model
		self.model_.courseTableModel_.clear()
		self.model_.courseTableModel_.setColumnCount(len(tableHeader))
		self.model_.courseTableModel_.setRowCount(len(self.model_.courseTableRows_) - 1)
		self.model_.classTableModel_.clear()
		self.model_.classTableModel_.setColumnCount(0)
		self.model_.classTableModel_.setRowCount(0)

		self.model_.courseTableModel_.setHorizontalHeaderLabels(tableHeader)
		for row in range(1, len(self.model_.courseTableRows_)):
			tableData = self.model_.courseTableRows_[row].xpath(".//td")[1:]
			for col in range(len(tableData)):
				self.model_.courseTableModel_.setItem(row - 1, col, QStandardItem(tableData[col].text))

		getCourseReply.deleteLater()

	def getClassData(self) -> None:
		# get class data
		selectedCourseRow = self.model_.selectedCourse_.row()
		if self.model_.courseTableModel_.item(selectedCourseRow, 0).text() == "未查询到数据":
			return

		selectCourseUrl = rootDomain + "/xsxk/getkcxxlist.do"
		if self.model_.type_ == "zybxk" or self.model_.type_ == "zyxxk" or self.model_.type_ == "fxxk":
			self._selectCompulsoryCourse(selectCourseUrl, selectedCourseRow)
		elif self.model_.type_ == "gxk":
			self._selectExtensionCourse(selectCourseUrl, selectedCourseRow)
		elif self.model_.type_ == "kzyxk":
			self._selectOtherMajorCourse(selectCourseUrl, selectedCourseRow)
		elif self.model_.type_ == "cxxk":
			self._selectOtherCourse(selectCourseUrl, selectedCourseRow)

	def _handleClassDataRes(self, getClassReply: QNetworkReply):
		classHtml = etree.HTML(getClassReply.readAll().data().decode(), etree.HTMLParser())
		classTableRows = classHtml.xpath("//tr")
		tableHeader = classTableRows[0].xpath(".//th/text()")[2:]

		# set class data to model
		self.model_.classTableModel_.clear()
		self.model_.classTableModel_.setColumnCount(len(tableHeader))
		self.model_.classTableModel_.setRowCount(len(classTableRows) - 1)

		self.model_.classTableModel_.setHorizontalHeaderLabels(tableHeader)
		for row in range(1, len(classTableRows)):
			tableData = classTableRows[row].xpath(".//td")[2:]
			for col in range(len(tableData)):
				titleList = tableData[col].xpath("./@title")
				rawText = tableData[col].text
				if len(titleList):
					self.model_.classTableModel_.setItem(row - 1, col, QStandardItem(titleList[0]))
				elif rawText:
					text = ' '.join(re.findall(r'[^ \n\r]+', rawText))
					self.model_.classTableModel_.setItem(row - 1, col, QStandardItem(text))
				else:
					self.model_.classTableModel_.setItem(row - 1, col, QStandardItem(str()))

		getClassReply.deleteLater()

	def _selectCompulsoryCourse(self, url: str, index: int) -> None:
		"""compulsory(major) course, optional course or minor course"""
		courseName = self.model_.courseTableModel_.item(index, 2).text()
		self.model_.courseCode_ = self.model_.courseTableRows_[index + 1].xpath("./@onclick")[0].split(',')[1][1:-1]
		params = {
			"xsid": "",
			"type": self.model_.type_,
			"opener": self.model_.opener_,
			"dqjx0502zbid": self.model_.epochCodeList_[self.model_.currentEpochIndex_],
			"kcfalx": "zx",
			"jx02id": self.model_.courseCode_,
			"zxfxct": "0",
			"sfzybxk": "1",
			"istyk": "1" if courseName[:2] == "体育" else "0"
		}
		self.get(url=url, callBack=self._handleClassDataRes, params=params)

	def _selectExtensionCourse(self, url: str, index: int) -> None:
		"""extension course"""
		courseData = self.model_.courseTableRows_[index + 1].xpath("./@onclick")[0].split(",'")
		self.model_.courseCode_ = courseData[1][:-1]
		self.model_.classIndexes_ = courseData[2][:-3]
		params = {
			"xsid": "",
			"type": self.model_.type_,
			"opener": self.model_.opener_,
			"dqjx0502zbid": self.model_.epochCodeList_[self.model_.currentEpochIndex_],
			"kcfalx": "zx",
			"jx02id": self.model_.courseCode_,
			"cxtzdid": self.model_.classIndexes_
		}
		self.get(url=url, callBack=self._handleClassDataRes, params=params)

	def _selectOtherMajorCourse(self, url: str, index: int) -> None:
		"""multi-disciplinary course"""
		courseData = self.model_.courseTableRows_[index + 1].xpath("./@onclick")[0].split(',')
		self.model_.courseCode_ = courseData[1][1:-1]
		selectionCode = courseData[2][1:-3]
		params = {
			"xsid": "",
			"type": self.model_.type_,
			"opener": self.model_.opener_,
			"dqjx0502zbid": self.model_.epochCodeList_[self.model_.currentEpochIndex_],
			"kcfalx": "zx",
			"jx02id": self.model_.courseCode_,
			"sfzybxk": "",
			"kcxzdm": selectionCode
		}
		self.get(url=url, callBack=self._handleClassDataRes, params=params)

	def _selectOtherCourse(self, url: str, index: int) -> None:
		"""other course"""
		self.model_.courseCode_ = self.model_.courseTableRows_[index + 1].xpath("./@onclick")[0].split(',')[1][1:-3]
		params = {
			"xsid": "",
			"type": self.model_.type_,
			"opener": self.model_.opener_,
			"dqjx0502zbid": self.model_.epochCodeList_[self.model_.currentEpochIndex_],
			"kcfalx": "zx",
			"jx02id": self.model_.courseCode_
		}
		self.get(url=url, callBack=self._handleClassDataRes, params=params)

	def getClassIndex(self) -> None:
		self.model_.classIndex_ = self.model_.classTableModel_.item(self.model_.selectedClass_.row(),
		                                                            self.model_.classTableModel_.columnCount() - 3).text()

	def chooseClass(self, class_: Class = None) -> None:
		chooseClassParam = {
			"jx0404id": class_.currentClassIndex if class_ else self.model_.classIndex_,
			"dqjx0502zbid": class_.epochCode if class_ else self.model_.epochCodeList_[self.model_.currentEpochIndex_],
			"yjx02id": class_.courseCode if class_ else self.model_.courseCode_,
			"xdlx": "1",
			"jx02id": class_.courseCode if class_ else self.model_.courseCode_,
			"type": class_.courseType if class_ else self.model_.type_,
			"kcfalx": "zx",
			"xsid": "",
			"opener": class_.opener if class_ else self.model_.opener_,
			"sfzybxk": "",
			"qzxkkz": "0",
			"glyxk": ""
		}
		self._sendChooseClassReq(1, chooseClassParam)

	def _sendChooseClassReq(self, times: int, params: dict) -> None:
		url = rootDomain + "/xsxk/xsxkoper"
		self.get(url, self._handleChooseClassReply, params, True, times, params)

	def _handleChooseClassReply(self, chooseClassReply: QNetworkReply, times: int, params: dict[str, str]) -> None:
		resData = json.loads(chooseClassReply.readAll().data().decode())
		if times == 1:
			if resData["success"]:
				self.dataUpdate_.updateChooseClass_.emit(True, resData["message"])
			else:
				if resData["wtlx"] == "kbct":
					if resData["ctxkkz"] == "1":
						params["bjckbct"] = "1"
						self._sendChooseClassReq(times + 1, params)
					else:
						self.dataUpdate_.updateChooseClass_.emit(False, resData["message"])
				elif resData["wtlx"] == "qzct":
					params["tyqzxk"] = "1"
					self._sendChooseClassReq(times + 1, params)
				else:
					print(params["yjx02id"], len(self.model_.autoReplyList_), end=" ")
					self.dataUpdate_.updateChooseClass_.emit(resData["message"] == "选课成功！", resData["message"])
		elif times == 2:
			self.dataUpdate_.updateChooseClass_.emit(resData["success"], resData["message"])

		self.model_.autoReplyList_.remove(chooseClassReply)
		chooseClassReply.deleteLater()

	def updateChooseClassRes(self, resState: bool, resMessage: str) -> None:
		print(resState, resMessage)

	def addAutoCourse(self) -> None:
		if not self.model_.autoClassTableModel_.columnCount():
			classTableCols = self.model_.classTableModel_.columnCount()
			self.model_.autoClassTableModel_.setColumnCount(classTableCols)
			for col in range(classTableCols):
				headerItem = self.model_.classTableModel_.horizontalHeaderItem(col)
				self.model_.autoClassTableModel_.setHorizontalHeaderItem(col, QStandardItem(headerItem))
		selectedClass = self.model_.selectedClass_.row()
		newRow = self.model_.autoClassTableModel_.rowCount()
		self.model_.autoClassTableModel_.setRowCount(newRow + 1)
		for col in range(self.model_.classTableModel_.columnCount()):
			item = self.model_.classTableModel_.item(selectedClass, col)
			self.model_.autoClassTableModel_.setItem(newRow, col, QStandardItem(item))

		self._spawnClass()

	def _spawnClass(self) -> None:
		class_ = ExtensionClass(
			self.model_.type_,
			self.model_.opener_,
			self.model_.epochCodeList_[self.model_.currentEpochIndex_],
			self.model_.courseCode_,
			self.model_.classIndexes_,
			self.model_.classIndex_
		)
		self.model_.autoClassList_.append(class_)

	def deleteAutoCourse(self) -> None:
		for row in sorted(self.model_.selectedAutoCourse_, key=lambda x: x.row(), reverse=True):
			self.model_.autoClassTableModel_.removeRow(row.row())
			self.model_.autoClassList_.pop(row.row())

	def timerSwitch(self) -> None:
		if self.timer_.isActive():
			self.timer_.stop()
		else:
			self.timer_.start(self.model_.timerInterval_)

	def autoChooseClass(self) -> None:
		if self.model_.autoClassList_:
			self.chooseClass(self.model_.autoClassList_[self.model_.autoClassIndex_])
			self.model_.autoClassIndex_ = (self.model_.autoClassIndex_ + 1) % len(self.model_.autoClassList_)
		else:
			print("选课列表为空")

	def saveAutoCourse(self) -> None:
		saveState, saveMsg = self.model_.saveAutoCourse()
		print(saveState, saveMsg)

	def clearAutoCourse(self) -> None:
		self.model_.autoClassTableModel_.clear()
		self.model_.autoClassList_.clear()

	def loadAutoCourse(self) -> None:
		loadState, loadMsg = self.model_.loadAutoCourse()
		print(loadState, loadMsg)

	def quitApp(self) -> None:
		exitUrl = rootDomain + "/glht/Logon.do?method=logoutFromJsxsd"
		exitData = {
			"view": "",
			"useraccount": self.model_.userName_,
			"ticket": ""
		}
		self.session_.post(url=exitUrl, data=exitData)
