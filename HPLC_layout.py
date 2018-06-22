"""GUI"""

from tkinter import *
from tkinter import messagebox

import pandas as pd


class Sample:
    """Sample object with all its information"""
    def __init__(self, name):
        self.name = name
        self.vial_num = None
        self.volume = None
        self.row = None
        self.peak = None
        self.result = None

    def set_vial(self, vial_num):
        """ Add in vial number"""
        self.vial_num = vial_num

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
# window.geometry('1200x850')  # Size of Window

# TODO: Add a scrollbar / make expandable
# TODO: Format so result ends up next to sample name
# TODO: Error checking for result values as well as volumes

# Figure out global variables

# Number of Samples Entry
samples_label = Label(window, text="Number of Samples: ", font=("Times New Roman", 14), width=20)
samples_label.grid(sticky=W, column=0, row=0)
samples = Entry(window, width=10)
samples.grid(column=1, row=0)


# Number of Injections Entry
inj_label = Label(window, text="Number of Injections: ", font=("Times New Roman", 14), width=20)
inj_label.grid(column=2, row=0)
inj = Entry(window, width=10)
inj.grid(column=3, row=0)

# Variables for sample sheet
# TODO: Make this into a dictionary?
samples_class_list = []
sample_names = []
samples_entries = []
volume_enteries = []
injection_volume = []
full_volume_list = []
samples_inj_num = []
sample_full_list = []
vial_num = []
row_num = [0]

# Standards
water_1 = BooleanVar()
water_1.set(True)

water_2 = BooleanVar()
water_2.set(True)

water_3 = BooleanVar()
water_3.set(True)

herclon = BooleanVar()
herclon.set(True)

# Variables for Results Sheet
slope_en = Entry(window)
intercept_en = Entry(window)
result_enteries = []
result_values = []


def calculate_results():
    # TODO: Add in calculation for standard
    """Calculate the results for the given values"""

    for i in range(len(result_enteries)):
        samples_class_list[i].set_peak(int(result_enteries[i].get()))

    for ent in result_enteries:
        result_values.append(int(ent.get()))

    slope = int(slope_en.get())
    intercept = int(intercept_en.get())

    for i in range(len(sample_names)):
        sample = samples_class_list[i]
        val = sample.peak - intercept
        x = val/slope
        results_text = sample.name + " :" + str(x)
        sample_name = Label(window, text=results_text, font=("Times New Roman", 14))
        sample_name.grid(column=4, row=sample.row)


def enter_results():
    """ Create space to enter the results"""
    # TODO: Place results in an excel sheet
    num_samples = len(samples_class_list)

    for c in range(num_samples):
        sample = samples_class_list[c]
        result_text = "Peak area for " + sample.name + ":"
        sample_name = Label(window, text=result_text, font=("Times New Roman", 14))
        sample_name.grid(column=0, row=sample.row)
        en = Entry(window)
        en.grid(column=1, row=sample.row)
        result_enteries.append(en)

    row_num[0] += 1
    slope_label = Label(window, text="Slope: ", font=("Times New Roman", 14))
    slope_label.grid(column=0, row=row_num[0])

    slope_en.grid(column=1, row=row_num[0])

    intercept_label = Label(window, text="Intercept: ", font=("Times New Roman", 14))
    intercept_label.grid(column=2, row=row_num[0])

    intercept_en.grid(column=3, row=row_num[0])

    submit_results = Button(window, text="Submit Results", command=calculate_results)
    submit_results.grid(column=4, row=row_num[0])


def fill_samples():
    """ Filling the samples into the list"""
    # switch off enter button so can't reenter sample names
    enter_btn.config(state=DISABLED)

    # Take in the values
    # for entry in samples_entries:
    #     sample_names.append(entry.get())

    for i in range(len(samples_entries)):
        samples_class_list.append(Sample(samples_entries[i].get()))
        samples_class_list[i].set_volume(volume_enteries[i].get())

        sample_names.append(samples_entries[i].get())
        injection_volume.append(volume_enteries[i].get())

    num_waters = 0
    num_herclons = 0
    samples_vial_num = 1

    # Checking for standards
    water_text = "purified water inj"
    herclon_text = "herclon 1mg_ml inj"

    # TODO: Make more Standard
    if water_1.get() == 1:
        num_waters += 1
        sample_full_list.append(water_text + str(num_waters))
        vial_num.append(1)
        samples_vial_num = 2
        full_volume_list.append("500")
    if water_2.get() == 1:
        num_waters += 1
        sample_full_list.append(water_text + str(num_waters))
        vial_num.append(1)
        samples_vial_num = 2
        full_volume_list.append("500")
    if herclon.get() == 1:
        sample_full_list.append(herclon_text + str(num_herclons))
        full_volume_list.append("500")
        if len(vial_num) == 0:
            samples_vial_num = 2
            vial_num.append(1)
        else:
            samples_vial_num = 3
            vial_num.append(2)
    if water_3.get() == 1:
        num_waters += 1
        sample_full_list.append(water_text + str(num_waters))
        full_volume_list.append("500")
        if samples_vial_num == 1:
            vial_num.append(1)
            samples_vial_num = 2
        elif samples_vial_num == 2:
            if num_waters > 1:
                vial_num.append(1)
            else:
                vial_num.append(2)
                samples_vial_num = 3
        elif samples_vial_num == 3:
            vial_num.append(1)

    # Insert number of injections and sample names etc into the list
    for i in range(samples_inj_num[0]):
        inj_num = 1
        for j in range(samples_inj_num[1]):
            inj_num += 1
            row_num[0] += 1

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
        num_waters += 1
        water = "purified water inj" + str(num_waters)
        full_volume_list.append(500)
        sample_full_list.append(water)
        vial_num.append(1)

    # Make DataFrame to create excel spreadsheet
    full_sample_series = pd.Series(sample_full_list)
    vial_series = pd.Series(vial_num)
    volume_series = pd.Series(full_volume_list)

    as_series = pd.concat([vial_series, full_sample_series, volume_series], axis=1)
    samples_dataframe = pd.DataFrame(as_series)
    samples_dataframe.columns = ['Vial Number', 'Sample Names', 'Injection Volume']

    # Create a Pandas Excel writer using XlsxWriter as the engine.
    # TODO: Add in a date to the name
    writer = pd.ExcelWriter('HPLC Samples.xlsx', engine='xlsxwriter')

    # Convert the dataframe to an XlsxWriter Excel object.
    samples_dataframe.to_excel(writer, sheet_name='Samples')

    results_btn = Button(window, text="Enter Results", command=enter_results)
    row_num[0] += 1
    results_btn.grid(column=2, row=row_num[0])


def enter_nums():
    """Upon entering the numbers required"""

    # switch off enter button so can't reenter sample names
    btn.config(state=DISABLED)

    try:
        num_samples = int(samples.get())
        samples_inj_num.append(num_samples)
        num_inj = int(inj.get())
        samples_inj_num.append(num_inj)
    except ValueError:
        messagebox.showerror(title="Error", message="Input integers only")
        # TODO: There should be a better way: issue is when injection number is wrong, sample numbers still come up
        window.destroy()

    num_samples = samples_inj_num[0]

    # Create the text boxes to enter in the samples
    for num in range(num_samples):
        row_num[0] +=1
        n = num + 1
        txt = ("What is the name of sample %d?\n" % n)
        sample_name_lbl = Label(window, text=txt, width=20)
        sample_name_lbl.grid(sticky=W, column=0, row=row_num[0])
        en = Entry(window, width=10)
        en.grid(column=1, row=row_num[0])
        samples_entries.append(en)
        sample_volume_lbl = Label(window, text="Volume Required: ", width=20)
        sample_volume_lbl.grid(column=2, row=row_num[0])
        vol_en = Entry(window, width=10)
        vol_en.grid(column=3, row=row_num[0])
        volume_enteries.append(vol_en)

    # Checkbox for Standards
    water_1_chk = Checkbutton(window, text="Do you want to include water?", var=water_1)
    water_2_chk = Checkbutton(window, text="Do you want to include water?", var=water_2)
    herclon_chk = Checkbutton(window, text="Do you want to include Herclon 1mg_ml?", var=herclon)
    water_3_chk = Checkbutton(window, text="Do you want to include water?", var=water_3)
    row_num[0] += 1
    water_1_chk.grid(column=0, row=row_num[0])
    water_2_chk.grid(column=1, row=row_num[0])
    herclon_chk.grid(column=2, row=row_num[0])
    water_3_chk.grid(column=3, row=row_num[0])

    # button to enter in sample names

    enter_btn.grid(column=4, row=row_num[0])

# button to enter in numbers
enter_btn = Button(window, text="Submit", command=fill_samples)
btn = Button(window, text="Enter", command=enter_nums)
btn.grid(column=4, row=0)

window.mainloop()
