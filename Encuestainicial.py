import streamlit as st
import pandas as pd
import time

# 1. Configuración de la página
st.set_page_config(page_title="Cyber & AI - Baseline Assessment", page_icon="🛡️", layout="centered")

# 2. Base de datos en memoria (Compartida entre todas las sesiones/estudiantes)
@st.cache_resource
def get_db():
    return {
        "skills_cyber": [],
        "skills_python": [],
        "skills_ai": [],
        "framework": {"ISO 27001": 0, "OWASP Top 10": 0, "MITRE ATT&CK": 0, "NIST CSF": 0},
        "adversarial": {"Hackear contraseñas": 0, "Engañar/Evadir modelos de IA": 0, "AV vs Malware": 0, "Reemplazar humanos SOC": 0}
    }

db = get_db()

# 3. Navegación Lateral
st.sidebar.title("Navegación")
modo = st.sidebar.radio("Selecciona tu vista:", ["👨‍🎓 Modo Estudiante (Votar)", "👨‍🏫 Modo Profesor (Resultados en Vivo)"])

# ==========================================
# VISTA DEL ESTUDIANTE
# ==========================================
if modo == "👨‍🎓 Modo Estudiante (Votar)":
    st.title("🛡️🤖 Diplomado: IA aplicada a Ciberseguridad")
    st.markdown("¡Bienvenido a la primera clase! Por favor, responde con honestidad (es **100% anónimo**).")

    with st.form("assessment_form"):
        st.subheader("1. Autoevaluación de Habilidades (1=Novato, 5=Experto)")
        cyber = st.slider("Fundamentos de Ciberseguridad (Redes, SOC, Arquitectura)", 1, 5, 3)
        python = st.slider("Programación en Python", 1, 5, 3)
        ai = st.slider("Machine Learning / Deep Learning / LLMs", 1, 5, 3)

        st.subheader("2. Conocimiento Core: Ciberseguridad")
        framework_resp = st.radio("¿Cuál es el framework estándar actual para mapear tácticas de atacantes?", 
                                  options=list(db["framework"].keys()))

        st.subheader("3. Conocimiento Core: Inteligencia Artificial")
        adv_resp = st.radio("¿Qué es el 'Adversarial Machine Learning'?", 
                            options=list(db["adversarial"].keys()))

        submitted = st.form_submit_button("Enviar mis respuestas 🚀")

        if submitted:
            # Guardar en la "base de datos" en vivo
            db["skills_cyber"].append(cyber)
            db["skills_python"].append(python)
            db["skills_ai"].append(ai)
            db["framework"][framework_resp] += 1
            db["adversarial"][adv_resp] += 1
            st.success("¡Respuestas enviadas correctamente! Mira la pantalla del profesor.")

# ==========================================
# VISTA DEL PROFESOR / DASHBOARD
# ==========================================
elif modo == "👨‍🏫 Modo Profesor (Resultados en Vivo)":
    st.title("📊 Dashboard de Resultados en Tiempo Real")
    
    # Botón para refrescar la pantalla manualmente si es necesario
    if st.button("🔄 Actualizar Datos"):
        st.rerun()

    # Mostrar métricas generales
    total_respuestas = len(db["skills_cyber"])
    st.metric(label="Total de Estudiantes que han respondido", value=total_respuestas)

    if total_respuestas > 0:
        st.divider()
        
        # Gráfico 1: Habilidades Promedio
        st.subheader("1. Nivel Promedio de la Clase")
        avg_skills = pd.DataFrame({
            "Habilidad": ["Ciberseguridad", "Python", "IA / ML"],
            "Promedio": [
                sum(db["skills_cyber"])/total_respuestas,
                sum(db["skills_python"])/total_respuestas,
                sum(db["skills_ai"])/total_respuestas
            ]
        })
        st.bar_chart(avg_skills.set_index("Habilidad"), color="#00ff00")

        st.divider()

        # Gráfico 2 y 3 en columnas
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Framework de Tácticas")
            df_framework = pd.DataFrame(list(db["framework"].items()), columns=["Opción", "Votos"])
            st.bar_chart(df_framework.set_index("Opción"), color="#ff4b4b")

        with col2:
            st.subheader("Adversarial ML")
            df_adv = pd.DataFrame(list(db["adversarial"].items()), columns=["Opción", "Votos"])
            st.bar_chart(df_adv.set_index("Opción"), color="#0099ff")
            
        # Botón de reset (Solo para el profesor)
        st.divider()
        if st.button("🗑️ Reiniciar Datos (Peligro)"):
            db["skills_cyber"].clear()
            db["skills_python"].clear()
            db["skills_ai"].clear()
            for k in db["framework"]: db["framework"][k] = 0
            for k in db["adversarial"]: db["adversarial"][k] = 0
            st.rerun()
    else:
        st.info("Esperando a que los estudiantes envíen sus respuestas...")
        
    # Auto-refresco de la pantalla del profesor cada 3 segundos
    time.sleep(3)
    st.rerun()