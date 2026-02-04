import shutil
from enum import Enum
from tempfile import TemporaryDirectory

from PyQt6.QtCore import Qt, QThreadPool, pyqtSignal
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLayout, QPushButton, QHBoxLayout, QProgressBar

from python_visual_update_express.data import general_info
from python_visual_update_express.libs.file_download import download_text_file
from python_visual_update_express.libs.icons import Icon
from python_visual_update_express.libs.threading import Worker
from python_visual_update_express.libs.update_manager import UpdateManager
from python_visual_update_express.libs.updates_info import UpdatesInfo
from python_visual_update_express.ui.error_handling import process_error
from python_visual_update_express.ui.status_text_widget import StatusTextWidget

TEXT_INITIAL_STATUS = 'Ready to update'
TEXT_CHECKING_FOR_UPDATE = 'Checking for update...'
TEXT_UP_TO_DATE = 'Your application is already up to date'
TEXT_UPDATE_IS_AVAILABLE_TEMPLATE = 'Newer version "{}" has been found and can be downloaded'
TEXT_UPDATE_CANCELED = 'Update has been canceled'
TEXT_DOWNLOADING = 'Downloading update...'
TEXT_INSTALLING_UPDATE = 'Installing update...'
TEXT_UPDATE_COMPLETE_TEMPLATE = 'Application has been updated to version {}'

UPDATESCRIPT_FILENAME = 'updatescript.ini'


class ContentState(Enum):
    CHECK_FOR_UPDATE = 0
    UPDATE_AVAILABLE = 1
    UP_TO_DATE = 2
    RUN_UPDATE = 3
    INSTALL_UPDATE = 4
    UPDATE_COMPLETE = 5
    UPDATE_FAILED = 6
    UPDATE_CANCELED = 7


class WindowContent(QWidget):
    current_state: ContentState
    update_failed_text: str = ''
    updates_info: UpdatesInfo
    progress_bar: QProgressBar
    download_directory: TemporaryDirectory

    layout: QVBoxLayout = None
    update_manager: UpdateManager
    threadpool: QThreadPool

    quit_triggered = pyqtSignal()

    def __init__(self) -> None:
        super().__init__()

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(10, 10, 10, 5)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.setLayout(self.layout)

        self.update_manager = UpdateManager()
        self.threadpool = QThreadPool()

        self._load_content_by_state(ContentState.CHECK_FOR_UPDATE)

    def _load_content_by_state(self, state: ContentState) -> None:
        current_state = state

        self._clear_layout(self.layout)
        status_text = StatusTextWidget()
        self.layout.addStretch()
        self.layout.addWidget(status_text)

        match current_state:
            case ContentState.CHECK_FOR_UPDATE:
                status_text.set_status(TEXT_CHECKING_FOR_UPDATE, True)
                self.layout.addStretch()
                self._start_update_check()

            case ContentState.UPDATE_FAILED:
                status_text.set_status(self.update_failed_text, icon=Icon.CROSS_CIRCLE)
                self.layout.addStretch()
                self._add_quit_button(self.layout)

            case ContentState.UP_TO_DATE:
                status_text.set_status(TEXT_UP_TO_DATE, icon=Icon.CHECKMARK_CIRCLE)
                self.layout.addStretch()
                self._add_quit_button(self.layout)

            case ContentState.UPDATE_AVAILABLE:
                update_text = TEXT_UPDATE_IS_AVAILABLE_TEMPLATE.format(self.updates_info.latest_version)
                status_text.set_status(update_text)
                self.layout.addStretch()
                self._add_download_button_bar(self.layout)

            case ContentState.UPDATE_CANCELED:
                status_text.set_status(TEXT_UPDATE_CANCELED)
                self.layout.addStretch()
                self._add_quit_button(self.layout)

            case ContentState.RUN_UPDATE:
                status_text.set_status(TEXT_DOWNLOADING)
                self._add_download_progress_bar(self.layout)
                self.layout.addStretch()
                self._start_update_download()

            case ContentState.INSTALL_UPDATE:
                status_text.set_status(TEXT_INSTALLING_UPDATE)
                self.layout.addStretch()
                self._install_update()

            case ContentState.UPDATE_COMPLETE:
                text = TEXT_UPDATE_COMPLETE_TEMPLATE.format(self.updates_info.latest_version)
                status_text.set_status(text)
                self.layout.addStretch()
                self._add_quit_button(self.layout)

    def _clear_layout(self, layout) -> None:
        if isinstance(layout, QLayout):
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self._clear_layout(item.layout())

    def _start_update_check(self) -> None:
        checker = Worker(self._fetch_updatescript, general_info.info.update_base_url)
        checker.signals.successResult.connect(self._process_updatescript)
        checker.signals.error.connect(process_error)
        checker.signals.error.connect(lambda: self._fail_update(
            'An error occurred while checking for updates. Please try again later.'))
        self.threadpool.start(checker)

    def _fetch_updatescript(self, url: str) -> None:
        fetch_url = url + UPDATESCRIPT_FILENAME
        return download_text_file(fetch_url)

    def _process_updatescript(self, updatescript: str) -> None:
        try:
            self.updates_info = UpdatesInfo(updatescript)
        except Exception as ex:
            process_error(ex, self)
            self._fail_update(
                'Failed to parse update info from the update script. Please inform the developer of this error.')
            return

        current_version = general_info.info.current_update_version
        if not current_version in self.updates_info.release_versions:
            self._fail_update(
                'Current version not supported by the update script. Please inform the developer of this error.')
            return

        if current_version != self.updates_info.latest_version:
            self._load_content_by_state(ContentState.UPDATE_AVAILABLE)
        else:
            self._load_content_by_state(ContentState.UP_TO_DATE)

    def _add_quit_button(self, layout: QVBoxLayout) -> None:
        quit_button_bar = QWidget()
        h_layout = QHBoxLayout()
        quit_button_bar.setLayout(h_layout)

        h_layout.addStretch()
        quit_button = QPushButton('Quit')
        quit_button.clicked.connect(self.quit_triggered.emit)
        h_layout.addWidget(quit_button)

        layout.addWidget(quit_button_bar)

    def _add_download_button_bar(self, layout: QVBoxLayout) -> None:
        button_bar = QWidget()
        bar_layout = QHBoxLayout()
        bar_layout.addStretch()
        button_bar.setLayout(bar_layout)

        cancel_button = QPushButton('Cancel')
        cancel_button.clicked.connect(lambda: self._load_content_by_state(ContentState.UPDATE_CANCELED))
        download_button = QPushButton('Download and install')
        download_button.clicked.connect(lambda: self._load_content_by_state(ContentState.RUN_UPDATE))

        bar_layout.addWidget(cancel_button)
        bar_layout.addWidget(download_button)
        layout.addWidget(button_bar)

    def _add_download_progress_bar(self, layout: QVBoxLayout) -> None:
        self._add_progress_bar(layout)
        self.update_manager.download_progress_update.connect(self._update_progress_bar)

    def _add_progress_bar(self, layout: QVBoxLayout) -> None:
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        layout.addWidget(self.progress_bar)
        layout.addStretch()

    def _start_update_download(self) -> None:
        error_text_base = 'An error occurred while downloading. Please inform the developer of this error: '

        updater = Worker(self._download_update)
        updater.signals.successResult.connect(self._complete_download_step)
        updater.signals.error.connect(lambda ex: self._fail_update(error_text_base + str(ex)))
        self.threadpool.start(updater)

    def _download_update(self) -> TemporaryDirectory:
        download_directory = self.update_manager.download_update_files(
            self.updates_info,
            general_info.info.update_base_url)

        if not download_directory:
            raise RuntimeError('Files to download are unknown')

        return download_directory

    def _update_progress_bar(self, progress_value: float) -> None:
        progress_value_int = int(progress_value)
        self.progress_bar.setValue(progress_value_int)

    def _complete_download_step(self, downloaded_files_dir: TemporaryDirectory):
        self.download_directory = downloaded_files_dir
        self._load_content_by_state(ContentState.INSTALL_UPDATE)

    def _install_update(self):
        shutil.copytree(self.download_directory.name, general_info.info.target_directory_path, dirs_exist_ok=True)
        self._load_content_by_state(ContentState.UPDATE_COMPLETE)

    def _fail_update(self, fail_text: str) -> None:
        self.update_failed_text = fail_text
        self._load_content_by_state(ContentState.UPDATE_FAILED)
