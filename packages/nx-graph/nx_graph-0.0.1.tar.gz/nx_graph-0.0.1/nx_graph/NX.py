# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class NX(Component):
    """A NX component.
ExampleComponent is an example component.
It takes a property, `label`, and
displays it.
It renders an input with the property `value`
which is editable by the user.

Keyword arguments:
- id (string; optional): The ID used to identify this component in Dash callbacks.
- data (dict; required): Vega-lite specification of the plot.
- tapNode (dict; optional): Node clicked."""
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, data=Component.REQUIRED, tapNode=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'data', 'tapNode']
        self._type = 'NX'
        self._namespace = 'nx_graph'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'data', 'tapNode']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in ['data']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(NX, self).__init__(**args)
