from krita import Krita, DockWidgetFactoryBase, DockWidgetFactory
from .layer_commander import LayerCommander

Krita.instance().addDockWidgetFactory(DockWidgetFactory(
    'layer_commander', DockWidgetFactoryBase.DockPosition.DockRight, LayerCommander))
