# -*- coding: utf-8 -*-
import os
from functools import partial
import bokeh_extended as bke

from bokeh.charts import output_file, show, BoxPlot
from bokeh.layouts import row, column
from bokeh.sampledata.autompg import autompg as df
from bokeh.io import curdoc

doc = curdoc()

#print(df)
box1 = bke.charts.BoxPlot(df, values='mpg', label='origin',
        show_limits=True, limit=[10,40],
        title="Auto MPG Boxplot", plot_width=800)

box2 = bke.charts.BoxPlot(df, values='displ', label='cyl',
        show_limits=True, limit=[100,400],
        title="Auto MPG Boxplot", plot_width=800)

l = column(box1(),box2())
doc.add_root(l)
doc.title = "BoxPlot"


if __name__ == "__main__":
    output_file(os.path.join(os.path.dirname(__file__),'tmp','histogram.html'))
    show(l)
    print("Not running in a server, no interaction.")
    print("Run: bokeh serve histogram.py")
else:
    print("Boxplot App")
    #hist2.figure.x_range.on_change('end',update_plot)
    #hist2.figure.x_range.on_change('start',update_plot)
