import subprocess

from py3dbp import Packer, Bin, Item, Painter
import streamlit as st
import random
import csv
import pandas as pd
import subprocess


def run_python_file(file_path):
    try:
        # Execute the Python file using subprocess
        subprocess.run(["python", file_path], check=True)
        st.success(f"Python file '{file_path}' executed successfully.")
    except Exception as e:
        st.error(f"Error executing '{file_path}': {e}")


st.set_page_config(page_title="Codesprint 3D Bin Packer", page_icon=":smiley:")

st.title("Codesprint 3D Bin Packer")
uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    # Read the contents of the uploaded file into memory
    file_contents = uploaded_file.read()
    # Save the uploaded file's contents to a file named "data.csv"
    with open("data.csv", "wb") as f:
        f.write(file_contents)
if st.button("Open interactive view"):
    file_path = "interactiveplot.py"  # Replace with the path to your Python file
    run_python_file(file_path)

seed_value = 42
random.seed(seed_value)
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
    with open('data.csv', mode='r', encoding='utf-8-sig') as csv_file:
        csv_reader = csv.reader(csv_file)

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

    for idx, b in enumerate(packer.bins):

        st.header(f"{b.string()} \n")

        current_bin_weight = 0

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
            "Total weight of items / kg": [],
            "Residual volume": []
        }
        data1["Space utilization"].append(
            f'{round(volume_t / float(volume) * 100, 2)}%')
        if round(volume_t / float(volume) * 100, 2) != 0.0:
            bins_used += 1
        data1["Total weight of items / kg"].append(current_bin_weight)
        data1["Residual volume"].append(float(volume) - volume_t)

        # draw results
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
        st.subheader("FITTED ITEMS")
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
