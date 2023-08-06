# -*- coding: utf-8 -*-
#
# Copyright (c) 2020 Kevin De Bruycker
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

import aprheology
import PySimpleGUI as sg
import re
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib
matplotlib.use('TkAgg')


def GUI():
    plot_size = (5, 4.5)

    InputParameters = [
        [
            sg.Text("Experiment:"),
        ],
        [
            sg.Radio('Stress relaxation', 'ExperimentType', pad=(5, 0), disabled=True, enable_events=True, key="-StressRelaxation-"),
        ],
        [
            sg.Text('  ', pad=(5, 0)),
            sg.Checkbox("Normalise the relaxation modulus", pad=(5, 0), default=True, disabled=True, key="-normalise_relax_mod-"),
        ],
        [
            sg.Radio('Frequency sweep', 'ExperimentType', pad=(5, 0), disabled=True, enable_events=True, key="-FrequencySweep-"),
        ],
        [
            sg.Text("", pad=(5, 0)),
        ],
        [
            sg.Text("Read temperature from:"),
        ],
        [
            sg.Radio('Additional column in table', 'get_T_from', pad=(5, 0), default=True, disabled=True, key="-T_from_datacolumns_names_last-"),
        ],
        [
            sg.Radio('Last number in curve header', 'get_T_from', pad=(5, 0), disabled=True, key="-T_from_curve_header_last_number-"),
        ],
        [
            sg.Text("Temperature unit:"),
            sg.DropDown(['°C', 'K'], default_value='°C', disabled=True, size=(4, 1), key="-T_unit-"),
        ],
        [
            sg.Text("", pad=(5, 0)),
        ],
        [
            sg.Text("Mode of extracting the relaxation time:"),
        ],
        [
            sg.Radio('Interpolate from curve', 'tau_mode', pad=(5, 0), default=True, disabled=True, key="-tau_mode_interpolate-"),
        ],
        [
            sg.Radio('Select closest datapoint', 'tau_mode', pad=(5, 0), disabled=True, key="-tau_mode_closest-"),
        ],
        [
            sg.Text("", pad=(5, 0)),
        ],
        [
            sg.Text('Discard first'),
            sg.Spin([i for i in range(0, 101)], initial_value=0, pad=(0, 3), size=(3,1), disabled=True, key='-datapoints_discarded-'),
            sg.Text('data points'),
        ],
    ]

    ParameterColumn = [
        [
            sg.Frame("Input parameters:", InputParameters, key="-InputParameters-")
        ],
        [
            sg.Button('Open file', disabled=True, key='-OpenFile-')
        ],
    ]

    TemperatureSelection = [
        [
            sg.Listbox(values=[], disabled=True, select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE, size=(11, 3), key="-Temperatures-"),
        ],
        [
            sg.Button('Update', disabled=True, key='-Update-')
        ],
    ]

    TemperatureColumn = [
        [
            sg.Frame("Temperatures:", TemperatureSelection, key="-TemperatureSelection-")
        ],
    ]

    InputColumn = [
        [
            sg.Text("File:"),
            sg.InputText(size=(41, 1), enable_events=True, key="-FILE-"),
            sg.FileBrowse(file_types=(("CSV/Text file", ["*.csv", "*.txt"]), ("All files", "*.*"), )),
        ],
        [
            sg.Column(ParameterColumn),
            sg.Column(TemperatureColumn),
        ],
    ]

    DataPlotColumn = [
        [
            sg.Canvas(size=[dim * 100 for dim in plot_size], key='-DataPlot-')
        ],
        [
            sg.Button('Open as interactive plot', disabled=True, key='-OpenDataPlot-'),
            sg.Save('Save CSV', disabled=True, key='-QuickSaveDataPlotCSV-'),
            sg.Save('Save XLSX', disabled=True, key='-QuickSaveDataPlotXLSX-'),
            sg.InputText(size=(35, 1), enable_events=True, visible=False, key="-SaveDataPlotAs-"),
            sg.FileSaveAs('Save raw plot data as...', disabled=True, file_types=(("CSV file", "*.csv"), ("Excel file", "*.xlsx"),), key='-SaveDataPlot-', ),
            # sg.Button('Save raw plot data as...', disabled=True, key='-SaveDataPlot-'),
        ],
    ]

    ArrheniusColumn = [
        [
            sg.Canvas(size=[dim * 100 for dim in plot_size], key='-ArrheniusPlot-')
        ],
        [
            sg.Button('Open as interactive plot', disabled=True, key='-OpenArrheniusPlot-'),
            sg.Save('Save CSV', disabled=True, key='-QuickSaveArrheniusPlotCSV-'),
            sg.Save('Save XLSX', disabled=True, key='-QuickSaveArrheniusPlotXLSX-'),
            sg.InputText(size=(35, 1), enable_events=True, visible=False, key="-SaveArrheniusPlotAs-"),
            sg.FileSaveAs('Save raw plot data as...', disabled=True, file_types=(("CSV file", "*.csv"), ("Excel file", "*.xlsx"),),
                          key='-SaveArrheniusPlot-', ),
            # sg.Button('Save raw plot data as...', disabled=True, key='-SaveArrheniusPlot-'),
        ],
    ]

    layout = [
        [
            sg.Column(InputColumn),
            sg.VSeperator(),
            sg.Column(DataPlotColumn),
            sg.VSeperator(),
            sg.Column(ArrheniusColumn),
        ],
        # [
        #     sg.Output(size=(160, 10)),
        # ],
    ]

    window = sg.Window("Anton Paar Rheology v" + aprheology.__version__, layout)
    window.Finalize()

    def draw_plot(canvas, plot):
        for child in canvas.winfo_children():
            child.destroy()
        # canvas.get_tk_widget().destroy()
        figure_canvas_agg = FigureCanvasTkAgg(plot, canvas)
        # figure_canvas_agg.get_tk_widget().destroy()
        # figure_canvas_agg.get_tk_widget().pack_forget()
        figure_canvas_agg.draw()
        figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
        # return figure_canvas_agg

    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        if event == "-FILE-":
            if not values["-FILE-"]:
                continue
            try:
                window["-T_unit-"].update(aprheology.RelaxationExperiment(values["-FILE-"], None).T_unit)
            except:
                pass
            window["-StressRelaxation-"].update(disabled=False)
            window["-FrequencySweep-"].update(disabled=False)
            window["-T_from_datacolumns_names_last-"].update(disabled=False)
            window["-T_from_curve_header_last_number-"].update(disabled=False)
            window["-T_unit-"].update(disabled=False)
            window["-tau_mode_interpolate-"].update(disabled=False)
            window["-tau_mode_closest-"].update(disabled=False)
            # window["-datapoints_discarded-"].update(disabled=False)
            # Gives an error that a wrong state is passed... Do it manually without update:
            window["-datapoints_discarded-"].TKSpinBox['state'] = 'normal'
            window["-OpenFile-"].update(disabled=False)
        if event == "-StressRelaxation-":
            window["-normalise_relax_mod-"].update(disabled=False)
        if event == "-FrequencySweep-":
            window["-normalise_relax_mod-"].update(disabled=True)
        if event == "-OpenFile-":
            if values['-T_from_datacolumns_names_last-']:
                get_T_from = 'datacolumns_names_last'
            elif values['-T_from_curve_header_last_number-']:
                get_T_from = 'curve_header_last_number'
            else:
                sg.popup_error('Something went wrong')
                continue
            if values['-tau_mode_interpolate-']:
                tau_mode = 'interpolate_highest'
            elif values['-tau_mode_highest-']:
                tau_mode = 'closest_highest'
            else:
                sg.popup_error('Something went wrong')
                continue
            datapoints_discarded = int(values['-datapoints_discarded-']) if values['-datapoints_discarded-'] != 0 else None
            if values['-StressRelaxation-']:
                try:
                    experiment = aprheology.StressRelaxation(filename=values["-FILE-"],
                                                             get_T_from=get_T_from,
                                                             T_unit=values["-T_unit-"],
                                                             datapoints_discarded=datapoints_discarded,
                                                             normalise_relax_mod=values["-normalise_relax_mod-"],
                                                             tau_mode=tau_mode)
                except:
                    sg.popup_error('Something went wrong, check the input file.')
                    continue
            elif values['-FrequencySweep-']:
                try:
                    experiment = aprheology.FrequencySweep(filename=values["-FILE-"],
                                                           get_T_from=get_T_from,
                                                           T_unit=values["-T_unit-"],
                                                           datapoints_discarded=datapoints_discarded,
                                                           tau_mode=tau_mode)
                except:
                    sg.popup_error('Something went wrong, check the input file.')
                    continue
            else:
                sg.popup_error('No experiment type selected.')
                continue
            draw_plot(window['-DataPlot-'].TKCanvas, experiment.plot(plot_size=plot_size, return_plot=True))
            experiment.analyse_arrhenius(plot_size=plot_size, show_plot=False, return_plot=True)
            draw_plot(window['-ArrheniusPlot-'].TKCanvas, experiment.arrhenius_plot)
            window["-Temperatures-"].update(disabled=False)
            temperatures = [curve['T'] for curve in experiment.curves]
            window["-Temperatures-"].update(values=temperatures)
            window["-Temperatures-"].SetValue(temperatures)
            window["-Temperatures-"].set_size(size=(None, len(temperatures)))
            window["-Update-"].update(disabled=False)
            window['-OpenDataPlot-'].update(disabled=False)
            window['-OpenArrheniusPlot-'].update(disabled=False)
            window['-QuickSaveDataPlotCSV-'].update(disabled=False)
            window['-QuickSaveDataPlotXLSX-'].update(disabled=False)
            window['-SaveDataPlot-'].update(disabled=False)
            window['-QuickSaveArrheniusPlotCSV-'].update(disabled=False)
            window['-QuickSaveArrheniusPlotXLSX-'].update(disabled=False)
            window['-SaveArrheniusPlot-'].update(disabled=False)
        if event == '-Update-':
            experiment.set_evaluated_T(T_list=values["-Temperatures-"])
            draw_plot(window['-DataPlot-'].TKCanvas, experiment.plot(plot_size=plot_size, return_plot=True))
            experiment.analyse_arrhenius(plot_size=plot_size, show_plot=False, return_plot=True)
            draw_plot(window['-ArrheniusPlot-'].TKCanvas, experiment.arrhenius_plot)
        if event == '-OpenDataPlot-':
            experiment.plot(return_plot=False)
        if event == '-OpenArrheniusPlot-':
            experiment.analyse_arrhenius(show_plot=True, return_plot=False)
        if event == '-QuickSaveDataPlotCSV-':
            experiment.export_plot_data(excel=False)
        if event == '-QuickSaveArrheniusPlotCSV-':
            experiment.export_arrhenius_data(excel=False)
        if event == '-QuickSaveDataPlotXLSX-':
            experiment.export_plot_data(excel=True)
        if event == '-QuickSaveArrheniusPlotXLSX-':
            experiment.export_arrhenius_data(excel=True)
        if event == '-SaveDataPlotAs-':
            extension = re.sub('\A.*\.([^.]*)\Z', '\\1', values['-SaveDataPlotAs-'])
            experiment.export_plot_data(filename=values['-SaveDataPlotAs-'], excel=(extension == 'xlsx'))
        if event == '-SaveArrheniusPlotAs-':
            extension = re.sub('\A.*\.([^.]*)\Z', '\\1', values['-SaveArrheniusPlotAs-'])
            experiment.export_arrhenius_data(filename=values['-SaveArrheniusPlotAs-'], excel=(extension == 'xlsx'))



    window.close()