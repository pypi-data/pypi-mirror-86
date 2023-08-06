from glue.core import Subset
from glue.external.echo import (CallbackProperty, SelectionCallbackProperty,
                                delay_callback)
from glue.core.state_objects import StateAttributeLimitsHelper
from glue.core.data_combo_helper import ComponentIDComboHelper
from ..common.layer_state import VispyLayerState

__all__ = ['VolumeLayerState']


class VolumeLayerState(VispyLayerState):
    """
    A state object for volume layers
    """

    attribute = SelectionCallbackProperty()
    vmin = CallbackProperty()
    vmax = CallbackProperty()
    subset_mode = CallbackProperty('data')
    limits_cache = CallbackProperty({})

    def __init__(self, layer=None, **kwargs):

        super(VolumeLayerState, self).__init__(layer=layer)

        if self.layer is not None:

            self.color = self.layer.style.color
            self.alpha = self.layer.style.alpha

        self.att_helper = ComponentIDComboHelper(self, 'attribute')

        self.lim_helper = StateAttributeLimitsHelper(self, attribute='attribute',
                                                     lower='vmin', upper='vmax',
                                                     cache=self.limits_cache)

        self.add_callback('layer', self._on_layer_change)
        if layer is not None:
            self._on_layer_change()

        if isinstance(self.layer, Subset):
            self.vmin = 0
            self.vmax = 1

        self.update_from_dict(kwargs)

    def _on_layer_change(self, layer=None):

        with delay_callback(self, 'vmin', 'vmin'):

            if self.layer is None:
                self.att_helper.set_multiple_data([])
            else:
                self.att_helper.set_multiple_data([self.layer])

    def update_priority(self, name):
        return 0 if name.endswith(('vmin', 'vmax')) else 1
