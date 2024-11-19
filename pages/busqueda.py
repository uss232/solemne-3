import pandas as pd
import streamlit as st
import random
import os


# Función para generar un ID único de usuario
def generate_user_id():
    return random.randint(100000, 999999)


# Función para guardar la calificación en el archivo `user_reviews_dataset.csv` usando bookIndex
def save_rating(user_id, book_index, rating):
    # Cargar el archivo de dataset de reviews de usuario
    if os.path.exists('user_reviews_dataset.csv'):
        reviews_df = pd.read_csv('user_reviews_dataset.csv')
    else:
        st.error("⚠️ El archivo 'user_reviews_dataset.csv' no se encuentra.")
        return

    # Verificar si el usuario ya ha calificado el libro
    review_index = reviews_df[(reviews_df['userId'] == user_id) & (reviews_df['bookIndex'] == book_index)].index

    if not review_index.empty:
        # Si ya existe, actualizar la calificación
        reviews_df.loc[review_index, 'score'] = rating
        st.success(f"✅ ¡Gracias por actualizar tu calificación!")
    else:
        # Si no existe, añadir una nueva fila con el ID de usuario, bookIndex y calificación
        new_rating = pd.DataFrame({'userId': [user_id], 'bookIndex': [book_index], 'score': [rating]})
        reviews_df = pd.concat([reviews_df, new_rating], ignore_index=True)
        st.success(f"✅ ¡Gracias por tu calificación! Tu ID de usuario es: {user_id}")

    # Guardar en el archivo CSV de reviews actualizado
    reviews_df.to_csv('user_reviews_dataset.csv', index=False)


def show():
    # Cargar los datos
    try:
        book = pd.read_csv('books_of_the_decade.csv')
        user_reviews = pd.read_csv('user_reviews_dataset.csv')
        st.success('🔍 ¡Datos cargados correctamente!')
    except FileNotFoundError as e:
        st.error(f"⚠️ Error al cargar los datos: {e}")
        st.stop()

    # Fusionar datasets
    books = pd.merge(user_reviews, book, left_on='bookIndex', right_on='Index', how='inner')

    # Título de la sección
    st.markdown("<h2>🔎 Búsqueda de Libros y Autores</h2>", unsafe_allow_html=True)

    # Búsqueda por libro o autor
    search_option = st.radio('Buscar por:', ['Libro', 'Autor'])

    if search_option == 'Libro':
        search_term = st.text_input('Introduce el nombre del libro:')
        if search_term:
            # Filtrar libros que contengan el término de búsqueda
            search_results = books[books['Book Name'].str.contains(search_term, case=False, na=False)]

            if not search_results.empty:
                st.markdown(f"<h3>Resultados para el libro: '{search_term}'</h3>", unsafe_allow_html=True)
                # Crear un selectbox para seleccionar un libro específico de la búsqueda
                selected_book_index = st.selectbox(
                    'Selecciona un libro para más detalles:',
                    search_results[['Book Name', 'bookIndex']].drop_duplicates().set_index('bookIndex')[
                        'Book Name'].to_dict()
                )

                # Mostrar detalles del libro seleccionado
                if selected_book_index:
                    book_details = search_results[search_results['bookIndex'] == selected_book_index].iloc[0]
                    st.write(f"**Nombre del Libro:** {book_details['Book Name']}")
                    st.write(f"**Autor:** {book_details['Author']}")
                    st.write(f"**Puntuación:** {book_details['Score']}")
                    st.write(f"**Calificación Media:** {book_details['Rating']}")

                    # Mostrar formulario para rankear el libro
                    st.markdown("<h4>📊 Rankea este libro</h4>", unsafe_allow_html=True)
                    user_id = generate_user_id()
                    rating = st.slider('Tu calificación:', min_value=1, max_value=5, step=1)

                    if st.button('Enviar Calificación'):
                        save_rating(user_id, selected_book_index, rating)
            else:
                st.warning('⚠️ No se encontraron resultados para ese libro.')

    elif search_option == 'Autor':
        search_term = st.text_input('Introduce el nombre del autor:')
        if search_term:
            # Filtrar autores que contengan el término de búsqueda
            search_results = books[books['Author'].str.contains(search_term, case=False, na=False)]

            if not search_results.empty:
                st.markdown(f"<h3>Resultados para el autor: '{search_term}'</h3>", unsafe_allow_html=True)
                # Crear un selectbox para seleccionar un libro específico del autor
                selected_book_index = st.selectbox(
                    'Selecciona un libro del autor para más detalles:',
                    search_results[['Book Name', 'bookIndex']].drop_duplicates().set_index('bookIndex')[
                        'Book Name'].to_dict()
                )

                # Mostrar detalles del libro seleccionado
                if selected_book_index:
                    book_details = search_results[search_results['bookIndex'] == selected_book_index].iloc[0]
                    st.write(f"**Nombre del Libro:** {book_details['Book Name']}")
                    st.write(f"**Autor:** {book_details['Author']}")
                    st.write(f"**Puntuación:** {book_details['Score']}")
                    st.write(f"**Calificación Media:** {book_details['Rating']}")

                    # Mostrar formulario para rankear el libro
                    st.markdown("<h4>📊 Rankea este libro</h4>", unsafe_allow_html=True)
                    user_id = generate_user_id()
                    rating = st.slider('Tu calificación:', min_value=1, max_value=5, step=1)

                    if st.button('Enviar Calificación'):
                        save_rating(user_id, selected_book_index, rating)
            else:
                st.warning('⚠️ No se encontraron resultados para ese autor.')
