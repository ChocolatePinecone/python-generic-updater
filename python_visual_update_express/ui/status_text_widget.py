from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QWidget, QLabel, QHBoxLayout
from pyqtwaitingspinner import WaitingSpinner, SpinnerParameters, SpinDirection
from qtawesome import IconWidget

from python_generic_updater.libs.icons import IconsLib, Icon

SPINNER_PARAMS = SpinnerParameters(  # These can be generated in the spinner editor `spinner-conf`
    roundness=100.0,
    trail_fade_percentage=50.0,
    number_of_lines=13,
    line_length=5,
    line_width=2,
    inner_radius=3,
    revolutions_per_second=1.57,
    color=QColor(80, 80, 80),
    minimum_trail_opacity=3.14,
    spin_direction=SpinDirection.CLOCKWISE,
    center_on_parent=True,
    disable_parent_when_spinning=False,
)
SPINNER_WIDGET_WIDTH = 30
SPINNER_WIDGET_HEIGHT = 30
MAX_TEXT_WIDTH = 300


class StatusTextWidget(QWidget):
    icon: IconWidget
    status_text: QLabel
    spinner_widget: QWidget
    spinner: WaitingSpinner

    def __init__(self):
        super().__init__()

        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.icon = IconWidget()
        layout.addWidget(self.icon)
        layout.addSpacing(5)

        self.status_text = QLabel()
        self.status_text.setFixedHeight(
            SPINNER_WIDGET_HEIGHT)  # Prevents vertical repositioning when spinner is activated
        layout.addWidget(self.status_text)

        self.spinner_widget = QWidget()
        self.spinner = WaitingSpinner(self.spinner_widget, SPINNER_PARAMS)
        self.set_spinner_active(False)
        layout.addWidget(self.spinner_widget)

        self.setLayout(layout)

    def set_spinner_active(self, active: bool):
        if active:
            self.spinner.start()
            self.spinner_widget.setFixedSize(SPINNER_WIDGET_WIDTH, SPINNER_WIDGET_HEIGHT)
        else:
            self.spinner.stop()
            self.spinner_widget.setFixedSize(0, 0)

    def set_status(self, status: str, spinner: bool = False, icon: Icon = None):
        self.status_text.setWordWrap(False)  # Disable word wrap for determining correct size hint
        self.status_text.setText(status)
        self.status_text.setStyleSheet('')
        width = min(self.status_text.sizeHint().width(), MAX_TEXT_WIDTH)
        self.status_text.setFixedWidth(width)
        self.status_text.setWordWrap(True)
        self.set_spinner_active(spinner)
        if icon:
            self.icon.setIcon(IconsLib.get_icon(icon))

    def set_warning_status(self, status: str):
        self.status_text.setText(status)
        self.status_text.setStyleSheet('color: red;')

    def reset_status(self):
        self.status_text.setText('')
        self.status_text.setStyleSheet('')
        self.set_spinner_active(False)
