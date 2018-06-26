#!/usr/bin/env python

"""GUI"""

from tkinter import *
from tkinter import messagebox

import pandas as pd
import datetime


class Sample:
    """Sample object with all its information"""
    def __init__(self, name):
        self.name = name
        self.vial_num = None
        self.volume = None
        self.row = None
        self.peak = None
        self.result = None

    def set_vial(self, vial):
        """ Add in vial number"""
        self.vial_num = vial

    def set_volume(self, volume):
        """ Add in volume"""
        self.volume = volume

    def set_row(self, row):
        """ Add in row"""
        self.row = row

    def set_peak(self, peak):
        """ Add in peak"""
        self.peak = peak

    def set_result(self, result):
        """ Add in result"""
        self.result = result

    def __str__(self):
        return self.name

# Creating window Here
window = Tk()
window.title("HPLC Sample Entry")  # Name of Window
w, h = window.winfo_screenwidth()-100, window.winfo_screenheight()-100
# use the next line if you also want to get rid of the titlebar
window.geometry("%dx%d+0+0" % (w, h))  # Size of Window

# Global Variables
num_samples = 0
num_inj = 0
samples_class_list = []
sample_names = []
samples_entries = []
volume_enteries = []
injection_volume = []
full_volume_list = []
sample_full_list = []
vial_num = []
row_num = [0]
standard_check = [0]

# Number of Samples Entry
samples_label = Label(window, text="Number of Samples: ", font=("Times New Roman", 14), width=40)
samples_label.grid(sticky=W, column=0, row=0)
samples = Entry(window, width=10)
samples.grid(column=1, row=0)


# Number of Injections Entry
inj_label = Label(window, text="Number of Injections: ", font=("Times New Roman", 14), width=40)
inj_label.grid(column=2, row=0)
inj = Entry(window, width=10)
inj.grid(column=3, row=0)


# Checkbox for Standards
standard = BooleanVar()
standard.set(False)
standard_chk = Checkbutton(window, text="Would you like to manually add in standards?", var=standard)
row_num[0] += 1
standard_chk.grid(column=0, row=row_num[0])
standard_name_lbl = Label(window, text="Name of Standard: ", width=40)
standard_en = Entry(window, width=10)
conc_lbl = Label(window, text="Concentration: ", width=40)
conc_en = Entry(window, width=10)

# Variables for Results Sheet
slope_en = Entry(window)
intercept_en = Entry(window)
standard_result_en = Entry(window)
result_enteries = []
result_values = []
results_list = []


def x_calculation(peak, intercept, slope):
    """ Calculates value of x"""
    mx = peak - intercept
    x = mx/slope
    return x


def calculate_results():
    """Calculate the results for the given values"""

    submit_results.config(state=DISABLED)
    result_names = sample_names

    try:
        for i in range(len(result_enteries)):
            samples_class_list[i].set_peak(int(result_enteries[i].get()))

        slope = int(slope_en.get())
        intercept = int(intercept_en.get())

        for i in range(len(sample_names)):
            sample = samples_class_list[i]
            x = x_calculation(int(sample.peak), intercept, slope)
            result_values.append(x)

        standard_result = standard_result_en.get()
        result_values.append(x_calculation(int(standard_result), intercept, slope))

        result_names.append("Standard")

    except ValueError:
        messagebox.showerror(title="Error", message="Input integers only")
        window.destroy()

    # Make DataFrame to create excel spreadsheet
    sample_series = pd.Series(result_names)
    result_series = pd.Series(result_values)

    as_series = pd.concat([sample_series, result_series], axis=1)
    samples_dataframe = pd.DataFrame(as_series)
    samples_dataframe.columns = ['Sample Name', 'Result']

    # Create a Pandas Excel writer using XlsxWriter as the engine.
    now = datetime.datetime.now()
    name = now.strftime("%d-%B-%y %H:%M:%S") + " HPLC Results.xlsx"
    writer = pd.ExcelWriter(name, engine='xlsxwriter')

    # Convert the dataframe to an XlsxWriter Excel object.
    samples_dataframe.to_excel(writer, sheet_name='Samples')

    window.destroy()


def enter_results():
    """ Create space to enter the results"""

    results_btn.config(state=DISABLED)

    for c in range(num_samples):
        sample = samples_class_list[c]
        result_text = "Peak area for " + sample.name + ":"
        sample_name = Label(window, text=result_text, font=("Times New Roman", 14))
        sample_name.grid(column=0, row=sample.row)
        en = Entry(window)
        en.grid(column=1, row=sample.row)
        result_enteries.append(en)

    standard_result_lbl = Label(window, text="Standard Result: ", font=("Times New Roman", 14))
    standard_result_lbl.grid(column=0, row=row_num[0])
    standard_result_en.grid(column=1, row=row_num[0])

    row_num[0] += 1
    slope_label = Label(window, text="Slope: ", font=("Times New Roman", 14))
    slope_label.grid(column=0, row=row_num[0])
    slope_en.grid(column=1, row=row_num[0])

    intercept_label = Label(window, text="Intercept: ", font=("Times New Roman", 14))
    intercept_label.grid(column=2, row=row_num[0])
    intercept_en.grid(column=3, row=row_num[0])

    submit_results.grid(column=4, row=row_num[0])


def fill_samples():
    """ Filling the samples into the list"""
    # switch off enter button so can't reenter sample names
    enter_btn.config(state=DISABLED)

    for i in range(len(samples_entries)):
        samples_class_list.append(Sample(samples_entries[i].get()))
        samples_class_list[i].set_volume(volume_enteries[i].get())

        sample_names.append(samples_entries[i].get())
        injection_volume.append(volume_enteries[i].get())

    num_waters = 1
    num_standard = 1
    samples_vial_num = 1

    water_text = "purified water inj"

    sample_full_list.append(water_text + str(num_waters))
    vial_num.append(1)
    full_volume_list.append("500")
    num_waters += 1

    sample_full_list.append(water_text + str(num_waters))
    vial_num.append(1)
    full_volume_list.append("500")
    num_waters += 1

    # Standards
    if standard_check[0] == 0:
        herclon_text = "herclon 1mg_ml inj"

        sample_full_list.append(herclon_text + str(num_standard))
        full_volume_list.append("500")
        vial_num.append(2)
        samples_vial_num = 3

        sample_full_list.append(water_text + str(num_waters))
        vial_num.append(1)
        full_volume_list.append("500")
        num_waters += 1
    elif standard_check[0] == 1:
        standard_text = standard_en.get()
        standard_conc = conc_en.get()
        sample_full_list.append(standard_text + " " + standard_conc + "mg_ml inj" + str(num_standard))
        vial_num.append(2)
        num_standard += 1

    # Insert number of injections and sample names etc into the list
    for i in range(num_samples):
        inj_num = 0
        row_num[0] += 1
        for j in range(num_inj):
            inj_num += 1

            # insert into sample object
            sample = samples_class_list[i]
            sample_name = sample.name + " inj" + str(inj_num)
            sample.set_volume(injection_volume[i])
            sample.set_vial(samples_vial_num)
            sample.set_row(row_num[0])

            sample_full_list.append(sample_name)
            vial_num.append(samples_vial_num)
            full_volume_list.append(injection_volume[i])

        samples_vial_num += 1
        water = "purified water inj" + str(num_waters)
        full_volume_list.append(500)
        sample_full_list.append(water)
        num_waters += 1
        vial_num.append(1)

    # Make DataFrame to create excel spreadsheet
    full_sample_series = pd.Series(sample_full_list)
    vial_series = pd.Series(vial_num)
    volume_series = pd.Series(full_volume_list)

    as_series = pd.concat([vial_series, full_sample_series, volume_series], axis=1)
    samples_dataframe = pd.DataFrame(as_series)
    samples_dataframe.columns = ['Vial Number', 'Sample Names', 'Injection Volume']

    # Create a Pandas Excel writer using XlsxWriter as the engine.
    now = datetime.datetime.now()
    name = now.strftime("%d-%B-%y %H:%M:%S") + " HPLC Samples.xlsx"
    writer = pd.ExcelWriter(name, engine='xlsxwriter')

    # Convert the dataframe to an XlsxWriter Excel object.
    samples_dataframe.to_excel(writer, sheet_name='Samples')

    # row_num[0] += 2
    results_btn.grid(column=4, row=row_num[0])
    row_num[0] += 1


def enter_nums():
    """Upon entering the numbers required"""

    # switch off enter button so can't reenter sample names
    btn.config(state=DISABLED)

    try:
        global num_samples
        num_samples = int(samples.get())
        global num_inj
        num_inj = int(inj.get())
    except ValueError:
        messagebox.showerror(title="Error", message="Input integers only")
        window.destroy()

    # Create the text boxes to enter in the samples
    for num in range(num_samples):
        row_num[0] += 1
        n = num + 1
        txt = ("What is the name of sample %d?\n" % n)
        sample_name_lbl = Label(window, text=txt, width=40)
        sample_name_lbl.grid(sticky=W, column=0, row=row_num[0])
        en = Entry(window, width=10)
        en.grid(column=1, row=row_num[0])
        samples_entries.append(en)
        sample_volume_lbl = Label(window, text="Volume Required: ", width=40)
        sample_volume_lbl.grid(column=2, row=row_num[0])
        vol_en = Entry(window, width=10)
        vol_en.grid(column=3, row=row_num[0])
        volume_enteries.append(vol_en)
        row_num[0] += 1

    # enter custom standard info
    if standard.get() == 1:
        standard_check[0] = 1
        standard_name_lbl.grid(column=0, row=row_num[0])
        standard_en.grid(column=1, row=row_num[0])
        conc_lbl.grid(column=2, row=row_num[0])
        conc_en.grid(column=3, row=row_num[0])

    # button to enter in sample names
    enter_btn.grid(column=4, row=row_num[0])

# buttons
submit_results = Button(window, text="Submit Results", command=calculate_results)
results_btn = Button(window, text="Enter Results", command=enter_results)
enter_btn = Button(window, text="Submit", command=fill_samples)
btn = Button(window, text="Enter", command=enter_nums)
btn.grid(column=4, row=0)

# keep window running
window.mainloop()
