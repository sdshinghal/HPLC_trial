"""GUI"""

from tkinter import *
from tkinter import messagebox

import pandas as pd

# Creating window Here
window = Tk()
window.title("HPLC Sample Entry")  # Name of Window
window.geometry('680x500')  # Size of Window

# TODO: Add a scrollbar / make expandable
# TODO: Format so result ends up next to sample name

# Number of Samples Entry
samples_label = Label(window, text="Number of Samples: ", font=("Times New Roman", 14))
samples_label.pack()
samples = Entry(window, width=10)
samples.pack()


# Number of Injections Entry
inj_label = Label(window, text="Number of Injections: ", font=("Times New Roman", 14))
inj_label.pack()
inj = Entry(window, width=10)
inj.pack()


# Variables for sample sheet
sample_names = []
samples_entries = []
volume_enteries = []
injection_volume = []
full_volume_list = []
samples_inj_num = []
sample_full_list = []
vial_num = []

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

    for ent in result_enteries:
        result_values.append(int(ent.get()))

    slope = int(slope_en.get())
    intercept = int(intercept_en.get())

    for i in range(len(sample_names)):
        val = result_values[i] - intercept
        x = val/slope
        results_text = sample_names[i] + " :" + str(x)
        sample_name = Label(window, text=results_text, font=("Times New Roman", 14))
        sample_name.pack()


def enter_results():
    """ Create space to enter the results"""
    num_samples = samples_inj_num[0]

    for c in range(num_samples):
        result_text = "Peak area for " + sample_names[c] + ":"
        sample_name = Label(window, text=result_text, font=("Times New Roman", 14))
        sample_name.pack()
        en = Entry(window)
        en.pack()
        result_enteries.append(en)

    slope_label = Label(window, text="Slope: ", font=("Times New Roman", 14))
    slope_label.pack()

    slope_en.pack()

    intercept_label = Label(window, text="Intercept: ", font=("Times New Roman", 14))
    intercept_label.pack()

    intercept_en.pack()

    submit_results = Button(window, text="Submit Results", command=calculate_results)
    submit_results.pack()


def fill_samples():
    """ Filling the samples into the list"""

    # Take in the values
    # for entry in samples_entries:
    #     sample_names.append(entry.get())

    for i in range(len(samples_entries)):
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
            sample = sample_names[i] + " inj" + str(inj_num)
            inj_num += 1
            sample_full_list.append(sample)
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
    results_btn.pack()


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
        n = num + 1
        txt = ("What is the name of sample %d?\n" % n)
        sample_name_lbl = Label(window, text=txt)
        sample_name_lbl.pack()
        en = Entry(window)
        en.pack()
        samples_entries.append(en)
        sample_volume_lbl = Label(window, text="Volume Required: ")
        sample_volume_lbl.pack()
        vol_en = Entry(window)
        vol_en.pack()
        volume_enteries.append(vol_en)

    # Checkbox for Standards
    water_1_chk = Checkbutton(window, text="Do you want to include water?", var=water_1)
    water_2_chk = Checkbutton(window, text="Do you want to include water?", var=water_2)
    herclon_chk = Checkbutton(window, text="Do you want to include Herclon 1mg_ml?", var=herclon)
    water_3_chk = Checkbutton(window, text="Do you want to include water?", var=water_3)
    water_1_chk.pack()
    water_2_chk.pack()
    herclon_chk.pack()
    water_3_chk.pack()

    # button to enter in sample names
    enter_btn = Button(window, text="Submit", command=fill_samples)
    enter_btn.pack()

# button to enter in numbers
btn = Button(window, text="Enter", command=enter_nums)
btn.pack()

window.mainloop()
