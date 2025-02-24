import requests
import zipfile
import os
import sys
import subprocess

def check_for_updates():
    repo_url = "https://api.github.com/repos/xdjanisxd/AccountManager/releases/latest"
    try:
        response = requests.get(repo_url)
        if response.status_code == 200:
            latest_release = response.json()
            latest_version = latest_release['tag_name']
            
            # Mevcut sürümü bir dosyadan okuyun veya sabit bir değer olarak tanımlayın
            current_version = "v.3172"  # Örnek olarak
            
            if latest_version != current_version:
                print(f"Yeni sürüm bulundu: {latest_version}")
                update_program(latest_release['zipball_url'])
            else:
                print("Program güncel.")
        else:
            print("Güncelleme kontrol edilirken bir hata oluştu.")
    except Exception as e:
        print(f"Hata: {e}")

def update_program(download_url):
    print("Güncelleme indiriliyor...")
    try:
        response = requests.get(download_url)
        with open("update.zip", "wb") as file:
            file.write(response.content)
        
        print("Güncelleme indirildi. Yükleniyor...")
        with zipfile.ZipFile("update.zip", 'r') as zip_ref:
            zip_ref.extractall("temp_update")
        
        # Güncelleme dosyalarını ana dizine taşıyın
        for root, dirs, files in os.walk("temp_update"):
            for file in files:
                src_path = os.path.join(root, file)
                dest_path = os.path.join(".", os.path.relpath(src_path, "temp_update"))
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                os.replace(src_path, dest_path)
        
        print("Güncelleme tamamlandı. Programı yeniden başlatın.")
        subprocess.Popen([sys.executable, "main.py"])  # Programı yeniden başlatın
        sys.exit()
    except Exception as e:
        print(f"Güncelleme sırasında bir hata oluştu: {e}")

if __name__ == "__main__":
    check_for_updates()