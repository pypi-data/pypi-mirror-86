import os
from scapy.all import *
import argparse
import requests
import urllib.request
from progressbar import ProgressBar

def simple_traceroute() :
    from firebase import firebase

    db_conn = firebase.FirebaseApplication('https://capitrain.firebaseio.com/', None)
    database_ips = db_conn.get('/traceroute/', '')
    target_ips = []
    pbar = ProgressBar()

    url = "https://ipinfo.io/?token=1ec60bcab59f26"
    call_for_ip = requests.get(url)
    my_ip = call_for_ip.json()['ip']

    for key, value in database_ips.items():
        if my_ip != value[-1]['ip'] :
            target_ips.append(value[-1]['ip'])
    final_ips = list(set(target_ips))

    result, unans = traceroute(final_ips, l4=UDP(sport=RandShort())/DNS(qd=DNSQR(qname="www.google.com")))
    list_of_ips = []

    for res in final_ips :
        list_of_ips.append({res:[my_ip]})
        for ret in result.get_trace().get(res).items():
            list_of_ips[-1][res].append(ret[1][0])
        list_of_ips[-1][res].append(res)

    pbar = ProgressBar()
    for ips in pbar(list_of_ips) :
        for tr in ips.values() :
            location_list = []
            for i in tr : 
                url = "https://ipinfo.io/" + i + "?token=1ec60bcab59f26"
                #url = "http://ipwhois.app/json/" + ip
                call = requests.get(url)
                if 'bogon' not in call.json() :
                    location_list.append({"ip" : i, "location" : {"longitude" : call.json()['loc'].split(',')[1], "latitude" : call.json()['loc'].split(',')[0], "city" : call.json()['city']}})
            db_conn = firebase.FirebaseApplication('https://capitrain.firebaseio.com/', None)
            db_conn.post('/traceroute/', location_list)

    return list_of_ips

def traceroute_to_ip(ip):
    from firebase import firebase
    target = ip
    ip_list = []
    location_list = []
    result, unans = traceroute(target, l4=UDP(sport=RandShort())/DNS(qd=DNSQR(qname="www.google.com")))
    for snd, rcv in result :
        ip_list.append(rcv.src)
    url = "https://ipinfo.io/?token=1ec60bcab59f26"
    call_for_ip = requests.get(url)
    server_ip = call_for_ip.json()['ip']
    ip_list.insert(0, server_ip)
    ip_list.append(ip)
    for ips in ip_list :
        url = "https://ipinfo.io/" + ips + "?token=1ec60bcab59f26"
        #url = "http://ipwhois.app/json/" + ip
        call = requests.get(url)
        if 'bogon' not in call.json() :
            location_list.append({"ip" : ips, "location" : {"longitude" : call.json()['loc'].split(',')[1], "latitude" : call.json()['loc'].split(',')[0], "city" : call.json()['city']}})

    db_conn = firebase.FirebaseApplication('https://capitrain.firebaseio.com/', None)
    result = db_conn.post('/traceroute/', location_list)

def install_npcap():
    if platform.system() == 'Windows' :
        url ="https://nmap.org/npcap/dist/npcap-1.00.exe"
        filename = 'npcap.exe'
        
        urllib.request.urlretrieve(url, filename)
        os.system(filename)
    

def main() :

    try:
        from firebase import firebase    
    except ImportError:
        import pip
        pip.main(['install', '--user', 'git+git://github.com/ozgur/python-firebase@0d79d7609844569ea1cec4ac71cb9038e834c355'])
        from firebase import firebase 

    parser = argparse.ArgumentParser(
        description= "Traceroute Python - Windows Edition"
    )

    parser.add_argument('--ip', help="IP Address of the target")
    parser.add_argument('--all', help="Traceroute to all IPs in database", action='store_true')
    parser.add_argument('--install', help="Install npcap for windows", action='store_true')

    args = parser.parse_args()

    if args.ip :
        traceroute_to_ip(args.ip)
    elif args.all :
        simple_traceroute()
    elif args.install :
        install_npcap()


