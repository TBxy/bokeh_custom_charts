# -*- coding: utf-8 -*-
import os
from functools import partial
import bokeh_extended as bke

from bokeh.charts import output_file, show
from bokeh.layouts import row, column
from bokeh.sampledata.autompg import autompg as df
from bokeh.io import curdoc
#from bokeh_extended import charts

doc = curdoc()

hist = bke.charts.Histogram(df, values='mpg',
        title="Auto MPG Histogram", plot_width=400,
        doc=doc, x_range=[15,40])
hist2 = bke.charts.Histogram(df, values='displ', label='cyl',
        color='cyl', legend='top_right', doc=doc,
        title="MPG Histogram by Cylinder Count", plot_width=400,
        limit=[200,300], details=False,
        kw_rug={'rug_scale':0.2, 'line_color': 'brown',
            'mirrored':False,'histo':False})
hist3 = bke.charts.Histogram(df, values='displ', show_limits=True,
        title="Auto MPG Histogram", plot_width=400,
        doc=doc, auto_update=True)
hist4 = bke.charts.Histogram(df, values='weight',
        title="Auto MPG Histogram", plot_width=400,
        doc=doc, auto_update=False)



hist2.limit = None
hist2.x_range = [200,500]
#hist2.update_view('reset',2)

#hist3.bins = 4
hist3.x_range = [2000,4000]
hist3.bins = 5
hist3.values = 'weight'
hist3.x_range = [2300,3985]
hist3.bins = 50
#hist3.x_range = [2000,4000]
#hist3.figure.x_range.start = 10
#hist3.update_view()

l = column(row(hist.menu(orientation='v'), hist(), hist2()),row(hist3.menu(orientation='v'), hist3(),hist4()))
doc.add_root(l)
doc.title = "Histograms"


#def update_plot(value, new, old):
#    print("x_range changed")
#    update_debounced(hist2)
#    #hist2.update_view()

#@bke.util.debounce(0.1)
#def update_debounced(hist):
#    print("UPDATE plot")
#    #doc.add_next_tick_callback(partial(hist.update_view))
#    doc.add_next_tick_callback(hist.update_view)
#    #hist.update_view()


if __name__ == "__main__":
    output_file(os.path.join(os.path.dirname(__file__),'tmp','histogram.html'))
    show(l)
    print("Not running in a server, no interaction.")
    print("Run: bokeh serve histogram.py")
else:
    print("Histogram App")
    #hist2.figure.x_range.on_change('end',update_plot)
    #hist2.figure.x_range.on_change('start',update_plot)
