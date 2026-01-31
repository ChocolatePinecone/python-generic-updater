from dataclasses import dataclass

from semver import Version


# This object will be filled with the needed info during runtime
@dataclass
class GeneralInfo:
    update_base_url: str
    current_update_version: Version
    target_directory_path: str


info: GeneralInfo
