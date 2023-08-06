"""
This file will replace current toolbar and tools
all button functions will be implemented as a tool function
"""


from glue.viewers.common.qt.toolbar import BasicToolbar

from .selection_tools import VispyMouseMode


class VispyViewerToolbar(BasicToolbar):

    def __init__(self, viewer=None, **kwargs):
        BasicToolbar.__init__(self, viewer, **kwargs)
        self._vispy_widget = viewer._vispy_widget
        self.canvas = self._vispy_widget.canvas

    def activate_tool(self, mode):
        if isinstance(mode, VispyMouseMode):
            self._vispy_widget.canvas.events.mouse_press.connect(mode.press)
            self._vispy_widget.canvas.events.mouse_release.connect(mode.release)
            self._vispy_widget.canvas.events.mouse_move.connect(mode.move)
            self.disable_camera_events()
        super(VispyViewerToolbar, self).activate_tool(mode)

    def deactivate_tool(self, mode):
        if isinstance(mode, VispyMouseMode):
            self._vispy_widget.canvas.events.mouse_press.disconnect(mode.press)
            self._vispy_widget.canvas.events.mouse_release.disconnect(mode.release)
            self._vispy_widget.canvas.events.mouse_move.disconnect(mode.move)
            self.enable_camera_events()
        super(VispyViewerToolbar, self).deactivate_tool(mode)

    @property
    def camera(self):
        return self._vispy_widget.view.camera

    def enable_camera_events(self):
        self.camera.interactive = True

    def disable_camera_events(self):
        self.camera.interactive = False
