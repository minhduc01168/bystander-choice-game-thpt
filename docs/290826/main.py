# import streamlit as st
# import pandas as pd
# import numpy as np

# st.title("Ứng dụng Streamlit đầu tiên của tôi")

# st.write("Đây là một ứng dụng Streamlit đơn giản. Hãy cùng thêm một biểu đồ.")

# chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["A", "B", "C"])

# st.line_chart(chart_data)

# if st.checkbox("Hiển thị dữ liệu thô"):
#     st.subheader("Dữ liệu thô")
#     st.write(chart_data)


# # Hiển thị text
# st.text("Đây là văn bản thông thường")
# st.markdown("**Đây là văn bản Markdown**")
# st.title("Tiêu đề")
# st.header("Header")
# st.subheader("Subheader")
# st.code("print('Hello, Streamlit!')", language="python")

# # Hiển thị dữ liệu
# st.dataframe(df)  # DataFrame với định dạng tương tác
# st.table(df)  # DataFrame dạng tĩnh
# st.json(data)  # Hiển thị JSON


# # Widgets cơ bản
# name = st.text_input("Tên của bạn:")
# age = st.number_input("Tuổi:", min_value=0, max_value=120)
# happy = st.checkbox("Bạn có hài lòng không?")

# # Lựa chọn
# option = st.selectbox("Chọn một option:", ["Option 1", "Option 2", "Option 3"])
# options = st.multiselect("Chọn nhiều options:", ["A", "B", "C", "D"])

# # Sliders
# values = st.slider("Chọn một khoảng:", 0, 100, (25, 75))
# value = st.slider("Chọn một giá trị:", 0, 100, 50)

# # Buttons
# if st.button("Click me"):
#     st.write("Bạn đã click vào button!")


# # Biểu đồ tích hợp
# st.line_chart(data)
# st.bar_chart(data)
# st.area_chart(data)

# # Sử dụng matplotlib
# import matplotlib.pyplot as plt

# fig, ax = plt.subplots()
# ax.plot([1, 2, 3], [1, 4, 9])
# st.pyplot(fig)

# # Plotly
# import plotly.express as px

# fig = px.scatter(df, x="sepal_width", y="sepal_length", color="species")
# st.plotly_chart(fig)


import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Tiêu đề ứng dụng
st.title("Phân tích Bộ dữ liệu Iris")


# Tải dữ liệu
@st.cache_data
def load_data():
    return sns.load_dataset("iris")


df = load_data()

# Sidebar với các tùy chọn
st.sidebar.header("Tùy chọn")
species = st.sidebar.multiselect(
    "Chọn loài hoa:", options=df["species"].unique(), default=df["species"].unique()
)

# Lọc dữ liệu
mask = df["species"].isin(species)
filtered_df = df[mask]

# Hiển thị dữ liệu
st.subheader("Dữ liệu Iris")
st.write(filtered_df)

# Thống kê cơ bản
st.subheader("Thống kê cơ bản")
st.write(filtered_df.describe())

# Vẽ biểu đồ
st.subheader("Biểu đồ")
chart_type = st.sidebar.selectbox(
    "Chọn loại biểu đồ:", ["Scatter", "Histogram", "Box Plot"]
)

if chart_type == "Scatter":
    x_axis = st.sidebar.selectbox("Chọn trục X:", df.columns[:-1])
    y_axis = st.sidebar.selectbox("Chọn trục Y:", df.columns[1:-1])

    fig, ax = plt.subplots(figsize=(10, 6))
    for species_name in species:
        species_df = df[df["species"] == species_name]
        ax.scatter(
            species_df[x_axis], species_df[y_axis], label=species_name, alpha=0.7
        )

    ax.set_xlabel(x_axis)
    ax.set_ylabel(y_axis)
    ax.legend()
    st.pyplot(fig)

elif chart_type == "Histogram":
    feature = st.sidebar.selectbox("Chọn đặc trưng:", df.columns[:-1])
    bins = st.sidebar.slider("Số lượng bins:", 5, 30, 15)

    fig, ax = plt.subplots(figsize=(10, 6))
    for species_name in species:
        species_df = df[df["species"] == species_name]
        ax.hist(species_df[feature], bins=bins, alpha=0.5, label=species_name)

    ax.set_xlabel(feature)
    ax.legend()
    st.pyplot(fig)

elif chart_type == "Box Plot":
    feature = st.sidebar.selectbox("Chọn đặc trưng:", df.columns[:-1])

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.boxplot(x="species", y=feature, data=filtered_df, ax=ax)
    st.pyplot(fig)
