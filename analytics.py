import plotly.graph_objects as go

def generate_radar_chart(scores):
    categories = ["Confidence", "Grammar", "Technical", "Communication"]

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=[
            scores["confidence_score"],
            scores["grammar_score"],
            scores["technical_score"],
            scores["communication_score"]
        ],
        theta=categories,
        fill='toself'
    ))

    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 10])),
        showlegend=False
    )

    return fig
