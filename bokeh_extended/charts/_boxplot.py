# -*- coding: utf-8 -*-
"""Extends bokeh histogram with additional feature and interactivity.
"""

# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------
from __future__ import absolute_import, print_function, division

import numpy as np
import pandas as pd
from bokeh.plotting import figure as bkfigure
#from bokeh.models.ranges import Range1d as bkRange1d
from bokeh.models.sources import ColumnDataSource as bkColumnDataSource
from bokeh.models import BoxAnnotation as bkBoxAnnotation
from bokeh.models import widgets as bkw
from bokeh.models import LabelSet as bkLabelSet
from bokeh.models import Label as bkLabel
from bokeh.layouts import row as bkrow
from bokeh.layouts import column as bkcolumn
from bokeh.layouts import widgetbox as bkwidgetbox
#from ..builder import Builder, create_and_build
#from ...models import FactorRange, Range1d
from ._rugplot import Rugplot
from bokeh.io import curdoc
from ..util import debounce
from functools import partial

from bokeh.charts import BoxPlot as bkBoxPlot

# -----------------------------------------------------------------------------
# Classes and functions
# -----------------------------------------------------------------------------
class BoxPlot(object):
    """This allows to draw boxplots.
    """

    def __init__(self,data, show_limits=None, limit=None, show_table=True, **kw):
        """ Create boxplot        """

        kw.setdefault('data',data)

        data = pd.DataFrame(data)
        self.figure = bkBoxPlot(**kw)
        self._limit = limit
        self._values = kw.get('values','x')
        self.data = data[self._values]
        self.show_limits = show_limits if show_limits != None else True if limit else False
        self.limit = limit
        # TODO create separete limits plot and/or limit mixin
        if self.show_limits:
            self.kw_outer_limit_box = {}
            self.kw_outer_limit_box.setdefault('fill_alpha',0.1)
            self.kw_outer_limit_box.setdefault('fill_color','red')
            self.kw_outer_limit_box.setdefault('line_width',2)
            self.kw_outer_limit_box.setdefault('line_alpha',0.4)
            self.kw_inner_limit_box = {}
            self.kw_inner_limit_box.setdefault('fill_alpha',0.1)
            self.kw_inner_limit_box.setdefault('fill_color','yellow')
            self.kw_inner_limit_box.setdefault('line_alpha',0)
            self._lower_limit_box = bkBoxAnnotation(top=self.limit[0], \
                    **self.kw_outer_limit_box)
            self._upper_limit_box = bkBoxAnnotation(bottom=self.limit[1], \
                    **self.kw_outer_limit_box)
            self._mid_limit_box = bkBoxAnnotation(top=self.limit[0], bottom=self.limit[1], \
                **self.kw_inner_limit_box)
            self.figure.add_layout(self._lower_limit_box)
            self.figure.add_layout(self._upper_limit_box)
            self.figure.add_layout(self._mid_limit_box)

        if show_table:
            self.stat = pd.DataFrame
            self.stat = data.groupby(kw.get('label'))[self._values].describe() #.transpose()
            #self.stat = self.stat.to_dict()
            self.stat[kw.get('label')] = self.stat.index
            self.stat['median'] = self.stat['50%']
            self.stat['x'] = np.arange(1,len(self.stat)+1)

            #print (self.stat)
            stat_source = bkColumnDataSource(self.stat)
            #print (stat_source.data)
            STATS = ['count','min','mean','median','std', 'max']
            offset = -20
            yoffset = -50
            fsize=kw.get('table_font_size','10pt')
            start = self.data.min()
            for st_label in STATS:
                #field = 'label_{}'.format(st_label)
                #self.stat[field] = '{}: {}'.format(st_label.title(), self.stat[st_label])
                #self.stat[field] = st_label.title() + ": " + self.stat[st_label].astype(str)
                #stat_source = bkColumnDataSource.from_df(self.stat)
                try:
                    self.stat[st_label] = self.stat[st_label].map('{:g}'.format)
                except Exception as e:
                    print(e)
                    pass
                self.stat_labels = bkLabelSet(x='x', y=start, text=st_label, level='glyph',
                 x_offset=-10, y_offset=yoffset, source=stat_source, text_font_size=fsize)
                stat_title = bkLabel(x=0.2, y=start, text=st_label.title(), level='glyph',
                 x_offset=0, y_offset=yoffset, text_font_size=fsize)
                yoffset += offset
                self.figure.add_layout(self.stat_labels)
                self.figure.add_layout(stat_title)
            stat_source.data = bkColumnDataSource.from_df(self.stat)
            #print (self.stat)



    @property
    def limit(self):
        limit = self._limit
        if self._limit:
            pass
#            if len(self._limit) == 2:
#                #if np.isnan(self._limit[0]) or np.isnan(self._limit[1]):
#                if self._limit[0] == np.nan or self._limit[1] == np.nan:
#                    limit = [self.data.min(), self.data.max()]
        else:
            limit = [self.data.min(), self.data.max()]
        return limit

    @limit.setter
    def limit(self, limit):
        #print("LIMIT")
        #print(limit)
        limit = limit if limit else [self.data.min(), self.data.max()] \
                    if len(self.data)>1 else [0,0]
        #print(limit)
        #print(self.data)
        self._limit = limit

    def __call__(self):
        return self.plot()
    def plot(self):
        #if self.add_menu:
            #return bkrow(self.menu(), self.hist)
        return self.figure



