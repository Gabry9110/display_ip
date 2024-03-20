# display_ip
Mostra indirizzi IP (pubblico e privato) di un Raspberry Pi su un display OLED I2C (SSD1306 128x64, come [questo](https://it.aliexpress.com/item/1005006373062872.html)) e su una API HTTP
Si avvia tramite servizio [systemd](https://systemd.io/), e lo script viene eseguito dalla cartella /media/

# Installazione
Collegare il display ai pin [GPIO](https://pinout.xyz/) corretti nel Raspberry Pi ed eseguire questi comandi da terminale

```
git clone https://github.com/Gabry9110/display_ip.git
sudo apt install python3-flask python3-luma.oled -y
sudo mv display_ip/display_ip.py /media
sudo mv display_ip/display_ip.service /etc/systemd/system
sudo systemctl enable --now display_ip.service
```
