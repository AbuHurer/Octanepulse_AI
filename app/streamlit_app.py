import os
import base64
import requests
import streamlit as st

# ==========================================================
# OCTANEPULSE AI | UFC-INSPIRED FIGHT PREDICTOR
# ==========================================================

st.set_page_config(
    page_title="OctanePulse AI | UFC Fight Predictor",
    page_icon="🥊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Resolve local images relative to this app.py file.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, "images")


def image_path(filename):
    """Return the absolute path for an image stored in ./images."""
    return os.path.join(IMAGE_DIR, filename)


def image_to_data_uri(filename):
    """Convert a local image to a browser-readable data URI for CSS."""
    path = image_path(filename)
    if not os.path.isfile(path):
        return None

    extension = os.path.splitext(filename)[1].lower()
    mime = {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".webp": "image/webp",
    }.get(extension, "application/octet-stream")

    with open(path, "rb") as image_file:
        encoded = base64.b64encode(image_file.read()).decode("utf-8")

    return f"data:{mime};base64,{encoded}"


# Optional local image files:
# images/ufc-arena.jpg
# images/red-corner.png
# images/blue-corner.png
# images/octagon.png
# images/fight-night.jpg
# images/logo.png

arena_uri = image_to_data_uri("ufc-arena.jpg")
fight_night_uri = image_to_data_uri("fight-night.jpg")

# ==========================================================
# UFC-INSPIRED THEME
# ==========================================================

background_layers = (
    f'linear-gradient(rgba(5, 5, 5, .91), rgba(5, 5, 5, .97)), '
    f'url("{arena_uri}")'
    if arena_uri
    else "radial-gradient(circle at 50% 0%, rgba(130, 0, 0, .16), transparent 42%), #080808"
)

st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@400;500;600;700;800;900&family=Inter:wght@400;500;600;700;800&display=swap');

    :root {{
        --ufc-red: #e50914;
        --corner-red: #ff303b;
        --corner-blue: #3294ff;
        --bg: #080808;
        --panel: #141414;
        --line: #2b2b2b;
        --muted: #8b8b8b;
    }}

    html, body, [data-testid="stAppViewContainer"] {{
        background: {background_layers} !important;
        background-size: cover !important;
        background-position: center top !important;
        background-attachment: fixed !important;
        color: #f5f5f5 !important;
        font-family: 'Inter', sans-serif;
    }}

    [data-testid="stHeader"] {{
        background: transparent;
    }}

    .block-container {{
        max-width: 1420px;
        padding-top: 1.35rem;
        padding-bottom: 3rem;
    }}

    [data-testid="stSidebar"] {{
        background: #101010 !important;
        border-right: 1px solid #292929;
    }}

    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {{
        font-family: 'Barlow Condensed', sans-serif;
        text-transform: uppercase;
        font-weight: 900;
        letter-spacing: 1px;
    }}

    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] label {{
        color: #a1a1a1;
        font-size: 12px;
    }}

    .brand-header {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 20px;
        padding: 14px 0 25px;
        border-bottom: 1px solid #292929;
        margin-bottom: 30px;
    }}

    .brand-logo {{
        font-family: 'Barlow Condensed', sans-serif;
        font-size: clamp(34px, 5vw, 58px);
        font-weight: 900;
        letter-spacing: -1.8px;
        line-height: .95;
        color: #fff;
    }}

    .brand-logo span {{
        color: var(--ufc-red);
    }}

    .brand-subtitle {{
        color: #777;
        font-size: 10px;
        font-weight: 800;
        letter-spacing: 2.4px;
        margin-top: 9px;
    }}

    .fight-badge {{
        padding: 9px 13px;
        border: 1px solid rgba(229, 9, 20, .5);
        background: rgba(229, 9, 20, .10);
        border-radius: 4px;
        color: #ff3842;
        font-size: 10px;
        font-weight: 900;
        letter-spacing: 1.5px;
        white-space: nowrap;
    }}

    .section-heading {{
        font-family: 'Barlow Condensed', sans-serif;
        font-size: 29px;
        line-height: 1;
        font-weight: 900;
        text-transform: uppercase;
        letter-spacing: .5px;
        margin: 7px 0 8px;
        color: #fff;
    }}

    .section-description {{
        color: #858585;
        font-size: 12px;
        margin-bottom: 20px;
    }}

    .corner-card {{
        border-radius: 7px;
        min-height: 152px;
        padding: 22px;
        overflow: hidden;
        position: relative;
        margin-bottom: 10px;
    }}

    .red-card {{
        background: linear-gradient(120deg, rgba(229, 9, 20, .24), #141414 75%);
        border: 1px solid rgba(229, 9, 20, .55);
    }}

    .blue-card {{
        background: linear-gradient(120deg, rgba(0, 105, 255, .24), #141414 75%);
        border: 1px solid rgba(0, 105, 255, .55);
    }}

    .corner-label {{
        font-size: 10px;
        font-weight: 900;
        letter-spacing: 2px;
        color: #a0a0a0;
        text-transform: uppercase;
    }}

    .fighter-name {{
        font-family: 'Barlow Condensed', sans-serif;
        font-size: 36px;
        font-weight: 900;
        text-transform: uppercase;
        line-height: 1;
        margin-top: 14px;
    }}

    .red-text {{ color: var(--corner-red); }}
    .blue-text {{ color: var(--corner-blue); }}

    .fighter-description {{
        color: #858585;
        font-size: 11px;
        margin-top: 9px;
    }}

    .vs-wrap {{
        min-height: 155px;
        display: flex;
        align-items: center;
        justify-content: center;
    }}

    .vs-badge {{
        font-family: 'Barlow Condensed', sans-serif;
        font-size: 43px;
        font-weight: 900;
        font-style: italic;
        color: white;
        text-shadow: 0 0 22px rgba(229, 9, 20, .45);
    }}

    .fighter-image {{
        border-radius: 6px;
        border: 1px solid #2a2a2a;
        overflow: hidden;
        margin-bottom: 10px;
    }}

    [data-testid="stNumberInput"] label {{
        color: #a5a5a5 !important;
        font-size: 11px !important;
        font-weight: 700 !important;
    }}

    [data-testid="stNumberInput"] input {{
        background: #151515 !important;
        color: #f5f5f5 !important;
        border: 1px solid #303030 !important;
        border-radius: 5px !important;
    }}

    [data-testid="stNumberInput"] input:focus {{
        border-color: var(--ufc-red) !important;
        box-shadow: 0 0 0 1px var(--ufc-red) !important;
    }}

    [data-testid="stNumberInput"] button {{
        background: #222 !important;
        color: #fff !important;
        border: none !important;
    }}

    .stButton > button {{
        background: var(--ufc-red) !important;
        color: white !important;
        border: 1px solid var(--ufc-red) !important;
        border-radius: 5px !important;
        padding: 13px 18px !important;
        font-family: 'Barlow Condensed', sans-serif !important;
        font-size: 19px !important;
        font-weight: 900 !important;
        letter-spacing: 1px !important;
        text-transform: uppercase !important;
        transition: all .2s ease;
    }}

    .stButton > button:hover {{
        background: #b80710 !important;
        border-color: #b80710 !important;
        box-shadow: 0 0 20px rgba(229, 9, 20, .22);
        transform: translateY(-1px);
    }}

    [data-testid="stMetric"] {{
        background: #141414;
        border: 1px solid #292929;
        border-radius: 6px;
        padding: 16px;
    }}

    [data-testid="stMetricLabel"] {{
        color: #999 !important;
        font-size: 11px !important;
    }}

    [data-testid="stMetricValue"] {{
        color: #fff !important;
        font-family: 'Barlow Condensed', sans-serif;
        font-size: 28px !important;
        font-weight: 800;
    }}

    [data-testid="stProgressBar"] > div {{
        background: #292929 !important;
        border-radius: 20px;
    }}

    [data-testid="stProgressBar"] > div > div {{
        background: var(--ufc-red) !important;
        border-radius: 20px;
    }}

    .result-panel {{
        background: linear-gradient(125deg, rgba(229, 9, 20, .17), #111 68%);
        border: 1px solid #393939;
        border-radius: 8px;
        padding: 26px;
        margin-top: 22px;
    }}

    .result-label {{
        color: #aaa;
        font-size: 10px;
        font-weight: 900;
        letter-spacing: 3px;
    }}

    .result-winner {{
        font-family: 'Barlow Condensed', sans-serif;
        font-size: clamp(32px, 5vw, 52px);
        font-weight: 900;
        text-transform: uppercase;
        line-height: 1.1;
        margin-top: 10px;
    }}

    .result-confidence {{
        display: inline-block;
        margin-top: 13px;
        padding: 8px 12px;
        background: #1c1c1c;
        border: 1px solid #333;
        border-radius: 4px;
        color: #ddd;
        font-size: 11px;
        font-weight: 800;
    }}

    .footer {{
        border-top: 1px solid #292929;
        margin-top: 45px;
        padding-top: 18px;
        color: #666;
        font-size: 10px;
        text-align: center;
        letter-spacing: 1.2px;
    }}

    hr {{
        border-color: #292929 !important;
    }}

    @media (max-width: 768px) {{
        .brand-header {{
            flex-direction: column;
            align-items: flex-start;
        }}
        .fighter-name {{
            font-size: 29px;
        }}
        .block-container {{
            padding-left: 1rem;
            padding-right: 1rem;
        }}
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# ==========================================================
# HEADER
# ==========================================================

st.markdown(
    """
    <div class="brand-header">
        <div>
            <div class="brand-logo">OCTANE<span>PULSE</span> AI</div>
            <div class="brand-subtitle">
                MMA ANALYTICS • FIGHT INTELLIGENCE • AI PREDICTION
            </div>
        </div>
        <div class="fight-badge">🥊 FIGHT ANALYTICS</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Optional fight-night banner image.
if fight_night_uri:
    st.markdown(
        f"""
        <div style="
            height: 145px;
            border: 1px solid #2a2a2a;
            border-radius: 7px;
            margin-bottom: 26px;
            background-image:
                linear-gradient(90deg, rgba(0,0,0,.85), rgba(0,0,0,.25)),
                url('{fight_night_uri}');
            background-size: cover;
            background-position: center;
            display: flex;
            align-items: center;
            padding: 25px;
        ">
            <div>
                <div style="
                    font-family: 'Barlow Condensed', sans-serif;
                    font-size: 30px;
                    font-weight: 900;
                    letter-spacing: 1px;
                    color: white;
                ">FIGHT NIGHT</div>
                <div style="
                    color: #ccc;
                    font-size: 10px;
                    letter-spacing: 2px;
                    font-weight: 700;
                ">MATCHUP ANALYSIS • AI-POWERED PREDICTION</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ==========================================================
# SIDEBAR
# ==========================================================

st.sidebar.markdown("## 🥊 FIGHT CONTROL")
st.sidebar.caption("Configure your prediction engine and matchup.")
st.sidebar.markdown("---")

api_url = st.sidebar.text_input(
    "FASTAPI PREDICTION ENDPOINT",
    value="http://127.0.0.1:8000/predict",
    help="Enter your deployed FastAPI prediction endpoint.",
)

st.sidebar.markdown("---")
st.sidebar.markdown("### MODEL INFORMATION")
st.sidebar.markdown(
    """
    **Prediction Engine**  
    Machine Learning Based

    **Input Features**  
    11 Fighter Differential Metrics

    **Output**  
    Predicted Winner + Win Probability
    """
)
st.sidebar.markdown("---")
st.sidebar.caption("OCTANEPULSE AI • MMA ANALYTICS")

# ==========================================================
# MATCHUP
# ==========================================================

st.markdown(
    '<div class="section-heading">Fight Night Matchup</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="section-description">'
    'Configure the matchup using statistical differences between both fighters.'
    '</div>',
    unsafe_allow_html=True,
)

red_col, vs_col, blue_col = st.columns([5, 1, 5], gap="small")

with red_col:
    st.markdown(
        """
        <div class="corner-card red-card">
            <div class="corner-label">🔴 RED CORNER</div>
            <div class="fighter-name red-text">RED FIGHTER</div>
            <div class="fighter-description">
                Statistical Advantage: Red − Blue
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    red_image = image_path("red-corner.png")
    if os.path.isfile(red_image):
        st.image(red_image, use_container_width=True)

with vs_col:
    octagon_image = image_path("octagon.png")
    if os.path.isfile(octagon_image):
        st.image(octagon_image, use_container_width=True)
    else:
        st.markdown(
            '<div class="vs-wrap"><div class="vs-badge">VS</div></div>',
            unsafe_allow_html=True,
        )

with blue_col:
    st.markdown(
        """
        <div class="corner-card blue-card">
            <div class="corner-label">🔵 BLUE CORNER</div>
            <div class="fighter-name blue-text">BLUE FIGHTER</div>
            <div class="fighter-description">
                Statistical Advantage: Blue − Red
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    blue_image = image_path("blue-corner.png")
    if os.path.isfile(blue_image):
        st.image(blue_image, use_container_width=True)

# ==========================================================
# INPUT FEATURES
# ==========================================================

st.markdown("---")
st.markdown(
    '<div class="section-heading">Fighter Statistics</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="section-description">'
    'Enter the differential metrics used by your trained prediction model.'
    '</div>',
    unsafe_allow_html=True,
)

col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown(
        '<div class="corner-label red-text">INPUT ACCURATEMETRICS</div>',
        unsafe_allow_html=True,
    )

    height_diff = st.number_input(
        "Height Differential (inches) [Red − Blue]",
        value=1.0,
        step=0.5,
    )
    weight_diff = st.number_input(
        "Weight Differential (lbs) [Red − Blue]",
        value=0.0,
        step=0.5,
    )
    reach_diff = st.number_input(
        "Reach Differential (inches) [Red − Blue]",
        value=1.5,
        step=0.5,
    )
    slpm_diff = st.number_input(
        "Significant Strikes Landed / Min Differential",
        value=0.5,
        step=0.1,
    )
    str_acc_diff = st.number_input(
        "Striking Accuracy Differential",
        value=0.05,
        step=0.01,
        format="%.2f",
    )
    sapm_diff = st.number_input(
        "Significant Strikes Absorbed / Min Differential",
        value=-0.2,
        step=0.1,
    )

with col2:
    st.markdown(
        '<div class="corner-label blue-text"> INPUT ACCURATE METRICS</div>',
        unsafe_allow_html=True,
    )

    str_def_diff = st.number_input(
        "Striking Defense Differential",
        value=0.03,
        step=0.01,
        format="%.2f",
    )
    td_avg_diff = st.number_input(
        "Takedown Average Differential / 15 Min",
        value=0.2,
        step=0.1,
    )
    td_acc_diff = st.number_input(
        "Takedown Accuracy Differential",
        value=0.0,
        step=0.01,
        format="%.2f",
    )
    td_def_diff = st.number_input(
        "Takedown Defense Differential",
        value=0.05,
        step=0.01,
        format="%.2f",
    )
    sub_avg_diff = st.number_input(
        "Submission Average Differential / 15 Min",
        value=0.0,
        step=0.1,
    )

# ==========================================================
# PREDICTION
# ==========================================================

st.markdown("---")
st.markdown(
    '<div class="section-heading">Fight Prediction Engine</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="section-description">'
    'Analyze fighter statistics and generate the predicted fight outcome.'
    '</div>',
    unsafe_allow_html=True,
)

predict_button = st.button(
    "🥊  PREDICT FIGHT OUTCOME",
    type="primary",
    use_container_width=True,
)

if predict_button:
    payload = {
        "height_diff": height_diff,
        "weight_diff": weight_diff,
        "reach_diff": reach_diff,
        "slpm_diff": slpm_diff,
        "str_acc_diff": str_acc_diff,
        "sapm_diff": sapm_diff,
        "str_def_diff": str_def_diff,
        "td_avg_diff": td_avg_diff,
        "td_acc_diff": td_acc_diff,
        "td_def_diff": td_def_diff,
        "sub_avg_diff": sub_avg_diff,
    }

    if not api_url.strip():
        st.error("Please enter your FastAPI prediction endpoint in the sidebar.")
    else:
        try:
            with st.spinner("🥊 ANALYZING MATCHUP • RUNNING PREDICTION ENGINE..."):
                response = requests.post(
                    api_url.strip(),
                    json=payload,
                    timeout=30,
                )

            if response.status_code == 200:
                result = response.json()

                required_fields = (
                    "predicted_winner",
                    "red_win_probability",
                    "blue_win_probability",
                    "confidence",
                )
                missing_fields = [
                    field for field in required_fields if field not in result
                ]

                if missing_fields:
                    st.error(
                        "Prediction response is missing fields: "
                        + ", ".join(missing_fields)
                    )
                else:
                    winner = str(result["predicted_winner"])
                    red_prob = float(result["red_win_probability"])
                    blue_prob = float(result["blue_win_probability"])
                    confidence = float(result["confidence"])

                    # Keep progress values within Streamlit's 0..1 range.
                    red_progress = max(0.0, min(1.0, red_prob / 100.0))
                    blue_progress = max(0.0, min(1.0, blue_prob / 100.0))

                    winner_normalized = winner.strip().lower()
                    if winner_normalized in ("red", "red corner", "red fighter"):
                        winner_color = "#ff303b"
                        winner_display = "RED CORNER"
                    elif winner_normalized in (
                        "blue",
                        "blue corner",
                        "blue fighter",
                    ):
                        winner_color = "#3294ff"
                        winner_display = "BLUE CORNER"
                    else:
                        winner_color = "#ffffff"
                        winner_display = winner.upper()

                    st.markdown(
                        f"""
                        <div class="result-panel">
                            <div class="result-label">🏆 PREDICTION RESULT</div>
                            <div class="result-winner" style="color:{winner_color};">
                                {winner_display}
                            </div>
                            <div class="result-confidence">
                                MODEL CONFIDENCE: {confidence:.1f}%
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                    st.markdown("")
                    st.markdown(
                        '<div class="section-heading">Win Probability Breakdown</div>',
                        unsafe_allow_html=True,
                    )

                    prob_red_col, prob_blue_col = st.columns(2)

                    with prob_red_col:
                        st.markdown(
                            '<div class="corner-label red-text">🔴 RED CORNER</div>',
                            unsafe_allow_html=True,
                        )
                        st.metric("Red Corner Win Probability", f"{red_prob:.1f}%")
                        st.progress(red_progress)

                    with prob_blue_col:
                        st.markdown(
                            '<div class="corner-label blue-text">🔵 BLUE CORNER</div>',
                            unsafe_allow_html=True,
                        )
                        st.metric("Blue Corner Win Probability", f"{blue_prob:.1f}%")
                        st.progress(blue_progress)

                    st.markdown("---")
                    st.markdown(
                        '<div class="section-heading">Matchup Summary</div>',
                        unsafe_allow_html=True,
                    )

                    metric_col1, metric_col2, metric_col3 = st.columns(3)

                    with metric_col1:
                        st.metric("Height Differential", f"{height_diff:+.1f} in")

                    with metric_col2:
                        st.metric("Reach Differential", f"{reach_diff:+.1f} in")

                    with metric_col3:
                        st.metric("Takedown Differential", f"{td_avg_diff:+.1f}")

                    st.caption(
                        "Prediction generated by your configured FastAPI model. "
                        "Probabilities are model estimates, not guaranteed outcomes."
                    )

            else:
                st.error(f"API ERROR ({response.status_code})")
                st.code(response.text)

        except requests.exceptions.ConnectionError:
            st.error(
                "Unable to connect to the prediction API. Check your FastAPI "
                "server and endpoint URL."
            )

        except requests.exceptions.Timeout:
            st.error(
                "The prediction API timed out. Try again or check backend performance."
            )

        except requests.exceptions.RequestException as exc:
            st.error(f"API request failed: {exc}")

        except (ValueError, KeyError, TypeError) as exc:
            st.error(f"Invalid prediction response: {exc}")

        except Exception as exc:
            st.error(f"Unexpected error: {exc}")

# ==========================================================
# FOOTER
# ==========================================================

st.markdown(
    """
    <div class="footer">
        OCTANEPULSE AI &nbsp; • &nbsp;
        MMA FIGHT ANALYTICS &nbsp; • &nbsp;
        MACHINE LEARNING PREDICTIONS
    </div>
    """,
    unsafe_allow_html=True,
)
