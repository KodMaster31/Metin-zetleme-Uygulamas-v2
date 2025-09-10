import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog
import re
from collections import Counter
from heapq import nlargest

def gelismis_metin_ozetle(metin, ozet_orani):
    if not metin or not metin.strip():
        return "Lütfen özetlemek için bir metin girin."

    # Çok daha genişletilmiş kelime alternatifleri sözlüğü
    kelime_alternatifleri = {
        'ancak': 'ama', 'yüzünden': 'nedeniyle', 'dolayısıyla': 'bu yüzden', 
        'sadece': 'yalnızca', 'hemen': 'derhal', 'ayrıca': 'ek olarak', 
        'bundan başka': 'ayrıca', 'bilhassa': 'özellikle', 'birçok': 'çok', 
        'böylece': 'bununla', 'çoğunlukla': 'genellikle', 'gerçekten': 'aslında', 
        'hâlbuki': 'oysa', 'neticede': 'sonuçta', 'öncelikle': 'ilk olarak',
        'zira': 'çünkü', 'şayet': 'eğer', 'mümkün': 'olası', 'vasıtasıyla': 'ile',
        'vesilesiyle': 'sayesinde', 'oldukça': 'epey', 'daima': 'hep',
        'kâfi': 'yeterli', 'önemli': 'önem', 'büyük': 'iri',
        'fakat': 'ama', 'ile': 've', 'gerekli': 'lazım', 'göre': 'uygun',
        'hâlihazırda': 'şu an', 'hiçbir': 'hiç', 'için': 'uğruna',
        'ilave': 'ek', 'kabaca': 'yaklaşık', 'maalesef': 'ne yazık ki',
        'mutlaka': 'kesinlikle', 'nedeni': 'sebep', 'öncelik': 'ilk',
        'özellikle': 'bilhassa', 'pek': 'çok', 'sağlamak': 'vermek',
        'sayesinde': 'ile', 'söz konusu': 'bahsi geçen', 'şöyle ki': 'yani',
        'tahmin': 'sanı', 'takriben': 'yaklaşık', 'tüm': 'bütün',
        'uzun süre': 'uzun', 'yapmakta': 'yapıyor', 'yeterli': 'kâfi',
        'yukarıda': 'üstte', 'zamanla': 'gittikçe', 'zira': 'çünkü',
        'ziyadesiyle': 'fazlasıyla', 'zaman': 'vakit', 'hakikaten': 'gerçekten',
        'tamamen': 'bütün', 'hususunda': 'konusunda', 'meselesi': 'konusu',
        'husus': 'konu', 'birebir': 'aynı', 'çarpıcı': 'dikkat çekici',
        'farklı': 'başka', 'bilakis': 'aksine', 'bununla birlikte': 'ayrıca',
        'daha da': 'daha', 'eğer ki': 'eğer', 'hem de': 'ayrıca',
        'her ne kadar': 'ne kadar', 'herhangi bir': 'bir', 'içinde': 'içinde',
        'kapsamında': 'dahil', 'netice itibarıyla': 'sonuçta',
        'öte yandan': 'ayrıca', 'özetlemek gerekirse': 'kısaca', 'sadece': 'yalnızca',
        'son derece': 'çok', 'şekilde': 'biçimde', 'tarafından': 'tarafından',
        'veya': 'ya da', 'zaman': 'vakit', 'bir anlamda': 'yani', 'dolaylı olarak': 'üstü kapalı',
        'esas itibarıyla': 'temelde', 'hâlihazırda': 'şu an', 'nezdinde': 'katında',
        'muhtemelen': 'büyük ihtimalle', 'tabii ki': 'elbette'
    }

    # Metindeki uzun kelimeleri kısa alternatifleriyle değiştir
    for uzun, kisa in kelime_alternatifleri.items():
        metin = metin.replace(uzun, kisa)
    
    # 1. Metni cümlelere ve kelimelere ayır
    cumleler = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!)\s', metin)
    kelimeler = re.findall(r'\b\w+\b', metin.lower())

    # 2. Durak kelimelerini (stopwords) filtrele
    durak_kelimeler = set([
        'bir', 'bu', 've', 'ile', 'ama', 'için', 'olan', 'olarak', 'gibi', 'de', 'da',
        'en', 'çok', 'daha', 'yani', 'gerek', 'ki', 'mi', 'ne', 'ise', 'her', 'tarafından'
    ])
    onemli_kelimeler = [kelime for kelime in kelimeler if kelime not in durak_kelimeler]

    # 3. Kelime frekanslarını hesapla
    kelime_frekanslari = Counter(onemli_kelimeler)

    # 4. Cümleleri puanla
    cumle_puanlari = {}
    for i, cumle in enumerate(cumleler):
        if len(cumle) < 10:  # Kısa cümleleri ele
            continue
        for kelime in re.findall(r'\b\w+\b', cumle.lower()):
            if kelime in kelime_frekanslari:
                if cumle not in cumle_puanlari:
                    cumle_puanlari[cumle] = 0
                cumle_puanlari[cumle] += kelime_frekanslari[kelime]

    # 5. En yüksek puana sahip cümleleri seç
    if not cumle_puanlari:
        return ""
        
    ozet_cumle_sayisi = int(len(cumleler) * ozet_orani)
    if ozet_cumle_sayisi == 0 and len(cumleler) > 0:
        ozet_cumle_sayisi = 1
    
    en_onemli_cumleler = nlargest(ozet_cumle_sayisi, cumle_puanlari, key=cumle_puanlari.get)
    
    # 6. Orijinal sıraya göre özeti oluştur
    en_onemli_cumleler.sort(key=lambda x: cumleler.index(x))
    
    return ' '.join(en_onemli_cumleler)

# Dosyayı kaydetme fonksiyonu
def save_file():
    ozet_metin = ozet_cikti.get("1.0", tk.END).strip()
    if ozet_metin == "" or ozet_metin == "Lütfen özetlemek için bir metin girin.":
        return

    dosya_yolu = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Metin Dosyaları", "*.txt"), ("Tüm Dosyalar", "*.*")]
    )
    if dosya_yolu:
        with open(dosya_yolu, "w", encoding="utf-8") as file:
            file.write(ozet_metin)

# GUI (Arayüz) fonksiyonu
def ozetle_button_click():
    metin = metin_girdi.get("1.0", tk.END).strip()
    ozet_oran = ozet_orani_kaydirici.get() / 100.0
    
    ozet_metin = gelismis_metin_ozetle(metin, ozet_oran)
    
    ozet_cikti.config(state=tk.NORMAL)
    ozet_cikti.delete("1.0", tk.END)
    ozet_cikti.insert(tk.END, ozet_metin)
    ozet_cikti.config(state=tk.DISABLED)

# Ana pencereyi oluştur
ana_pencere = tk.Tk()
ana_pencere.title("Gelişmiş Metin Özetleme Uygulaması")
ana_pencere.geometry("800x600")

# Menü çubuğunu oluştur
menubar = tk.Menu(ana_pencere)
ana_pencere.config(menu=menubar)

# "Dosya" menüsünü oluştur
file_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="Dosya", menu=file_menu)
file_menu.add_command(label="Farklı Kaydet", command=save_file)

# Çerçeveleri oluştur
sol_cerceve = ttk.Frame(ana_pencere, padding="10")
sol_cerceve.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

sag_cerceve = ttk.Frame(ana_pencere, padding="10")
sag_cerceve.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

# Sol taraf (Metin Girişi ve Ayarlar)
ttk.Label(sol_cerceve, text="Orijinal Metni Buraya Yapıştırın:", font=("Arial", 12, "bold")).pack(pady=(0, 5))
metin_girdi = scrolledtext.ScrolledText(sol_cerceve, wrap=tk.WORD, width=40, height=20, font=("Arial", 10))
metin_girdi.pack(fill=tk.BOTH, expand=True)

ttk.Label(sol_cerceve, text="Özetleme Oranı:", font=("Arial", 10)).pack(pady=(10, 0))
ozet_orani_kaydirici = ttk.Scale(sol_cerceve, from_=10, to=90, orient=tk.HORIZONTAL, length=200)
ozet_orani_kaydirici.set(30)
ozet_orani_kaydirici.pack()

ttk.Button(sol_cerceve, text="Özetle", command=ozetle_button_click).pack(pady=(10, 0))

# Sağ taraf (Özet Çıktısı)
ttk.Label(sag_cerceve, text="Özetlenmiş Metin:", font=("Arial", 12, "bold")).pack(pady=(0, 5))
ozet_cikti = scrolledtext.ScrolledText(sag_cerceve, wrap=tk.WORD, width=40, height=20, font=("Arial", 10), state=tk.DISABLED)
ozet_cikti.pack(fill=tk.BOTH, expand=True)

# Uygulamayı başlat
ana_pencere.mainloop()
