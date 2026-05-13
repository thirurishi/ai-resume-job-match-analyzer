import streamlit as st


def inject_css():
    st.markdown(
        """
        <style>
        :root {
            color-scheme: light;
        }
        * {
            box-sizing: border-box;
        }
        body, .stApp {
            background: #F8FAFC;
            color: #111827;
            font-family: 'Inter', 'Plus Jakarta Sans', 'Sora', 'Segoe UI', system-ui, sans-serif;
            min-height: 100vh;
        }
        .stApp {
            padding-top: 0;
        }
        section[data-testid="stSidebar"] {
            background: #FFFFFF;
            border-right: 1px solid #E5E7EB;
            padding: 22px 18px;
            box-shadow: 2px 0 10px rgba(15, 23, 42, 0.05);
        }
        .sidebar-brand {
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 20px;
        }
        .sidebar-icon {
            width: 32px;
            height: 32px;
            border-radius: 12px;
            background: linear-gradient(135deg, #10B981 0%, #3B82F6 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: 800;
            font-size: 14px;
        }
        .sidebar-title-text {
            font-size: 14px;
            font-weight: 700;
            color: #111827;
            margin-bottom: 2px;
        }
        .sidebar-subtitle {
            font-size: 12px;
            color: #64748B;
            line-height: 1.5;
        }
        .workflow-section {
            margin-top: 24px;
            margin-bottom: 24px;
        }
        .workflow-label {
            font-size: 11px;
            font-weight: 700;
            color: #64748B;
            text-transform: uppercase;
            letter-spacing: 0.12em;
            margin-bottom: 12px;
        }
        .workflow-item {
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 10px 12px;
            margin-bottom: 8px;
            border-radius: 14px;
            color: #0F172A;
            font-size: 13px;
            background: #FFFFFF;
            border: 1px solid #E5E7EB;
        }
        .workflow-item.active {
            background: #FFFFFF;
            color: #0F172A;
            border-color: #E5E7EB;
            font-weight: 600;
        }
        .workflow-dot {
            width: 24px;
            height: 24px;
            border-radius: 50%;
            background: #10B981;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 11px;
            font-weight: 700;
            color: white;
            border: 1px solid #10B981;
        }
        .workflow-item.active .workflow-dot {
            background: #10B981;
            color: white;
            border-color: #10B981;
        }
        .sidebar-divider {
            height: 1px;
            background: #E5E7EB;
            margin: 18px 0;
        }
        .recent-history-card {
            background: #FFFFFF;
            border: 1px solid #E5E7EB;
            border-radius: 16px;
            padding: 14px;
            margin-bottom: 12px;
            font-size: 13px;
            color: #475569;
            line-height: 1.6;
        }
        .sidebar-small {
            font-size: 12px;
            color: #64748B;
            line-height: 1.6;
            margin-top: 10px;
        }
        .privacy-card {
            background: #F8FAFC;
            border: 1px solid #D1D5DB;
            border-radius: 16px;
            padding: 14px;
            font-size: 12px;
            color: #475569;
            text-align: left;
            line-height: 1.6;
        }
        .page-header {
            text-align: center;
            padding: 30px 20px 14px;
            max-width: 880px;
            margin: 0 auto 10px;
        }
        .small-badge {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            padding: 6px 12px;
            border-radius: 999px;
            background: #ECFDF5;
            color: #047857;
            font-size: 11px;
            font-weight: 700;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            margin-bottom: 12px;
        }
        .page-title {
            font-size: 30px;
            font-weight: 800;
            color: #111827;
            margin: 0 auto 10px;
            line-height: 1.12;
            max-width: 720px;
        }
        .page-subtitle {
            color: #64748B;
            font-size: 15px;
            line-height: 1.9;
            max-width: 700px;
            margin: 0 auto;
            font-weight: 500;
        }
        .analysis-card {
            background: white;
            border: 1px solid #E5E7EB;
            border-radius: 22px;
            box-shadow: 0 12px 30px rgba(15, 23, 42, 0.06);
            padding: 28px 28px 24px;
            margin: 0 auto 20px;
            max-width: 920px;
        }
        .card-title {
            font-size: 22px;
            font-weight: 800;
            color: #111827;
            margin-bottom: 6px;
        }
        .card-note {
            color: #64748B;
            font-size: 14px;
            line-height: 1.75;
            margin-bottom: 20px;
            font-weight: 500;
        }
        .stFileUploader>div {
            border: 1px solid transparent;
            background: transparent;
            padding: 0;
        }
        .stFileUploader>div>div {
            border: 1px dashed #D1D5DB;
            border-radius: 18px;
            background: white;
            padding: 28px 24px;
            transition: border-color 0.2s ease, box-shadow 0.2s ease;
        }
        .stFileUploader>div>div:hover {
            border-color: #10B981;
            box-shadow: 0 10px 24px rgba(16, 185, 129, 0.12);
        }
        .stFileUploader>div>div>button {
            width: 100%;
            background: linear-gradient(135deg, #10B981 0%, #3B82F6 55%, #8B5CF6 100%);
            color: white;
            border: none;
            border-radius: 14px;
            padding: 16px;
            font-size: 15px;
            font-weight: 700;
            box-shadow: 0 12px 24px rgba(16, 185, 129, 0.2);
        }
        .stTextArea>div>div {
            background: white;
            border: 1px solid #E5E7EB;
            border-radius: 18px;
            padding: 0;
        }
        .stTextArea>div>div:hover {
            border-color: #D1D5DB;
        }
        .stTextArea>div>div:focus-within {
            border-color: #3B82F6;
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.12);
        }
        .stTextArea>div>div>textarea {
            background: white;
            color: #111827;
            border: none;
            border-radius: 18px;
            padding: 18px;
            font-size: 14px;
            line-height: 1.8;
            font-family: inherit;
            min-height: 220px;
            font-weight: 500;
        }
        .stTextArea>div>div>textarea:disabled {
            background: white;
            color: #111827;
        }
        .stTextArea>div>div>textarea::placeholder {
            color: #94A3B8;
        }
        .stButton>button {
            width: 100%;
            background: linear-gradient(135deg, #10B981 0%, #3B82F6 55%, #8B5CF6 100%);
            color: white;
            border: none;
            border-radius: 14px;
            padding: 16px 20px;
            font-size: 15px;
            font-weight: 700;
            box-shadow: 0 14px 28px rgba(16, 185, 129, 0.2);
        }
        .stButton>button:hover {
            transform: translateY(-1px);
            box-shadow: 0 16px 32px rgba(16, 185, 129, 0.24);
        }
        .feature-chip-row {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin-top: 18px;
            justify-content: center;
        }
        .feature-chip {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            padding: 8px 14px;
            border-radius: 999px;
            border: 1px solid #E5E7EB;
            background: white;
            color: #475569;
            font-size: 13px;
            font-weight: 600;
        }
        .result-section {
            background: white;
            border: 1px solid #E5E7EB;
            border-radius: 22px;
            box-shadow: 0 10px 26px rgba(15, 23, 42, 0.05);
            padding: 26px;
            margin: 0 auto 20px;
            max-width: 920px;
        }
        .section-title {
            font-size: 20px;
            font-weight: 800;
            color: #111827;
            margin-bottom: 8px;
        }
        .section-note {
            color: #475569;
            font-size: 14px;
            line-height: 1.8;
            margin-bottom: 18px;
            font-weight: 500;
        }
        .stat-card {
            background: white;
            border: 1px solid #E5E7EB;
            border-radius: 18px;
            padding: 18px;
            box-shadow: 0 10px 20px rgba(15, 23, 42, 0.04);
            text-align: center;
        }
        .stat-number {
            font-size: 30px;
            font-weight: 800;
            color: #111827;
            margin-bottom: 8px;
        }
        .stat-label {
            font-size: 14px;
            color: #64748B;
            font-weight: 600;
        }
        .stMetric {
            background: white;
            border: 1px solid #E5E7EB;
            border-radius: 18px;
            padding: 18px;
            box-shadow: 0 10px 20px rgba(15, 23, 42, 0.04);
        }
        .chip-pill {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            padding: 7px 12px;
            border-radius: 999px;
            font-size: 12px;
            font-weight: 600;
            margin: 4px 4px 4px 0;
            color: #1F2937;
            background: #F8FAFC;
            border: 1px solid #E5E7EB;
        }
        .chip-pill.matched {
            color: #047857;
            background: rgba(16, 185, 129, 0.12);
            border-color: rgba(16, 185, 129, 0.22);
        }
        .chip-pill.missing {
            color: #B91C1C;
            background: rgba(248, 113, 113, 0.12);
            border-color: rgba(248, 113, 113, 0.22);
        }
        .stTabs>div>div>button {
            border-radius: 14px;
            background: white;
            border: 1px solid #E5E7EB;
            color: #111827;
            padding: 10px 14px;
            font-weight: 600;
        }
        .stTabs>div>div>button[aria-selected="true"] {
            background: linear-gradient(135deg, rgba(16, 185, 129, 0.1), rgba(59, 130, 246, 0.12));
            color: #0F172A;
            border-color: #3B82F6;
        }
        .stExpander {
            background: white;
            border: 1px solid #E5E7EB;
            border-radius: 18px;
            color: #111827;
        }
        .stExpander>div {
            background: white;
            color: #111827;
        }
        .stExpander button {
            color: #111827;
        }
        #MainMenu, header, footer {
            visibility: hidden;
        }
        .css-1lcbmhc.e1fqkh3o3 {
            padding-top: 0 !important;
        }
        ::selection {
            background: rgba(59, 130, 246, 0.12);
            color: #111827;
        }
        .stApp,
        .stApp p,
        .stApp div,
        .stApp span,
        .stApp label,
        .stMarkdown,
        .stMarkdown p {
            color: #111827 !important;
        }
        .stButton button,
        button[kind="primary"] {
            color: #FFFFFF !important;
        }
        textarea,
        .stTextArea textarea {
            color: #111827 !important;
            background-color: #FFFFFF !important;
            caret-color: #111827 !important;
        }
        textarea::placeholder {
            color: #94A3B8 !important;
        }
        [data-testid="stFileUploader"] * {
            color: #111827 !important;
        }
        [data-testid="stMetric"],
        [data-testid="stMetric"] *,
        [data-testid="stMetricValue"],
        [data-testid="stMetricLabel"] {
            color: #111827 !important;
            opacity: 1 !important;
        }
        [data-baseweb="tab"],
        [data-baseweb="tab"] * {
            color: #111827 !important;
            opacity: 1 !important;
        }
        .streamlit-expanderHeader,
        .streamlit-expanderHeader *,
        [data-testid="stExpander"] *,
        [data-testid="stExpander"] p,
        [data-testid="stExpander"] div {
            color: #111827 !important;
            opacity: 1 !important;
        }
        .result-section,
        .analysis-card,
        .sidebar-brand,
        .sidebar-icon,
        .sidebar-title-text,
        .sidebar-subtitle,
        .workflow-item,
        .workflow-dot,
        .recent-history-card,
        .privacy-card,
        .page-header,
        .small-badge,
        .page-title,
        .page-subtitle,
        .card-title,
        .card-note,
        .feature-chip-row,
        .feature-chip,
        .section-title,
        .section-note,
        .stat-card,
        .stat-number,
        .stat-label,
        .chip-pill,
        .stTabs>div>div>button,
        .stTabs>div>div>button[aria-selected="true"],
        .stExpander,
        .stExpander>div {
            color: #111827 !important;
            opacity: 1 !important;
        }
        * {
            color: inherit !important;
            opacity: 1 !important;
        }
        [style*="color: white"],
        [style*="color: #fff"],
        [style*="color: #F8FAFC"],
        [style*="opacity: 0.05"],
        [style*="opacity: 0.1"],
        [style*="opacity: 0.2"] {
            color: #111827 !important;
            opacity: 1 !important;
        }
        textarea {
            color: #111827 !important;
            -webkit-text-fill-color: #111827 !important;
            opacity: 1 !important;
            background-color: #FFFFFF !important;
        }
        textarea * {
            color: #111827 !important;
            -webkit-text-fill-color: #111827 !important;
            opacity: 1 !important;
        }
        .stTextArea textarea {
            color: #111827 !important;
            -webkit-text-fill-color: #111827 !important;
            opacity: 1 !important;
            background-color: #FFFFFF !important;
        }
        [data-testid="stTextArea"] textarea {
            color: #111827 !important;
            -webkit-text-fill-color: #111827 !important;
            opacity: 1 !important;
            background-color: #FFFFFF !important;
        }
        [data-testid="stTextArea"] textarea:disabled,
        [data-testid="stTextArea"] textarea[disabled] {
            color: #111827 !important;
            -webkit-text-fill-color: #111827 !important;
            opacity: 1 !important;
            background-color: #FFFFFF !important;
        }
        textarea::placeholder {
            color: #64748B !important;
            -webkit-text-fill-color: #64748B !important;
            opacity: 1 !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
