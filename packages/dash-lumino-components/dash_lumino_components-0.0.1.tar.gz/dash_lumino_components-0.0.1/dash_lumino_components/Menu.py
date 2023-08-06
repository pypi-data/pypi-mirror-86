# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Menu(Component):
    """A Menu component.
A widget which displays items as a canonical menu.

Keyword arguments:
- children (a list of or a singular dash component, string or number; optional): An array of the menu items in the menu.
- id (string; required): The ID used to identify this component in Dash callbacks.
- title (string; required): The title of the menu
- iconClass (string; optional): The icon class of the menu"""
    @_explicitize_args
    def __init__(self, children=None, id=Component.REQUIRED, title=Component.REQUIRED, iconClass=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'title', 'iconClass']
        self._type = 'Menu'
        self._namespace = 'dash_lumino_components'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'title', 'iconClass']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in ['id', 'title']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(Menu, self).__init__(children=children, **args)
