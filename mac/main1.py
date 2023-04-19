#!/usr/bin/env python3

# metod for change mac-addres
import subprocess

# metod for --help and argument for linux terminal
import optparse

# regular options (expression), or search MAC-address for us
import re

# func for parse user
def get_arguments():
    # use optparse
    parser = optparse.OptionParser()
    # commands for argiment
    parser.add_option("-i", "--interface", dest="interface", help="Change name MAC address")
    parser.add_option("-m", "--mac", dest="new_mac", help="Change MAC address")
    # parser argument users, where options for users and arguments(comannds)
    (options, arguments) = parser.parse_args()
    # this is for try full text change mac-address, if use one options then this if-elif
    if not options.interface:
        parser.error("[-] Please you need write name for MAC-address or use --help")
    elif not options.new_mac:
        parser.error("[-] Please you need write MAC-address or use --help")
    return options

# function for new MAC-address
def change_mac(interface, new_mac):
    # method for input user
    # method 1
    print("[+] Change Mac address for " + interface + " to " + new_mac)
    # method 2
    subprocess.call(['ifconfig', interface, "down"])
    subprocess.call(['ifconfig', interface, "hw", "ether", new_mac])
    subprocess.call(['ifconfig', interface, "up"])

# func for get MAC address with all step
def get_mac_address(interface):
    # 1 step - which ifconfig with check_uot where [cmd, func-input]
    ifconf_result = str(subprocess.check_output(["ifconfig", interface]))
    # 2 step - search MAC-address and use re where [search for python, MAC-address(this need str or utf8 beacouse not found)]
    mac_search = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconf_result)
    # print where group 0 - this first coincidence and [if] for not MAC-address
    if mac_search:
        # for no found - for return MAC-address
        return mac_search.group(0)
    else:
        print("[-] This interface not found MAC-address")

# use func  get_arg
options = get_arguments()

# use func get_mac for user write
mac_address_found = get_mac_address(options.interface)
# str - beacouse Linux read str
print("Found MAC-address on computer " + str(mac_address_found))

# use func change_mac
change_mac(options.interface, options.new_mac)

# use func get_mac for == with MAC-address on computer
mac_address_found = get_mac_address(options.interface)
if mac_address_found == options.new_mac:
    print("[+] Successfuly change on new MAC address to " + mac_address_found)
else:
    print("[-] MAC-address no changed on new")
# print("Found MAC-address " + str(mac_address_found))

# 1 step - which ifconfig with check_uot where [cmd, func-input]
# ifconf_result = str(subprocess.check_output(["ifconfig", options.interface]))
# print(ifconf_result)

# 2 step - search MAC-address and use re where [search for python, MAC-address(this need str or utf8 beacouse not found)]
# mac_search = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconf_result)
# print where group 0 - this first coincidence and [if] for not MAC-address
# if mac_search:
#     print(mac_search.group(0))
# else:
#     print("[-] This interface not found MAC-address")

# use optparse
# parser = optparse.OptionParser()

# commands for argiment
# parser.add_option("-i", "--interface", dest="interface", help="Change name MAC address")
# parser.add_option("-m", "--mac", dest="new_mac", help="Change MAC address")

# parser argument users, where options for users and arguments(comannds)
# (options, arguments) = parser.parse_args()


# method for input user

# method 1
# interface = input("interface > ")
# new_mac = input("new MAC > ")
# print("[+] Change Mac address for " + interface + " to " + new_mac)

# method 2
# interface = options.interface
# new_mac = options.new_mac
# print("[+] Change Mac address for " + interface + " to " + new_mac)

# method 1
# subprocess.call("ifconfig " + interface + " down", shell=True)
# subprocess.call("ifconfig " + interface + " hw ether " + new_mac, shell=True)
# subprocess.call("ifconfig " + interface + " up", shell=True)

# method 2
# subprocess.call(['ifconfig', interface, "down"])
# subprocess.call(['ifconfig', interface, "hw", "ether", new_mac])
# subprocess.call(['ifconfig', interface, "up"])