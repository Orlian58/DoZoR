# Сетевой сканер для СОВ DOZOR

## Первый запуск для ОС Debian/Ubuntu

```bash
sudo apt update
sudo apt install -y python3-venv python3 build-essential libssl-dev libffi-dev python3-dev
cd dozor_ids
chmod 777 auto_run.sh
sudo ./auto_run.sh <your_intetface_for_listning>
```

Сервер работает на 5000 порту

Логи сохрвняются в директорию logs, каждый день новый файл
Правила загружаются в rules
