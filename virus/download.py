import requests

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
    
download("https://img.cliparto.com/pic/xl/180375/3014744-american-style.jpg")