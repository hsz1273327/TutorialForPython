from tkinter import Tk,Frame
from pandastable import Table, TableModel

data = {
    'rec1': {'col1': 99.88, 'col2': 108.79, 'label': 'rec1'},
    'rec2': {'col1': 99.88, 'col2': 108.79, 'label': 'rec2'}
}

root = Tk()
f = Frame(root)
f.pack(fill="both",expand=1)
model = TableModel.getSampleData()
table = Table(f, dataframe=model,showtoolbar=True, showstatusbar=True)
table.show()
table.showPlotViewer(layout='horizontal')
#table.showPlot()

root.mainloop()