import streamlit as st
import pandas as pd
import math

def game_score_distribution(pA):
    """
    pA: probabilidad de que el jugador A gane un punto
    Devuelve las probabilidades de resultados finales del game,
    indicando ganador y marcador.
    """
    pB = 1 - pA
    scores = {}

    # --- A gana sin deuce ---
    scores["A gana 40-0"] = pA**4
    scores["A gana 40-15"] = math.comb(4,1) * (pA**4) * (pB**1)
    scores["A gana 40-30"] = math.comb(5,2) * (pA**4) * (pB**2)

    # --- B gana sin deuce ---
    scores["B gana 0-40"] = pB**4
    scores["B gana 15-40"] = math.comb(4,1) * (pB**4) * (pA**1)
    scores["B gana 30-40"] = math.comb(5,2) * (pB**4) * (pA**2)

    # --- Casos desde deuce (40-40) ---
    p_deuce = math.comb(6,3) * (pA**3) * (pB**3)

    # Geométrica para salir de deuce
    denom = 1 - 2*pA*pB

    scores["A gana Adv-40"] = p_deuce * (pA**2) / denom
    scores["B gana 40-Adv"] = p_deuce * (pB**2) / denom

    return scores

# --- Streamlit UI ---
st.title("🎾 Probabilidades de resultado en un Game de Tenis")

st.sidebar.header("Ingresar Odds")
odd_A = st.sidebar.number_input("Odd Jugador A", value=1.5, min_value=1.01, step=0.01)
odd_B = st.sidebar.number_input("Odd Jugador B", value=2.5, min_value=1.01, step=0.01)

# Calcular probabilidad implícita de ganar un punto
pA = 1/odd_A / (1/odd_A + 1/odd_B)
distribution = game_score_distribution(pA)

# Pasar a DataFrame
df = pd.DataFrame(list(distribution.items()), columns=["Resultado", "Probabilidad"])
df["Probabilidad %"] = df["Probabilidad"] * 100
df["Odd"] = df["Probabilidad"].apply(lambda x: (1/x) if x > 0 else None)

# Ordenar por probabilidad descendente
df = df.sort_values("Probabilidad %", ascending=False).reset_index(drop=True)

st.subheader("Resultados posibles del game")
st.dataframe(df.style.background_gradient(subset=["Probabilidad %"], cmap="YlGnBu"))

# Resumen por jugador
pA_win = df[df["Resultado"].str.startswith("A")]["Probabilidad"].sum() * 100
pB_win = df[df["Resultado"].str.startswith("B")]["Probabilidad"].sum() * 100

st.markdown(f"""
### 📊 Resumen
- **Jugador A gana el game**: {pA_win:.1f}%
- **Jugador B gana el game**: {pB_win:.1f}%
""")
