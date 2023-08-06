from PyQt5 import QtDesigner, QtGui, QtWidgets, QtCore
#from qtpy.QtWidgets import QLabel, QApplication, QDoubleSpinBox, QWidget, QPushButton
from PyQt5.QtWidgets import QLabel, QApplication, QDoubleSpinBox, QWidget, QPushButton, QPlainTextEdit
#from qtpy.QtDesigner import QExtensionFactory
from PyQt5.QtDesigner import QExtensionFactory
from PyQt5.QtCore import pyqtProperty as Property
import inspect
from itertools import dropwhile
import textwrap
from .Base import BaseWidget
import sys
from IPython import get_ipython
from PyQt5 import QtCore
from PyQt5.QtCore import QThread
from ..worker import Worker, WorkerSignals
from functools import partial
import logging
import time

logger = logging.getLogger(__name__)
#logger.setLevel(logging.DEBUG)
logger.setLevel(logging.WARN)


class WorkerThread(QThread):
	#lock = QReadWriteLock()
	cancelled = False
	def cancel(self):
		WorkerThread.cancelled = True
	def resume(self):
		WorkerThread.cancelled = False
	def setFunc(self, func):
		self.func = func
	def run(self):
		self.func()	


class CodeObject(BaseWidget):

	def __init__(self, parent=None, copyNameSpace=True):
		#self.parent = parent
		super().__init__(parent)
		code = textwrap.dedent(self.default_code())
		self._code = bytes(code, "utf-8")
		self._paused = True
		self._useThreading = False
		self._copyNameSpace = copyNameSpace
		self.ns_extras = {}
		self.worker = WorkerThread(self)

	def addToNameSpace(self, key, val):
		self.ns_extras[key] = val

	@Property("QByteArray", designable=True)
	def code(self):
		return self._code

	@code.setter
	def code(self, val):
		self._code = val
	
	def default_code(self):
		return ""

	def pause_widget(self):
		logger.info("pausing widget")
		self._paused = True

	def resume_widget(self):
		logger.info("unpausing widget")
		self._paused = False
		#self.setup_namespace()

		
	def setup_namespace(self):
		t0 = time.time()
		ip = get_ipython()
		if self._copyNameSpace:
			ns = ip.user_ns.copy()
		else:
			ns = ip.user_ns
			
		ns['self'] = self
		ns.update(self.ns_extras)
		self.ns = ns
		logger.info("setup_namespace duration for "+self.objectName()+": "+str(time.time()-t0))

	def runInNameSpace(self, codeString):
		if self._paused:
			logger.info("widget paused")
			return
		#ns = vars(sys.modules[self.__class__.__module__])
		self.setup_namespace()
		logger.info("runInNameSpace for "+self.objectName())
		
		try:
			#exec(self._code, ns)
			t0 = time.time()
			exec(codeString, self.ns)
			#exec(b'', self.ns)
			#exec("", self.ns)
			logger.info("exec duration for "+self.objectName()+": "+str(time.time()-t0))
		except BaseException as e:
			additional_info = " Check code in "+self.objectName()+" widget"
			raise type(e)(str(e) + additional_info).with_traceback(sys.exc_info()[2])
		#for v in self.ns.values():
		#	del v
		#self.ns.clear()
		del self.ns


	def runPaused(self):
		pass

	def runCode(self):
		if self._paused:
			self.runPaused()
			return
		if not self._useThreading:
			self.runInNameSpace(self._code)
		else:
			#worker = Worker(partial(self.runInNameSpace, self._code))
			#self.threadpool.start(worker)
			self.worker.setFunc(partial(self.runInNameSpace, self._code))
			self.worker.start()
