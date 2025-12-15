import pandas as pd
import random
from dash import Dash, dcc, html, Input, Output
import plotly.express as px

# === Daten laden ===
df_sentences = pd.read_excel("nur_Semantik_FINAL.xlsx")
df_freq = pd.read_excel("Tabelle 1;_Semantik.xlsx")

# Sätze nach Kategorie sammeln (inklusive Konditional)
sentences_by_cat = (
    df_sentences
    .groupby("Semantische Klasse")["Satz"]
    .apply(list)
    .to_dict()
)

# === Regenbogenfarben definieren ===
rainbow_colors = [
    "#FF0000", "#FF7F00", "#FFFF00", "#7FFF00", "#00FF00",
    "#00FF7F", "#00FFFF", "#007FFF", "#0000FF", "#7F00FF",
    "#FF00FF", "#FF007F", "#B30059", "#FF3366", "#FF6666"
]

# === Grunddiagramm erstellen ===
fig = px.bar(
    df_freq,
    x="Semantik",
    y="Abs",
    title="Häufigkeit semantischer Kategorien",
    color="Semantik",
    color_discrete_sequence=rainbow_colors
)

# Hover wird dynamisch ersetzt
fig.update_traces(hoverinfo="none")

# === Dash App ===
app = Dash(__name__)

app.layout = html.Div([
    dcc.Graph(id="bar-chart", figure=fig),
    html.Div(
        id="hover-text",
        style={
            "marginTop": "20px",
            "fontSize": "16px",
            "fontStyle": "italic",
            "border": "1px solid #ccc",
            "padding": "10px"
        }
    )
])


@app.callback(
    Output("hover-text", "children"),
    Input("bar-chart", "hoverData")
)
def update_hover(hoverData):
    if hoverData is None:
        return "Fahre mit der Maus über einen Balken, um einen Beispielsatz zu sehen."

    category = hoverData["points"][0]["x"]
    sents = sentences_by_cat.get(category, ["Kein Satz vorhanden"])
    beispiel = random.choice(sents)

    # Optional: zeige auch Konnektor, Semantik, Beleg, Anzahl
    # Du kannst hier weitere Spalten aus df_sentences ergänzen, z.B. "Konnektor"
    row = df_sentences[df_sentences["Satz"] == beispiel].iloc[0]
    konnektor = row.get("Konnektor", "")
    semantik = row.get("Semantische Klasse", "")
    anzahl = row.get("Abs", "")  # falls vorhanden
    beleg = beispiel

    return f"Konnektor: {konnektor} | Semantik: {semantik} | Beleg: {beleg} | Anzahl: {anzahl}"


if __name__ == "__main__":
    app.run(debug=True)
    