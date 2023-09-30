from py3dbp import Packer, Bin, Item, Painter
import streamlit as st
import random
import csv
import pandas as pd
import subprocess

st.set_page_config(page_title="Streamlit App", page_icon=":smiley:")

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

    st.title("Packing information:")

    # output = "***************************************************\n"
    # output = ''
    for idx, b in enumerate(packer.bins):
        # output += f"** {b.string()} **\n"

        st.header(f"{b.string()} \n")
        bins_used += 1
        current_bin_weight = 0
        # output = f"{b.string()} \n"
        # output += "***************************************************\n"

        st.subheader("FITTED ITEMS")
        output = ""
        # output += "***************************************************\n"
        volume = b.width * b.height * b.depth
        volume_t = 0
        volume_f = 0
        unfitted_name = ''
        data = {
            "Package no": [],
            "Dimensions / meters": [],
            "Weight / kg": []
        }
        for item in b.items:
            current_bin_weight += float(item.weight)

            data["Package no"].append(item.partno)
            data["Dimensions / meters"].append(
                f"{item.width} x {item.height} x {item.depth}")
            data["Weight / kg"].append(item.weight)
            volume_t += float(item.width) * \
                float(item.height) * float(item.depth)
        data1 = {
            "Space utilization": [],
            "Total weight of items": [],
            "Residual volume": []
        }
        data1["Space utilization"].append(
            f'{round(volume_t / float(volume) * 100, 2)}%')
        data1["Total weight of items"].append(current_bin_weight)
        data1["Residual volume"].append(float(volume) - volume_t)

        # draw results

        st.markdown(output)
        painter = Painter(b)
        fig = painter.plotBoxAndItems(
            title=b.partno,
            alpha=0.8,
            write_num=False,
            fontsize=10
        )

        df = pd.DataFrame(data)
        df1 = pd.DataFrame(data1)
        df.index += 1
        st.pyplot(fig)
        st.table(df)
        st.table(df1)

    unfitted_items = {
        "Package no": [],
        "Dimensions / meters": [],
        "Weight / kg": []
    }
    for item in packer.unfit_items:
        unfitted_items["Package no"].append(item.partno)
        unfitted_items["Dimensions / meters"].append(
            f"{item.width} x {item.height} x {item.depth}")
        unfitted_items["Weight / kg"].append(item.weight)
    if len(packer.unfit_items) == 0:
        unfitted_name = "None"
    else:
        unfitted_name = unfitted_name[:-2]

    # Print the entire output
    st.header("Summary:")
    st.subheader("Total Containers utilised: " +
                 str(bins_used) + "/" + str(len(bins)))
    st.subheader("Unpacked Items:")
    unfitted_items = pd.DataFrame(unfitted_items)
    unfitted_items.index += 1
    st.table(unfitted_items)
    # st.pyplot(fig)
