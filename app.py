import subprocess

from py3dbp import Packer, Bin, Item, Painter
import streamlit as st
import matplotlib.pyplot as plt
import random
import csv
from PIL import Image
from saved_fig import FIG

def run_python_file(file_path):
    try:
        with open("data.csv", "wb") as f:
            f.write(uploaded_file.read())
        # Execute the Python file using subprocess
        subprocess.run(["python", file_path], check=True)
        st.success(f"Python file '{file_path}' executed successfully.")
    except Exception as e:
        st.error(f"Error executing '{file_path}': {e}")

st.set_page_config(page_title="Streamlit App", page_icon=":smiley:")
st.title("Codesprint 3D Bin Packer")
uploaded_file = st.file_uploader("Choose a file")
if st.button("Open interactive view"):
    file_path = "interactiveplot.py"  # Replace with the path to your Python file
    run_python_file(file_path)

COLORS = ["yellow", "olive", "pink", "brown", "red",
          "blue", "green", "purple", "orange", "gray"]
# Initialize variables to store bins and items
bins = []
bin_size = -1
items = []
item_size = 0
counter = 0
bin_weights = []
item_weights = []
bins_used = 0

if uploaded_file is not None:
    # Use uploaded file content instead of hardcoded path
    uploaded_data = uploaded_file.read().decode('utf-8').splitlines()
    csv_reader = csv.reader(uploaded_data)


    # Iterate through the rows and parse bins and items
    for row in csv_reader:
        # Check if the row is empty
        if not any(row):
            continue

        # If there is a single number in the row, it represents the number of bins or items
        if row[1] == "":
            num = int(row[0].strip('\ufeff'))
            if bin_size == -1:
                bin_size = num
                counter = bin_size
            else:
                item_size = num
        else:
            dimensions = tuple(int(val) for val in row[:3])
            if counter > 0:
                bins.append(dimensions)
                bin_weights.append(int(row[3]))
                counter -= 1
            else:
                items.append(dimensions)
                item_weights.append(int(row[3]))

    # init packing function
    packer = Packer()
    #  init bin
    for i in range(len(bins)):
        box = Bin('Container {}'.format(str(i+1)), bins[i], 100, 0, 0)
        packer.addBin(box)

    #  add item
    for i in range(len(items)):
        packer.addItem(Item(
            partno='{}'.format(str(i+1)),
            name='test{}'.format(str(i+1)),
            typeof='cube',
            WHD=items[i],
            weight=item_weights[i],
            level=1,
            loadbear=100,
            updown=True,
            color=random.choice(COLORS)
        )
        )

    # calculate packing
    packer.pack(
        bigger_first=True,
        distribute_items=True,
        fix_point=True,
        check_stable=True,
        support_surface_ratio=0.75,
        number_of_decimals=0
    )

    # put order
    packer.putOrder()

    output = "***************************************************\n"
    for idx, b in enumerate(packer.bins):
        output += f"** {b.string()} **\n"
        bins_used += 1
        current_bin_weight = 0
        output += "***************************************************\n"
        output += "FITTED ITEMS:\n"
        output += "***************************************************\n"
        volume = b.width * b.height * b.depth
        volume_t = 0
        volume_f = 0
        unfitted_name = ''
        for item in b.items:
            current_bin_weight += float(item.weight)
            output += f"Package no: {item.partno}, "
            output += f"Dimensions : {item.width} x {item.height} x {item.depth}, "
            output += f"Weight : {item.weight}\n"
            volume_t += float(item.width) * \
                float(item.height) * float(item.depth)

        output += f'Space utilization : {round(volume_t / float(volume) * 100, 2)}%\n'
        output += f'Total weight of items: {current_bin_weight}\n'
        output += f'Residual volume : {float(volume) - volume_t}\n'
        output += "***************************************************\n"
        # draw results
        painter = Painter(b)
        fig = painter.plotBoxAndItems(
            title=b.partno,
            alpha=0.8,
            write_num=False,
            fontsize=10
        )
        FIG = fig
        fig_name = "fig{index}.png".format(index=idx)
        fig.savefig(fig_name)
        st.image(Image.open(fig_name))


    output += "***************************************************\n"
    output += "UNFITTED ITEMS:\n"
    for item in packer.unfit_items:
        volume_f += float(item.width) * \
            float(item.height) * float(item.depth)
        unfitted_name += f'{item.partno}, '
    if len(packer.unfit_items) == 0:
        unfitted_name = "None"
    else:
        unfitted_name = unfitted_name[:-2]
    output += "***************************************************\n"
    output += f'Unpacked package no: {unfitted_name}\n'
    output += f'Unpacked package volume : {volume_f}\n'

    # Print the entire output
    print(output)
    st.text("Containers utilised: " + str(bins_used) + "/" + str(len(bins)))
    st.text("Packing information:")
    st.text(output)

