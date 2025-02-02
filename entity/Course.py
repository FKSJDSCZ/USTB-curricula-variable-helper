class Course:
	def __init__(self, courseType: str, opener: str, epochCode: str, courseCode: str):
		self.courseType_ = courseType
		"""课程类型"""
		self.opener_ = opener
		self.epochCode_ = epochCode
		"""选课轮次代码"""
		self.courseCode_ = courseCode
		"""课程代码"""


class ExtensionCourse(Course):
	def __init__(self, courseType: str, opener: str, epochCode: str, courseCode: str, classIndexes: str):
		super().__init__(courseType, opener, epochCode, courseCode)
		self.classIndexes_ = classIndexes
