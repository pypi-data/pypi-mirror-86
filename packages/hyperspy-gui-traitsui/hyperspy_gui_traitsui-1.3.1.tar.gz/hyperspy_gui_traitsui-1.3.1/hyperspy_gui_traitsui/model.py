import traitsui.api as tu

from hyperspy_gui_traitsui.utils import add_display_arg
from hyperspy_gui_traitsui.buttons import OurFitButton, OurCloseButton
from hyperspy_gui_traitsui.tools import SpanSelectorInSignal1DHandler


class ComponentFitHandler(SpanSelectorInSignal1DHandler):

    def fit(self, info):
        """Handles the **Apply** button being clicked.

        """
        obj = info.object
        obj._fit_fired()
        return


@add_display_arg
def fit_component_traitsui(obj, **kwargs):
    fit_component_view = tu.View(
        tu.Item('only_current', show_label=True,),
        buttons=[OurFitButton, OurCloseButton],
        title='Fit single component',
        handler=ComponentFitHandler,
    )
    return obj, {"view": fit_component_view}
