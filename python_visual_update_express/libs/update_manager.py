import os
from tempfile import TemporaryDirectory
from typing import Union

from PyQt6.QtCore import pyqtSignal, QObject

from python_visual_update_express.data import general_info
from python_visual_update_express.libs.file_download import download_file_to_location
from python_visual_update_express.libs.updates_info import UpdatesInfo

DOWNLOADABLE_FILES_PATH = 'Updates/'


class UpdateManager(QObject):
    completed_steps: int = 0
    step_percentage_increment: float

    download_progress_update = pyqtSignal(float)

    def download_update_files(self, info: UpdatesInfo, update_base_url: str) -> Union[TemporaryDirectory, None]:
        steps = info.get_remaining_release_steps(general_info.info.current_update_version)

        files_to_download = steps['files_to_download']
        if len(files_to_download) <= 0:
            return None

        self.step_percentage_increment = 100.0 / len(files_to_download)

        tmpdir = TemporaryDirectory()
        tmpdir_path = os.path.join(tmpdir.name, '')  # This adds a trailing slash if it's missing

        download_base_url = update_base_url + DOWNLOADABLE_FILES_PATH
        for file in files_to_download:
            download_file_to_location(download_base_url, file, tmpdir_path, self._update_download_progress)
        return tmpdir

    def _update_download_progress(self, block_num: int, block_size: int, total_size: int):
        downloaded = block_num * block_size
        if downloaded < total_size:
            total_percentage_gain = downloaded / total_size * self.step_percentage_increment
            progress_value = self._get_completion_percentage(total_percentage_gain)
        else:
            self.completed_steps += 1
            progress_value = self._get_completion_percentage()

        self.download_progress_update.emit(progress_value)

    def _get_completion_percentage(self, offset: float = 0.0) -> float:
        return self.completed_steps * self.step_percentage_increment + offset
