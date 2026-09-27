import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import os
import urllib.parse
from datetime import datetime
import html
import re
import textwrap

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
    .task-card-progress {
        border-left: 5px solid #38bdf8 !important;
        border-color: rgba(56, 189, 248, 0.25);
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

    /* Pedagojik Hafıza - Timeline & Editoryal Kart Tasarımı */
    .timeline-container {
        position: relative;
        padding-left: 32px;
        margin-top: 20px;
        margin-bottom: 25px;
    }

    .timeline-container::before {
        content: '';
        position: absolute;
        top: 20px;
        bottom: 20px;
        left: 11px;
        width: 2px;
        background: linear-gradient(180deg, #38bdf8 0%, #818cf8 40%, rgba(99, 102, 241, 0.15) 100%);
        box-shadow: 0 0 10px rgba(56, 189, 248, 0.4);
    }

    .timeline-item {
        position: relative;
        margin-bottom: 24px;
    }

    .timeline-node {
        position: absolute;
        left: -32px;
        top: 22px;
        width: 22px;
        height: 22px;
        border-radius: 50%;
        background: #0b1120;
        border: 3px solid #38bdf8;
        box-shadow: 0 0 14px rgba(56, 189, 248, 0.6);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 2;
        transition: all 0.25s ease;
    }

    .timeline-item:hover .timeline-node {
        transform: scale(1.15);
        border-color: #c084fc;
        box-shadow: 0 0 18px rgba(192, 132, 252, 0.8);
    }

    .pedagogic-card {
        background: linear-gradient(135deg, rgba(20, 28, 48, 0.9) 0%, rgba(12, 17, 32, 0.96) 100%);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 18px;
        padding: 22px 26px;
        box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.5);
        backdrop-filter: blur(14px);
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }

    .pedagogic-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 4px;
        height: 100%;
        background: linear-gradient(180deg, #38bdf8 0%, #818cf8 100%);
        opacity: 0.85;
    }

    .pedagogic-card:hover {
        transform: translateY(-2px);
        border-color: rgba(56, 189, 248, 0.35);
        box-shadow: 0 16px 36px -10px rgba(56, 189, 248, 0.2);
    }

    .pedagogic-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 12px;
        margin-bottom: 14px;
        padding-bottom: 12px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.06);
    }

    .pedagogic-date {
        color: #94a3b8;
        font-size: 13px;
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 6px;
    }

    .teacher-quote-box {
        background: rgba(15, 23, 42, 0.7);
        border-radius: 14px;
        padding: 18px 22px;
        border-left: 3px solid #818cf8;
        margin-top: 10px;
        position: relative;
    }

    .teacher-quote-author {
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 0.8px;
        text-transform: uppercase;
        color: #818cf8;
        margin-bottom: 8px;
        display: flex;
        align-items: center;
        gap: 6px;
    }

    .teacher-quote-text {
        font-size: 15.5px;
        line-height: 1.75;
        color: #f1f5f9;
        font-weight: 400;
        margin: 0;
        letter-spacing: 0.1px;
    }

    /* VIP HERO DIAGNOSTIC CARD */
    .vip-hero-card {
        background: radial-gradient(circle at 10% 20%, rgba(30, 41, 59, 0.9) 0%, rgba(15, 23, 42, 0.98) 100%);
        border: 1px solid rgba(129, 140, 248, 0.3);
        border-radius: 20px;
        padding: 24px 28px;
        margin-bottom: 24px;
        box-shadow: 0 16px 40px -12px rgba(0, 0, 0, 0.7), 0 0 25px -5px rgba(56, 189, 248, 0.15);
        backdrop-filter: blur(16px);
        position: relative;
        overflow: hidden;
    }
    
    .vip-hero-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #38bdf8 0%, #818cf8 50%, #c084fc 100%);
    }

    .vip-hero-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 16px;
        margin-bottom: 20px;
        padding-bottom: 16px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    }

    .vip-avatar-glow {
        width: 52px;
        height: 52px;
        border-radius: 16px;
        background: linear-gradient(135deg, rgba(56, 189, 248, 0.25) 0%, rgba(99, 102, 241, 0.3) 100%);
        border: 2px solid rgba(56, 189, 248, 0.5);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 26px;
        box-shadow: 0 0 20px rgba(56, 189, 248, 0.35);
    }

    .vip-panel-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 16px;
    }

    .vip-panel-box {
        border-radius: 16px;
        padding: 18px 20px;
        position: relative;
        backdrop-filter: blur(10px);
        transition: all 0.25s ease;
    }
    .vip-panel-box:hover {
        transform: translateY(-2px);
    }

    .vip-box-strength {
        background: linear-gradient(145deg, rgba(16, 185, 129, 0.1) 0%, rgba(6, 78, 59, 0.15) 100%);
        border: 1px solid rgba(16, 185, 129, 0.35);
        box-shadow: 0 8px 24px -6px rgba(16, 185, 129, 0.15);
    }
    .vip-box-focus {
        background: linear-gradient(145deg, rgba(244, 63, 94, 0.1) 0%, rgba(136, 19, 55, 0.15) 100%);
        border: 1px solid rgba(244, 63, 94, 0.35);
        box-shadow: 0 8px 24px -6px rgba(244, 63, 94, 0.15);
    }
    .vip-box-strategy {
        background: linear-gradient(145deg, rgba(56, 189, 248, 0.1) 0%, rgba(30, 58, 138, 0.15) 100%);
        border: 1px solid rgba(56, 189, 248, 0.35);
        box-shadow: 0 8px 24px -6px rgba(56, 189, 248, 0.15);
    }

    .vip-box-title {
        font-size: 12px;
        font-weight: 800;
        letter-spacing: 0.8px;
        text-transform: uppercase;
        margin-bottom: 10px;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    .vip-pill-list {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
    }
    .vip-pill {
        display: inline-block;
        padding: 5px 12px;
        border-radius: 12px;
        font-size: 13px;
        font-weight: 600;
    }
    .vip-pill-green {
        background: rgba(16, 185, 129, 0.18);
        color: #6ee7b7;
        border: 1px solid rgba(16, 185, 129, 0.4);
    }
    .vip-pill-red {
        background: rgba(244, 63, 94, 0.18);
        color: #fda4af;
        border: 1px solid rgba(244, 63, 94, 0.4);
    }
    .vip-pill-blue {
        background: rgba(56, 189, 248, 0.18);
        color: #7dd3fc;
        border: 1px solid rgba(56, 189, 248, 0.4);
    }

    /* VIP STATS GRID */
    .vip-stat-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
        gap: 16px;
        margin-bottom: 24px;
    }
    .vip-stat-card {
        background: linear-gradient(145deg, rgba(20, 28, 48, 0.85) 0%, rgba(12, 17, 32, 0.95) 100%);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 18px 20px;
        box-shadow: 0 8px 24px -6px rgba(0, 0, 0, 0.5);
        transition: all 0.25s ease;
        position: relative;
    }
    .vip-stat-card:hover {
        transform: translateY(-2px);
        border-color: rgba(56, 189, 248, 0.4);
        box-shadow: 0 12px 28px -6px rgba(56, 189, 248, 0.2);
    }
    .vip-stat-label {
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
        color: #94a3b8;
        letter-spacing: 0.8px;
        margin-bottom: 6px;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    .vip-stat-value {
        font-size: 26px;
        font-weight: 800;
        color: #ffffff;
        margin-bottom: 6px;
        letter-spacing: -0.5px;
    }
    .vip-stat-delta {
        font-size: 12px;
        color: #38bdf8;
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 4px;
    }

    /* VIP PARENT COACHING BOX */
    .vip-parent-coaching-box {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.6) 0%, rgba(15, 23, 42, 0.8) 100%);
        border: 1px dashed rgba(129, 140, 248, 0.4);
        border-radius: 14px;
        padding: 14px 18px;
        margin-top: 14px;
        font-size: 13px;
        line-height: 1.6;
        color: #cbd5e1;
        position: relative;
    }
    .vip-parent-coaching-box b {
        color: #fbbf24;
    }

    /* WATERMARK QUOTE */
    .quote-watermark {
        position: absolute;
        right: 18px;
        bottom: 12px;
        font-size: 72px;
        font-family: Georgia, serif;
        line-height: 1;
        color: rgba(255, 255, 255, 0.03);
        pointer-events: none;
        user-select: none;
    }
</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# CANLI GOOGLE SHEETS VERİ ENTEGRASYONU (MÜFREDAT)
# ---------------------------------------------------------
LIVE_SHEET_URL = "https://docs.google.com/spreadsheets/d/10kmoJUbzHdXAFtY1kOy474SL2D9tZKNPz-h3QG3kg9c/export?format=csv"
LOCAL_BACKUP_CSV = os.path.join(os.path.dirname(__file__), "ogrenci_verileri.csv")

# 6. Sınıf MEB Müfredat Kataloğu (Asya için Garantili Liste)
ASYA_6TH_GRADE_DATA = [
    # --- MATEMATİK (6. Sınıf MEB) ---
    ["Asya", 6, "Matematik", "Sayılar ve İşlemler", "Üslü İfadeler ve İşlem Önceliği", "Kritik", "Başlamadı", 0],
    ["Asya", 6, "Matematik", "Sayılar ve İşlemler", "Dağılma Özelliği ve Ortak Çarpan Parantezi", "Orta", "Başlamadı", 0],
    ["Asya", 6, "Matematik", "Sayılar ve İşlemler", "Doğal Sayı Problemleri", "Kritik", "Başlamadı", 0],
    ["Asya", 6, "Matematik", "Sayılar ve İşlemler", "Çarpanlar ve Katlar", "Kritik", "Başlamadı", 0],
    ["Asya", 6, "Matematik", "Sayılar ve İşlemler", "Bölünebilme Kuralları", "Kritik", "Başlamadı", 0],
    ["Asya", 6, "Matematik", "Sayılar ve İşlemler", "Asal Sayılar ve Asal Çarpanlar", "Orta", "Başlamadı", 0],
    ["Asya", 6, "Matematik", "Sayılar ve İşlemler", "Ortak Bölenler ve Katlar", "Kritik", "Başlamadı", 0],
    ["Asya", 6, "Matematik", "Kümeler", "Kümeler ve Kesişim-Birleşim", "Temel", "Başlamadı", 0],
    ["Asya", 6, "Matematik", "Tam Sayılar", "Tam Sayılar ve Sayı Doğrusunda Gösterim", "Kritik", "Başlamadı", 0],
    ["Asya", 6, "Matematik", "Tam Sayılar", "Tam Sayılarda Karşılaştırma ve Mutlak Değer", "Kritik", "Başlamadı", 0],
    ["Asya", 6, "Matematik", "Kesirlerle İşlemler", "Kesirleri Karşılaştırma ve Sıralama", "Orta", "Başlamadı", 0],
    ["Asya", 6, "Matematik", "Kesirlerle İşlemler", "Kesirlerle Toplama ve Çıkarma", "Kritik", "Başlamadı", 0],
    ["Asya", 6, "Matematik", "Kesirlerle İşlemler", "Kesirlerle Çarpma ve Bölme", "Kritik", "Başlamadı", 0],
    ["Asya", 6, "Matematik", "Kesirlerle İşlemler", "Kesir Problemleri", "Kritik", "Başlamadı", 0],
    ["Asya", 6, "Matematik", "Ondalık Gösterim", "Ondalık Gösterimleri Yuvarlama ve Çözümleme", "Orta", "Başlamadı", 0],
    ["Asya", 6, "Matematik", "Ondalık Gösterim", "Ondalık Gösterimle Çarpma ve Bölme", "Kritik", "Başlamadı", 0],
    ["Asya", 6, "Matematik", "Ondalık Gösterim", "Ondalık Gösterim Problemleri", "Orta", "Başlamadı", 0],
    ["Asya", 6, "Matematik", "Oran", "Oran Kavramı ve Birimli-Birimsiz Oran", "Orta", "Başlamadı", 0],
    ["Asya", 6, "Matematik", "Cebir", "Cebirsel İfadeler ve Değer Hesaplama", "Kritik", "Başlamadı", 0],
    ["Asya", 6, "Matematik", "Veri İşleme", "Veri Toplama ve İkili Sütun Grafiği", "Temel", "Başlamadı", 0],
    ["Asya", 6, "Matematik", "Veri İşleme", "Aritmetik Ortalama ve Açıklık", "Orta", "Başlamadı", 0],
    ["Asya", 6, "Matematik", "Geometri ve Ölçme", "Açılar (Komşu, Tümler, Bütünler, Ters)", "Orta", "Başlamadı", 0],
    ["Asya", 6, "Matematik", "Geometri ve Ölçme", "Üçgende Alan ve Yükseklik", "Kritik", "Başlamadı", 0],
    ["Asya", 6, "Matematik", "Geometri ve Ölçme", "Paralelkenarda Alan", "Orta", "Başlamadı", 0],
    ["Asya", 6, "Matematik", "Geometri ve Ölçme", "Alan ve Arazi Ölçü Birimleri", "Temel", "Başlamadı", 0],
    ["Asya", 6, "Matematik", "Geometri ve Ölçme", "Çember ve Çevre Uzunluğu", "Orta", "Başlamadı", 0],
    ["Asya", 6, "Matematik", "Geometri ve Ölçme", "Dikdörtgenler Prizmasının Hacmi", "Kritik", "Başlamadı", 0],
    ["Asya", 6, "Matematik", "Geometri ve Ölçme", "Hacim ve Sıvı Ölçme İlişkisi", "Temel", "Başlamadı", 0],

    # --- FEN BİLİMLERİ (6. Sınıf MEB) ---
    ["Asya", 6, "Fen Bilimleri", "Güneş Sistemi ve Tutulmalar", "Güneş Sistemi ve Gezegenler", "Temel", "Başlamadı", 0],
    ["Asya", 6, "Fen Bilimleri", "Güneş Sistemi ve Tutulmalar", "Güneş ve Ay Tutulmaları", "Temel", "Başlamadı", 0],
    ["Asya", 6, "Fen Bilimleri", "Vücudumuzdaki Sistemler", "Destek ve Hareket Sistemi", "Orta", "Başlamadı", 0],
    ["Asya", 6, "Fen Bilimleri", "Vücudumuzdaki Sistemler", "Sindirim Sistemi ve Enzimler", "Kritik", "Başlamadı", 0],
    ["Asya", 6, "Fen Bilimleri", "Vücudumuzdaki Sistemler", "Dolaşım Sistemi ve Kan Grupları", "Kritik", "Başlamadı", 0],
    ["Asya", 6, "Fen Bilimleri", "Vücudumuzdaki Sistemler", "Solunum Sistemi ve Gaz Alışverişi", "Kritik", "Başlamadı", 0],
    ["Asya", 6, "Fen Bilimleri", "Vücudumuzdaki Sistemler", "Boşaltım Sistemi ve Organları", "Kritik", "Başlamadı", 0],
    ["Asya", 6, "Fen Bilimleri", "Kuvvet ve Hareket", "Bileşke Kuvvet ve Net Kuvvet", "Kritik", "Başlamadı", 0],
    ["Asya", 6, "Fen Bilimleri", "Kuvvet ve Hareket", "Dengelenmiş ve Dengelenmemiş Kuvvetler", "Kritik", "Başlamadı", 0],
    ["Asya", 6, "Fen Bilimleri", "Kuvvet ve Hareket", "Sabit Süratli Hareket ve Grafikleri", "Kritik", "Başlamadı", 0],
    ["Asya", 6, "Fen Bilimleri", "Madde ve Isı", "Maddenin Tanecikli Yapısı", "Temel", "Başlamadı", 0],
    ["Asya", 6, "Fen Bilimleri", "Madde ve Isı", "Yoğunluk ve Yoğunluk Hesaplama", "Kritik", "Başlamadı", 0],
    ["Asya", 6, "Fen Bilimleri", "Madde ve Isı", "Isı İletkenliği ve Yalıtım Malzemeleri", "Orta", "Başlamadı", 0],
    ["Asya", 6, "Fen Bilimleri", "Madde ve Isı", "Yakıtlar ve Yanma Ürünleri", "Temel", "Başlamadı", 0],
    ["Asya", 6, "Fen Bilimleri", "Ses ve Özellikleri", "Sesin Yayılması ve Farklı Ortamlarda İletimi", "Temel", "Başlamadı", 0],
    ["Asya", 6, "Fen Bilimleri", "Ses ve Özellikleri", "Sesin Sürati ve Işıkla Karşılaştırılması", "Orta", "Başlamadı", 0],
    ["Asya", 6, "Fen Bilimleri", "Ses ve Özellikleri", "Sesin Maddeyle Etkileşimi ve Ses Yalıtımı", "Orta", "Başlamadı", 0],
    ["Asya", 6, "Fen Bilimleri", "Vücudumuzdaki Sistemler ve Sağlığı", "Denetleyici ve Düzenleyici Sistemler", "Kritik", "Başlamadı", 0],
    ["Asya", 6, "Fen Bilimleri", "Vücudumuzdaki Sistemler ve Sağlığı", "İç Salgı Bezleri ve Hormonlar", "Kritik", "Başlamadı", 0],
    ["Asya", 6, "Fen Bilimleri", "Vücudumuzdaki Sistemler ve Sağlığı", "Duyu Organları ve Görevleri", "Orta", "Başlamadı", 0],
    ["Asya", 6, "Fen Bilimleri", "Vücudumuzdaki Sistemler ve Sağlığı", "Sistemlerin Sağlığı ve İlk Yardım", "Temel", "Başlamadı", 0],
    ["Asya", 6, "Fen Bilimleri", "Elektriğin İletimi", "İletken ve Yalıtkan Maddeler", "Orta", "Başlamadı", 0],
    ["Asya", 6, "Fen Bilimleri", "Elektriğin İletimi", "Elektriksel Direnç ve Bağlı Olduğu Faktörler", "Kritik", "Başlamadı", 0]
]

def ensure_asya_6th_grade(df: pd.DataFrame) -> pd.DataFrame:
    """Asya'nın sınıfını ve müfredatını her zaman 6. sınıf MEB müfredatı olarak garanti eder."""
    cols = ["Öğrenci", "Sınıf", "Ders", "Ana Ünite", "Konu", "Stratejik Önem", "Durum", "Ustalık Oranı (%)"]
    asya_df = pd.DataFrame(ASYA_6TH_GRADE_DATA, columns=cols)
    
    if df.empty or "Öğrenci" not in df.columns:
        return asya_df
    
    asya_mask = df["Öğrenci"].astype(str).str.strip().str.casefold() == "asya"
    
    needs_update = False
    if asya_mask.any():
        asya_grades = [str(x).strip().replace(".0", "") for x in df.loc[asya_mask, "Sınıf"].unique()]
        asya_topics = df.loc[asya_mask, "Konu"].tolist() if "Konu" in df.columns else []
        # Eğer 7. sınıf olarak gelmişse veya eski 7. sınıf konuları (Tam Sayılarla İşlemler, Hücre vb.) içeriyorsa
        if "7" in asya_grades or any(old in " ".join(map(str, asya_topics)) for old in ["Tam Sayılarla İşlemler", "Hücre ve Bölünmeler", "Güneş Sistemi ve Ötesi", "Rasyonel"]):
            needs_update = True
    else:
        needs_update = True

    if needs_update:
        if asya_mask.any():
            existing_asya = df[asya_mask]
            status_map = dict(zip(existing_asya["Konu"], existing_asya["Durum"])) if "Durum" in existing_asya.columns else {}
            mastery_map = dict(zip(existing_asya["Konu"], existing_asya["Ustalık Oranı (%)"])) if "Ustalık Oranı (%)" in existing_asya.columns else {}
            for idx, row in asya_df.iterrows():
                t = row["Konu"]
                if t in status_map:
                    asya_df.at[idx, "Durum"] = status_map[t]
                if t in mastery_map:
                    asya_df.at[idx, "Ustalık Oranı (%)"] = mastery_map[t]
        df = pd.concat([df[~asya_mask], asya_df], ignore_index=True)
        
    return df

def normalize_turkish_str(s: str) -> str:
    """Türkçe karakter ve büyük/küçük harf duyarsız metin karşılaştırması sağlar."""
    if not s or pd.isna(s):
        return ""
    return str(s).strip().replace("İ", "i").replace("I", "ı").replace("ı", "i").lower()

def normalize_task_status(val: str) -> str:
    """Görev durumunu emoji ve serbest metin varyasyonlarından arındırıp standartlaştırır."""
    if not val or pd.isna(val):
        return "Bekliyor"
    s = str(val).strip().casefold().replace("ı", "i").replace("İ", "i")
    if any(w in s for w in ["tamamlan", "bitti", "yapildi", "done", "completed", "tamam"]):
        return "Tamamlandı"
    elif any(w in s for w in ["devam", "suruyor", "progress"]):
        return "Devam Ediyor"
    elif any(w in s for w in ["iptal", "cancel"]):
        return "İptal"
    elif any(w in s for w in ["bekli", "pending", "yapilacak", "baslamadi"]):
        return "Bekliyor"
    return str(val).strip()

def normalize_mufredat_status(val: str) -> str:
    """Müfredat durumunu standartlaştırır."""
    if not val or pd.isna(val):
        return "Başlamadı"
    s = str(val).strip().casefold().replace("ı", "i").replace("İ", "i")
    if any(w in s for w in ["tamamlan", "bitti", "done", "completed", "tamam"]):
        return "Tamamlandı"
    elif any(w in s for w in ["devam", "suruyor", "progress"]):
        return "Devam Ediyor"
    elif any(w in s for w in ["baslamadi", "bekli"]):
        return "Başlamadı"
    return str(val).strip()

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
    Google Sheets'te Asya henüz 6. sınıfa güncellenmemiş olsa bile,
    Asya her zaman 6. sınıf MEB müfredatı ile gösterilir.
    """
    is_live = False
    try:
        df_live = pd.read_csv(LIVE_SHEET_URL, encoding="utf-8")
        df = normalize_columns(df_live)
        is_live = True
    except Exception:
        if os.path.exists(LOCAL_BACKUP_CSV):
            df = pd.read_csv(LOCAL_BACKUP_CSV, encoding="utf-8-sig")
            df = normalize_columns(df)
        else:
            df = pd.DataFrame()

    # Asya'nın 6. sınıf müfredatını garanti altına al
    df = ensure_asya_6th_grade(df)

    # Güncel tabloyu yerel yedek dosyasına kaydet
    try:
        df.to_csv(LOCAL_BACKUP_CSV, index=False, encoding="utf-8-sig")
    except Exception:
        pass

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
            df["Durum"] = df["Durum"].apply(normalize_mufredat_status)
        
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
            df_tasks["Durum"] = df_tasks["Durum"].apply(normalize_task_status)
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

        # Standartlaştırılmış veriyi yerel yedek dosyasına kaydet
        if is_live:
            df_tasks.to_csv(LOCAL_TASKS_BACKUP, index=False, encoding="utf-8-sig")

    return df_tasks, is_live

df, is_live_connected = fetch_data()
df_tasks, is_tasks_live_connected = fetch_tasks_data()

# ---------------------------------------------------------
# CANLI GOOGLE SHEETS VERİ ENTEGRASYONU (PEDAGOJİK HAFIZA & GÖZLEMLER)
# ---------------------------------------------------------
LIVE_OBSERVATIONS_URL = "https://docs.google.com/spreadsheets/d/10kmoJUbzHdXAFtY1kOy474SL2D9tZKNPz-h3QG3kg9c/gviz/tq?tqx=out:csv&sheet=" + urllib.parse.quote("Gözlemler")
LOCAL_OBSERVATIONS_BACKUP = os.path.join(os.path.dirname(__file__), "gozlemler_yedek.csv")

@st.cache_data(ttl=15)
def fetch_observations_data():
    """
    Canlı Google E-Tablo 'Gözlemler' sayfasından pedagojik hafıza ve öğretmen notlarını çeker.
    E-tablo henüz boşsa veya bağlantı hatası durumunda yerel yedek devreye girer.
    """
    is_live = False
    df_obs = pd.DataFrame()
    try:
        df_live = pd.read_csv(LIVE_OBSERVATIONS_URL, encoding="utf-8")
        df_live.columns = df_live.columns.str.strip()
        is_live = True
        if not df_live.empty:
            df_obs = df_live
        else:
            # E-tablo henüz yeni açılmış ve boşsa örnek/yerel yedeğe bak
            if os.path.exists(LOCAL_OBSERVATIONS_BACKUP):
                try:
                    df_obs = pd.read_csv(LOCAL_OBSERVATIONS_BACKUP, encoding="utf-8-sig", on_bad_lines='skip')
                except Exception:
                    df_obs = pd.read_csv(LOCAL_OBSERVATIONS_BACKUP, encoding="utf-8", on_bad_lines='skip')
            else:
                df_obs = df_live
    except Exception:
        if os.path.exists(LOCAL_OBSERVATIONS_BACKUP):
            try:
                df_obs = pd.read_csv(LOCAL_OBSERVATIONS_BACKUP, encoding="utf-8-sig", on_bad_lines='skip')
            except Exception:
                df_obs = pd.read_csv(LOCAL_OBSERVATIONS_BACKUP, encoding="utf-8", on_bad_lines='skip')
        else:
            df_obs = pd.DataFrame(columns=["Tarih", "Öğrenci", "Ders", "Etiket", "Öğretmen Notu"])

    if not df_obs.empty:
        if len(df_obs.columns) == 5:
            df_obs.columns = ["Tarih", "Öğrenci", "Ders", "Etiket", "Öğretmen Notu"]
        else:
            col_rename = {}
            for col in df_obs.columns:
                c = normalize_turkish_str(col)
                if "tarih" in c or "date" in c:
                    col_rename[col] = "Tarih"
                elif "ogr" in c or "renci" in c or "enci" in c or "student" in c:
                    col_rename[col] = "Öğrenci"
                elif "ders" in c or "konu" in c:
                    col_rename[col] = "Ders"
                elif "etiket" in c or "kategori" in c or "tag" in c:
                    col_rename[col] = "Etiket"
                elif "not" in c or "gozlem" in c or "retmen" in c or "degerlendirme" in c:
                    col_rename[col] = "Öğretmen Notu"
            if col_rename:
                df_obs = df_obs.rename(columns=col_rename)

        for req in ["Tarih", "Öğrenci", "Ders", "Etiket", "Öğretmen Notu"]:
            if req in df_obs.columns:
                df_obs[req] = df_obs[req].fillna("").astype(str).str.strip()
            else:
                df_obs[req] = ""

        if is_live and not df_obs.empty:
            try:
                df_obs.to_csv(LOCAL_OBSERVATIONS_BACKUP, index=False, encoding="utf-8-sig")
            except Exception:
                pass

    return df_obs, is_live

df_obs, is_obs_live_connected = fetch_observations_data()

def get_tag_badge_html(tag: str) -> str:
    """Etiketin anlamsal önemine göre modern renkli bir badge HTML'i üretir."""
    tag_clean = tag.strip()
    if not tag_clean:
        return ""
    tag_lower = tag_clean.lower()
    
    if any(k in tag_lower for k in ["analitik", "strateji", "mantık", "metot", "problem", "kavram"]):
        bg = "rgba(129, 140, 248, 0.16)"
        color = "#818cf8"
        border = "rgba(129, 140, 248, 0.35)"
        icon = "💡"
    elif any(k in tag_lower for k in ["başarı", "kavrama", "tebrik", "özgüven", "güçlü", "motivasyon", "ilerleme"]):
        bg = "rgba(16, 185, 129, 0.16)"
        color = "#34d399"
        border = "rgba(16, 185, 129, 0.35)"
        icon = "🌟"
    elif any(k in tag_lower for k in ["dikkat", "odak", "rutin", "disiplin", "hız", "ödev", "pratik"]):
        bg = "rgba(245, 158, 11, 0.16)"
        color = "#fbbf24"
        border = "rgba(245, 158, 11, 0.35)"
        icon = "🎯"
    elif any(k in tag_lower for k in ["eksik", "yanılgı", "kritik", "uyarı", "tekrar", "destek"]):
        bg = "rgba(244, 63, 94, 0.16)"
        color = "#fb7185"
        border = "rgba(244, 63, 94, 0.35)"
        icon = "⚠️"
    else:
        bg = "rgba(56, 189, 248, 0.16)"
        color = "#38bdf8"
        border = "rgba(56, 189, 248, 0.35)"
        icon = "🔖"
        
    return f'<span class="badge" style="background: {bg}; color: {color}; border: 1px solid {border}; font-size: 12px; font-weight: 700; padding: 5px 12px; border-radius: 20px;">{icon} {tag_clean}</span>'

def get_lesson_badge_html(lesson: str) -> str:
    """Ders adına göre zarif bir ikon ve stil rozeti üretir."""
    lesson_clean = lesson.strip()
    if not lesson_clean:
        return ""
    l_lower = lesson_clean.lower()
    if "matematik" in l_lower:
        icon = "📐"
        color = "#38bdf8"
        bg = "rgba(56, 189, 248, 0.1)"
        border = "rgba(56, 189, 248, 0.25)"
    elif "fen" in l_lower:
        icon = "🔬"
        color = "#a78bfa"
        bg = "rgba(167, 139, 250, 0.1)"
        border = "rgba(167, 139, 250, 0.25)"
    elif "rehberlik" in l_lower or "gelişim" in l_lower or "koçluk" in l_lower:
        icon = "🧭"
        color = "#34d399"
        bg = "rgba(52, 211, 153, 0.1)"
        border = "rgba(52, 211, 153, 0.25)"
    else:
        icon = "📚"
        color = "#cbd5e1"
        bg = "rgba(148, 163, 184, 0.1)"
        border = "rgba(148, 163, 184, 0.25)"
    return f'<span class="badge" style="background: {bg}; color: {color}; border: 1px solid {border}; font-size: 12px; font-weight: 600; padding: 4px 10px; border-radius: 12px;">{icon} {lesson_clean}</span>'

def render_html(html_str: str):
    """HTML içeriğini Markdown kod bloğu tuzağına düşmeden garantili olarak render eder."""
    st.markdown(textwrap.dedent(html_str).strip(), unsafe_allow_html=True)


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
    live_sources = []
    if is_live_connected:
        live_sources.append("Müfredat")
    if is_tasks_live_connected:
        live_sources.append("Görevler")
    if is_obs_live_connected:
        live_sources.append("Gözlemler")
    
    if len(live_sources) == 3:
        st.success("🟢 Canlı Google Sheet Bağlı (Müfredat, Görevler & Gözlemler)", icon="✅")
    elif len(live_sources) > 0:
        st.success(f"🟢 Canlı Google Sheet Bağlı ({', '.join(live_sources)})", icon="✅")
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
    all_students_set = set(["Asya", "Utku", "İpek"])
    if "Öğrenci" in df.columns and not df.empty:
        all_students_set.update(df["Öğrenci"].dropna().unique().tolist())
    if "Ogrenci" in df_tasks.columns and not df_tasks.empty:
        all_students_set.update(df_tasks["Ogrenci"].dropna().unique().tolist())
    if "Öğrenci" in df_obs.columns and not df_obs.empty:
        all_students_set.update(df_obs["Öğrenci"].dropna().unique().tolist())
    all_students_set.discard("")
    students = sorted(list(all_students_set))

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
raw_grade = student_df["Sınıf"].iloc[0] if not student_df.empty and "Sınıf" in student_df.columns else "6"
grade_label = f"{raw_grade}. Sınıf"
if str(raw_grade) == "8":
    sub_grade_label = "LGS Hazırlık Grubu"
elif str(raw_grade) == "6":
    sub_grade_label = "6. Sınıf Temel & Beceri Temelli Müfredat"
elif str(raw_grade) == "4":
    sub_grade_label = "Ortaokula Hazırlık Grubu"
elif str(raw_grade) == "7":
    sub_grade_label = "Ortaokul Ara Sınıf / LGS Altyapı"
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
# ANA SEKMELER (MÜFREDAT, AKTİF GÖREVLER VE GELİŞİM GÜNLÜĞÜ)
# ---------------------------------------------------------
tab_mufredat, tab_gorevler, tab_gunluk = st.tabs([
    "📊 Müfredat ve İlerleme",
    "📚 Aktif Görevler ve Ödevler",
    "🧠 Gelişim Günlüğü"
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
        student_tasks = df_tasks[df_tasks["Ogrenci"].apply(normalize_turkish_str) == normalize_turkish_str(selected_student)].copy()
    else:
        student_tasks = pd.DataFrame(columns=["Tarih", "Ogrenci", "Gorev Tipi", "Konu ve Hedef", "Durum", "Gorev"])

    # 2. TARİHE GÖRE SIRALAMA (En yeni tarihler en üstte)
    if not student_tasks.empty and "Tarih" in student_tasks.columns:
        student_tasks["_tarih_dt"] = pd.to_datetime(student_tasks["Tarih"], errors="coerce", dayfirst=True)
        student_tasks = student_tasks.sort_values(by=["_tarih_dt", "Tarih"], ascending=[False, False]).drop(columns=["_tarih_dt"])

    # 3. GÖREV İSTATİSTİKLERİ (METRİKLER)
    total_tasks_count = len(student_tasks)
    pending_tasks = student_tasks[student_tasks["Durum"] == "Bekliyor"] if not student_tasks.empty else pd.DataFrame()
    completed_tasks = student_tasks[student_tasks["Durum"] == "Tamamlandı"] if not student_tasks.empty else pd.DataFrame()
    in_progress_tasks = student_tasks[student_tasks["Durum"] == "Devam Ediyor"] if not student_tasks.empty else pd.DataFrame()

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
            options=["Tümü", "Bekliyor", "Tamamlandı", "Devam Ediyor"],
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
        if st.button("🔄 Görevleri Şimdi Yenile", key="btn_refresh_tasks", use_container_width=True):
            st.cache_data.clear()
            st.rerun()
        if is_parent_mode:
            st.caption(f"🔒 **{selected_student}** öğrencisine kilitli görünüm.")
        else:
            st.caption(f"👤 Yönetici Görünümü: **{selected_student}** listeleniyor.")

    # Filtre uygulama
    filtered_tasks = student_tasks.copy()
    if task_status_filter != "Tümü":
        filtered_tasks = filtered_tasks[filtered_tasks["Durum"] == task_status_filter]
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
            is_completed = status == "Tamamlandı"
            is_in_progress = status == "Devam Ediyor"
            
            if is_completed:
                card_class = "task-card-completed"
                badge_status = '<span class="badge badge-success">✅ Tamamlandı</span>'
            elif is_in_progress:
                card_class = "task-card-progress"
                badge_status = '<span class="badge badge-info">🔄 Devam Ediyor</span>'
            else:
                card_class = "task-card-pending"
                badge_status = '<span class="badge badge-warning">⏳ Bekliyor</span>'

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


# =========================================================
# SEKME 3: PEDAGOJİK HAFIZA & GELİŞİM GÜNLÜĞÜ
# =========================================================
with tab_gunluk:
    # 1. ÖĞRENCİ KİLİDİ: Aktif / Kilitli öğrencinin gözlemlerini dinamik olarak filtrele
    if not df_obs.empty and "Öğrenci" in df_obs.columns:
        student_obs = df_obs[df_obs["Öğrenci"].apply(normalize_turkish_str) == normalize_turkish_str(selected_student)].copy()
    else:
        student_obs = pd.DataFrame(columns=["Tarih", "Öğrenci", "Ders", "Etiket", "Öğretmen Notu"])

    # 2. KRONOLOJİK SIRALAMA: En güncel tarihler en üstte
    if not student_obs.empty and "Tarih" in student_obs.columns:
        student_obs["_tarih_dt"] = pd.to_datetime(student_obs["Tarih"], errors="coerce", dayfirst=True)
        student_obs = student_obs.sort_values(by=["_tarih_dt", "Tarih"], ascending=[False, False]).drop(columns=["_tarih_dt"])

    # 3. İSTATİSTİKLER VE PEDAGOJİK METRİK KARTLARI
    total_obs_count = len(student_obs)
    latest_obs_date = student_obs["Tarih"].iloc[0] if total_obs_count > 0 else "-"
    
    top_tag = "Henüz Yok"
    top_tag_count = 0
    if total_obs_count > 0 and "Etiket" in student_obs.columns:
        valid_tags = student_obs["Etiket"].replace("", pd.NA).dropna()
        if not valid_tags.empty:
            tag_counts = valid_tags.value_counts()
            if not tag_counts.empty:
                top_tag = tag_counts.index[0]
                top_tag_count = tag_counts.iloc[0]

    o_col1, o_col2, o_col3 = st.columns(3)
    with o_col1:
        st.metric(
            label="Toplam Pedagojik Gözlem",
            value=f"{total_obs_count} Kayıt",
            delta=f"{selected_student} Akademik Arşivi"
        )
    with o_col2:
        st.metric(
            label="Son Değerlendirme Tarihi",
            value=f"{latest_obs_date}",
            delta="En Güncel Değerlendirme" if total_obs_count > 0 else "Kayıt Bekleniyor"
        )
    with o_col3:
        st.metric(
            label="Öne Çıkan Gözlem Alanı",
            value=f"{top_tag}",
            delta=f"{top_tag_count} Gözlem Notu" if top_tag != "Henüz Yok" else "Kayıt Bekleniyor"
        )

    st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)

    # 4. HIZLI FİLTRELEME VE CANLI ARAMA ÇUBUĞU
    f1, f2, f3 = st.columns([1.5, 1.5, 2])
    with f1:
        obs_courses = ["Tümü"] + sorted([c for c in student_obs["Ders"].replace("", pd.NA).dropna().unique().tolist() if c]) if not student_obs.empty else ["Tümü"]
        selected_obs_course = st.selectbox("📚 Ders Filtresi", options=obs_courses, key="obs_course_filter")
    with f2:
        obs_tags = ["Tümü"] + sorted([t for t in student_obs["Etiket"].replace("", pd.NA).dropna().unique().tolist() if t]) if not student_obs.empty else ["Tümü"]
        selected_obs_tag = st.selectbox("🏷️ Etiket Filtresi", options=obs_tags, key="obs_tag_filter")
    with f3:
        search_query = st.text_input("🔍 Notlarda Arama Yap...", placeholder="Örn: karekök, ebob, cebirsel, basamak...", key="obs_search_query")

    # Filtreleri uygula
    filtered_obs = student_obs.copy()
    if selected_obs_course != "Tümü" and not filtered_obs.empty:
        filtered_obs = filtered_obs[filtered_obs["Ders"] == selected_obs_course]
    if selected_obs_tag != "Tümü" and not filtered_obs.empty:
        filtered_obs = filtered_obs[filtered_obs["Etiket"] == selected_obs_tag]
    if search_query and not filtered_obs.empty:
        q = search_query.strip().lower()
        filtered_obs = filtered_obs[
            filtered_obs["Öğretmen Notu"].astype(str).str.lower().str.contains(q, na=False) |
            filtered_obs["Etiket"].astype(str).str.lower().str.contains(q, na=False) |
            filtered_obs["Ders"].astype(str).str.lower().str.contains(q, na=False)
        ]

    st.markdown("---")

    # 5. DİKEY ZAMAN AKIŞI (TIMELINE) & EDİTORYAL KARTLAR
    if filtered_obs.empty:
        if total_obs_count == 0:
            render_html(f"""
            <div class="info-box" style="border-left-color: #818cf8; text-align: center; padding: 36px 24px; background: rgba(15, 23, 42, 0.7); border-radius: 16px;">
                <div style="font-size: 42px; margin-bottom: 12px;">🌱</div>
                <h3 style="color: #818cf8; margin: 0 0 8px 0; font-size: 20px; font-weight: 700;">Henüz Kayıtlı Gözlem Bulunmuyor</h3>
                <p style="color: #94a3b8; margin: 0 auto; max-width: 520px; font-size: 14px; line-height: 1.6;">
                    <b>{selected_student}</b> için Google E-Tablo <i>Gözlemler</i> sekmesine yeni pedagojik değerlendirmeler eklendikçe burada şık bir editoryal zaman akışı olarak listelenecektir.
                </p>
            </div>
            """)
        else:
            st.info(f"Seçilen filtrelere uygun ({selected_obs_course} / {selected_obs_tag}) pedagojik not bulunamadı.")
    else:
        st.markdown(f"#### 🧠 {selected_student} - Pedagojik Gözlem ve Gelişim Akışı ({len(filtered_obs)} Kayıt)")
        
        # Timeline kapsayıcısı
        render_html('<div class="timeline-container">')

        for idx, row in filtered_obs.iterrows():
            date_val = str(row.get("Tarih", "-")).strip()
            lesson_val = str(row.get("Ders", "")).strip()
            tag_val = str(row.get("Etiket", "Genel")).strip()
            teacher_note = str(row.get("Öğretmen Notu", "")).strip()

            safe_note = html.escape(teacher_note).replace("\n", "<br>")
            safe_note = re.sub(r'\*\*(.*?)\*\*', r'<b style="color: #38bdf8;">\1</b>', safe_note)

            badge_tag_html = get_tag_badge_html(tag_val)
            badge_lesson_html = get_lesson_badge_html(lesson_val) if lesson_val else ""

            render_html(f"""
            <div class="timeline-item">
                <div class="timeline-node"></div>
                <div class="pedagogic-card">
                    <div class="pedagogic-header">
                        <div style="display: flex; align-items: center; gap: 10px; flex-wrap: wrap;">
                            <span class="pedagogic-date">📅 {date_val}</span>
                            {badge_lesson_html}
                        </div>
                        <div>
                            {badge_tag_html}
                        </div>
                    </div>
                    <div class="teacher-quote-box">
                        <div class="teacher-quote-author">
                            <span>👩‍🏫 ÖĞRETMEN DEĞERLENDİRMESİ & PEDAGOJİK GÖZLEM</span>
                        </div>
                        <p class="teacher-quote-text">
                            {safe_note}
                        </p>
                    </div>
                </div>
            </div>
            """)

        render_html('</div>')

        # 6. CSV İNDİRME BUTONU
        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
        csv_obs_bytes = filtered_obs.to_csv(index=False, encoding="utf-8-sig").encode("utf-8-sig")
        st.download_button(
            label=f"📥 {selected_student} Gelişim Günlüğünü İndir (CSV)",
            data=csv_obs_bytes,
            file_name=f"{selected_student}_gelisim_gunlugu.csv",
            mime="text/csv",
            use_container_width=True,
            help=f"{selected_student} öğrencisinin gelişim günlüğünü CSV olarak indirir."
        )

