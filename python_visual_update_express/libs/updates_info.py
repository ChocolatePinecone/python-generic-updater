import re
from typing import List

from semver import Version


class UpdatesInfo:
    release_versions: List[Version]  # Ordered list of versions from oldest to newest
    release_version_step_lists: dict[str, dict]  # Steps needed per version
    latest_version: Version

    def __init__(self, updatescript: str):
        self.release_versions = self._get_release_versions(updatescript)
        self.latest_version = self.release_versions[-1] if self.release_versions else None
        self.release_version_step_lists = self._get_all_release_steps(updatescript)

    def get_remaining_release_steps(self, current_version: Version):
        steps = {'files_to_download': []}

        if current_version == self.release_versions[-1]:
            return steps

        current_version_index = self.release_versions.index(current_version)
        newer_version_nrs = self.release_versions[current_version_index + 1:]
        newer_versions_steps = []
        for version_nr in newer_version_nrs:
            version_str = str(version_nr)
            newer_versions_steps.append(self.release_version_step_lists[version_str])

        for step in newer_versions_steps:
            steps['files_to_download'].extend(step['files_to_download'])

        # Remove duplicates by converting to a set and back (since set keys cannot be duplicate)
        steps['files_to_download'] = list(set(steps['files_to_download']))

        return steps

    def _get_release_versions(self, updatescript: str) -> List[Version]:
        match = re.search(r"releases\{([^}]*)}", updatescript, re.DOTALL)
        if not match:
            return []

        block_content = match.group(1)

        versions = []
        for line in block_content.splitlines():
            if line.strip():
                try:
                    version = Version.parse(line.strip())
                except:
                    continue

                versions.append(version)

        versions.sort()
        return versions

    def _get_all_release_steps(self, updatescript: str) -> dict:
        release_steps = {}

        matches = re.findall(r"release:(.*?)\{([^}]*)}", updatescript)
        if not matches:
            return {}

        for match in matches:
            version_nr = match[0]
            block_content = match[1]

            step = {
                'files_to_download': self._get_filenames_to_download(block_content)
            }

            release_steps[version_nr] = step

        return release_steps

    def _get_filenames_to_download(self, step_content: str) -> List[str]:
        matches = re.findall(r"DownloadFile:(.*?)\n", step_content)
        if not matches:
            return []

        filenames = []
        for match in matches:
            filenames.append(match)

        return filenames
