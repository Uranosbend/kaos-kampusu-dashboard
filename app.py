import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import os
import urllib.parse
from datetime import datetime

# ---------------------------------------------------------
# SAYFA YAPILANDIRMASI
# ---------------------------------------------------------
st.set_page_config(
    page_title="Öğrenci Başarı & Veli Takip Paneli",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# ULTRA PREMİUM DARK THEME CSS
# ---------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Arka Plan */
    .stApp {
        background: radial-gradient(circle at 12% 18%, #141c2e 0%, #0b0f19 60%, #060911 100%);
        color: #f1f5f9;
    }

    /* Sol Menü (Sidebar) */
    [data-testid="stSidebar"] {
        background-color: #0c1222;
        border-right: 1px solid rgba(255, 255, 255, 0.08);
    }
    
    /* Üst Karşılama Kartı */
    .header-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.75) 0%, rgba(15, 23, 42, 0.95) 100%);
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 18px;
        padding: 24px 30px;
        margin-bottom: 22px;
        box-shadow: 0 12px 35px -10px rgba(0, 0, 0, 0.6);
        backdrop-filter: blur(14px);
    }

    .header-title {
        font-size: 28px;
        font-weight: 800;
        letter-spacing: -0.5px;
        background: linear-gradient(90deg, #38bdf8, #818cf8, #c084fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        padding-bottom: 6px;
    }

    .header-subtitle {
        color: #94a3b8;
        font-size: 14px;
        margin: 0;
    }

    /* Tabs Tasarımı */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        background-color: rgba(15, 23, 42, 0.7);
        padding: 8px 12px;
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        margin-bottom: 24px;
    }

    .stTabs [data-baseweb="tab"] {
        height: 48px;
        border-radius: 12px;
        color: #94a3b8;
        font-weight: 700;
        font-size: 15px;
        padding: 0 24px;
        border: 1px solid transparent !important;
        background-color: transparent;
        transition: all 0.25s ease;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, rgba(56, 189, 248, 0.18) 0%, rgba(99, 102, 241, 0.22) 100%) !important;
        color: #38bdf8 !important;
        border: 1px solid rgba(56, 189, 248, 0.4) !important;
        box-shadow: 0 4px 16px rgba(56, 189, 248, 0.15);
    }

    /* KPI Kart Tasarımları */
    [data-testid="stMetric"] {
        background: linear-gradient(145deg, #111a2e 0%, #0c1220 100%);
        border: 1px solid rgba(99, 102, 241, 0.25);
        padding: 20px 22px;
        border-radius: 16px;
        box-shadow: 0 8px 24px -6px rgba(0, 0, 0, 0.5);
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
    }

    [data-testid="stMetric"]:hover {
        transform: translateY(-3px);
        border-color: rgba(129, 140, 248, 0.5);
        box-shadow: 0 12px 28px -6px rgba(99, 102, 241, 0.25);
    }

    [data-testid="stMetricLabel"] {
        color: #94a3b8 !important;
        font-size: 12px !important;
        font-weight: 700 !important;
        text-transform: uppercase;
        letter-spacing: 0.8px;
    }

    [data-testid="stMetricValue"] {
        color: #ffffff !important;
        font-size: 28px !important;
        font-weight: 800 !important;
    }

    /* Grafik Taşıyıcı Kartları */
    .chart-container {
        background: #0f172a;
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 18px;
        padding: 22px;
        margin-bottom: 22px;
        box-shadow: 0 10px 30px -8px rgba(0, 0, 0, 0.5);
    }

    .chart-header {
        font-size: 16px;
        font-weight: 700;
        color: #f8fafc;
        margin-bottom: 14px;
        display: flex;
        align-items: center;
        gap: 10px;
    }

    /* Özel Rozetler */
    .badge {
        display: inline-block;
        padding: 5px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 0.3px;
    }
    .badge-critical {
        background: rgba(244, 63, 94, 0.15);
        color: #fb7185;
        border: 1px solid rgba(244, 63, 94, 0.35);
    }
    .badge-info {
        background: rgba(56, 189, 248, 0.15);
        color: #38bdf8;
        border: 1px solid rgba(56, 189, 248, 0.35);
    }
    .badge-success {
        background: rgba(16, 185, 129, 0.15);
        color: #34d399;
        border: 1px solid rgba(16, 185, 129, 0.35);
    }
    .badge-warning {
        background: rgba(245, 158, 11, 0.15);
        color: #fbbf24;
        border: 1px solid rgba(245, 158, 11, 0.35);
    }

    /* Veli Bilgi Kartı */
    .info-box {
        background: rgba(30, 41, 59, 0.45);
        border-left: 4px solid #38bdf8;
        border-radius: 12px;
        padding: 14px 18px;
        margin-top: 14px;
        color: #cbd5e1;
        font-size: 13px;
        line-height: 1.6;
    }

    /* Görev Kartı Tasarımları */
    .task-card {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(10, 16, 29, 0.95) 100%);
        border-radius: 16px;
        padding: 20px 24px;
        margin-bottom: 16px;
        transition: all 0.25s ease;
        border: 1px solid rgba(255, 255, 255, 0.08);
    }
    .task-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 28px -8px rgba(0, 0, 0, 0.6);
    }
    .task-card-pending {
        border-left: 5px solid #f59e0b !important;
        border-color: rgba(245, 158, 11, 0.25);
    }
    .task-card-completed {
        border-left: 5px solid #10b981 !important;
        border-color: rgba(16, 185, 129, 0.25);
    }
    .task-title {
        font-size: 18px;
        font-weight: 700;
        color: #f8fafc;
        margin-bottom: 10px;
        line-height: 1.4;
    }
    .task-meta-row {
        display: flex;
        flex-wrap: wrap;
        align-items: center;
        gap: 10px;
        margin-top: 12px;
        padding-top: 10px;
        border-top: 1px solid rgba(255, 255, 255, 0.06);
    }
</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# CANLI GOOGLE SHEETS VERİ ENTEGRASYONU (MÜFREDAT)
# ---------------------------------------------------------
LIVE_SHEET_URL = "https://docs.google.com/spreadsheets/d/10kmoJUbzHdXAFtY1kOy474SL2D9tZKNPz-h3QG3kg9c/export?format=csv"
LOCAL_BACKUP_CSV = os.path.join(os.path.dirname(__file__), "ogrenci_verileri.csv")

def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Müfredat tablosu sütunlarını standart hale getirir."""
    if len(df.columns) == 8:
        df.columns = ["Öğrenci", "Sınıf", "Ders", "Ana Ünite", "Konu", "Stratejik Önem", "Durum", "Ustalık Oranı (%)"]
    else:
        df.columns = df.columns.str.strip()
        col_map = {}
        for col in df.columns:
            c = col.lower()
            if "stratejik" in c:
                col_map[col] = "Stratejik Önem"
            elif "ustal" in c:
                col_map[col] = "Ustalık Oranı (%)"
            elif "renci" in c:
                col_map[col] = "Öğrenci"
            elif "sınıf" in c or "sinif" in c:
                col_map[col] = "Sınıf"
            elif "ders" in c:
                col_map[col] = "Ders"
            elif "nite" in c:
                col_map[col] = "Ana Ünite"
            elif "konu" in c:
                col_map[col] = "Konu"
            elif "durum" in c:
                col_map[col] = "Durum"
        if col_map:
            df = df.rename(columns=col_map)
    return df

@st.cache_data(ttl=15)
def fetch_data():
    """
    Canlı Google E-Tablo'dan müfredat verisini çeker.
    Google Sheets asıl ve tek veri kaynağıdır. Canlı bağlantı başarılı olduğunda
    tüm ekleme/silme işlemleri doğrudan yansır ve yerel yedek güncellenir.
    Yerel yedek SADECE Google Sheets bağlantısı koptuğunda devreye girer.
    """
    is_live = False
    try:
        df_live = pd.read_csv(LIVE_SHEET_URL, encoding="utf-8")
        df = normalize_columns(df_live)
        is_live = True
        # Canlı veriyi yerel yedek dosyasına kaydet
        df.to_csv(LOCAL_BACKUP_CSV, index=False, encoding="utf-8-sig")
    except Exception:
        if os.path.exists(LOCAL_BACKUP_CSV):
            df = pd.read_csv(LOCAL_BACKUP_CSV, encoding="utf-8-sig")
            df = normalize_columns(df)
        else:
            df = pd.DataFrame()

    if not df.empty:
        if "Ustalık Oranı (%)" in df.columns:
            df["Ustalık Oranı (%)"] = (
                df["Ustalık Oranı (%)"]
                .astype(str)
                .str.replace("%", "", regex=False)
                .str.strip()
            )
            df["Ustalık Oranı (%)"] = pd.to_numeric(df["Ustalık Oranı (%)"], errors="coerce").fillna(0).astype(int)
        
        if "Durum" in df.columns:
            df["Durum"] = df["Durum"].fillna("Başlamadı").str.strip()
        
        if "Stratejik Önem" in df.columns:
            df["Stratejik Önem"] = df["Stratejik Önem"].fillna("Temel").str.strip()

    return df, is_live


# ---------------------------------------------------------
# CANLI GOOGLE SHEETS VERİ ENTEGRASYONU (GÖREVLER & ÖDEVLER)
# ---------------------------------------------------------
LIVE_TASKS_URL = "https://docs.google.com/spreadsheets/d/10kmoJUbzHdXAFtY1kOy474SL2D9tZKNPz-h3QG3kg9c/gviz/tq?tqx=out:csv&sheet=G%C3%B6revler"
LOCAL_TASKS_BACKUP = os.path.join(os.path.dirname(__file__), "gorevler_yedek.csv")

@st.cache_data(ttl=15)
def fetch_tasks_data():
    """
    Canlı Google E-Tablo 'Görevler' sayfasından ödev ve görev verilerini çeker.
    Google Sheets asıl kaynaktır; kullanıcı görevleri sildiğinde anında silinmiş (boş) olarak yansır.
    Yerel yedek SADECE internet/bağlantı hatası durumunda (offline modda) devreye girer.
    """
    is_live = False
    df_tasks = pd.DataFrame()
    try:
        df_live = pd.read_csv(LIVE_TASKS_URL, encoding="utf-8")
        df_live.columns = df_live.columns.str.strip()
        
        # Canlı veriyi doğrudan al (kullanıcı satırları sildiyse boş gelir ve boş yansır)
        df_tasks = df_live
        is_live = True
        # Canlı tabloyu anında yerel yedek dosyasına kaydet
        df_tasks.to_csv(LOCAL_TASKS_BACKUP, index=False, encoding="utf-8-sig")
    except Exception:
        # Yalnızca bağlantı hatasında yerel yedeğe başvur
        if os.path.exists(LOCAL_TASKS_BACKUP):
            df_tasks = pd.read_csv(LOCAL_TASKS_BACKUP, encoding="utf-8-sig")
        else:
            df_tasks = pd.DataFrame(columns=["Tarih", "Ogrenci", "Gorev Tipi", "Konu ve Hedef", "Durum", "Gorev"])

    # Sütun isimlerini standartlaştır
    if not df_tasks.empty:
        col_rename = {}
        for col in df_tasks.columns:
            c = col.lower()
            if "tarih" in c:
                col_rename[col] = "Tarih"
            elif "ogrenci" in c or "öğrenci" in c:
                col_rename[col] = "Ogrenci"
            elif "tip" in c:
                col_rename[col] = "Gorev Tipi"
            elif "konu" in c or "hedef" in c:
                col_rename[col] = "Konu ve Hedef"
            elif "durum" in c:
                col_rename[col] = "Durum"
            elif "gorev" in c or "görev" in c:
                col_rename[col] = "Gorev"
        if col_rename:
            df_tasks = df_tasks.rename(columns=col_rename)

        if "Durum" in df_tasks.columns:
            df_tasks["Durum"] = df_tasks["Durum"].fillna("Bekliyor").astype(str).str.strip()
        if "Ogrenci" in df_tasks.columns:
            df_tasks["Ogrenci"] = df_tasks["Ogrenci"].fillna("").astype(str).str.strip()
        if "Tarih" in df_tasks.columns:
            df_tasks["Tarih"] = df_tasks["Tarih"].fillna("").astype(str).str.strip()
        if "Gorev Tipi" in df_tasks.columns:
            df_tasks["Gorev Tipi"] = df_tasks["Gorev Tipi"].fillna("Genel Görev").astype(str).str.strip()
        if "Konu ve Hedef" in df_tasks.columns:
            df_tasks["Konu ve Hedef"] = df_tasks["Konu ve Hedef"].fillna("Belirtilmedi").astype(str).str.strip()
        if "Gorev" in df_tasks.columns:
            df_tasks["Gorev"] = df_tasks["Gorev"].fillna("-").astype(str).str.strip()

    return df_tasks, is_live

df, is_live_connected = fetch_data()
df_tasks, is_tasks_live_connected = fetch_tasks_data()


# ---------------------------------------------------------
# SIDEBAR (SOL MENÜ & FİLTRELER)
# ---------------------------------------------------------
with st.sidebar:
    st.markdown("""
        <div style="text-align: center; padding: 10px 0 16px 0;">
            <h2 style="color: #38bdf8; margin: 0 0 6px 0; font-weight: 800; font-size: 22px;">🚀 Veli Takip Paneli</h2>
            <p style="color: #94a3b8; font-size: 13px; margin: 0;">Matematik & Fen Bilimleri Eğitimi</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")

    # Canlı Bağlantı Rozeti
    if is_live_connected and is_tasks_live_connected:
        st.success("🟢 Canlı Google Sheet Bağlı (Müfredat & Görevler)", icon="✅")
    elif is_live_connected:
        st.success("🟢 Canlı Google Sheet Bağlı", icon="✅")
    else:
        st.info("🟡 Yerel Yedek Veri Devrede", icon="ℹ️")

    # URL Parametresi & Veli Kilit Modu Kontrolü
    raw_params = {}
    try:
        if hasattr(st, "query_params"):
            raw_params = st.query_params
        elif hasattr(st, "experimental_get_query_params"):
            raw_params = st.experimental_get_query_params()
    except Exception:
        raw_params = {}

    url_student_param = None
    for param_key in ["ogrenci", "öğrenci", "student"]:
        if param_key in raw_params:
            val = raw_params[param_key]
            if isinstance(val, list) and len(val) > 0:
                url_student_param = str(val[0]).strip()
            elif isinstance(val, str):
                url_student_param = val.strip()
            if url_student_param:
                break

    # Öğrenci Seçimi ve Yetkilendirme
    students = sorted(df["Öğrenci"].dropna().unique().tolist()) if "Öğrenci" in df.columns and not df.empty else ["Asya", "Utku"]

    if url_student_param:
        # Veli Modu: URL'den gelen öğrenciye kilitlenir, selectbox kilitlenir
        matched_student = None
        for s in students:
            if s.lower() == url_student_param.lower():
                matched_student = s
                break
        selected_student = matched_student if matched_student else url_student_param
        is_parent_mode = True

        st.success(f"👤 Öğrenci: **{selected_student}** (Veli Modu)", icon="🔒")
    else:
        # Yönetici Modu: Tüm öğrencileri seçebilen selectbox
        is_parent_mode = False
        selected_student = st.selectbox(
            "👤 Öğrenci Seçiniz",
            options=students,
            index=0
        )

    st.markdown("---")

    # Müfredat Filtreleri
    student_records = df[df["Öğrenci"] == selected_student] if "Öğrenci" in df.columns else pd.DataFrame()
    courses = ["Tümü"] + sorted(student_records["Ders"].dropna().unique().tolist()) if "Ders" in student_records.columns else ["Tümü"]
    selected_course = st.selectbox("📚 Ders Filtresi (Müfredat)", options=courses)

    strategic_list = ["Tümü", "Kritik", "Orta", "Temel"]
    selected_strategic = st.selectbox("🎯 Stratejik Önem Filtresi", options=strategic_list)

    statuses = ["Tümü", "Başlamadı", "Devam Ediyor", "Tamamlandı"]
    selected_status = st.selectbox("⚡ Konu Durumu (Müfredat)", options=statuses)

    st.markdown("---")

    # Anlık Yenileme Butonu
    if st.button("🔄 Verileri Şimdi Yenile", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

    # CSV İndirme Butonu
    if is_parent_mode:
        csv_data = student_records.to_csv(index=False, encoding="utf-8-sig")
        st.download_button(
            label=f"📥 {selected_student} Müfredatını İndir (CSV)",
            data=csv_data,
            file_name=f"{selected_student}_verileri.csv",
            mime="text/csv",
            use_container_width=True,
            help=f"{selected_student} öğrencisinin güncel müfredat tablosunu CSV olarak indirir."
        )
    else:
        csv_data = df.to_csv(index=False, encoding="utf-8-sig")
        st.download_button(
            label="📥 Güncel Müfredatı İndir (CSV)",
            data=csv_data,
            file_name="ogrenci_verileri.csv",
            mime="text/csv",
            use_container_width=True,
            help="Tüm öğrencilerin güncel tablosunu CSV olarak indirir."
        )

    st.markdown("""
        <div class="info-box">
            📌 <b>Canlı Senkronizasyon:</b> Google E-Tablo'ya eklenen tüm yeni konu ve ödev durumları panele otomatik olarak yansır.
        </div>
    """, unsafe_allow_html=True)


# ---------------------------------------------------------
# MÜFREDAT HESAPLAMALARI & METRİKLER
# ---------------------------------------------------------
student_df = df[df["Öğrenci"] == selected_student].copy() if "Öğrenci" in df.columns else pd.DataFrame()

filtered_df = student_df.copy()
if not filtered_df.empty:
    if selected_course != "Tümü" and "Ders" in filtered_df.columns:
        filtered_df = filtered_df[filtered_df["Ders"] == selected_course]
    if selected_strategic != "Tümü" and "Stratejik Önem" in filtered_df.columns:
        filtered_df = filtered_df[filtered_df["Stratejik Önem"] == selected_strategic]
    if selected_status != "Tümü" and "Durum" in filtered_df.columns:
        filtered_df = filtered_df[filtered_df["Durum"] == selected_status]

# Sınıf Bilgisi
raw_grade = student_df["Sınıf"].iloc[0] if not student_df.empty and "Sınıf" in student_df.columns else "8"
grade_label = f"{raw_grade}. Sınıf"
if str(raw_grade) == "8":
    sub_grade_label = "LGS Hazırlık Grubu"
elif str(raw_grade) == "4":
    sub_grade_label = "Ortaokula Hazırlık Grubu"
else:
    sub_grade_label = "Ortaokul Müfredatı"

total_topics = len(student_df)
course_counts = student_df["Ders"].value_counts().to_dict() if "Ders" in student_df.columns else {}
courses_summary = " • ".join([f"{c} ({cnt} Konu)" for c, cnt in course_counts.items()]) if course_counts else "Müfredat"
delta_course_summary = " • ".join([f"{cnt} {c}" for c, cnt in course_counts.items()]) if course_counts else "Dersler"

completed_topics = len(student_df[student_df["Durum"] == "Tamamlandı"]) if not student_df.empty and "Durum" in student_df.columns else 0
in_progress_topics = len(student_df[student_df["Durum"] == "Devam Ediyor"]) if not student_df.empty and "Durum" in student_df.columns else 0
not_started_topics = len(student_df[student_df["Durum"] == "Başlamadı"]) if not student_df.empty and "Durum" in student_df.columns else 0

completed_df = student_df[student_df["Durum"] == "Tamamlandı"] if not student_df.empty and "Durum" in student_df.columns else pd.DataFrame()
avg_mastery = round(completed_df["Ustalık Oranı (%)"].mean(), 1) if not completed_df.empty and "Ustalık Oranı (%)" in completed_df.columns else 0.0
completion_rate = round((completed_topics / total_topics * 100), 1) if total_topics > 0 else 0

critical_df = student_df[student_df["Stratejik Önem"] == "Kritik"] if not student_df.empty and "Stratejik Önem" in student_df.columns else pd.DataFrame()
total_critical = len(critical_df)


# ---------------------------------------------------------
# ÜST BİLGİ BANNERI
# ---------------------------------------------------------
st.markdown(f"""
<div class="header-card">
    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 16px;">
        <div>
            <h1 class="header-title">✨ {selected_student} - Akademik Başarı & İlerleme Paneli</h1>
            <p class="header-subtitle">
                <b>Dersler:</b> {courses_summary} | Toplam <b>{total_topics}</b> Müfredat Konusu
            </p>
        </div>
        <div>
            <span class="badge badge-info">{grade_label} ({sub_grade_label})</span>
            <span class="badge badge-critical">🎯 Toplam {total_critical} Kritik Konu</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# ANA SEKMELER (MÜFREDAT VE AKTİF GÖREVLER)
# ---------------------------------------------------------
tab_mufredat, tab_gorevler = st.tabs([
    "📊 Müfredat ve İlerleme",
    "📚 Aktif Görevler ve Ödevler"
])


# =========================================================
# SEKME 1: MÜFREDAT VE İLERLEME
# =========================================================
with tab_mufredat:
    # KPI Metrik Kartları
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            label="Öğrencinin Sınıfı",
            value=f"{grade_label}",
            delta=sub_grade_label
        )

    with col2:
        st.metric(
            label="Toplam Konu Sayısı",
            value=f"{total_topics} Konu",
            delta=delta_course_summary
        )

    with col3:
        if completed_topics == 0:
            st.metric(
                label="Tamamlanan Konu Sayısı",
                value="0 Konu",
                delta="Ders Başlangıç Seviyesi"
            )
        else:
            st.metric(
                label="Tamamlanan Konu Sayısı",
                value=f"{completed_topics} Konu",
                delta=f"%{completion_rate} Tamamlanma Oranı"
            )

    st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)

    # Grafikler
    g_col1, g_col2 = st.columns([1, 1])

    # --- GRAFİK 1: GAUGE (USTALIK ORANI) ---
    with g_col1:
        st.markdown("""
            <div class="chart-container">
                <div class="chart-header">
                    <span>⚡ Genel Ustalık Oranı Ortalaması</span>
                </div>
        """, unsafe_allow_html=True)

        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=avg_mastery,
            domain={'x': [0, 1], 'y': [0, 1]},
            number={'suffix': "%", 'font': {'size': 44, 'color': '#ffffff', 'family': 'Plus Jakarta Sans'}},
            gauge={
                'axis': {'range': [0, 100], 'tickwidth': 2, 'tickcolor': "#475569", 'tickfont': {'color': '#94a3b8'}},
                'bar': {'color': "#38bdf8", 'thickness': 0.28},
                'bgcolor': "rgba(30, 41, 59, 0.4)",
                'borderwidth': 1,
                'bordercolor': "rgba(255, 255, 255, 0.1)",
                'steps': [
                    {'range': [0, 50], 'color': 'rgba(239, 68, 68, 0.22)'},
                    {'range': [50, 75], 'color': 'rgba(245, 158, 11, 0.22)'},
                    {'range': [75, 100], 'color': 'rgba(16, 185, 129, 0.22)'}
                ],
                'threshold': {
                    'line': {'color': "#ec4899", 'width': 3},
                    'thickness': 0.8,
                    'value': 85
                }
            }
        ))

        fig_gauge.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font={'color': "#f1f5f9", 'family': "Plus Jakarta Sans"},
            height=300,
            margin=dict(l=25, r=25, t=25, b=20)
        )

        st.plotly_chart(fig_gauge, use_container_width=True, config={'displayModeBar': False})

        if completed_topics == 0:
            st.markdown("""
                <div style="text-align: center; color: #94a3b8; font-size: 13px; margin-top: -10px;">
                    💡 <i>Dersler başladıkça ve konu tarama testleri yapıldıkça ustalık seviyesi burada otomatik hesaplanacaktır.</i>
                </div>
            """, unsafe_allow_html=True)
            
        st.markdown("</div>", unsafe_allow_html=True)

    # --- GRAFİK 2: DONUT CHART (STRATEJİK ÖNEM DAĞILIMI) ---
    with g_col2:
        st.markdown("""
            <div class="chart-container">
                <div class="chart-header">
                    <span>🎯 Müfredat Stratejik Önem Dağılımı</span>
                </div>
        """, unsafe_allow_html=True)

        color_map = {
            "Kritik": "#f43f5e",
            "Orta": "#38bdf8",
            "Temel": "#10b981"
        }

        if completed_topics == 0:
            chart_data = student_df["Stratejik Önem"].value_counts().reset_index() if not student_df.empty else pd.DataFrame(columns=["Stratejik Önem", "Konu Sayısı"])
            if not chart_data.empty:
                chart_data.columns = ["Stratejik Önem", "Konu Sayısı"]
            center_text = f"<b>{total_topics}</b><br><span style='font-size:12px;color:#94a3b8;'>Toplam Konu</span>"
        else:
            chart_data = student_df[student_df["Durum"] == "Tamamlandı"]["Stratejik Önem"].value_counts().reset_index()
            if not chart_data.empty:
                chart_data.columns = ["Stratejik Önem", "Konu Sayısı"]
            center_text = f"<b>{completed_topics}</b><br><span style='font-size:12px;color:#94a3b8;'>Bitirilen</span>"

        if not chart_data.empty:
            fig_donut = px.pie(
                chart_data,
                values="Konu Sayısı",
                names="Stratejik Önem",
                hole=0.62,
                color="Stratejik Önem",
                color_discrete_map=color_map
            )

            fig_donut.update_traces(
                textposition='inside',
                textinfo='percent+label',
                hovertemplate="<b>%{label}</b>: %{value} Konu (%{percent})<extra></extra>",
                marker=dict(line=dict(color='#0f172a', width=3))
            )

            fig_donut.add_annotation(
                text=center_text,
                x=0.5, y=0.5,
                font_size=20,
                font_color="#ffffff",
                showarrow=False
            )

            fig_donut.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font={'color': "#f1f5f9", 'family': "Plus Jakarta Sans"},
                showlegend=True,
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=-0.15,
                    xanchor="center",
                    x=0.5,
                    font=dict(color="#cbd5e1", size=12)
                ),
                height=300,
                margin=dict(l=20, r=20, t=20, b=20)
            )

            st.plotly_chart(fig_donut, use_container_width=True, config={'displayModeBar': False})
        else:
            st.info("Gösterilecek veri bulunamadı.")

        orta_count = len(student_df[student_df["Stratejik Önem"] == "Orta"]) if not student_df.empty else 0
        temel_count = len(student_df[student_df["Stratejik Önem"] == "Temel"]) if not student_df.empty else 0
        st.markdown(f"""
            <div style="text-align: center; color: #94a3b8; font-size: 13px; margin-top: -10px;">
                🎯 <i>Müfredatta <b>{total_critical} Kritik</b>, <b>{orta_count} Orta</b> ve <b>{temel_count} Temel</b> konu bulunmaktadır.</i>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    # --- DİNAMİK VERİ TABLOSU (MÜFREDAT DETAYI) ---
    st.markdown("### 📋 Müfredat & İlerleme Detay Tablosu")

    display_cols = ["Ders", "Ana Ünite", "Konu", "Stratejik Önem", "Durum", "Ustalık Oranı (%)"]
    valid_cols = [c for c in display_cols if c in filtered_df.columns]
    table_df = filtered_df[valid_cols].reset_index(drop=True)

    def highlight_status(val):
        if val == "Tamamlandı":
            return "background-color: rgba(16, 185, 129, 0.22); color: #34d399; font-weight: 600; border-radius: 6px;"
        elif val == "Devam Ediyor":
            return "background-color: rgba(245, 158, 11, 0.22); color: #fbbf24; font-weight: 600; border-radius: 6px;"
        elif val == "Başlamadı":
            return "background-color: rgba(148, 163, 184, 0.12); color: #94a3b8; border-radius: 6px;"
        return ""

    def highlight_importance(val):
        if val == "Kritik":
            return "color: #fb7185; font-weight: bold;"
        elif val == "Orta":
            return "color: #38bdf8;"
        elif val == "Temel":
            return "color: #34d399;"
        return ""

    styled_table = (
        table_df.style
        .map(highlight_status, subset=["Durum"])
        .map(highlight_importance, subset=["Stratejik Önem"])
    )

    st.dataframe(
        styled_table,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Ustalık Oranı (%)": st.column_config.ProgressColumn(
                "Ustalık Oranı",
                help="Öğrencinin ilgili konudaki test başarısı",
                format="%d%%",
                min_value=0,
                max_value=100
            ),
            "Durum": st.column_config.TextColumn("Çalışma Durumu"),
            "Stratejik Önem": st.column_config.TextColumn("Sınav Önemi"),
            "Ders": st.column_config.TextColumn("Ders", width="small")
        }
    )

    b_col1, b_col2 = st.columns([2, 1])
    with b_col1:
        st.caption(f"📅 Son Veri Güncellemesi: {datetime.now().strftime('%d.%m.%Y %H:%M')} | Filtrelenen {len(table_df)} / {total_topics} konu listeleniyor.")
    with b_col2:
        csv_bytes = table_df.to_csv(index=False).encode('utf-8-sig')
        st.download_button(
            label="📥 Tabloyu CSV Olarak İndir",
            data=csv_bytes,
            file_name=f"{selected_student}_mufredat_takip.csv",
            mime="text/csv",
            use_container_width=True
        )


# =========================================================
# SEKME 2: AKTİF GÖREVLER VE ÖDEVLER (ÖĞRENCİ KİLİTLİ)
# =========================================================
with tab_gorevler:
    # 1. ÖĞRENCİ KİLİDİ: Sadece seçili/kilitli öğrencinin görevlerini al
    if not df_tasks.empty and "Ogrenci" in df_tasks.columns:
        student_tasks = df_tasks[df_tasks["Ogrenci"].str.lower() == selected_student.lower()].copy()
    else:
        student_tasks = pd.DataFrame(columns=["Tarih", "Ogrenci", "Gorev Tipi", "Konu ve Hedef", "Durum", "Gorev"])

    # 2. TARİHE GÖRE SIRALAMA (En yeni tarihler en üstte)
    if not student_tasks.empty and "Tarih" in student_tasks.columns:
        student_tasks["_tarih_dt"] = pd.to_datetime(student_tasks["Tarih"], errors="coerce", dayfirst=True)
        student_tasks = student_tasks.sort_values(by=["_tarih_dt", "Tarih"], ascending=[False, False]).drop(columns=["_tarih_dt"])

    # 3. GÖREV İSTATİSTİKLERİ (METRİKLER)
    total_tasks_count = len(student_tasks)
    pending_tasks = student_tasks[student_tasks["Durum"].str.lower() == "bekliyor"] if not student_tasks.empty else pd.DataFrame()
    completed_tasks = student_tasks[student_tasks["Durum"].str.lower() == "tamamlandı"] if not student_tasks.empty else pd.DataFrame()

    t_col1, t_col2, t_col3 = st.columns(3)
    with t_col1:
        st.metric(
            label="Toplam Görev & Ödev",
            value=f"{total_tasks_count} Görev",
            delta=f"{selected_student} İçin Atanan"
        )
    with t_col2:
        st.metric(
            label="Bekleyen Görevler",
            value=f"{len(pending_tasks)} Görev",
            delta="Aktif Çalışma Bekliyor" if len(pending_tasks) > 0 else "Tümü Tamamlandı 🎉"
        )
    with t_col3:
        st.metric(
            label="Tamamlanan Görevler",
            value=f"{len(completed_tasks)} Görev",
            delta=f"%{round(len(completed_tasks) / total_tasks_count * 100, 1)} Başarı Oranı" if total_tasks_count > 0 else "0% Başarı"
        )

    st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)

    # 4. HIZLI FİLTRELEME ÇUBUĞU
    f_col1, f_col2, f_col3 = st.columns([1.5, 1.5, 2])
    with f_col1:
        task_status_filter = st.selectbox(
            "⚡ Durum Filtresi",
            options=["Tümü", "Bekliyor", "Tamamlandı"],
            key="task_status_filter"
        )
    with f_col2:
        all_types = ["Tümü"] + sorted(student_tasks["Gorev Tipi"].dropna().unique().tolist()) if not student_tasks.empty else ["Tümü"]
        task_type_filter = st.selectbox(
            "📂 Görev Tipi",
            options=all_types,
            key="task_type_filter"
        )
    with f_col3:
        st.write("") # Boşluk
        st.write("")
        if is_parent_mode:
            st.caption(f"🔒 **{selected_student}** öğrencisine kilitli görünüm.")
        else:
            st.caption(f"👤 Yönetici Görünümü: **{selected_student}** listeleniyor.")

    # Filtre uygulama
    filtered_tasks = student_tasks.copy()
    if task_status_filter != "Tümü":
        filtered_tasks = filtered_tasks[filtered_tasks["Durum"].str.lower() == task_status_filter.lower()]
    if task_type_filter != "Tümü":
        filtered_tasks = filtered_tasks[filtered_tasks["Gorev Tipi"] == task_type_filter]

    st.markdown("---")

    # 5. MODERN GÖREV KARTLARI LİSTESİ
    if filtered_tasks.empty:
        if total_tasks_count == 0:
            st.markdown(f"""
                <div class="info-box" style="border-left-color: #10b981; text-align: center; padding: 24px;">
                    <h3 style="color: #34d399; margin: 0 0 6px 0;">🎉 Harika! Bekleyen Görev Yok</h3>
                    <p style="color: #94a3b8; margin: 0; font-size: 14px;">
                        <b>{selected_student}</b> için şu an atanmış aktif bir ödev veya görev bulunmuyor.
                    </p>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.info(f"Seçilen filtrelere uygun ({task_status_filter} / {task_type_filter}) görev bulunamadı.")
    else:
        st.markdown(f"#### 📋 {selected_student} - Görev Listesi ({len(filtered_tasks)} Adet)")
        
        for idx, row in filtered_tasks.iterrows():
            status = str(row.get("Durum", "Bekliyor")).strip()
            is_completed = status.lower() == "tamamlandı"
            
            card_class = "task-card-completed" if is_completed else "task-card-pending"
            badge_status = (
                '<span class="badge badge-success">✅ Tamamlandı</span>'
                if is_completed
                else '<span class="badge badge-warning">⏳ Bekliyor</span>'
            )

            topic_title = str(row.get("Konu ve Hedef", "Belirtilmedi"))
            task_type = str(row.get("Gorev Tipi", "Genel Görev"))
            task_code = str(row.get("Gorev", "-"))
            task_date = str(row.get("Tarih", "-"))

            # Kart HTML Render
            st.markdown(f"""
            <div class="task-card {card_class}">
                <div style="display: flex; justify-content: space-between; align-items: flex-start; gap: 14px; flex-wrap: wrap;">
                    <div style="flex: 1; min-width: 250px;">
                        <div class="task-title">🎯 {topic_title}</div>
                        <div style="color: #94a3b8; font-size: 13px; display: flex; align-items: center; gap: 8px;">
                            <span>📅 Tarih: <b style="color: #cbd5e1;">{task_date}</b></span>
                        </div>
                    </div>
                    <div>
                        {badge_status}
                    </div>
                </div>
                <div class="task-meta-row">
                    <span class="badge badge-info">📂 {task_type}</span>
                    <span class="badge" style="background: rgba(148, 163, 184, 0.12); color: #cbd5e1; border: 1px solid rgba(148, 163, 184, 0.25); font-family: monospace;">🔖 Kod: {task_code}</span>
                    <span class="badge" style="background: rgba(56, 189, 248, 0.08); color: #7dd3fc; border: 1px solid rgba(56, 189, 248, 0.2);">👤 Öğrenci: {row.get('Ogrenci', selected_student)}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Görevler CSV İndir
        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
        csv_tasks_bytes = filtered_tasks.to_csv(index=False, encoding="utf-8-sig").encode("utf-8-sig")
        st.download_button(
            label=f"📥 {selected_student} Görev Listesini İndir (CSV)",
            data=csv_tasks_bytes,
            file_name=f"{selected_student}_gorevler.csv",
            mime="text/csv",
            use_container_width=True
        )
