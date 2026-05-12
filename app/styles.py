import streamlit as st


def inject_css():
    st.markdown(
        """
        <style>
        :root {
            color-scheme: dark;
        }
        .stApp {
            background: #0f172a;
            color: #e2e8f0;
        }
        .hero-card, .input-card, .metric-card, .result-card, .history-card {
            border: 1px solid rgba(148, 163, 184, 0.18);
            border-radius: 20px;
            padding: 22px;
            margin-bottom: 18px;
            background: rgba(15, 23, 42, 0.92);
            box-shadow: 0 10px 30px rgba(15, 23, 42, 0.35);
        }
        .hero-title {
            color: #f8fafc;
            font-size: 42px;
            font-weight: 700;
            margin-bottom: 8px;
        }
        .hero-subtitle {
            color: #cbd5e1;
            font-size: 18px;
            line-height: 1.7;
            margin-bottom: 18px;
        }
        .badge-pill {
            display: inline-block;
            padding: 6px 12px;
            margin: 4px 4px 4px 0;
            border-radius: 999px;
            background: rgba(96, 165, 250, 0.18);
            color: #bfdbfe;
            font-size: 13px;
            border: 1px solid rgba(96, 165, 250, 0.3);
        }
        .step-box {
            border: 1px solid rgba(148, 163, 184, 0.18);
            border-radius: 16px;
            padding: 16px;
            margin-bottom: 16px;
            background: rgba(15, 23, 42, 0.9);
        }
        .step-title {
            color: #f8fafc;
            font-weight: 700;
            margin-bottom: 10px;
        }
        .tag-pill {
            display: inline-block;
            padding: 6px 10px;
            margin: 4px 4px 4px 0;
            border-radius: 999px;
            background: rgba(34, 197, 94, 0.15);
            color: #d1fae5;
            font-size: 13px;
            border: 1px solid rgba(34, 197, 94, 0.3);
        }
        .tag-pill.missing {
            background: rgba(248, 113, 113, 0.14);
            color: #fecaca;
            border: 1px solid rgba(248, 113, 113, 0.3);
        }
        .stButton>button {
            border-radius: 999px;
            padding: 12px 24px;
            font-weight: 700;
        }
        .stDownloadButton>button {
            border-radius: 999px;
            padding: 12px 24px;
            font-weight: 700;
        }
        .footer-note {
            color: #94a3b8;
            font-size: 13px;
            margin-top: 8px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
