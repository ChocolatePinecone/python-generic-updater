from PyQt6.QtCore import QObject, pyqtSignal, QRunnable, pyqtSlot


class WorkerSignals(QObject):
    error = pyqtSignal(Exception)
    finished = pyqtSignal()
    success = pyqtSignal()
    successResult = pyqtSignal(object)


class Worker(QRunnable):
    signals: WorkerSignals

    def __init__(self, fn, *args, **kwargs):
        super().__init__()
        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        try:
            result = self.fn(*self.args, **self.kwargs)
            self.signals.success.emit()
            self.signals.successResult.emit(result)
        except Exception as ex:
            self.signals.error.emit(ex)
        finally:
            self.signals.finished.emit()
