import chart


class ChartStock(chart.Chart):
    """
    A class for writing the Excel XLSX Stock charts.

    """

    ###########################################################################
    #
    # Public API.
    #
    ###########################################################################

    def __init__(self, options=None):
        """
        Constructor.

        """
        super(ChartStock, self).__init__()

        if options is None:
            options = {}

        self.show_crosses = 0
        self.hi_low_lines = {}
        self.date_category = True

        # Override and reset the default axis values.
        self.x_axis['defaults']['num_format'] = 'dd/mm/yyyy'
        self.x2_axis['defaults']['num_format'] = 'dd/mm/yyyy'

        self.set_x_axis({})
        self.set_x2_axis({})

    ###########################################################################
    #
    # Private API.
    #
    ###########################################################################

    def _write_chart_type(self, args):
        # Override the virtual superclass method with a chart specific method.
        # Write the c:stockChart element.
        self._write_stock_chart(args)

    ###########################################################################
    #
    # XML methods.
    #
    ###########################################################################

    def _write_stock_chart(self, args):
    # Write the <c:stockChart> element.
    # Overridden to add hi_low_lines().

        if args['primary_axes']:
            series = self._get_primary_axes_series()
        else:
            series = self._get_secondary_axes_series()

        if not len(series):
            return

        # Add default formatting to the series data.
        self._modify_series_formatting()

        self._xml_start_tag('c:stockChart')

        # Write the series elements.
        for data in series:
            self._write_ser(data)

        # Write the c:dropLines element.
        self._write_drop_lines()

        # Write the c:hiLowLines element.
        if args.get('primary_axes'):
            self._write_hi_low_lines()

        # Write the c:upDownBars element.
        self._write_up_down_bars()

        # Write the c:marker element.
        self._write_marker_value()

        # Write the c:axId elements
        self._write_axis_ids(args)

        self._xml_end_tag('c:stockChart')

    def _modify_series_formatting(self):
        # Add default formatting to the series data.

        index = 0

        for series in self.series:
            if index % 4 != 3:
                if not series['line']['defined']:
                    series['line'] = {'width': 2.25,
                                      'none': 1,
                                      'defined': 1}

                if series['marker'] is None:
                    if index % 4 == 2:
                        series['marker'] = {'type': 'dot', 'size': 3}
                    else:
                        series['marker'] = {'type': 'none'}

            index += 1