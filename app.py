from py3dbp import Packer, Bin, Item, Painter
import streamlit as st
import matplotlib.pyplot as plt
import random
import csv
from PIL import Image
import subprocess

st.set_page_config(page_title="Streamlit App", page_icon=":smiley:", layout="wide")
col1, col2 = st.columns((1,2))
with col1:
    st.title("Codesprint 3D Bin Packer")
    uploaded_file = st.file_uploader("Choose a file")


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
    with col1:
        st.title("Packing information:")

    # output = "***************************************************\n"
    # output = ''
    for idx, b in enumerate(packer.bins):
        # output += f"** {b.string()} **\n"
        with col1:
            st.header(f"{b.string()} \n")
        bins_used += 1
        current_bin_weight = 0
        # output = f"{b.string()} \n"
        # output += "***************************************************\n"
        with col1:
            st.subheader("FITTED ITEMS")
        output = ""
        # output += "***************************************************\n"
        volume = b.width * b.height * b.depth
        volume_t = 0
        volume_f = 0
        unfitted_name = ''
        for item in b.items:
            current_bin_weight += float(item.weight)
            output = f"Package no : {item.partno}\n"
            with col1:
                st.write(output)
            output = f"Dimensions : {item.width} * {item.height} * {item.depth}\n"
            with col1:
                st.write(output)
            output = f"Weight : {item.weight}\n"
            with col1:
                st.write(output)
            volume_t += float(item.width) * \
                float(item.height) * float(item.depth)
            output = "***************************************************\n"
            with col1:
                st.write(output)

        output = f'Space utilization: {round(volume_t / float(volume) * 100, 2)}%\n'
        output += f'Total weight of items: {current_bin_weight}\n'
        output += f'Residual volume: {float(volume) - volume_t}\n'
        # output += "***************************************************\n"
        # draw results
        with col1:
            st.markdown(output)
        painter = Painter(b)
        fig = painter.plotBoxAndItems(
            title=b.partno,
            alpha=0.8,
            write_num=False,
            fontsize=10
        )

        with col2:
            fig_name = "fig{index}.png".format(index=idx)
            fig.savefig(fig_name)
            st.image(Image.open(fig_name))


    output += "***************************************************\n"
    output = "UNFITTED ITEMS:\n"
    with col1:
            st.subheader("UNFITTED ITEMS")
    for item in packer.unfit_items:
        # output += "***************************************************\n"
        volume_f += float(item.width) * \
            float(item.height) * float(item.depth)
        unfitted_name += f'{item.partno}, '
        if len(packer.unfit_items) == 0:
            unfitted_name = "None"
        else:
            unfitted_name = unfitted_name[:-2]
    #     output += "***************************************************\n"
    # output += "***************************************************\n"
        output = f'Unpacked package no: {unfitted_name}\n'
        with col1:
            st.write(output)
        output = f'Unpacked package volume: {volume_f}\n'
        with col1:
            st.write(output)
            st.write("***************************************************")
    with col1:
        st.text("Containers utilised: " + str(bins_used) + "/" + str(len(bins)))


