import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Judul aplikasi
st.title("📊 Analisis dan Klasifikasi Gizi Balita")

# Upload file
uploaded_file = st.file_uploader("Unggah file CSV hasil prediksi", type=["csv"])
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # Mapping label prediksi ke kategori
    df['prediction'] = df['prediction'].map({0: 'Low', 1: 'Medium', 2: 'High'})

    st.subheader("📄 Data Hasil Prediksi")
    st.dataframe(df.head(20))

    # Sidebar filter
    st.sidebar.header("🔍 Filter Data")
    selected_label = st.sidebar.multiselect(
        "Pilih Kategori Gizi", options=df['prediction'].unique(), default=df['prediction'].unique()
    )
    filtered_df = df[df['prediction'].isin(selected_label)]

    # Visualisasi Pie Chart
    st.subheader("📈 Proporsi Kategori Gizi")
    pie_data = filtered_df['prediction'].value_counts()
    st.pyplot(
        pie_data.plot.pie(autopct='%1.1f%%', figsize=(5, 5), title="Proporsi Gizi").figure
    )

    # Visualisasi Countplot
    st.subheader("📊 Distribusi Gizi per Jenis Kelamin")
    if 'JENIS KELAMIN' in df.columns:
        fig, ax = plt.subplots()
        sns.countplot(data=filtered_df, x='prediction', hue='JENIS KELAMIN', palette='pastel', ax=ax)
        ax.set_title("Distribusi Gizi Berdasarkan Jenis Kelamin")
        st.pyplot(fig)

    # Visualisasi Scatter Berat vs Tinggi
    if 'Berat' in df.columns and 'Tinggi' in df.columns:
        st.subheader("⚖️ Scatter Plot Berat vs Tinggi")
        fig2, ax2 = plt.subplots()
        sns.scatterplot(data=filtered_df, x='Tinggi', y='Berat', hue='prediction', palette='Set1', ax=ax2)
        st.pyplot(fig2)

    # Download CSV
    st.download_button(
        label="📥 Unduh Data Filtered",
        data=filtered_df.to_csv(index=False).encode('utf-8'),
        file_name='filtered_gizi_balita.csv',
        mime='text/csv'
    )
else:
    st.info("⬅️ Silakan unggah file CSV terlebih dahulu.")