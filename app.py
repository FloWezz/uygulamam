import streamlit as st
import sqlite3
import pandas as pd
from datetime import date
import random

# --- 1. VERİTABANI KURULUMU ---
def init_db():
    conn = sqlite3.connect('spor_veritabani.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS kullanicilar (kullanici_adi TEXT PRIMARY KEY, yas INTEGER, cinsiyet TEXT, boy INTEGER, kilo REAL)''')
    c.execute('''CREATE TABLE IF NOT EXISTS ekipmanlar (kullanici_adi TEXT, ekipman TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS antrenman_gecmisi (kullanici_adi TEXT, tarih TEXT, program_detayi TEXT)''')
    conn.commit()
    conn.close()

init_db()

# --- 2. OTURUM YÖNETİMİ ---
if 'giris_yapildi' not in st.session_state:
    st.session_state.giris_yapildi = False
if 'aktif_kullanici' not in st.session_state:
    st.session_state.aktif_kullanici = ""

# --- 3. GİRİŞ EKRANI ---
if not st.session_state.giris_yapildi:
    st.title("🔐 Giriş Yap veya Kayıt Ol")
    kullanici_adi_input = st.text_input("Kullanıcı Adı (Örn: ahmet):").lower().strip()
    
    if st.button("Giriş / Kayıt"):
        if kullanici_adi_input:
            conn = sqlite3.connect('spor_veritabani.db')
            c = conn.cursor()
            c.execute("SELECT * FROM kullanicilar WHERE kullanici_adi=?", (kullanici_adi_input,))
            kayit = c.fetchone()
            conn.close()
            
            st.session_state.aktif_kullanici = kullanici_adi_input
            st.session_state.giris_yapildi = True
            
            if kayit:
                st.session_state.yeni_kayit = False
            else:
                st.session_state.yeni_kayit = True
            st.rerun()

# --- 4. ANA UYGULAMA EKRANI ---
else:
    kullanici = st.session_state.aktif_kullanici
    st.sidebar.success(f"👤 Aktif Hesap: {kullanici.capitalize()}")
    if st.sidebar.button("Çıkış Yap"):
        st.session_state.giris_yapildi = False
        st.rerun()

    # --- PROFİL OLUŞTURMA (SADECE YENİ KAYITLAR İÇİN) ---
    if st.session_state.get('yeni_kayit', False):
        st.title(f"Hoş Geldin, {kullanici.capitalize()}! Profilini Oluşturalım")
        
        col1, col2 = st.columns(2)
        with col1:
            yas = st.number_input("Yaşın:", 10, 100, 19)
            boy = st.number_input("Boyun (cm):", 100, 250, 182)
        with col2:
            cinsiyet = st.selectbox("Cinsiyet:", ["Erkek", "Kadın"])
            kilo = st.number_input("Kilon (kg):", 30.0, 200.0, 93.0)
        
        st.divider()
        st.subheader("Evdeki Ekipmanların Neler?")
        ekipman_dambil = st.checkbox("10 kg Dambıl Çifti", value=True)
        ekipman_bant = st.checkbox("Direnç Bandı", value=True)
        ekipman_teker = st.checkbox("Ab Wheel (Karın Tekeri)", value=True)
        ekipman_barfiks = st.checkbox("Barfiks Demiri (Kapı Tipi)", value=False)
        ekipman_kardiyo = st.checkbox("Koşu Bandı", value=True)
        
        if st.button("Profili Kaydet ve Başla"):
            conn = sqlite3.connect('spor_veritabani.db')
            c = conn.cursor()
            c.execute("INSERT INTO kullanicilar VALUES (?, ?, ?, ?, ?)", (kullanici, yas, cinsiyet, boy, kilo))
            
            if ekipman_dambil: c.execute("INSERT INTO ekipmanlar VALUES (?, ?)", (kullanici, "Dambıl"))
            if ekipman_bant: c.execute("INSERT INTO ekipmanlar VALUES (?, ?)", (kullanici, "Bant"))
            if ekipman_teker: c.execute("INSERT INTO ekipmanlar VALUES (?, ?)", (kullanici, "Ab Wheel"))
            if ekipman_barfiks: c.execute("INSERT INTO ekipmanlar VALUES (?, ?)", (kullanici, "Barfiks"))
            if ekipman_kardiyo: c.execute("INSERT INTO ekipmanlar VALUES (?, ?)", (kullanici, "Kardiyo Aleti"))
                
            conn.commit()
            conn.close()
            st.session_state.yeni_kayit = False
            st.rerun()

    # --- ANTRENÖR MOTORU VE TAKVİM (KAYITLI KULLANICILAR İÇİN) ---
    else:
        # Ekipmanları veritabanından çek
        conn = sqlite3.connect('spor_veritabani.db')
        c = conn.cursor()
        c.execute("SELECT ekipman FROM ekipmanlar WHERE kullanici_adi=?", (kullanici,))
        kullanici_ekipmanlari = [row[0] for row in c.fetchall()]
        
        st.title("🔥 Akıllı Antrenör Motoru")
        
        # Kullanıcı Girdileri
        col_e, col_y = st.columns(2)
        with col_e:
            enerji = st.slider("⚡ Enerji Seviyen (1-10):", 1, 10, 5)
        with col_y:
            yorgun_bolgeler = st.multiselect("🛌 Dünden Yorgun Bölgeler:", ["Göğüs", "Sırt", "Bacak", "Karın"])
            
        # Ekipmana Göre Dinamik Egzersiz Havuzu
        hareketler_gogus = ["Şınav (Normal veya Diz Üstü)", "Geniş Tutuş Şınav"]
        hareketler_sirt = ["Ters Kar Leoparı (Yerde Yüzüstü Sırt Sıkıştırma)"]
        hareketler_bacak = ["Air Squat", "Geriye Adımlama (Lunge)"]
        hareketler_karin = ["Plank", "Bicycle Crunch"]
        hareketler_kardiyo = ["Yerinde Tempolu Adımlama (Ter Atma)"]
        
        if "Dambıl" in kullanici_ekipmanlari:
            hareketler_gogus.extend(["10kg Dambıl Floor Press (Yerde Pres)"])
            hareketler_sirt.extend(["10kg Dambıl Bent-Over Row (Eğilerek Çekiş)"])
            hareketler_bacak.extend(["10kg Dambıl Goblet Squat", "10kg Dambıl Lunge"])
            hareketler_kardiyo.extend(["Dambıl Thruster (Tüm Vücut Yağ Yakımı)"])
            
        if "Bant" in kullanici_ekipmanlari:
            hareketler_sirt.extend(["Direnç Bandı Lat Pulldown", "Direnç Bandı Seated Row"])
            
        if "Ab Wheel" in kullanici_ekipmanlari:
            hareketler_karin.extend(["Ab Wheel Rollout"])
            
        if "Barfiks" in kullanici_ekipmanlari:
            hareketler_sirt.extend(["Barfiks"])
            
        if "Kardiyo Aleti" in kullanici_ekipmanlari:
            hareketler_kardiyo.insert(0, "Koşu Bandı (Yüksek Eğim - Tempolu Yürüyüş)")
            
        egzersizler = {"Göğüs": hareketler_gogus, "Sırt": hareketler_sirt, "Bacak": hareketler_bacak, "Karın": hareketler_karin}
        
        # Program Üretme Mekanizması
        if st.button("💪 Program Üret", type="primary"):
            program_listesi = []
            if enerji < 4:
                st.warning("Enerjin düşük. Bugün ağırlıklara girmiyoruz, aktif dinlenme günü.")
                program_listesi.append(f"1. {hareketler_kardiyo[0]} - 30 Dakika")
                program_listesi.append("2. Plank - 3 Set x Maksimum Süre")
            else:
                hedef_bolgeler = [b for b in ["Göğüs", "Sırt", "Bacak", "Karın"] if b not in yorgun_bolgeler]
                for bolge in hedef_bolgeler:
                    hareket = random.choice(egzersizler[bolge])
                    if bolge == "Karın":
                        program_listesi.append(f"🧱 {hareket} - 3 Set x Tükenene Kadar")
                    else:
                        set_tek = "4 Set x 12 Tekrar" if enerji >= 7 else "3 Set x 10 Tekrar"
                        program_listesi.append(f"🏋️ {hareket} - {set_tek}")
                
                # Sona Kardiyo/Yağ yakıcı ekle
                program_listesi.append(f"🏃‍♂️ Kapanış: {random.choice(hareketler_kardiyo)} - 15 Dakika")
                
            
        # Programı aralarına iki satır boşluk koyarak birleştir (Alt alta düzgün görünmesi için)
        st.session_state.gecici_program = "\n\n".join(program_listesi)
            
        # Programı Ekranda Gösterme ve Kaydetme
        if 'gecici_program' in st.session_state and st.session_state.gecici_program != "":
            st.success("Günün Programı Hazır!")
            st.info(st.session_state.gecici_program)
            
            if st.button("✅ Bu Programı Yaptım / Takvime Kaydet"):
                bugun = str(date.today())
                c.execute("INSERT INTO antrenman_gecmisi VALUES (?, ?, ?)", (kullanici, bugun, st.session_state.gecici_program))
                conn.commit()
                st.session_state.gecici_program = "" # Ekrani temizle
                st.balloons()
                st.toast("Antrenman başarıyla takvime eklendi!")
                st.rerun()
                
        # --- GEÇMİŞ TABLOSU ---
        st.divider()
        st.subheader("📅 Antrenman Geçmişim")
        
        # Veritabanından geçmişi liste olarak çek
        c.execute("SELECT tarih, program_detayi FROM antrenman_gecmisi WHERE kullanici_adi=? ORDER BY tarih DESC", (kullanici,))
        gecmis_kayitlar = c.fetchall()
        
        if gecmis_kayitlar:
            for tarih, program in gecmis_kayitlar:
                # Her bir tarih için açılır-kapanır şık bir kutu (expander) oluştur
                with st.expander(f"🗓️ {tarih} Tarihli Antrenmanın"):
                    st.markdown(program) # Hareketleri formatlı ve alt alta göster
        else:
            st.info("Henüz kaydedilmiş bir antrenmanın yok. İlk programını üretip kaydet!")
            
        conn.close()