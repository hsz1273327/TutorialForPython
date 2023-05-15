import PySimpleGUI as sg
from .seg import seg
layout = [
    [sg.Text('Enter txt'), sg.InputText()],
    [sg.Button('Ok'), sg.Button('Cancel')],
    [sg.Text(size=(100, 1), key='-OUTPUT-')],
]


def guiseg() -> None:
    window = sg.Window(title="txt seg", layout=layout, margins=(100, 50))
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Cancel':  # if user closes window or clicks cancel
            break
        print('You entered ', values[0])
        result = ",".join(seg(values[0]))
        window['-OUTPUT-'].update(f'Result: {result}')
    window.close()
