import json
import re
import logging

from lxml import etree
from urllib.parse import urlencode, urlparse, parse_qs
from PySide6.QtCore import QUrl, QUrlQuery, QByteArray, QTimer, QObject, Signal
from PySide6.QtNetwork import *
from PySide6.QtGui import QStandardItem

from model.MainWindowModel import MainWindowModel
from entity.Class import Class, ExtensionClass
from entity.NetworkAccessManager import NetworkAccessManager

rootDomain = "https://jwgl.ustb.edu.cn"


class MainWindowService(QObject):
	epochTimeUpdated_ = Signal()
	typeNameUpdated_ = Signal()
	chooseClassUpdated_ = Signal(bool, str)

	def __init__(self, manager: NetworkAccessManager, mainWindowModel: MainWindowModel):
		super().__init__()
		self.model_: MainWindowModel = mainWindowModel
		self.manager_: NetworkAccessManager = manager
		self.timer_: QTimer = QTimer()

	# def get(self, url: str, callBack, params: dict[str, str] = None, save: bool = False, *other) -> None:
	# 	paramStr = str()
	# 	if params:
	# 		paramStr = "?" + urlencode(params)
	# 	qurl = QUrl(url + paramStr)
	# 	reply = self.manager_.get(QNetworkRequest(qurl))
	# 	reply.finished.connect(lambda: callBack(reply, *other))
	# 	if save:
	# 		self.model_.autoReplyList_.append(reply)

	def getEpochList(self) -> None:
		"""Step 0: get epoch selection list"""
		self.manager_.get(
			f"{rootDomain}/xsxk/xsxkzx_index",
			self._setEpochList
		)

	def _setEpochList(self, reply: QNetworkReply) -> None:
		"""Step 1: parse epoch code & set epoch selection list"""
		epochHtml = etree.HTML(reply.readAll().data().decode(), etree.HTMLParser())
		tableRows = epochHtml.xpath("//tr")[1:]
		for row in tableRows:
			unitList = row.xpath(".//td")
			self.model_.epochTimeList_.append(unitList[1].text)
			self.model_.epochCodeList_.append(unitList[3].xpath("./a/@onclick")[0][6:-3])
		self.epochTimeUpdated_.emit()
		reply.deleteLater()

	def getTypeList(self) -> None:
		"""Step 2: get course type selection in selected epoch"""
		self.manager_.post(
			f"{rootDomain}/xsxk/xsxkzx_zy",
			self._setTypeList,
			{
				"glyxk": "1",
				"jx0502zbid": self.model_.epochCodeList_[self.model_.currentEpochIndex_],
				"isgld": "null"
			},
			{"": ""},
			"application/x-www-form-urlencoded"
		)

	def _setTypeList(self, reply: QNetworkReply) -> None:
		"""Step 3: parse type name & url of course list & set type name"""
		typeHtml = etree.HTML(reply.readAll().data().decode(), etree.HTMLParser())
		self.model_.typeNameList_ = typeHtml.xpath("//li/a/text()")
		self.model_.typeUrlList_ = typeHtml.xpath("//li/a/@href")

		self.typeNameUpdated_.emit()
		reply.deleteLater()

	def getCourseList(self) -> None:
		"""
		Step 4: parse "type" and "opener" params & get course list in selected course type.
		Type "课表日志查询" has no "type" and "opener" params
		"""
		urlToParse = self.model_.typeUrlList_[self.model_.currentTypeIndex_]
		typeParams = parse_qs(urlparse(urlToParse).query)
		self.model_.type_ = typeParams.get("type", [str()])[0]
		self.model_.opener_ = typeParams.get("opener", [str()])[0]

		self.manager_.get(
			f"{rootDomain}{self.model_.typeUrlList_[self.model_.currentTypeIndex_]}",
			self._setCourseList
		)

	def _setCourseList(self, reply: QNetworkReply) -> None:
		"""Step 5: set course list"""
		courseHtml = etree.HTML(reply.readAll().data().decode(), etree.HTMLParser())
		self.model_.courseTableRows_ = courseHtml.xpath("//tr")
		tableHeader = self.model_.courseTableRows_[0].xpath(".//th/text()")[1:]

		if len(self.model_.courseTableRows_) >= 2 and self.model_.courseTableRows_[1].xpath(".//td")[0].text == "未查询到数据":
			self.model_.courseTableRows_.clear()
		else:
			self.model_.courseTableRows_ = self.model_.courseTableRows_[1:]

		self.model_.courseTableModel_.clear()
		self.model_.courseTableModel_.setColumnCount(len(tableHeader))
		self.model_.courseTableModel_.setRowCount(len(self.model_.courseTableRows_))
		self.model_.classTableModel_.clear()
		self.model_.classTableModel_.setColumnCount(0)
		self.model_.classTableModel_.setRowCount(0)

		self.model_.courseTableModel_.setHorizontalHeaderLabels(tableHeader)
		for rowIdx, row in enumerate(self.model_.courseTableRows_):
			tableData = row.xpath(".//td")[1:]
			for colIdx, col in enumerate(tableData):
				self.model_.courseTableModel_.setItem(rowIdx, colIdx, QStandardItem(col.text))

		reply.deleteLater()

	def getClassList(self) -> None:
		"""Step 6: get class list of selected course"""
		selectedCourseRow = self.model_.selectedCourse_.row()

		selectCourseUrl = f"{rootDomain}/xsxk/getkcxxlist.do"
		if self.model_.type_ == "zybxk" or self.model_.type_ == "zyxxk" or self.model_.type_ == "fxxk":
			self._getCompulsoryCourse(selectCourseUrl, selectedCourseRow)
		elif self.model_.type_ == "gxk":
			self._getExpansionCourse(selectCourseUrl, selectedCourseRow)
		elif self.model_.type_ == "kzyxk":
			self._getOtherMajorCourse(selectCourseUrl, selectedCourseRow)
		elif self.model_.type_ == "cxxk":
			self._getOtherCourse(selectCourseUrl, selectedCourseRow)

	def _getCompulsoryCourse(self, url: str, index: int) -> None:
		"""Step 6.1: get class list of compulsory course, optional course or minor course"""
		courseName = self.model_.courseTableModel_.item(index, 2).text()
		self.model_.courseCode_ = self.model_.courseTableRows_[index].xpath("./@onclick")[0].split(',')[1][1:-1]
		self.manager_.get(
			url,
			self._setClassData,
			{
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
		)

	def _getExpansionCourse(self, url: str, index: int) -> None:
		"""Step 6.2: get class list of quality expansion course"""
		courseData = self.model_.courseTableRows_[index].xpath("./@onclick")[0].split(",'")
		self.model_.courseCode_ = courseData[1][:-1]
		self.model_.classIndexes_ = courseData[2][:-3]

		self.manager_.get(
			url,
			self._setClassData,
			{
				"xsid": "",
				"type": self.model_.type_,
				"opener": self.model_.opener_,
				"dqjx0502zbid": self.model_.epochCodeList_[self.model_.currentEpochIndex_],
				"kcfalx": "zx",
				"jx02id": self.model_.courseCode_,
				"cxtzdid": self.model_.classIndexes_
			}
		)

	def _getOtherMajorCourse(self, url: str, index: int) -> None:
		"""Step 6.3: get class list of multidisciplinary course"""
		courseData = self.model_.courseTableRows_[index].xpath("./@onclick")[0].split(',')
		self.model_.courseCode_ = courseData[1][1:-1]
		selectionCode = courseData[2][1:-3]

		self.manager_.get(
			url,
			self._setClassData,
			{
				"xsid": "",
				"type": self.model_.type_,
				"opener": self.model_.opener_,
				"dqjx0502zbid": self.model_.epochCodeList_[self.model_.currentEpochIndex_],
				"kcfalx": "zx",
				"jx02id": self.model_.courseCode_,
				"sfzybxk": "",
				"kcxzdm": selectionCode
			}
		)

	def _getOtherCourse(self, url: str, index: int) -> None:
		"""Step 6.4: get class list of other course(MOOC, major expansion course, major course learned before major change, etc.)"""
		self.model_.courseCode_ = self.model_.courseTableRows_[index].xpath("./@onclick")[0].split(',')[1][1:-3]

		self.manager_.get(
			url,
			self._setClassData,
			{
				"xsid": "",
				"type": self.model_.type_,
				"opener": self.model_.opener_,
				"dqjx0502zbid": self.model_.epochCodeList_[self.model_.currentEpochIndex_],
				"kcfalx": "zx",
				"jx02id": self.model_.courseCode_
			}
		)

	def _setClassData(self, reply: QNetworkReply):
		"""Step 7: parse & set class list"""
		classHtml = etree.HTML(reply.readAll().data().decode(), etree.HTMLParser())
		classTableRows: list[etree._Element] = classHtml.xpath("//tr")
		tableHeader = classTableRows[0].xpath(".//th/text()")[2:]

		if len(classTableRows) >= 2 and classTableRows[1].xpath(".//td")[0].text == "未查询到数据":
			classTableRows.clear()
		else:
			classTableRows = classTableRows[1:]

		self.model_.classTableModel_.clear()
		self.model_.classTableModel_.setColumnCount(len(tableHeader))
		self.model_.classTableModel_.setRowCount(len(classTableRows))

		self.model_.classTableModel_.setHorizontalHeaderLabels(tableHeader)
		for rowIdx, row in enumerate(classTableRows):
			tableData = row.xpath(".//td")[2:]
			for colIdx, col in enumerate(tableData):
				titleList = col.xpath("./@title")
				if len(titleList):
					self.model_.classTableModel_.setItem(rowIdx, colIdx, QStandardItem(titleList[0]))
				elif col.text:
					text = ' '.join(re.findall(r'[^ \n\r]+', col.text))
					self.model_.classTableModel_.setItem(rowIdx, colIdx, QStandardItem(text))
				else:
					self.model_.classTableModel_.setItem(rowIdx, colIdx, QStandardItem(str()))

		reply.deleteLater()

	def getClassIndex(self) -> None:
		self.model_.classIndex_ = self.model_.classTableModel_.item(self.model_.selectedClass_.row(),
		                                                            self.model_.classTableModel_.columnCount() - 3).text()

	def chooseClass(self, times: int, **kwargs) -> None:
		params = {
			"jx0404id": self.model_.classIndex_,
			"dqjx0502zbid": self.model_.epochCodeList_[self.model_.currentEpochIndex_],
			"yjx02id": self.model_.courseCode_,
			"xdlx": "1",
			"jx02id": self.model_.courseCode_,
			"type": self.model_.type_,
			"kcfalx": "zx",
			"xsid": "",
			"opener": self.model_.opener_,
			"sfzybxk": "1",
			"qzxkkz": "0",
			"glyxk": ""
		}
		params.update(kwargs)
		self.manager_.get(
			f"{rootDomain}/xsxk/xsxkoper",
			self._handleChooseClassReply,
			params,
			True,
			times
		)

	def _handleChooseClassReply(self, reply: QNetworkReply, times: int) -> None:
		resData = json.loads(reply.readAll().data().decode())
		if times == 0:
			if resData["success"]:
				self.chooseClassUpdated_.emit(True, resData["message"])
			else:
				if resData["wtlx"] == "kbct":
					if resData["ctxkkz"] == "1":
						self.chooseClass(times + 1, bjckbct="1")
					else:
						self.chooseClassUpdated_.emit(False, resData["message"])
				elif resData["wtlx"] == "qzct":
					self.chooseClass(times + 1, tyqzxk="1")
				else:
					# print(params["yjx02id"], len(self.model_.autoReplyList_), end=" ")
					self.chooseClassUpdated_.emit(resData["message"] == "选课成功！", resData["message"])
		elif times == 1:
			self.chooseClassUpdated_.emit(resData["success"], resData["message"])

		# self.model_.autoReplyList_.remove(reply)
		reply.deleteLater()

	def updateChooseClassRes(self, resState: bool, resMessage: str) -> None:
		print(resState, resMessage)

	# def addAutoCourse(self) -> None:
	# 	if not self.model_.autoClassTableModel_.columnCount():
	# 		classTableCols = self.model_.classTableModel_.columnCount()
	# 		self.model_.autoClassTableModel_.setColumnCount(classTableCols)
	# 		for col in range(classTableCols):
	# 			headerItem = self.model_.classTableModel_.horizontalHeaderItem(col)
	# 			self.model_.autoClassTableModel_.setHorizontalHeaderItem(col, QStandardItem(headerItem))
	# 	selectedClass = self.model_.selectedClass_.row()
	# 	newRow = self.model_.autoClassTableModel_.rowCount()
	# 	self.model_.autoClassTableModel_.setRowCount(newRow + 1)
	# 	for col in range(self.model_.classTableModel_.columnCount()):
	# 		item = self.model_.classTableModel_.item(selectedClass, col)
	# 		self.model_.autoClassTableModel_.setItem(newRow, col, QStandardItem(item))
	#
	# 	self.model_.autoClassList_.append(
	# 		ExtensionClass(
	# 			self.model_.type_,
	# 			self.model_.opener_,
	# 			self.model_.epochCodeList_[self.model_.currentEpochIndex_],
	# 			self.model_.courseCode_,
	# 			self.model_.classIndexes_,
	# 			self.model_.classIndex_
	# 		)
	# 	)
	#
	# def deleteAutoCourse(self) -> None:
	# 	for row in sorted(self.model_.selectedAutoCourse_, key=lambda x: x.row(), reverse=True):
	# 		self.model_.autoClassTableModel_.removeRow(row.row())
	# 		self.model_.autoClassList_.pop(row.row())
	#
	# def timerSwitch(self) -> None:
	# 	if self.timer_.isActive():
	# 		self.timer_.stop()
	# 	else:
	# 		self.timer_.start(self.model_.timerInterval_)
	#
	# def autoChooseClass(self) -> None:
	# 	if self.model_.autoClassList_:
	# 		self.chooseClass(self.model_.autoClassList_[self.model_.autoClassIndex_])
	# 		self.model_.autoClassIndex_ = (self.model_.autoClassIndex_ + 1) % len(self.model_.autoClassList_)
	# 	else:
	# 		print("选课列表为空")
	#
	# def saveAutoCourse(self) -> None:
	# 	saveState, saveMsg = self.model_.saveAutoCourse()
	# 	print(saveState, saveMsg)
	#
	# def clearAutoCourse(self) -> None:
	# 	self.model_.autoClassTableModel_.clear()
	# 	self.model_.autoClassList_.clear()
	#
	# def loadAutoCourse(self) -> None:
	# 	loadState, loadMsg = self.model_.loadAutoCourse()
	# 	print(loadState, loadMsg)

	def quitApp(self) -> None:
		"""Step 0: logout"""
		self.manager_.post(
			f"{rootDomain}/glht/Logon.do",
			self._exit,
			{"method": "logoutFromJsxsd"},
			{
				"view": "",
				"useraccount": self.model_.userName_,
				"ticket": ""
			},
			"application/x-www-form-urlencoded"
		)

	def _exit(self, reply: QNetworkReply) -> None:
		"""Step 1: exit system"""
		self.manager_.get(
			f"{rootDomain}/xk/LoginToXk",
			None,
			{"method": "exit"}
		)
		reply.deleteLater()
