# 💰 SmartExpenses

Aplicación web financiera desarrollada con Python, Streamlit y SQLite para la gestión inteligente de gastos e ingresos personales.

---

# 📌 Descripción

SmartExpenses es una aplicación enfocada en la administración financiera personal, permitiendo a cada usuario:

* Registrar gastos e ingresos
* Visualizar estadísticas financieras
* Administrar metas de ahorro
* Generar reportes en Excel y PDF
* Analizar tendencias mensuales
* Gestionar información de forma segura mediante autenticación de usuarios

La aplicación fue desarrollada utilizando Streamlit como framework principal para la interfaz web y SQLite como sistema de base de datos.

---

# 🚀 Características Principales

## 🔐 Sistema de autenticación

* Registro de usuarios
* Inicio de sesión
* Contraseñas protegidas mediante hash
* Sesiones por usuario
* Datos separados por cuenta

---

## 💸 Gestión de gastos

* Crear gastos
* Editar gastos
* Eliminar gastos
* Categorías personalizadas
* Métodos de pago
* Historial completo

---

## 💰 Gestión de ingresos

* Registro de ingresos
* Edición y eliminación
* Clasificación por fuente
* Historial financiero

---

## 📊 Dashboard inteligente

* Balance financiero automático
* Total de ingresos
* Total de gastos
* Promedio de gastos
* Métricas dinámicas
* Gráficas interactivas con Plotly
* Tendencia de gastos
* Filtros mensuales y anuales

---

## 🎯 Metas de ahorro

* Configuración de metas
* Barra de progreso
* Porcentaje completado
* Alertas automáticas

---

## 📄 Exportación de reportes

* Exportación a Excel
* Exportación a PDF
* Reportes financieros descargables

---

# 🛠️ Tecnologías Utilizadas

| Tecnología | Uso                   |
| ---------- | --------------------- |
| Python     | Lógica principal      |
| Streamlit  | Interfaz web          |
| SQLite     | Base de datos         |
| Pandas     | Manipulación de datos |
| Plotly     | Visualización gráfica |
| FPDF       | Generación de PDFs    |
| OpenPyXL   | Exportación Excel     |

---

# 📂 Estructura del Proyecto

```bash
SmartExpenses/
│
├── app.py
├── requirements.txt
├── database/
│   └── db.py
├── styles/
│   └── style.css
└── README.md
```

---

# ⚙️ Instalación

## 1️⃣ Clonar repositorio

```bash
git clone https://github.com/TU-USUARIO/SmartExpenses.git
```

---

## 2️⃣ Entrar al proyecto

```bash
cd SmartExpenses
```

---

## 3️⃣ Crear entorno virtual

### Linux / Mac

```bash
python3 -m venv venv
source venv/bin/activate
```

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

---

## 4️⃣ Instalar dependencias

```bash
pip install -r requirements.txt
```

---

# ▶️ Ejecutar aplicación

```bash
streamlit run app.py
```

---

# 📦 Dependencias Principales

```txt
streamlit
pandas
plotly
fpdf
openpyxl
streamlit-option-menu
```

---

# 🔒 Seguridad

La aplicación implementa:

* Hash de contraseñas
* Separación de información por usuario
* Manejo de sesiones
* Validación básica de autenticación

---

# 📸 Capturas

## Dashboard

*Agregar imagen aquí*

---

## Gestión de gastos

*Agregar imagen aquí*

---

## Reportes

*Agregar imagen aquí*

---

# 🌐 Despliegue

La aplicación puede desplegarse fácilmente mediante:

* Streamlit Community Cloud
* GitHub Codespaces
* Render
* Railway

---

# 📈 Futuras Mejoras

* Recuperación de contraseña
* Base de datos PostgreSQL
* API REST
* Modo oscuro
* Notificaciones automáticas
* IA para análisis financiero
* OCR para tickets
* Multiusuario avanzado

---

# 👨‍💻 Autor

Desarrollado por Kevin Tolentino.

---

# ⭐ Contribuciones

Las contribuciones, mejoras y sugerencias son bienvenidas.

---

# 📄 Licencia

Proyecto desarrollado con fines educativos y de portafolio.
