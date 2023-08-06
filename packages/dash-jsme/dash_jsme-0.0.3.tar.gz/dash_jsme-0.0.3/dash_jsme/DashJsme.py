# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class DashJsme(Component):
    """A DashJsme component.
ExampleComponent is an example component.
It takes a property, `label`, and
displays it.
It renders an input with the property `value`
which is editable by the user.

Keyword arguments:
- id (string; optional): The ID used to identify this component in Dash callbacks.
- label (string; required): A label that will be printed when this component is rendered.
- value (string; optional): The value displayed in the input.
- height (string; required)
- width (string; required)"""
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, label=Component.REQUIRED, value=Component.UNDEFINED, height=Component.REQUIRED, width=Component.REQUIRED, **kwargs):
        self._prop_names = ['id', 'label', 'value', 'height', 'width']
        self._type = 'DashJsme'
        self._namespace = 'dash_jsme'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'label', 'value', 'height', 'width']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in ['label', 'height', 'width']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(DashJsme, self).__init__(**args)
