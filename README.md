# Propuesta Económica para Seguro de Jubilación

## Descripción del Proyecto
El objetivo principal de este proyecto es desarrollar una propuesta económica para un seguro de jubilación dirigido a los empleados de EMBALAJES DEL NORTE S.A. Este proyecto se lleva a cabo en colaboración con Seguros Lagun Aro, donde se realiza un análisis actuarial completo, incluyendo la predicción de los años hasta la jubilación de los trabajadores y el cálculo de las primas necesarias para diferentes escenarios económicos.

## Objetivos del Proyecto
### Objetivo 1: Predicción de Años hasta la Jubilación
Desarrollar un modelo predictivo capaz de estimar los años hasta la jubilación de cada trabajador en función de sus características laborales y demográficas. Este modelo ayudará a Seguros Lagun Aro a asignar una edad estimada de jubilación para cada trabajador, facilitando la creación de la propuesta de seguro.

### Objetivo 2: Cálculo de Primas de Seguro
Realizar los cálculos actuariales necesarios para estimar las primas de seguro de jubilación, teniendo en cuenta diferentes escenarios de inflación y rendimiento de inversión. Se evaluarán tres modalidades de pago: primas mensuales, prima única en 2025 o prima única al momento de jubilación.

### Objetivo 3: Desarrollo de una Aplicación Flask
Crear una aplicación Flask que permita a Seguros Lagun Aro consultar la información relacionada con el seguro de jubilación de cada trabajador, con la capacidad de ajustar los cálculos según diferentes variables, como tasas de interés y proyecciones económicas.

## Datos Utilizados
### Fuentes de Datos
- **Dataset 1:** Información laboral de los empleados, incluyendo fecha de nacimiento, fecha de entrada en la empresa, salario bruto, entre otros.
- **Dataset 2:** Datos históricos de edades de jubilación y características adicionales de los trabajadores.
- **Proyecciones de Inflación y Rendimiento de Inversión:** Datos económicos utilizados para ajustar los cálculos actuariales.

## Metodología
### Procesamiento de Datos
1. **Limpieza y Preprocesamiento de Datos:**
   - Limpieza de los datasets, eliminación de valores nulos y datos inconsistentes.
   - Análisis exploratorio de los datos para extraer características relevantes.
2. **Modelización:**
   - Creación de un modelo de predicción de los años hasta la jubilación, utilizando técnicas de aprendizaje automático.
   - Evaluación de la precisión del modelo y ajustes según sea necesario.
3. **Cálculos Financieros:**
   - Realización de cálculos actuariales para estimar las primas de seguro de jubilación, teniendo en cuenta los rendimientos financieros y las proyecciones de inflación.

### Modelos Utilizados
- **Modelo Predictivo para Años hasta la Jubilación:**
  - Diferentes técnicas como **stacking**,  **bagging** y **boosting**
  - Bagging: RandomForestRegressor, ExtraTreesRegressor, BaggingRegressor, DecisionTreeRegressor,
  - Boosting: AdaBoostRegressor, GradientBoostingRegressor, XGBRegressor y CatBoostRegressor
  - Otros: LinealRegresor, Lasso y Ridge
- **Cálculos Actuariales:**
  - Fórmulas actuariales para calcular las primas mensuales y primas únicas, considerando las tasas de interés y las proyecciones económicas.

## Scripts y Código
### Scripts Principales
- **Preprocesamiento de Datos:** Limpieza y transformación de los datos laborales.
- **Modelado Predictivo:** Creación y entrenamiento del modelo de predicción de años hasta la jubilación.
- **Cálculos Actuariales:** Implementación de las fórmulas actuariales para el cálculo de primas y flujos financieros.
- **Aplicación Flask:** Desarrollo de la aplicación web para la consulta de los cálculos y escenarios financieros.

## Tecnologías Utilizadas
- **Lenguajes:** Python, Flask.
- **Librerías de Python:**
  - Pandas, NumPy (procesamiento de datos).
  - Scikit-learn (modelado predictivo).
  - Matplotlib, Seaborn (visualización de datos).
- **Herramientas Adicionales:** Jupyter Notebook, herramientas de Flask para el desarrollo web.

## Resultados Esperados
1. Un modelo predictivo fiable para estimar los años hasta la jubilación de los empleados.
2. Un conjunto de propuestas económicas que cubran los distintos escenarios de pago de las primas.
3. Una aplicación Flask funcional que permita a Seguros Lagun Aro obtener resultados personalizados según diferentes variables económicas.
4. Un informe detallado sobre los riesgos financieros asociados a cada propuesta y las recomendaciones para la viabilidad del proyecto.


