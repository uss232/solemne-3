import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

def show():
    # Cargar los datos
    try:
        book = pd.read_csv('books_of_the_decade.csv')
        user_reviews = pd.read_csv('user_reviews_dataset.csv')
        st.success('📈 ¡Datos cargados correctamente!')
    except FileNotFoundError as e:
        st.error(f"⚠️ Error al cargar los datos: {e}")
        st.stop()

    # Fusionar datasets
    books = pd.merge(user_reviews, book, left_on='bookIndex', right_on='Index', how='inner')

    # Parámetros de visualización interactivos
    st.markdown("<h2>📈 Distribución de Calificaciones</h2>", unsafe_allow_html=True)
    bins = st.sidebar.slider('📊 Número de Bins para la Distribución de Calificaciones', min_value=5, max_value=50, value=10, step=1)

    # Gráfico interactivo de distribución de calificaciones
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.set_style("whitegrid")
    sns.histplot(books['Rating'], bins=bins, kde=True, color='#4CAF50', ax=ax)
    ax.set_title('Distribución de Calificaciones', fontsize=16)
    ax.set_xlabel('Calificación', fontsize=14)
    ax.set_ylabel('Frecuencia', fontsize=14)
    st.pyplot(fig)
