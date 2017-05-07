# -*- coding: utf-8 -*-
import os

import bokeh_extended as bke

from bokeh.charts import output_file, show
from bokeh.layouts import row, column
from bokeh.sampledata.autompg import autompg as df
from bokeh.io import curdoc
#from bokeh_extended import charts


hist = bke.charts.Histogram(df, values='mpg', title="Auto MPG Histogram", plot_width=400,
         x_range=[15,40])
hist2 = bke.charts.Histogram(df, values='displ', label='cyl', color='cyl', legend='top_right',
        title="MPG Histogram by Cylinder Count", plot_width=400, limit=[200,300],
        details=True, kw_rug={'rug_scale':0.008, 'fill_color': 'brown'})
hist3 = bke.charts.Histogram(df, values='weight', title="Auto MPG Histogram", plot_width=400)



hist2.limit = [250,450]
hist2.update_view('reset',2)

#hist3.bins = 4
hist3.x_range = [2000,4000]
#hist3.figure.x_range.start = 10
#hist3.update_view()

l = column(row(hist(), hist2()),row(hist3()))
output_file(os.path.join(os.path.dirname(__file__),'..','..','tmp','histogram.html'))
show(column(row(hist(), hist2()),row(hist3())))
curdoc().add_root(l)
#curdoc().title = "Histograms"


# if __name__ == "__main__":
#     output_file(os.path.join(os.path.dirname(__file__),'tmp','histogram.html'))
#     show(column(row(hist(), hist2()),row(hist3())))
#     print("Bokeh App not app")
# else:
#     print("Bokeh App")
