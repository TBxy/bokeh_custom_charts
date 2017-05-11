# -*- coding: utf-8 -*-
"""Extends bokeh histogram with additional feature and interactivity.
"""

# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------
from __future__ import absolute_import, print_function, division

import numpy as np
import pandas as pd
from bokeh.charts import Histogram as bkHistogram
from bokeh.plotting import figure as bkfigure
from bokeh.models.ranges import Range1d as bkRange1d
from bokeh.models.sources import ColumnDataSource as bkColumnDataSource
#from ..builder import Builder, create_and_build
#from ...models import FactorRange, Range1d


# -----------------------------------------------------------------------------
# Classes and functions
# -----------------------------------------------------------------------------
class Rugplot(object):
    """Plot datapoints in an array as sticks on an axis.
    """

    def __init__(self, figure=None, source=None, values=None , height=None, max_height=None,
            rug_scale=0.05, alpha_min=0.2, alpha_max=0.6, axis='x',
            histo=True, alpha=None, mirrored=True, inside=False, kw_figure={}, **kw):
        """ Adds datapoints in an array as sticks to a figure.
        Args:
          data (list(float)): the data source for the chart.
          figure (Figure): figure to add Rugplot.
          height (float): height of the sticks.
          max_height (float): max height of the plot, if not specified y_range.end is taken.
          rug_scale (float): stick scale from max_height. This is used to calculate height
            height is not specified.
          alpha_range (float): range for the alpha values: range goes from
            1-alpha_range to 1.
          axis (str): Axis to add sticks (either 'x', 'horizontal', 'y', or 'veritical').
          **kw: additional argument for hBar or vBar glyph.
        Returns:
            :class:`Figure`: the rugs are added to the given figure automatically
        """
        if source is not None:
            self.source = source
        else:
            self.source = bkColumnDataSource()
        if values is not None:
            if isinstance(values,basestring):
                self.values = values
            else:
                self.values = 'x'
                self.source.data['x'] = values

#             if data is None:
#                 data = pd.DataFrame()
#             else:
#                 data = pd.DataFrame(data)
#             #self.source = bkColumnDataSource()
#             print("[Rugplot] data:")
#             print(data)
            # self.source = bkColumnDataSource(data)

        self.data = pd.DataFrame()
        self.data[self.values] = self.source.data[self.values]
        #self.source.data['length'] = 5

        if figure:
            self.figure = figure
        else:
            self.figure = bkfigure(**kw_figure)




        hist_all, edges_all = np.histogram(self.data, bins=len(self.data))
        max_height = max_height if max_height else np.max(hist_all)
        if histo:
            self.data['hist'] = hist_all / hist_all.max() * max_height * rug_scale + max_height/5 * rug_scale
        else:
            self.data['hist'] = max_height * rug_scale
        if mirrored:
                self.data['hist_neg'] = self.data['hist'] * -1
        else:
            if inside:
                self.data['hist_neg'] = 0
            else:
                self.data['hist_neg'] = self.data['hist'] * -1
                self.data['hist'] = 0
        print (self.data)
        if alpha == None or alpha == True:
            alpha_range = alpha_max - alpha_min
            alpha = hist_all/np.max(hist_all)  * alpha_range + alpha_min
        #kw.setdefault('fill_alpha',alpha)
        self.data['alpha'] = alpha
        kw.setdefault('line_width',1.5)
        #kw.setdefault('line_alpha',alpha)
        kw.setdefault('line_color',"green")
        self.source.data = bkColumnDataSource.from_df(self.data)
        self.figure = figure
        if axis.lower() in ['y' ,'vertical']:
            self.rug = self.figure.segment(source=self.source, x0='hist',
                    y0=self.values, x1='hist_neg',y1=self.values,
                    line_alpha='alpha', **kw)
        else:
            self.rug = self.figure.segment(source=self.source, y0='hist',
                    x0=self.values, y1='hist_neg',x1=self.values,
                    line_alpha='alpha', **kw)

        self.kw = kw

    def remove(self):
        self.rug.glyph.line_color = None

    def add(self):
        self.rug.glyph.line_color = self.kw.get('line_color')

    def update(self, options):
        """ update the rugs wiht new settings.

        Example:
            rug_plot.update({'fill_color': 'blue'})
        """
        for key in options:
            pass
            #setattr(self.rug.glyph,key, options.get(key))
            #self.kw[key] = options.get(key)


    def __call__(self):
        return self.figure
    def plot(self):
        return self.figure



