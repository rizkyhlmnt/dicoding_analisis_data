import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

######### mendefinisikan fungsi fungsi ############
def create_top_bottom_seller(df):
    seller_frequency_df = df.groupby(by="seller_state").seller_id.nunique().reset_index()
    seller_frequency_df.rename(columns={"seller_id": "unique_seller_count"}, inplace=True)
    seller_frequency_df.sort_values(by="unique_seller_count", ascending=False, inplace=True)
    
    return seller_frequency_df


def create_top_bottom_produk(df):
    kategori_produk_frequency_df = df.groupby(by="product_category_name_english").order_id.nunique().reset_index()
    kategori_produk_frequency_df.rename(columns={"order_id": "unique_order_id_count"}, inplace=True)
    kategori_produk_frequency_df.sort_values(by="unique_order_id_count", ascending=False, inplace=True)
    
    return kategori_produk_frequency_df


def create_top_bottom_review(df):
    average_review_scores_df = df.groupby(by="product_category_name_english")['review_score'].mean().reset_index()
    average_review_scores_df.rename(columns={"review_score": "average_review_score"}, inplace=True)
    average_review_scores_df.sort_values(by='average_review_score', ascending=False, inplace=True)
    
    return average_review_scores_df


def create_top_bottom_customer(df):
    customer_frequency_df = df.groupby(by="customer_state")['customer_id'].nunique().reset_index()
    customer_frequency_df.rename(columns={"customer_id": "unique_customer_count"}, inplace=True)
    customer_frequency_df.sort_values(by='unique_customer_count', ascending=False, inplace=True)
    
    return customer_frequency_df


def create_waktu_pengiriman(df):
    min_delivery_time = round(df["delivery_time"].min())
    max_delivery_time = round(df["delivery_time"].max())
    mean_delivery_time = round(df["delivery_time"].mean())
    
    return min_delivery_time, max_delivery_time, mean_delivery_time


### import data ###
all_df = pd.read_csv("final_data.csv")

# Konversi kolom tanggal menjadi datetime tanpa format spesifik
all_df["order_purchase_timestamp"] = pd.to_datetime(all_df["order_purchase_timestamp"])
all_df["order_delivered_carrier_date"] = pd.to_datetime(all_df["order_delivered_carrier_date"])
all_df["order_delivered_customer_date"] = pd.to_datetime(all_df["order_delivered_customer_date"])

# Mengurutkan dan mereset indeks
all_df.sort_values(by="order_delivered_carrier_date", inplace=True)
all_df.reset_index(drop=True, inplace=True)

####### membuat komponen filter #######
min_date = all_df["order_purchase_timestamp"].min().date()  # Mengambil hanya tanggal
max_date = all_df['order_purchase_timestamp'].max().date()  # Mengambil hanya tanggal

### bikin side bar ###
with st.sidebar:
    # menambahkan logo perusahaan
    st.image('https://d1csarkz8obe9u.cloudfront.net/posterpreviews/e-commerce-logo-design-template-5dcf2e4daab6379d4824c6dc04e26f17_screen.jpg?ts=1645336764')

    # ambil start & end date dari data_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu', 
        min_value=min_date, 
        max_value=max_date,
        value=[min_date, max_date]
    )

# start date & end date dipake buat ngefilter all_df
main_df = all_df[(all_df["order_purchase_timestamp"] >= pd.to_datetime(start_date)) & 
                  (all_df["order_purchase_timestamp"] <= pd.to_datetime(end_date))]

# Panggil fungsi yang telah didefinisikan
seller_frequency_df = create_top_bottom_seller(main_df)
kategori_produk_frequency_df = create_top_bottom_produk(main_df)
average_review_scores_df = create_top_bottom_review(main_df)
customer_frequency_df = create_top_bottom_customer(main_df)
min_delivery_time, max_delivery_time, mean_delivery_time = create_waktu_pengiriman(main_df)



####### melengkapi dashboard dengan berbagai visualisasi data #######

st.header('E-Commerce Public Dashboard :sparkles:')



### membuat estimasi waktu pengiriman ###

st.subheader('Estimated Delivery Time')

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Fastest", value=f"{min_delivery_time} Day")

with col2:
    st.metric("Average", value=f"{mean_delivery_time} Day")

with col3:
    st.metric("longest", value=f"{max_delivery_time} Day")




### membuat top & bottom state by number of sellers ###
st.subheader("Top & Bottom State by Number of Sellers")

# Membuat plot untuk 3 negara bagian dengan jumlah penjual terbanyak dan tersedikit
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))

# Warna untuk visualisasi
colors_top = ["#FF6F61", "#6B5B95", "#88B04B"]
colors_bottom = ["#F7CAC9", "#92A8D1", "#F4E1D2"]

# Top 3 seller states (negara bagian dengan penjual terbanyak)
sns.barplot(x="unique_seller_count", y="seller_state", data=seller_frequency_df.head(3), palette=colors_top, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("Number of Sellers", fontsize=30)
ax[0].set_title("Top 3 States by Sellers", loc="center", fontsize=50)
ax[0].tick_params(axis='y', labelsize=35)
ax[0].tick_params(axis='x', labelsize=30)

# Bottom 3 seller states (negara bagian dengan penjual tersedikit)
sns.barplot(x="unique_seller_count", y="seller_state", data=seller_frequency_df.tail(3), palette=colors_bottom, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("Number of Sellers", fontsize=30)
ax[1].invert_xaxis()  # Membalikkan sumbu X agar lebih intuitif
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Bottom 3 States by Sellers", loc="center", fontsize=50)
ax[1].tick_params(axis='y', labelsize=35)
ax[1].tick_params(axis='x', labelsize=30)

# Mengatur rentang sumbu x untuk bar chart bottom
ax[1].set_xlim(0, 50)  # Rentang dari 0 sampai 20


# Menampilkan plot
st.pyplot(fig)




### top & bottom category product salles by number of orders ###
st.subheader("Top & Bottom Product Category by Number of orders")

# Membuat plot untuk 3 negara bagian dengan jumlah penjual terbanyak dan tersedikit
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))

# Warna untuk visualisasi
colors_top = ["#4CAF50", "#FFEB3B", "#2196F3"]
colors_bottom = ["#F44336", "#9E9E9E", "#FF9800"]

# Top 3 product categories (kategori produk dengan jumlah pesanan terbanyak)
sns.barplot(x="unique_order_id_count", y="product_category_name_english", data=kategori_produk_frequency_df.head(3), palette=colors_top, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("Number of Orders", fontsize=30)
ax[0].set_title("Top 3 Product Categories by Orders", loc="center", fontsize=50)
ax[0].tick_params(axis='y', labelsize=35)
ax[0].tick_params(axis='x', labelsize=30)

# Bottom 3 product categories (kategori produk dengan jumlah pesanan tersedikit)
sns.barplot(x="unique_order_id_count", y="product_category_name_english", data=kategori_produk_frequency_df.tail(3), palette=colors_bottom, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("Number of Orders", fontsize=30)
ax[1].invert_xaxis()  # Membalikkan sumbu X agar lebih intuitif
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Bottom 3 Product Categories by Orders", loc="center", fontsize=50)
ax[1].tick_params(axis='y', labelsize=35)
ax[1].tick_params(axis='x', labelsize=30)

# Mengatur rentang sumbu x untuk bar chart bottom
ax[1].set_xlim(0, 200)  # Rentang dari 0 sampai 50 (sesuaikan jika diperlukan)

# Menampilkan plot
st.pyplot(fig)


### Best and Worst Reviewed Product Categories ###
st.subheader("Best and Worst Reviewed Product Categories")

# Ambil kategori produk dengan review tertinggi dan terendah
best_review = average_review_scores_df.head(1)  # Kategori dengan review tertinggi
worst_review = average_review_scores_df.tail(1)  # Kategori dengan review terendah

# Gabungkan kedua dataframe
best_worst_review = pd.concat([best_review, worst_review])

# Membuat plot
fig, ax = plt.subplots(figsize=(8, 6))

# Warna untuk visualisasi
colors = ["#4CAF50", "#F44336"]  # Hijau untuk terbaik, Merah untuk terburuk

# Bar chart untuk kategori produk dengan review terbaik dan terburuk
sns.barplot(x="average_review_score", y="product_category_name_english", data=best_worst_review, palette=colors, ax=ax)
ax.set_xlabel("Average Review Score", fontsize=15)
ax.set_ylabel("Product Category", fontsize=15)
ax.set_title("Best and Worst Reviewed Product Categories", fontsize=20)

# Menampilkan plot
st.pyplot(fig)



### membuat top & bottom state by number of customer ###

st.subheader("Top & Bottom State by Number of Customers")
# Membuat plot untuk 3 negara bagian dengan jumlah pelanggan terbanyak dan tersedikit
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(18, 8))  # Ukuran lebih kecil dari contoh sebelumnya

# Warna untuk visualisasi
colors_top = ["#66BB6A", "#26A69A", "#FFCA28"]
colors_bottom = ["#FFAB91", "#90CAF9", "#B39DDB"]

# Top 3 states dengan jumlah customer terbanyak
sns.barplot(x="unique_customer_count", y="customer_state", data=customer_frequency_df.head(3), palette=colors_top, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("Number of Customers", fontsize=15)
ax[0].set_title("Top 3 States by Customers", loc="center", fontsize=20)
ax[0].tick_params(axis='y', labelsize=12)
ax[0].tick_params(axis='x', labelsize=12)

# Bottom 3 states dengan jumlah customer tersedikit
sns.barplot(x="unique_customer_count", y="customer_state", data=customer_frequency_df.tail(3), palette=colors_bottom, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("Number of Customers", fontsize=15)
ax[1].invert_xaxis()  # Membalikkan sumbu X agar lebih intuitif
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Bottom 3 States by Customers", loc="center", fontsize=20)
ax[1].tick_params(axis='y', labelsize=12)
ax[1].tick_params(axis='x', labelsize=12)

# Mengatur rentang sumbu x untuk bar chart bottom
ax[1].set_xlim(0, 4000)  # Rentang dari 0 sampai 50, sesuaikan dengan dataset Anda

# Menampilkan plot
st.pyplot(fig)


st.caption('Created by Rizky Hilmianto')