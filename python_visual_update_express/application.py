from pathlib import Path

from python_visual_update_express.ui.updater_window import UpdaterWindow

TMP_UPDATE_BASE_URL = 'http://jelmerpijnappel.nl/releases/broers-optiek/lensplan-hulp-applicatie/'
TMP_CURRENT_UPDATE_VERSION = '1.3.0'
TMP_TARGET_DIR = str(Path(__file__).resolve().parent.parent / "target")

window = UpdaterWindow(TMP_UPDATE_BASE_URL, TMP_CURRENT_UPDATE_VERSION, TMP_TARGET_DIR)
window.show()
