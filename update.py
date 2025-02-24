import requests
import json
import os

def check_for_updates():
    # GitHub'daki glist.json dosyasının raw URL'si
    glist_url = "https://raw.githubusercontent.com/xdjanisxd/AccountManager/main/glist.json"
    
    try:
        # GitHub'dan glist.json dosyasını indir
        response = requests.get(glist_url)
        if response.status_code == 200:
            # İndirilen içeriği mevcut glist.json dosyasıyla karşılaştır
            if os.path.exists("glist.json"):
                with open("glist.json", "r", encoding="utf-8") as file:
                    current_content = file.read()
                
                if current_content != response.text:
                    # Dosya güncel değilse, güncelle
                    with open("glist.json", "w", encoding="utf-8") as file:
                        file.write(response.text)
                    print("glist.json dosyası güncellendi.")
                else:
                    print("glist.json dosyası zaten güncel.")
            else:
                # glist.json dosyası yoksa, oluştur
                with open("glist.json", "w", encoding="utf-8") as file:
                    file.write(response.text)
                print("glist.json dosyası oluşturuldu.")
        else:
            print(f"glist.json dosyası indirilirken bir hata oluştu. HTTP Status Code: {response.status_code}")
            print(f"Hata Mesajı: {response.text}")
    except Exception as e:
        print(f"Hata: {e}")

if __name__ == "__main__":
    check_for_updates()