from PySide2 import QtCore, QtGui


class Field(object):
    """Base class for all fields used to create settings for indicators"""

    def __init__(self, attribute_name):

        # Constants
        self._attribute_name = attribute_name

    @property
    def attribute_name(self) -> str:
        """Return the attribute name of the InputField

        :return: The attribute name
        :rtype: str
        """
        return self._attribute_name

    def reset(self):
        """Reset all settings to default values"""
        raise NotImplemented

    def __getitem__(self, key):
        return getattr(self, key, None)

    def __repr__(self):
        return "<%s %s @0x%08x>" % (
            __class__.__name__,
            self._attribute_name,
            id(self),
        )

    def __str__(self):
        return "%s %s" % (__class__.__name__, self._attribute_name)


class ChoiceField(Field):
    """Object for choice management for indicators"""

    def __init__(
        self, attribute_name: str, choices: tuple, default=None, **kwargs
    ):
        super(ChoiceField, self).__init__(attribute_name)
        """Create a customisable field in order to customise graph.
        This class represent a choice setting. (creates automatically
        a combobox in the input settings page)

        :param attribute_name: The name of the field
        :type attribute_name: str
        :param choices: All available choices
        :type choices: tuple, list, optional
        :param default: The default value
        :type default: int or float

        kwargs parameters:

        :param value_type: The type of value (list or tuple). defaults to list
        :type value_type: list, tuple
        """

        # Constants
        self._choices = choices
        self._default = default
        self.current = default
        self.value_type = list

        # kwargs settings
        if kwargs.get("value_type", list):
            value_type = kwargs.get("value_type")
            if value_type in [list, tuple]:
                self.value_type = value_type

    @property
    def choices(self):
        """Return available choices

        :return: All choices
        :rtype: list
        """
        return self._choices

    @property
    def default(self):
        """Return default choice

        :return: The default choice
        :rtype: string or number
        """
        return self._default

    def set_choice(self, choice):
        """Set the current choice

        :param choice: The new choice
        :type choice: string or number
        """
        if choice in self._choices:
            self.current = choice

    def reset(self):
        """Reset che ChoiceField to default value"""
        self.current = self._default

    def __repr__(self):
        return "<InputField %s @0x%08x>" % (self._attribute_name, id(self))

    def __str__(self):
        return "InputField %s" % (self._attribute_name)


class InputField(Field):
    """Object for value and style management for indicators"""

    def __init__(
        self, attribute_name: str, color=None, value=None, width=None, **kwargs
    ):
        super(InputField, self).__init__(attribute_name)
        """Create a customisable field in order to customise graph.
        - If no value is providen but a color is, this field will be present
        in the "style" setting page.
        - If no color is provided but a value is, this field will be present
        in the "Input" setting page.
        - If both are provided, this will be present in both settings.

        :param attribute_name: The name of the field
        :type attribute_name: str
        :param color: The color to apply by default, defaults to None
        :type color: tuple, optional
        :param value: The value to apply by default, defaults to None
        :type value: int or float, optional
        :param width: The width to apply by default, defaults to None
        :type width: int or float, optional

        kwargs parameters:

        :param disable_line_style: Disable the posibility to choose a
        line stype from the style page. defaults to False
        :param disable_line_width: Disable the posibility to choose a
        line width from the width page. defaults to False
        :type disable_line_style: bool
        :param line_style: Choose a style to apply for lines.
        3 Choices are available (line, dash-line and dot-line). defaults to line
        :type line_style: str
        """

        # Constans
        self._line_styles = {
            "line": {"icon": ":/svg/line.svg", "style": QtCore.Qt.SolidLine},
            "dash-line": {
                "icon": ":/svg/dash-line.svg",
                "style": QtCore.Qt.DashLine,
            },
            "dot-line": {
                "icon": ":/svg/dot-line.svg",
                "style": QtCore.Qt.DotLine,
            },
        }

        self._default_color = QtGui.QColor(*color) if color else None
        self._default_value = value
        self._default_width = width
        self._default_line_style = QtCore.Qt.SolidLine

        self.color = self._default_color
        self.value = self._default_value
        self.width = self._default_width
        self.disable_line_style = False
        self.disable_line_width = False
        self.value_type = int
        self.line_style = self._default_line_style

        # Kwargs settings
        if kwargs.get("disable_line_style", False):
            self.disable_line_style = True
        if kwargs.get("disable_line_width", False):
            self.disable_line_width = True
        if kwargs.get("line_style", None):
            self.set_line_style(kwargs.get("line_style"))
        if kwargs.get("value_type", int):
            value_type = kwargs.get("value_type")
            if value_type in [int, float]:
                self.value_type = value_type

    def set_color(self, color: QtGui.QColor):
        """Set the color of the InputField

        :param color: The new color to set
        :type color: tuple
        """
        self.color = color

    def set_value(self, value):
        """Set the value of the InputField

        :param value: The new value to set
        :type value: int, float
        """
        self.value = value

    def set_width(self, width):
        """Set the width of the InputField

        :param width: The new width to set
        :type width: int, float
        """
        self.width = width

    def set_line_style(self, line_style_name: str = None, line_style=None):
        """Set the line style of the InputField

        :param line_style_name: The style of the line (line, dash-line, dot-line)
        :type line_style_name: str, optional
        :param line_style: The style of the line (1, 2, 3)
        :type line_style: int, optional
        :raises KeyError: If the style doesn't exists
        """
        if not line_style_name and not line_style:
            return
        if line_style_name:
            if line_style_name not in self._line_styles:
                raise KeyError("%s not in available styles" % line_style_name)
            self.line_style = self._line_styles.get(line_style_name).get(
                "style"
            )
            return
        if line_style:
            for style_data in self._line_styles.values():
                if style_data.get("style") != line_style:
                    continue
                self.line_style = line_style

    def reset(self):
        """Reset the InputField to default values"""
        self.color = self._default_color
        self.value = self._default_value
        self.width = self._default_width
        self.line_style = self._default_line_style

    def __repr__(self):
        return "<%s %s @0x%08x>" % (
            __class__.__name__,
            self._attribute_name,
            id(self),
        )

    def __str__(self):
        return "%s %s" % (__class__.__name__, self._attribute_name)


class Indicator(object):
    """Base class that each indicator must inherit from. Within this class
    you must define the methods that all of your plugins must implement
    """

    def __init__(self):
        self.name = "Indicator"
        self.description = "Indicator description"
        self.enabled = False

        self._fields = []
        self._plots = []

    @property
    def fields(self) -> list:
        """Return all registered fields in the Indicator plugin

        :return: List of registered fields
        :rtype: list
        """
        return self._fields

    def register_field(self, field: InputField):
        """Register a field setting

        :param field: The input
        :type field: object
        """
        self._fields.append(field)

    def register_fields(self, *args: list):
        """Register all given fields settings"""
        for arg in args:
            if not isinstance(arg, (InputField, ChoiceField)):
                continue
            self.register_field(field=arg)

    def get_field(self, attribute_name: str) -> InputField:
        """Get the filed which correspond to the given attribute name

        :param attribute_name: The name of the attribute what the InputField
        represents.
        :type attribute_name: str
        :return: The InputField which correspond to the given attribute name
        :rtype: InputField
        """
        for _field in self._fields:
            if _field.attribute_name == attribute_name:
                return _field

    def register_plot(self, plot):
        """Register a plot inside the indicator in order to be abble to delete
        it later, if it is necessary.

        :param plot: The plot to add
        :type plot: pyqtgraph.plotItem
        """
        self._plots.append(plot)

    def register_plots(self, *args: list):
        """Register all given plots"""
        for arg in args:
            self.register_plot(plot=arg)

    def create_indicator(self, graph_view, *args, **kwargs):
        """The method that we expect all plugins to implement. This is the
        method that our framework will call to draw the indicator
        """
        self.enabled = True

    def remove_indicator(self, graph_view, *args, **kwargs):
        """The method that we expect all plugins to implement. This is the
        method that our framework will call to remove the indicator
        """
        self.enabled = False
        if not self._plots:
            return
        # Remove all plots
        for plot in self._plots:
            plot.clear()
        self._plots = []
        # Update graph
        graph_view.update()
