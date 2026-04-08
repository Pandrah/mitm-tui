une opération contiendra plusieurs attaques 

un module de scan ping sweep

un module de routage de paquets 

operation

classes hosts 

- hostname
- ip
- mac

class attaque:

- host victim
- <ip> "is at" <mac>
- attack()

- pouvoir cancel le scan ping sweep ?
le faire en threadé avec la progress bar de textual
afficher le temps de scan restant ?


attention au masque de sous réseau trop petit, on peut rester bloqué à scanner pendant trop longtemps

requirements.txt


avoir une option pour scan avec scapy (arp comme dans l'exemple, vérifier si le user est root)
\nsudo ./venv/bin/python main.py
