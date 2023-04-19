#!/usr/bin/env python3

import scapy.all as scapy
# импорт для аргументов
import argparse

# фун для аргум
def get_arg():
    pars = argparse.ArgumentParser()
    # создаем аргуемнты и их значения
    pars.add_argument("-t","--target", dest="target", help="Target IP")
    # вызывзаем агрументы
    options = pars.parse_args()
    return options

# фун поиска  ip
def scan(ip):
    # здесь мы создаем запрос который есть в пакете
    # scapy.arping(ip)

    # созда переменную которая будет отправлять запросы и хранить в себе свои ip
    arg_request = scapy.ARP(pdst=ip)#передали запросы
    # укз шировещатильный адрес
    brodcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    # комбинируем
    arg_requst_brodcast = brodcast/arg_request
    # выводим полученные ответы  где получаем ответы полученые и нет
    answer = scapy.srp(arg_requst_brodcast, timeout=1, verbose=False)[0]# огр времени на запрос, также убираем 
загаловок не нужный и укз индекс так как в ответе два значения
    # создаем массив для перебора 
    clients_list = []
    # пишем цикл для перебора
    for el in answer:
        # созда массив который будем перебирать
        client_dict = {"ip": el[1].psrc, "mac": el[1].hwsrc}
        # добавляем элемент
        clients_list.append(client_dict)
    return clients_list
        # выводим где индекс это нужные нам данные
        # print(el[1].psrc + "\t\t" +  el[1].hwsrc)#ip с полученного запроса и mac с полученного запроса
    
#фун вывода на экран
def print_results(results_list):
    # делаем свою таблицу 
    print("IP\t\t\tMAC Address\n-----------------------------------------")
    # итерируем все полученое выше
    for client in results_list:
        # получаем в нормальном виде из массива
        print(client["ip"] + "\t\t" + client["mac"])

# вызываем аргум
options = get_arg()
# выведит ip точки доступа (route -n)
scan_res = scan("172.18.0.1/24")
print_results(scan_res)
