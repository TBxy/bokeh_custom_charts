# -*- coding: utf-8 -*-
"""Extends bokeh histogram with additional feature and interactivity.
"""

# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------
from __future__ import absolute_import, print_function, division

import numpy as np
from bokeh.charts import Histogram as bkHistogram
from bokeh.plotting import figure as bkfigure
from bokeh.models.ranges import Range1d as bkRange1d
#from ..builder import Builder, create_and_build
#from ...models import FactorRange, Range1d


# -----------------------------------------------------------------------------
# Classes and functions
# -----------------------------------------------------------------------------
class Rugplot(object):
    """Plot datapoints in an array as sticks on an axis.
    """

    def __init__(self, data, figure, height=None, max_height=None,
            rug_scale=0.03, alpha_range=0.8, axis='x',**kw):
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
        self.data = data
        hist_all, edges_all = np.histogram(self.data, bins=len(self.data))
        diff = np.abs(np.diff(self.data))
        width  = np.min(diff[diff>0])
        kw.setdefault('width',width)
        max_height = max_height if max_height else np.max(hist_all)
        height = height if height else max_height * rug_scale
        kw.setdefault('top',height)
        kw.setdefault('bottom',0)
        kw.setdefault('alpha_range',0.8)
        alpha = hist_all/np.max(hist_all)  * kw.get('alpha_range') +  \
            1- alpha_range
        del kw['alpha_range']
        kw.setdefault('fill_alpha',alpha)
        kw.setdefault('line_width',0)
        kw.setdefault('line_alpha',0)
        kw.setdefault('fill_color',"#000000")
        self.figure = figure
        if axis.lower() in ['y' ,'vertical']:
            kw.setdefault('height',width)
            kw.setdefault('right',height)
            kw.setdefault('left',0)
            del kw['bottom']
            del kw['top']
            del kw['width']
            self.rug = self.figure.hbar(y=self.data, **kw)
        else:
            self.rug = self.figure.vbar(x=self.data, **kw)
        self.kw = kw

    def remove(self):
        self.rug.glyph.fill_color = None
        self.rug.glyph.line_color = None

    def add(self):
        self.rug.glyph.fill_color = self.kw.get('fill_color')
        self.rug.glyph.line_color = self.kw.get('line_color')

    def update(self, options):
        """ update the rugs wiht new settings.

        Example:
            rug_plot.update({'fill_color': 'blue'})
        """
        for key in options:
            setattr(self.rug.glyph,key, options.get(key))
            self.kw[key] = options.get(key)


    def __call__(self):
        return self.figure
    def plot(self):
        return self.figure



