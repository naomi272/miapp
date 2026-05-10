import streamlit as st
from streamlit_option_menu import option_menu
from database.db import (
    insertar_gasto,
    obtener_gastos,
    insertar_ingreso,
    obtener_ingresos,
    eliminar_gasto,
    actualizar_gasto,
    eliminar_ingreso,
    actualizar_ingreso,
    registrar_usuario,
    login_usuario,
    guardar_meta,
    obtener_meta
)

import pandas as pd
import plotly.express as px
from io import BytesIO
from datetime import datetime
from fpdf import FPDF

st.set_page_config(
    page_title="SmartExpenses",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CARGAR CSS
with open("styles/style.css") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )

# SESIÓN
if "login" not in st.session_state:
    st.session_state.login = False

# LOGIN
if not st.session_state.login:

    st.title("💰 SmartExpenses")

    tab1, tab2 = st.tabs([
        "🔐 Iniciar Sesión",
        "📝 Registrarse"
    ])

    # INICIAR SESIÓN
    with tab1:

        st.subheader("Iniciar Sesión")

        usuario = st.text_input(
            "Usuario",
            key="login_usuario"
        )

        password = st.text_input(
            "Contraseña",
            type="password",
            key="login_password"
        )

        if st.button("Ingresar"):

            usuario_db = login_usuario(
                usuario,
                password
            )

            if usuario_db:

                st.session_state.login = True
                st.session_state.usuario_id = usuario_db[0]

                st.rerun()

            else:

                st.error("❌ Usuario o contraseña incorrectos")

    # REGISTRO
    with tab2:

        st.subheader("Crear Cuenta")

        nuevo_usuario = st.text_input(
            "Nuevo usuario"
        )

        nueva_password = st.text_input(
            "Nueva contraseña",
            type="password"
        )

        if st.button("Registrarse"):

            registrado = registrar_usuario(
                nuevo_usuario,
                nueva_password
            )

            if registrado:

                st.success("✅ Usuario registrado")

            else:

                st.error("❌ El usuario ya existe")

# APP PRINCIPAL
else:

    # SIDEBAR
    with st.sidebar:

        st.title("💰 SmartExpenses")

        if st.button("Cerrar Sesión"):

            st.session_state.login = False
            st.rerun()

        selected = option_menu(
            menu_title="Menú Principal",
            options=[
                "Dashboard",
                "Gastos",
                "Ingresos",
                "Reportes",
                "Configuración"
            ],
            icons=[
                "house",
                "cash-coin",
                "wallet2",
                "bar-chart",
                "gear"
            ],
            menu_icon="cast",
            default_index=0,
        )

    # DASHBOARD
    if selected == "Dashboard":

        st.title("📊 Dashboard Financiero")

        # FILTROS
        colf1, colf2 = st.columns(2)

        with colf1:

            mes = st.selectbox(
                "📅 Seleccionar Mes",
                [
                    "Todos",
                    "01", "02", "03", "04",
                    "05", "06", "07", "08",
                    "09", "10", "11", "12"
                ]
            )

        with colf2:

            anio = st.selectbox(
            "📆 Seleccionar Año",
            [
                "Todos",
                "2024",
                "2025",
                "2026"
            ]
        )

        gastos = obtener_gastos(
            st.session_state.usuario_id
        )
        ingresos = obtener_ingresos(
            st.session_state.usuario_id
        )

        if gastos:

            df = pd.DataFrame(
                gastos,
                columns=[
                    "ID",
                    "Nombre",
                    "Categoría",
                    "Monto",
                    "Fecha",
                    "Método de Pago",
                    "Descripción"
                ]
            )
            # CONVERTIR FECHA
            df["Fecha"] = pd.to_datetime(df["Fecha"])

            # FILTRAR MES
            if mes != "Todos":

               df = df[
                   df["Fecha"].dt.strftime("%m") == mes
               ]

            # FILTRAR AÑO
            if anio != "Todos":

                df = df[
                    df["Fecha"].dt.strftime("%Y") == anio
                ]   

            total_gastos = df["Monto"].sum()

            total_ingresos = 0

            if ingresos:

                df_ingresos = pd.DataFrame(
                    ingresos,
                    columns=[
                        "ID",
                        "Nombre",
                        "Monto",
                        "Fecha",
                        "Fuente",
                        "Descripción"
                    ]
                )
                # CONVERTIR FECHA
                df_ingresos["Fecha"] = pd.to_datetime(
                    df_ingresos["Fecha"]
                )

                # FILTRAR MES
                if mes != "Todos":

                    df_ingresos = df_ingresos[
                        df_ingresos["Fecha"].dt.strftime("%m") == mes
                    ]

                # FILTRAR AÑO
                if anio != "Todos":

                    df_ingresos = df_ingresos[
                        df_ingresos["Fecha"].dt.strftime("%Y") == anio
                    ]

                total_ingresos = df_ingresos["Monto"].sum()

            balance = total_ingresos - total_gastos
            # META
            meta_data = obtener_meta(
                st.session_state.usuario_id
            )

            meta = 0

            if meta_data:

                meta = meta_data[0]

            total_registros = len(df)
            promedio = df["Monto"].mean()

            col1, col2, col3, col4, col5 = st.columns(5)

            col1.metric(
                "💸 Total Gastado",
                f"${total_gastos:,.2f}"
            )

            col2.metric(
                "💰 Total Ingresos",
                f"${total_ingresos:,.2f}"
            )

            col3.metric(
                "📈 Balance",
                f"${balance:,.2f}"
            )

            col4.metric(
                "📋 Registros",
                total_registros
            )

            col5.metric(
                "📊 Promedio",
                f"${promedio:,.2f}"
            )

            st.divider()

            # PROGRESO DE AHORRO
            if meta > 0:

                progreso = balance / meta

                if progreso < 0:
                    progreso = 0

                if progreso > 1:
                    progreso = 1

                st.subheader("🎯 Progreso de Ahorro")

                st.progress(progreso)

                porcentaje = progreso * 100

                st.write(
                    f"{porcentaje:.1f}% completado"
                )

                st.write(
                    f"Meta: ${meta:,.2f}"
                )

            # ALERTAS
            if balance < 0:

                st.error(
                    "🚨 Estás gastando más de lo que ganas"
                )

            elif total_gastos > total_ingresos * 0.8:

                st.warning(
                    "⚠️ Tus gastos superan el 80% de tus ingresos"
                )

            if meta > 0 and balance >= meta:

                st.success(
                    "🎉 Has alcanzado tu meta de ahorro"
                )

            categorias = df.groupby(
                "Categoría"
            )["Monto"].sum().reset_index()

            fig_pie = px.pie(
                categorias,
                names="Categoría",
                values="Monto",
                title="Distribución de Gastos"
            )

            st.plotly_chart(
                fig_pie,
                use_container_width=True
            )

            fig_bar = px.bar(
                categorias,
                x="Categoría",
                y="Monto",
                title="Gastos por Categoría"
            )

            st.plotly_chart(
                fig_bar,
                use_container_width=True
            )

            st.divider()

            # GASTOS POR FECHA
            gastos_fecha = df.groupby(
                df["Fecha"].dt.strftime("%Y-%m-%d")
            )["Monto"].sum().reset_index()

            fig_line = px.line(
                gastos_fecha,
                x="Fecha",
                y="Monto",
                title="Tendencia de Gastos"
            )

            st.plotly_chart(
                fig_line,
                use_container_width=True
            )

            st.subheader("📋 Últimos Gastos")

            st.dataframe(
                df,
                use_container_width=True
            )

        else:

            st.info("Aún no hay gastos registrados.")

    # GASTOS
    elif selected == "Gastos":

        st.title("💸 Gestión de Gastos")

        st.divider()

        with st.form("form_gastos"):

            nombre = st.text_input(
                "Nombre del gasto"
            )

            categoria = st.selectbox(
                "Categoría",
                [
                    "Comida",
                    "Transporte",
                    "Salud",
                    "Entretenimiento",
                    "Servicios",
                    "Educación",
                    "Otros"
                ]
            )

            monto = st.number_input(
                "Monto",
                min_value=0.0,
                format="%.2f"
            )

            fecha = st.date_input("Fecha")

            metodo_pago = st.selectbox(
                "Método de pago",
                [
                    "Efectivo",
                    "Tarjeta",
                    "Transferencia"
                ]
            )

            descripcion = st.text_area(
                "Descripción"
            )

            guardar = st.form_submit_button(
                "Guardar Gasto"
            )

            if guardar:

                insertar_gasto(
                    st.session_state.usuario_id,
                    nombre,
                    categoria,
                    monto,
                    str(fecha),
                    metodo_pago,
                    descripcion
                )

                st.success(
                    "✅ Gasto guardado correctamente"
                )

        st.divider()

        st.subheader(
            "📋 Historial de Gastos"
        )

        gastos = obtener_gastos(
            st.session_state.usuario_id
        )

        if gastos:

            df = pd.DataFrame(
                gastos,
                columns=[
                    "ID",
                    "Nombre",
                    "Categoría",
                    "Monto",
                    "Fecha",
                    "Método de Pago",
                    "Descripción"
                ]
            )

            st.dataframe(
                df,
                use_container_width=True
            )

            st.divider()

            st.subheader(
                "🗑️ Eliminar Gasto"
            )

            id_eliminar = st.number_input(
                "ID del gasto a eliminar",
                min_value=1,
                step=1
            )

            if st.button("Eliminar Gasto"):

                eliminar_gasto(id_eliminar)

                st.success(
                    "✅ Gasto eliminado"
                )

            st.divider()

            st.subheader(
                "✏️ Editar Gasto"
            )

            with st.form("editar_gasto"):

                id_editar = st.number_input(
                    "ID del gasto",
                    min_value=1,
                    step=1,
                    key="editar_gasto"
                )

                nuevo_nombre = st.text_input(
                    "Nuevo nombre"
                )

                nueva_categoria = st.selectbox(
                    "Nueva categoría",
                    [
                        "Comida",
                        "Transporte",
                        "Salud",
                        "Entretenimiento",
                        "Servicios",
                        "Educación",
                        "Otros"
                    ]
                )

                nuevo_monto = st.number_input(
                    "Nuevo monto",
                    min_value=0.0,
                    format="%.2f",
                    key="nuevo_monto_gasto"
                )

                nueva_fecha = st.date_input(
                    "Nueva fecha"
                )

                nuevo_metodo = st.selectbox(
                    "Nuevo método de pago",
                    [
                        "Efectivo",
                        "Tarjeta",
                        "Transferencia"
                    ]
                )

                nueva_descripcion = st.text_area(
                    "Nueva descripción"
                )

                actualizar = st.form_submit_button(
                    "Actualizar Gasto"
                )

                if actualizar:

                    actualizar_gasto(
                        id_editar,
                        nuevo_nombre,
                        nueva_categoria,
                        nuevo_monto,
                        str(nueva_fecha),
                        nuevo_metodo,
                        nueva_descripcion
                    )

                    st.success(
                        "✅ Gasto actualizado"
                    )

        else:

            st.info(
                "No hay gastos registrados."
            )

    # INGRESOS
    elif selected == "Ingresos":

        st.title("💰 Gestión de Ingresos")

        st.divider()

        with st.form("form_ingresos"):

            nombre = st.text_input(
                "Nombre del ingreso"
            )

            monto = st.number_input(
                "Monto del ingreso",
                min_value=0.0,
                format="%.2f",
                key="monto_ingreso"
            )

            fecha = st.date_input(
                "Fecha del ingreso"
            )

            fuente = st.selectbox(
                "Fuente",
                [
                    "Sueldo",
                    "Ventas",
                    "Freelance",
                    "Negocio",
                    "Inversiones",
                    "Otros"
                ]
            )

            descripcion = st.text_area(
                "Descripción"
            )

            guardar = st.form_submit_button(
                "Guardar Ingreso"
            )

            if guardar:

                insertar_ingreso(
                    st.session_state.usuario_id,
                    nombre,
                    monto,
                    str(fecha),
                    fuente,
                    descripcion
                )

                st.success(
                    "✅ Ingreso guardado correctamente"
                )

        st.divider()

        st.subheader(
            "📋 Historial de Ingresos"
        )

        ingresos = obtener_ingresos(
            st.session_state.usuario_id
        )

        if ingresos:

            df = pd.DataFrame(
                ingresos,
                columns=[
                    "ID",
                    "Nombre",
                    "Monto",
                    "Fecha",
                    "Fuente",
                    "Descripción"
                ]
            )

            st.dataframe(
                df,
                use_container_width=True
            )

        else:

            st.info(
                "No hay ingresos registrados."
            )

    # REPORTES
    elif selected == "Reportes":

        st.title("📊 Reportes Financieros")

        gastos = obtener_gastos(
            st.session_state.usuario_id
        )
        ingresos = obtener_ingresos(
            st.session_state.usuario_id
        )

        st.subheader(
            "💸 Reporte de Gastos"
        )

        if gastos:

            df_gastos = pd.DataFrame(
                gastos,
                columns=[
                    "ID",
                    "Nombre",
                    "Categoría",
                    "Monto",
                    "Fecha",
                    "Método de Pago",
                    "Descripción"
                ]
            )

            st.dataframe(
                df_gastos,
                use_container_width=True
            )

            excel_gastos = BytesIO()

            with pd.ExcelWriter(
                excel_gastos,
                engine="openpyxl"
            ) as writer:

                df_gastos.to_excel(
                    writer,
                    index=False,
                    sheet_name="Gastos"
                )

            st.download_button(
                label="⬇️ Descargar Gastos Excel",
                data=excel_gastos.getvalue(),
                file_name="reporte_gastos.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

            pdf = FPDF()

            pdf.add_page()

            pdf.set_font(
                "Arial",
                size=12
            )

            pdf.cell(
                200,
                10,
                txt="Reporte de Gastos",
                ln=True,
                align="C"
            )

            pdf.ln(10)

            for index, row in df_gastos.iterrows():

                texto = (
                    f"{row['Nombre']} | "
                    f"{row['Categoría']} | "
                    f"${row['Monto']}"
                )

                pdf.cell(
                    200,
                    10,
                    txt=texto,
                    ln=True
                )

            pdf_output = pdf.output(
                dest="S"
            ).encode("latin-1")

            st.download_button(
                label="⬇️ Descargar Gastos PDF",
                data=pdf_output,
                file_name="reporte_gastos.pdf",
                mime="application/pdf"
            )

        else:

            st.info(
                "No hay gastos registrados."
            )

    # CONFIGURACIÓN
    elif selected == "Configuración":

        st.title("⚙️ Configuración")

        st.subheader("🎯 Meta de Ahorro")

        meta_actual = obtener_meta(
            st.session_state.usuario_id
        )

        valor_meta = 0

        if meta_actual:

            valor_meta = meta_actual[0]

        meta = st.number_input(
            "Ingresa tu meta de ahorro",
            min_value=0.0,
            value=float(valor_meta),
            format="%.2f"
        )

        if st.button("Guardar Meta"):

            guardar_meta(
                st.session_state.usuario_id,
                meta
            )

            st.success("✅ Meta guardada")