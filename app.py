import streamlit as st
import random

# --- ŞİFRE EKRANI ---
sifre = st.sidebar.text_input("Uygulama Şifresi", type="password")
dogru_sifre = "sifre123" # Buraya kendi belirlediğin zor bir şifreyi yaz

if sifre != dogru_sifre:
    st.warning("Lütfen sol taraftaki menüden doğru şifreyi girin.")
    st.stop() # Şifre yanlışsa kodun geri kalanını çalıştırmaz ve ekranı kilitler
# --------------------

# Başlık ve Açıklama
st.title("🔥 Akıllı Yağ Yakım ve Antrenman Motoru")
st.write("Enerji seviyene ve yorgunluğuna göre bugünün en verimli programını oluştur.")

st.divider()

# Kullanıcı Girdileri (Arayüz)
enerji = st.slider("Bugün genel enerji seviyen nasıl? (1: Çok yorgun, 10: Harika)", 1, 10, 5)

st.write("Hangi bölgelerin dünden yorgun veya ağrılı? (Birden fazla seçebilirsin)")
yorgun_bolgeler = st.multiselect("Dinlendirilecek Bölgeler:", ["Göğüs", "Sırt", "Bacak", "Karın"])

st.divider()

# Egzersiz Havuzu 
egzersizler = {
    "Göğüs": ["10kg Dambıl Pres", "10kg Dambıl Floor Press (Yerde)", "Şınav (Diz üstü veya Normal)"],
    "Sırt": ["Direnç Bandı Lat Pulldown", "10kg Dambıl Bent-Over Row", "Direnç Bandı Seated Row"],
    "Bacak": ["Dambıl Goblet Squat", "Dambıl Lunge (Adımlama)"],
    "Karın": ["Ab Wheel Rollout", "Plank", "Bicycle Crunch"],
    "Yağ Yakımı Kompleksi": ["Dambıl Thruster", "Mountain Climber", "Burpee (Şınavsız)"]
}

# Program Oluşturma Butonu
if st.button("💪 Günün Programını Üret", type="primary"):
    st.subheader("İşte Bugünün Rotası:")
    
    # Düşük Enerji Durumu
    if enerji < 4:
        st.warning("Bugün enerjin düşük. Ağırlıklara girmiyoruz, sadece aktif dinlenme ve ter atma!")
        st.success("1. Koşu Bandı (Yüksek Eğim - Tempolu Yürüyüş) - 30 Dk\n\n2. Plank - 3 Set x Maksimum Süre")
    else:
        # Yorgun bölgeleri çıkar
        hedef_bolgeler = [b for b in ["Göğüs", "Sırt", "Bacak", "Karın", "Yağ Yakımı Kompleksi"] if b not in yorgun_bolgeler]
        
        program = []
        for bolge in hedef_bolgeler:
            hareket = random.choice(egzersizler[bolge])
            
            if bolge == "Yağ Yakımı Kompleksi":
                program.append(f"🧨 **{hareket}** - Nabzı fırlatmak için 4 Set x 15 Tekrar (Tempolu)")
            elif bolge == "Karın":
                program.append(f"🧱 **{hareket}** - 3 Set x Tükenene Kadar")
            else:
                set_tekrar = "4 Set x 12 Tekrar" if enerji >= 7 else "3 Set x 10 Tekrar"
                program.append(f"🏋️ **{hareket}** - {set_tekrar}")
        
        # Ekrana yazdırma
        for madde in program:
            st.write(madde)
            
        st.info("🏃‍♂️ **Kapanış:** Koşu Bandı (Hafif Eğim - Soğuma Yürüyüşü) - 15 Dk")