class Class:
	def __init__(
			self,
			courseType: str,
			opener: str,
			epochCode: str,
			courseCode: str,
			currentClassIndex: str
	):
		self.courseType = courseType
		"""课程类型"""
		self.opener = opener
		self.epochCode = epochCode
		"""选课轮次代码"""
		self.courseCode = courseCode
		"""课程代码"""
		self.currentClassIndex = currentClassIndex
		"""班级编号（通知单编号）"""


class ExtensionClass(Class):
	def __init__(
			self,
			courseType: str,
			opener: str,
			epochCode: str,
			courseCode: str,
			classIndexes: str,
			currentClassIndex: str
	):
		super().__init__(courseType, opener, epochCode, courseCode, currentClassIndex)
		self.classIndexes = classIndexes
