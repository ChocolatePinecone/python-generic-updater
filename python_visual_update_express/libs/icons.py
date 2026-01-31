from dataclasses import dataclass
from enum import Enum

import qtawesome as qta
from PyQt6.QtCore import QSize
from PyQt6.QtGui import QColor


class Icon(Enum):
    CROSS_CIRCLE = 0
    CHECKMARK_CIRCLE = 1


@dataclass
class IconProperties:
    id: str
    color: QColor = QColor(50, 50, 50)


ICON_PROPERTIES = {
    Icon.CROSS_CIRCLE: IconProperties('fa5s.times-circle', QColor('red')),
    Icon.CHECKMARK_CIRCLE: IconProperties('fa5s.check-circle', QColor('green')),
}


class IconsLib:
    @staticmethod
    def get_icon(icon: Icon, size: QSize = QSize(30, 30)):
        icons = [item.value for item in Icon]
        if not icon.value in icons:
            raise AssertionError('Icon "%s" could be found' % str(icon))
        if not icon in ICON_PROPERTIES.keys():
            raise AssertionError('Properties for icon "%s" could be found' % str(icon))

        icon_props = ICON_PROPERTIES.get(icon)

        return qta.icon(icon_props.id, color=icon_props.color, size=size)
