import streamlit as st
import pandas as pd
import time
from collections import Counter

# ==========================================
# 1. CONFIGURACIÓN DE LA PÁGINA
# ==========================================
st.set_page_config(page_title="Cyber & AI - Baseline Assessment", page_icon="🛡️", layout="wide")

# ==========================================
# 2. BASE DE DATOS EN MEMORIA (Caché compartida)
# ==========================================
@st.cache_resource
def get_db():
    # Estructura para almacenar todas las respuestas
    return {
        "palabras_clave": [],
        "skills_cyber": [],
        "skills_python": [],
        "skills_ml": [],
        "skills_llm": [],
        "q_framework": {"ISO/IEC 27001": 0, "OWASP Top 10": 0, "MITRE ATT&CK": 0, "NIST CSF": 0},
        "q_anomaly": {"Supervisado (Clasificación)": 0, "No Supervisado (Anomalías)": 0, "Por Refuerzo": 0, "Regresión Lineal": 0},
        "q_adversarial": {"IA adivinando contraseñas": 0, "Engañar, evadir o envenenar modelos": 0, "AV vs Malware aislado": 0, "Reemplazar humanos del SOC": 0},
        "q_llm_vuln": {"SQL Injection Clásico": 0, "Prompt Injection": 0, "Cross-Site Scripting (XSS)": 0, "Buffer Overflow en el modelo": 0},
        "q_impacto": {"Detección Phishing/Spam": 0, "UEBA (Comportamiento de Usuarios)": 0, "Automatización en SOC": 0, "Exploits ofensivos automatizados": 0},
        "retos_abiertos": []
    }

db = get_db()

# ==========================================
# 3. BARRA LATERAL (NAVEGACIÓN)
# ==========================================
st.sidebar.title("Navegación")
modo = st.sidebar.radio("Selecciona tu vista:", ["👨‍🎓 Modo Estudiante (Votar)", "👨‍🏫 Modo Profesor (Resultados en Vivo)"])
st.sidebar.markdown("---")
st.sidebar.info("App interactiva para la 1ra clase del Diplomado en IA y Ciberseguridad.")

# ==========================================
# VISTA DEL ESTUDIANTE
# ==========================================
if modo == "👨‍🎓 Modo Estudiante (Votar)":
    st.title("🛡️🤖 Diplomado: IA aplicada a Ciberseguridad")
    st.markdown("¡Bienvenido! Por favor, responde con honestidad para ajustar el nivel de nuestras clases. Todo es **100% anónimo**.")

    with st.form("assessment_form"):
        # Bloque 1
        st.header("Bloque 1: Rompehielos y Autoevaluación")
        palabra = st.text_input("1. ¿Qué es lo primero que te viene a la mente cuando escuchas 'IA aplicada a la Ciberseguridad'? (1 o 2 palabras)")
        
        st.markdown("**2. Evalúa tu nivel de experiencia (1 = Básico/Nulo, 5 = Experto/Diario):**")
        cyber = st.slider("Fundamentos de Ciberseguridad (Redes, SOC, Arquitectura)", 1, 5, 3)
        python = st.slider("Programación en Python", 1, 5, 3)
        ml = st.slider("Conceptos de Machine Learning / Deep Learning", 1, 5, 3)
        llm = st.slider("Uso e ingeniería de Prompts en LLMs (ChatGPT, Claude, etc.)", 1, 5, 3)

        st.divider()

        # Bloque 2 y 3
        st.header("Bloques 2 y 3: Conocimientos Core")
        framework = st.radio("3. ¿Cuál es el framework estándar actual para mapear y entender tácticas de atacantes?", 
                             options=list(db["q_framework"].keys()), index=None)
        
        anomaly = st.radio("4. Sin datos etiquetados de ataques, ¿qué enfoque de Machine Learning usarías para detectar tráfico anómalo (Zero-Days)?", 
                           options=list(db["q_anomaly"].keys()), index=None)

        st.divider()

        # Bloque 4
        st.header("Bloque 4: Amenazas Emergentes")
        adversarial = st.radio("5. ¿Qué es el 'Adversarial Machine Learning' en ciberseguridad?", 
                               options=list(db["q_adversarial"].keys()), index=None)
        
        llm_vuln = st.radio("6. Según OWASP, ¿cuál es una de las vulnerabilidades más críticas al integrar LLMs corporativos?", 
                            options=list(db["q_llm_vuln"].keys()), index=None)

        st.divider()

        # Bloque 5
        st.header("Bloque 5: Visión Estratégica")
        impacto = st.radio("7. ¿En qué caso de uso crees que la IA tiene el MAYOR impacto o madurez en la actualidad?", 
                           options=list(db["q_impacto"].keys()), index=None)
        
        reto = st.text_area("8. ¿Cuál es el principal desafío de ciberseguridad en tu trabajo que esperas resolver usando IA? (Opcional)")

        # Botón de envío
        submitted = st.form_submit_button("Enviar mis respuestas 🚀")

        if submitted:
            # Validación simple para que no envíen radios vacíos
            if None in [framework, anomaly, adversarial, llm_vuln, impacto]:
                st.error("⚠️ Por favor, responde todas las preguntas de opción múltiple antes de enviar.")
            else:
                # Guardar datos en memoria
                if palabra.strip(): db["palabras_clave"].append(palabra.strip().title())
                
                db["skills_cyber"].append(cyber)
                db["skills_python"].append(python)
                db["skills_ml"].append(ml)
                db["skills_llm"].append(llm)
                
                db["q_framework"][framework] += 1
                db["q_anomaly"][anomaly] += 1
                db["q_adversarial"][adversarial] += 1
                db["q_llm_vuln"][llm_vuln] += 1
                db["q_impacto"][impacto] += 1
                
                if reto.strip(): db["retos_abiertos"].append(reto.strip())
                
                st.success("✅ ¡Respuestas enviadas correctamente! Mira la pantalla del profesor.")

# ==========================================
# VISTA DEL PROFESOR / DASHBOARD
# ==========================================
elif modo == "👨‍🏫 Modo Profesor (Resultados en Vivo)":
    st.title("📊 Dashboard de Resultados (En Vivo)")
    
    total_respuestas = len(db["skills_cyber"])
    
    col_metric, col_btn = st.columns([4, 1])
    col_metric.metric(label="👥 Estudiantes que han completado el assessment", value=total_respuestas)
    if col_btn.button("🔄 Refrescar Manualmente"):
        st.rerun()

    if total_respuestas > 0:
        st.divider()
        
        # --- SECCIÓN 1: PALABRAS CLAVE Y SKILLS ---
        st.header("1. El Perfil de la Clase")
        c1, c2 = st.columns(2)
        
        with c1:
            st.subheader("💡 ¿Qué es la IA en Ciberseguridad?")
            if db["palabras_clave"]:
                # Contar frecuencias y mostrar como tabla limpia
                conteo_palabras = Counter(db["palabras_clave"])
                df_palabras = pd.DataFrame(conteo_palabras.items(), columns=["Concepto", "Menciones"]).sort_values(by="Menciones", ascending=False)
                st.dataframe(df_palabras, use_container_width=True, hide_index=True)
            else:
                st.write("Aún no hay palabras registradas.")

        with c2:
            st.subheader("📈 Nivel Promedio de Habilidades")
            avg_skills = pd.DataFrame({
                "Habilidad": ["Ciberseguridad", "Python", "Machine Learning", "LLMs (Prompts)"],
                "Nivel Promedio (1-5)": [
                    sum(db["skills_cyber"])/total_respuestas,
                    sum(db["skills_python"])/total_respuestas,
                    sum(db["skills_ml"])/total_respuestas,
                    sum(db["skills_llm"])/total_respuestas
                ]
            })
            st.bar_chart(avg_skills.set_index("Habilidad"), color="#1dd1a1")

        st.divider()

        # --- SECCIÓN 2: PREGUNTAS TÉCNICAS (4 columnas para pantallas anchas) ---
        st.header("2. Conocimientos Técnicos Core")
        col_t1, col_t2 = st.columns(2)
        
        with col_t1:
            st.markdown("**Framework de Atacantes (Ciberseguridad)**")
            st.bar_chart(pd.DataFrame(list(db["q_framework"].items()), columns=["Opción", "Votos"]).set_index("Opción"), color="#ff6b6b")

        with col_t2:
            st.markdown("**Detección de Anomalías / Zero-Days (IA)**")
            st.bar_chart(pd.DataFrame(list(db["q_anomaly"].items()), columns=["Opción", "Votos"]).set_index("Opción"), color="#54a0ff")

        st.divider()

        st.header("3. Amenazas Emergentes")
        col_a1, col_a2 = st.columns(2)

        with col_a1:
            st.markdown("**Adversarial Machine Learning**")
            st.bar_chart(pd.DataFrame(list(db["q_adversarial"].items()), columns=["Opción", "Votos"]).set_index("Opción"), color="#ff9f43")

        with col_a2:
            st.markdown("**Vulnerabilidades Críticas en LLMs (OWASP)**")
            st.bar_chart(pd.DataFrame(list(db["q_llm_vuln"].items()), columns=["Opción", "Votos"]).set_index("Opción"), color="#ee5253")

        st.divider()

        # --- SECCIÓN 3: ESTRATEGIA Y RETOS ---
        st.header("4. Visión Estratégica y Expectativas")
        c_imp, c_ret = st.columns(2)

        with c_imp:
            st.markdown("**Caso de Uso con Mayor Impacto Actual**")
            st.bar_chart(pd.DataFrame(list(db["q_impacto"].items()), columns=["Opción", "Votos"]).set_index("Opción"), color="#9b59b6")

        with c_ret:
            st.markdown("**Desafíos que los estudiantes quieren resolver:**")
            if db["retos_abiertos"]:
                for reto in db["retos_abiertos"]:
                    st.info(f'"{reto}"')
            else:
                st.write("Sin respuestas aún.")
            
        # Botón de reset (Oculto al final)
        st.divider()
        if st.button("🗑️ Limpiar todos los datos (Reiniciar clase)"):
            db.clear()
            db.update(get_db.__wrapped__()) # Reinicia la caché al estado original
            st.rerun()
            
    else:
        st.info("⏳ Esperando a que los estudiantes comiencen a enviar sus respuestas...")
        
    # Auto-refresco de la pantalla del profesor cada 3 segundos
    time.sleep(3)
    st.rerun()
