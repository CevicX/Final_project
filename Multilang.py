import streamlit as st
import pandas as pd
import numpy as np
import base64
import pickle
import plotly.express as px

model = pickle.load(open('forest_2.pkl', 'rb'))

# Sample DataFrame (replace this with your actual DataFrame)
unique_values_grouped = pd.read_csv('data_2.csv')

# Create a Streamlit app
st.title("Seletor de Atributos")

# Create a selector to switch between pages
language_selector = st.radio("Escolha o Idioma / Elija el Idioma:", ("English", "Português", "Español"))

if language_selector == "English":
    page_selector = st.selectbox("Select Page", ["Attribute Selection", "Graphics Page"])
    if page_selector == "Attribute Selection":
        st.write(
            "This app allows you to select programming languages and attribute values to suggest a salary range."
        )

        # Create a sidebar for attribute selection
        st.sidebar.title("Options")

        # List of attributes where multiple selections are allowed (Programming Languages)
        multi_select_attributes = [
            'Bash/Shell ( all shells )', 'HTML/CSS', 'JavaScript', 'Ruby', 'SQL',
            'TypeScript', 'C#', 'PowerShell', 'Kotlin', 'Python', 'Java', 'Perl',
            'Dart', 'Go', 'Haskell', 'PHP', 'Delphi', 'C++', 'Clojure', 'Elixir',
            'Lua', 'Rust', 'C', 'Scala', 'GDScript', 'F#', 'Groovy', 'Lisp', 'Swift',
            'Objective-C', 'Visual Basic (.Net)', 'R', 'VBA', 'APL', 'Assembly',
            'Cobol', 'Fortran', 'Julia', 'MATLAB', 'Prolog', 'Crystal', 'SAS',
            'Apex', 'Solidity', 'Erlang', 'Raku', 'Nim', 'Zig', 'Ada', 'OCaml',
            'Flow'
        ]

        # Create a flag to track if "Programming Language" has been displayed
        programming_language_displayed = False

        # Attributes to show outside the "Programming Language" multi-select box
        attributes_to_show = ['RemoteWork', 'EdLevel', 'DevType', 'OrgSize', 'Country', 'YearsCodePro']

        # Initialize selected_programming_languages with an empty list
        selected_programming_languages = []

        # Allow the user to select "Programming Language"
        if not programming_language_displayed:
            selected_programming_languages = st.sidebar.multiselect(
                "Select the programming languages you're familiar with:",
                multi_select_attributes,
                key="programming_languages",  # Unique key
            )
            programming_language_displayed = True

        # Allow the user to select attributes (YearsCodePro, OrgSize, and others)
        selected_attributes = {}
        for column in attributes_to_show:
            options = ['Select one:'] + [str(val) for val in unique_values_grouped[column].unique()]
            selected_value = st.sidebar.selectbox(
                f"Select {column}",
                options,
                key=f"{column}_selectbox",  # Unique key
            )

            # Store selected value in a dictionary
            selected_attributes[column] = selected_value

        # Display the selected attributes
        st.header("Selected Attributes")
        st.write(selected_attributes)

        # Define a function to adapt a skeleton DataFrame with user inputs
        def adapt_skeleton_with_user_inputs(skeleton_data, user_inputs):
            # Iterate over user_inputs and update skeleton_data accordingly
            for key, value in user_inputs.items():
                if key in skeleton_data.columns:
                    skeleton_data[key] = value

            return skeleton_data

        # Create a skeleton DataFrame based on the training data (replace this with your actual training data)
        training_data = pd.read_csv('X.csv')

        # Create a skeleton DataFrame with 0 values for selected or not selected columns
        skeleton_data = pd.DataFrame(0, columns=training_data.columns, index=[0])

        # Check if the user has clicked the "Apply" button
        if st.sidebar.button("Apply"):
            # Adapt the skeleton DataFrame with user inputs for programming languages
            for language in multi_select_attributes:
                if language in selected_programming_languages:
                    skeleton_data[language] = 1

            # Adapt the skeleton DataFrame with user inputs for other attributes (YearsCodePro, OrgSize, etc.)
            for column, selected_value in selected_attributes.items():
                if selected_value and selected_value != 'Select one:':
                    skeleton_data[column + '_' + selected_value] = 1
        
            skeleton_data.to_csv('adapted_data.csv', index=False)
            adapted_data = pd.read_csv('adapted_data.csv')
            predictions = model.predict(adapted_data)
            st.header("Predictions")
            st.write('Our model predicts that you will earn between: ', predictions,
                'Based on this you should ask a salary range between: ', (predictions+predictions*.1), 'and', (predictions-predictions*.1))
    else:
        # Load your dataset for the graphics page
        data = pd.read_csv('data_test.csv')

        st.title("Graphics Page")

        # Create sidebar filters for developer type, remote work, education level, organization size, and country
        selected_devtype = st.sidebar.selectbox('Select Developer Type', ['- Select Developer Type -'] + list(data['DevType'].unique()), index=0)
        selected_remote_work = st.sidebar.selectbox('Select Remote Work', ['- Select Remote Work -'] + list(data['RemoteWork'].unique()), index=0)
        selected_ed_level = st.sidebar.selectbox('Select Education Level', ['- Select Education Level -'] + list(data['EdLevel'].unique()), index=0)
        selected_org_size = st.sidebar.selectbox('Select Organization Size', ['- Select Organization Size -'] + list(data['OrgSize'].unique()), index=0)
        selected_country = st.sidebar.selectbox('Select Country', ['- Select Country -'] + list(data['Country'].unique()), index=0)

        # Filter the dataset based on the selected filters
        if selected_devtype != '- Select Developer Type -':
            filtered_data = data[data['DevType'] == selected_devtype]
        else:
            filtered_data = data

        if selected_remote_work != '- Select Remote Work -':
            filtered_data = filtered_data[filtered_data['RemoteWork'] == selected_remote_work]

        if selected_ed_level != '- Select Education Level -':
            filtered_data = filtered_data[filtered_data['EdLevel'] == selected_ed_level]

        if selected_org_size != '- Select Organization Size -':
            filtered_data = filtered_data[filtered_data['OrgSize'] == selected_org_size]

        if selected_country != '- Select Country -':
            filtered_data = filtered_data[filtered_data['Country'] == selected_country]

        # Scatter Plot
        st.subheader("Scatter Plot")

        # Define the desired order of 'YearsCodePro' categories
        desired_order = [
            "Less than 1 year",
            "2 to 5 years",
            "6 to 10 years",
            "11 to 20 years",
            "21 to 30 years",
            "More than 30 years"
        ]

        # Create the scatter plot with color-coding for the 'YearsCodePro' categories
        scatter_fig = px.scatter(
            filtered_data,
            x='YearsCodePro',        # X-axis: YearsCodePro
            y='ConvertedCompYearly', # Y-axis: ConvertedCompYearly
            color='YearsCodePro',    # Color points by 'YearsCodePro' category
            title='Relationship Between Years of Coding and Yearly Compensation',
            labels={'YearsCodePro': 'Years of Coding Experience', 'ConvertedCompYearly': 'Yearly Compensation'},
            
            # Specify the order of 'YearsCodePro' categories
            category_orders={'YearsCodePro': desired_order}
        )

        # Show the scatter plot inside Streamlit with all categories in the legend
        st.plotly_chart(scatter_fig, use_container_width=True)

        # Bar Chart
        st.subheader("Bar Chart")

        # Calculate the total count of each programming language for the selected developer type
        language_counts = filtered_data.iloc[:, 7:-1].sum()  # Select columns with programming languages and sum

        # Determine the top N programming languages by usage
        top_languages = language_counts.sort_values(ascending=False).head(10)  # Adjust the number of top languages as needed

        # Create a bar chart showing top programming languages usage
        bar_fig = px.bar(
            x=top_languages.index,  # Programming languages
            y=top_languages.values, # Usage counts
            title=f'Top Programming Languages for {selected_devtype}',
            labels={'x': 'Programming Language', 'y': 'Count'},
        )

        # Show the bar chart inside Streamlit with all categories in the legend
        st.plotly_chart(bar_fig, use_container_width=True)

elif language_selector == "Português":
    page_selector = st.selectbox("Selecione a Página", ["Seleção de Atributos", "Página de Gráficos"])
    if page_selector == "Seleção de Atributos":
        st.write(
            "Este aplicativo permite que você selecione linguagens de programação e valores de atributos para sugerir uma faixa salarial."
        )

        # Create a sidebar for attribute selection
        st.sidebar.title("Opções")

        # List of attributes where multiple selections are allowed (Programming Languages)
        multi_select_attributes = [
            'Bash/Shell ( todos os shells )', 'HTML/CSS', 'JavaScript', 'Ruby', 'SQL',
            'TypeScript', 'C#', 'PowerShell', 'Kotlin', 'Python', 'Java', 'Perl',
            'Dart', 'Go', 'Haskell', 'PHP', 'Delphi', 'C++', 'Clojure', 'Elixir',
            'Lua', 'Rust', 'C', 'Scala', 'GDScript', 'F#', 'Groovy', 'Lisp', 'Swift',
            'Objective-C', 'Visual Basic (.Net)', 'R', 'VBA', 'APL', 'Assembly',
            'Cobol', 'Fortran', 'Julia', 'MATLAB', 'Prolog', 'Crystal', 'SAS',
            'Apex', 'Solidity', 'Erlang', 'Raku', 'Nim', 'Zig', 'Ada', 'OCaml',
            'Flow'
        ]

        # Create a flag to track if "Programming Language" has been displayed
        programming_language_displayed = False

        # Attributes to show outside the "Programming Language" multi-select box
        attributes_to_show = ['RemoteWork', 'EdLevel', 'DevType', 'OrgSize', 'Country', 'YearsCodePro']

        # Initialize selected_programming_languages with an empty list
        selected_programming_languages = []

        # Allow the user to select "Programming Language"
        if not programming_language_displayed:
            selected_programming_languages = st.sidebar.multiselect(
                "Selecione as linguagens de programação com as quais você está familiarizado:",
                multi_select_attributes,
                key="programming_languages",  # Chave única
            )
            programming_language_displayed = True

        # Allow the user to select attributes (YearsCodePro, OrgSize, and others)
        selected_attributes = {}
        for column in attributes_to_show:
            options = ['Selecione um:'] + [str(val) for val in unique_values_grouped[column].unique()]
            selected_value = st.sidebar.selectbox(
                f"Selecione {column}",
                options,
                key=f"{column}_selectbox",  # Chave única
            )

            # Armazene o valor selecionado em um dicionário
            selected_attributes[column] = selected_value

        # Display the selected attributes
        st.header("Atributos Selecionados")
        st.write(selected_attributes)

        # Defina uma função para adaptar um DataFrame esqueleto com entradas do usuário
        def adapt_skeleton_with_user_inputs(skeleton_data, user_inputs):
            # Itere sobre user_inputs e atualize skeleton_data de acordo
            for key, value in user_inputs.items():
                if key in skeleton_data.columns:
                    skeleton_data[key] = value

            return skeleton_data

        # Crie um DataFrame esqueleto com base nos dados de treinamento (substitua isso pelos seus dados reais de treinamento)
        training_data = pd.read_csv('X.csv')

        # Crie um DataFrame esqueleto com valores 0 para colunas selecionadas ou não selecionadas
        skeleton_data = pd.DataFrame(0, columns=training_data.columns, index=[0])

        # Verifique se o usuário clicou no botão "Aplicar"
        if st.sidebar.button("Aplicar"):
            # Adapte o DataFrame esqueleto com entradas do usuário para linguagens de programação
            for language in multi_select_attributes:
                if language in selected_programming_languages:
                    skeleton_data[language] = 1

            # Adapte o DataFrame esqueleto com entradas do usuário para outros atributos (YearsCodePro, OrgSize, etc.)
            for column, selected_value in selected_attributes.items():
                if selected_value and selected_value != 'Selecione um:':
                    skeleton_data[column + '_' + selected_value] = 1
        
            skeleton_data.to_csv('adapted_data.csv', index=False)
            adapted_data = pd.read_csv('adapted_data.csv')
            predictions = model.predict(adapted_data)
            st.header("Previsões")
            st.write('Nosso modelo prevê que você ganhará entre: ', predictions,
                'Com base nisso, você deve pedir uma faixa salarial entre: ', (predictions+predictions*.1), 'e', (predictions-predictions*.1))
    else:
        # Carregue seu conjunto de dados para a página de gráficos
        data = pd.read_csv('data_test.csv')

        st.title("Página de Gráficos")

        # Crie filtros de barra lateral para tipo de desenvolvedor, trabalho remoto, nível de educação, tamanho da organização e país
        selected_devtype = st.sidebar.selectbox('Selecione o Tipo de Desenvolvedor', ['- Selecione o Tipo de Desenvolvedor -'] + list(data['DevType'].unique()), index=0)
        selected_remote_work = st.sidebar.selectbox('Selecione o Trabalho Remoto', ['- Selecione o Trabalho Remoto -'] + list(data['RemoteWork'].unique()), index=0)
        selected_ed_level = st.sidebar.selectbox('Selecione o Nível de Educação', ['- Selecione o Nível de Educação -'] + list(data['EdLevel'].unique()), index=0)
        selected_org_size = st.sidebar.selectbox('Selecione o Tamanho da Organização', ['- Selecione o Tamanho da Organização -'] + list(data['OrgSize'].unique()), index=0)
        selected_country = st.sidebar.selectbox('Selecione o País', ['- Selecione o País -'] + list(data['Country'].unique()), index=0)

        # Filtrar o conjunto de dados com base nos filtros selecionados
        if selected_devtype != '- Selecione o Tipo de Desenvolvedor -':
            filtered_data = data[data['DevType'] == selected_devtype]
        else:
            filtered_data = data

        if selected_remote_work != '- Selecione o Trabalho Remoto -':
            filtered_data = filtered_data[filtered_data['RemoteWork'] == selected_remote_work]

        if selected_ed_level != '- Selecione o Nível de Educação -':
            filtered_data = filtered_data[filtered_data['EdLevel'] == selected_ed_level]

        if selected_org_size != '- Selecione o Tamanho da Organização -':
            filtered_data = filtered_data[filtered_data['OrgSize'] == selected_org_size]

        if selected_country != '- Selecione o País -':
            filtered_data = filtered_data[filtered_data['Country'] == selected_country]

        # Gráfico de Dispersão
        st.subheader("Gráfico de Dispersão")

        # Definir a ordem desejada das categorias de 'YearsCodePro'
        desired_order = [
            "Menos de 1 ano",
            "2 a 5 anos",
            "6 a 10 anos",
            "11 a 20 anos",
            "21 a 30 anos",
            "Mais de 30 anos"
        ]

        # Criar o gráfico de dispersão com codificação de cores para as categorias 'YearsCodePro'
        scatter_fig = px.scatter(
            filtered_data,
            x='YearsCodePro',        # Eixo X: YearsCodePro
            y='ConvertedCompYearly', # Eixo Y: ConvertedCompYearly
            color='YearsCodePro',    # Colorir pontos pela categoria 'YearsCodePro'
            title='Relação Entre Anos de Codificação e Remuneração Anual',
            labels={'YearsCodePro': 'Anos de Experiência em Codificação', 'ConvertedCompYearly': 'Remuneração Anual'},
            
            # Especificar a ordem das categorias 'YearsCodePro'
            category_orders={'YearsCodePro': desired_order}
        )

        # Mostrar o gráfico de dispersão dentro do Streamlit com todas as categorias na legenda
        st.plotly_chart(scatter_fig, use_container_width=True)

        # Gráfico de Barras
        st.subheader("Gráfico de Barras")

        # Calcular a contagem total de cada linguagem de programação para o tipo de desenvolvedor selecionado
        language_counts = filtered_data.iloc[:, 7:-1].sum()  # Selecionar colunas com linguagens de programação e somar

        # Determine as principais linguagens de programação por uso
        top_languages = language_counts.sort_values(ascending=False).head(10)  # Ajuste o número de principais linguagens conforme necessário

        # Criar um gráfico de barras mostrando o uso das principais linguagens de programação
        bar_fig = px.bar(
            x=top_languages.index,  # Linguagens de programação
            y=top_languages.values, # Contagens de uso
            title=f'Principais Linguagens de Programação para {selected_devtype}',
            labels={'x': 'Linguagem de Programação', 'y': 'Contagem'},
        )

        # Mostrar o gráfico de barras dentro do Streamlit com todas as categorias na legenda
        st.plotly_chart(bar_fig, use_container_width=True)

elif language_selector == "Español":
    page_selector = st.selectbox("Seleccione la Página", ["Selección de Atributos", "Página de Gráficos"])
    if page_selector == "Selección de Atributos":
        st.write(
            "Esta aplicación le permite seleccionar lenguajes de programación y valores de atributos para sugerir un rango salarial."
        )

        # Create a sidebar for attribute selection
        st.sidebar.title("Opciones")

        # List of attributes where multiple selections are allowed (Programming Languages)
        multi_select_attributes = [
            'Bash/Shell ( todos los shells )', 'HTML/CSS', 'JavaScript', 'Ruby', 'SQL',
            'TypeScript', 'C#', 'PowerShell', 'Kotlin', 'Python', 'Java', 'Perl',
            'Dart', 'Go', 'Haskell', 'PHP', 'Delphi', 'C++', 'Clojure', 'Elixir',
            'Lua', 'Rust', 'C', 'Scala', 'GDScript', 'F#', 'Groovy', 'Lisp', 'Swift',
            'Objective-C', 'Visual Basic (.Net)', 'R', 'VBA', 'APL', 'Assembly',
            'Cobol', 'Fortran', 'Julia', 'MATLAB', 'Prolog', 'Crystal', 'SAS',
            'Apex', 'Solidity', 'Erlang', 'Raku', 'Nim', 'Zig', 'Ada', 'OCaml',
            'Flow'
        ]

        # Create a flag to track if "Programming Language" has been displayed
        programming_language_displayed = False

        # Attributes to show outside the "Programming Language" multi-select box
        attributes_to_show = ['RemoteWork', 'EdLevel', 'DevType', 'OrgSize', 'Country', 'YearsCodePro']

        # Initialize selected_programming_languages with an empty list
        selected_programming_languages = []

        # Allow the user to select "Programming Language"
        if not programming_language_displayed:
            selected_programming_languages = st.sidebar.multiselect(
                "Seleccione los lenguajes de programación con los que está familiarizado:",
                multi_select_attributes,
                key="programming_languages",  # Clave única
            )
            programming_language_displayed = True

        # Allow the user to select attributes (YearsCodePro, OrgSize, and others)
        selected_attributes = {}
        for column in attributes_to_show:
            options = ['Seleccione uno:'] + [str(val) for val in unique_values_grouped[column].unique()]
            selected_value = st.sidebar.selectbox(
                f"Seleccione {column}",
                options,
                key=f"{column}_selectbox",  # Clave única
            )

            # Almacene el valor seleccionado en un diccionario
            selected_attributes[column] = selected_value

        # Display the selected attributes
        st.header("Atributos Seleccionados")
        st.write(selected_attributes)

        # Defina una función para adaptar un DataFrame esqueleto con entradas del usuario
        def adapt_skeleton_with_user_inputs(skeleton_data, user_inputs):
            # Itere sobre user_inputs y actualice skeleton_data en consecuencia
            for key, value in user_inputs.items():
                if key in skeleton_data.columns:
                    skeleton_data[key] = value

            return skeleton_data

        # Cree un DataFrame esqueleto basado en los datos de entrenamiento (reemplace esto con sus datos de entrenamiento reales)
        training_data = pd.read_csv('X.csv')

        # Cree un DataFrame esqueleto con valores 0 para columnas seleccionadas o no seleccionadas
        skeleton_data = pd.DataFrame(0, columns=training_data.columns, index=[0])

        # Compruebe si el usuario ha hecho clic en el botón "Aplicar"
        if st.sidebar.button("Aplicar"):
            # Adapte el DataFrame esqueleto con las entradas del usuario para los lenguajes de programación
            for language in multi_select_attributes:
                if language in selected_programming_languages:
                    skeleton_data[language] = 1

            # Adapte el DataFrame esqueleto con las entradas del usuario para otros atributos (YearsCodePro, OrgSize, etc.)
            for column, selected_value in selected_attributes.items():
                if selected_value and selected_value != 'Seleccione uno:':
                    skeleton_data[column + '_' + selected_value] = 1
        
            skeleton_data.to_csv('adapted_data.csv', index=False)
            adapted_data = pd.read_csv('adapted_data.csv')
            predictions = model.predict(adapted_data)
            st.header("Predicciones")
            st.write('Nuestro modelo predice que ganará entre: ', predictions,
                'Basado en esto, debería solicitar un rango salarial entre: ', (predictions+predictions*.1), 'y', (predictions-predictions*.1))
    else:
        # Cargue su conjunto de datos para la página de gráficos
        data = pd.read_csv('data_test.csv')

        st.title("Página de Gráficos")

        # Cree filtros de barra lateral para el tipo de desarrollador, el trabajo remoto, el nivel de educación, el tamaño de la organización y el país
        selected_devtype = st.sidebar.selectbox('Seleccione el Tipo de Desarrollador', ['- Seleccione el Tipo de Desarrollador -'] + list(data['DevType'].unique()), index=0)
        selected_remote_work = st.sidebar.selectbox('Seleccione el Trabajo Remoto', ['- Seleccione el Trabajo Remoto -'] + list(data['RemoteWork'].unique()), index=0)
        selected_ed_level = st.sidebar.selectbox('Seleccione el Nivel de Educación', ['- Seleccione el Nivel de Educación -'] + list(data['EdLevel'].unique()), index=0)
        selected_org_size = st.sidebar.selectbox('Seleccione el Tamaño de la Organización', ['- Seleccione el Tamaño de la Organización -'] + list(data['OrgSize'].unique()), index=0)
        selected_country = st.sidebar.selectbox('Seleccione el País', ['- Seleccione el País -'] + list(data['Country'].unique()), index=0)

        # Filtre el conjunto de datos en función de los filtros seleccionados
        if selected_devtype != '- Seleccione el Tipo de Desarrollador -':
            filtered_data = data[data['DevType'] == selected_devtype]
        else:
            filtered_data = data

        if selected_remote_work != '- Seleccione el Trabajo Remoto -':
            filtered_data = filtered_data[filtered_data['RemoteWork'] == selected_remote_work]

        if selected_ed_level != '- Seleccione el Nivel de Educación -':
            filtered_data = filtered_data[filtered_data['EdLevel'] == selected_ed_level]

        if selected_org_size != '- Seleccione el Tamaño de la Organización -':
            filtered_data = filtered_data[filtered_data['OrgSize'] == selected_org_size]

        if selected_country != '- Seleccione el País -':
            filtered_data = filtered_data[filtered_data['Country'] == selected_country]

        # Gráfico de Dispersión
        st.subheader("Gráfico de Dispersión")

        # Defina el orden deseado de las categorías de 'YearsCodePro'
        desired_order = [
            "Menos de 1 año",
            "2 a 5 años",
            "6 a 10 años",
            "11 a 20 años",
            "21 a 30 años",
            "Más de 30 años"
        ]

        # Cree el gráfico de dispersión con codificación de colores para las categorías 'YearsCodePro'
        scatter_fig = px.scatter(
            filtered_data,
            x='YearsCodePro',        # Eje X: YearsCodePro
            y='ConvertedCompYearly', # Eje Y: ConvertedCompYearly
            color='YearsCodePro',    # Colorear puntos por la categoría 'YearsCodePro'
            title='Relación Entre Años de Codificación y Remuneración Anual',
            labels={'YearsCodePro': 'Años de Experiencia en Codificación', 'ConvertedCompYearly': 'Remuneración Anual'},
            
            # Especifique el orden de las categorías 'YearsCodePro'
            category_orders={'YearsCodePro': desired_order}
        )

        # Muestre el gráfico de dispersión dentro de Streamlit con todas las categorías en la leyenda
        st.plotly_chart(scatter_fig, use_container_width=True)

        # Gráfico de Barras
        st.subheader("Gráfico de Barras")

        # Calcule el recuento total de cada lenguaje de programación para el tipo de desarrollador seleccionado
        language_counts = filtered_data.iloc[:, 7:-1].sum()  # Seleccione columnas con lenguajes de programación y sume

        # Determine las principales lenguas
