import json

from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtCore import QModelIndex, QSortFilterProxyModel
from PySide6.QtNetwork import QNetworkReply
from entity.Class import ExtensionClass


class MainWindowModel:
	def __init__(self):
		self.currentEpochIndex_: int = 0
		"""epochComboBox的选中项索引"""
		self.currentTypeIndex_: int = 0
		"""TypeComboBox的选中项索引"""
		self.timerInterval_: int = 100
		self.autoClassIndex_: int = 0

		self.userName_: str = str()
		self.type_: str = str()
		self.opener_: str = str()
		self.courseCode_: str = str()
		"""courseTable选中课程的课程代码"""
		self.classIndexes_: str = str()
		"""courseTable选中的课程的通知单编号序列，形式为：xxxx,xxxx,xxxx"""
		self.classIndex_: str = str()
		"""classTable选中班级的通知单编号"""
		self.loadFileName_: str = str()
		"""读取文件路径"""
		self.saveFileName_: str = str()
		"""保存文件路径"""

		self.epochTimeList_: list[str] = list()
		"""选课轮次时间列表"""
		self.epochCodeList_: list[str] = list()
		"""选课轮次代码列表"""
		self.typeNameList_: list[str] = list()
		"""课程类型列表"""
		self.typeUrlList_: list[str] = list()
		"""各类型课程的查询URL列表"""
		self.courseTableRows_: list = list()
		"""type: list[lxml.etree._Element]"""
		self.autoClassList_: list[ExtensionClass] = list()
		self.autoReplyList_: list[QNetworkReply] = list()

		self.courseFile_ = None

		self.courseTableModel_: QStandardItemModel = QStandardItemModel()
		self.courseTableProxyModel_: QSortFilterProxyModel = QSortFilterProxyModel()
		self.classTableModel_: QStandardItemModel = QStandardItemModel()
		self.autoClassTableModel_: QStandardItemModel = QStandardItemModel()

		self.selectedCourse_: QModelIndex = QModelIndex()
		self.selectedClass_: QModelIndex = QModelIndex()
		self.selectedAutoCourse_: list[QModelIndex] = list()

	def loadAutoCourse(self) -> tuple[bool, str]:
		if self.loadFileName_:
			self.courseFile_ = open(self.loadFileName_, "r", encoding="utf-8")
			accountDict = json.loads(self.courseFile_.read())
			classDict = accountDict.get(self.userName_)
			self.courseFile_.close()
			if classDict:
				headers = classDict["headers"]
				classes = classDict["classes"]
				data = classDict["data"]
				self.autoClassTableModel_.clear()
				self.autoClassList_.clear()
				self.autoClassTableModel_.setColumnCount(len(headers))
				self.autoClassTableModel_.setRowCount(len(classes))
				for col in range(len(headers)):
					self.autoClassTableModel_.setHorizontalHeaderItem(col, QStandardItem(headers[col]))
				for row in range(len(classes)):
					for col in range(len(classes[row])):
						self.autoClassTableModel_.setItem(row, col, QStandardItem(classes[row][col]))
				for class_ in data:
					self.autoClassList_.append(ExtensionClass(**class_))
				return True, "加载成功"
			return False, "该账号没有保存的选课"
		return False, str()

	def saveAutoCourse(self) -> tuple[bool, str]:
		if self.saveFileName_:
			self.courseFile_ = open(self.saveFileName_, "w", encoding="utf-8")
			headers = list()
			classes = list()
			data = list()
			for col in range(self.autoClassTableModel_.columnCount()):
				headers.append(self.autoClassTableModel_.horizontalHeaderItem(col).text())
			for row in range(self.autoClassTableModel_.rowCount()):
				class_ = list()
				for col in range(self.autoClassTableModel_.columnCount()):
					class_.append(self.autoClassTableModel_.item(row, col).text())
				classes.append(class_)
			for class_ in self.autoClassList_:
				data.append(class_.__dict__)

			accountDict = {
				self.userName_: {
					"headers": headers,
					"classes": classes,
					"data": data
				}
			}
			self.courseFile_.write(json.dumps(accountDict))
			self.courseFile_.close()
			return True, "保存成功"
		return False, str()
