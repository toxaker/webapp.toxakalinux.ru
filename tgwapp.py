import socket
import subprocess
import psutil
import shutil
import smtplib
import os
import re
import concurrent.futures
from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from email.mime.text import MIMEText
from loguru import logger
from functools import wraps
import requests
import logging
import random
import time
import ipaddress
from telegram import Bot

TOKEN='BOT_TOKEN'
token = TOKEN

app = Flask(__name__)

logging.basicConfig(filename='app.log', level=logging.DEBUG)
app.logger.debug('Понеслась пизда по кочкам!')

@app.before_request
def log_request_info():
    logging.info(f"Request from {request.remote_addr} to {request.url}")

def is_valid_ip(ip):
    ip_regex = re.compile(
        r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$"
    )
    domain_regex = re.compile(
        r"^(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,6}$"  # Validate domains
    )
    return ip_regex.match(ip) or domain_regex.match(ip)

def is_valid_ip(ip):
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False



# Home Page
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/main')
def main ():
    return render_templates('main.html')

@app.route('/submit_data', methods=['POST'])
def submit_data():
    data = request.json
    # Process data and send it to the bot or save to the database
    print(data)
    return jsonify({"status": "success", "message": "Data received"})

@app.route('/tools')
def tools():
    return render_template('tools.html')

@app.route('/tools/webtools')
def webtools():
    return render_template('webtools.html')

@app.route('/tools/scantools')
def scantools():
    return render_template('scantools.html')

@app.route('/tools/advancedtools')
def advancedtools():
    return render_template('advancedtools.html')

# Information Page
@app.route('/info')
def info():
    return render_template('info.html')

# Tutorial Page
@app.route('/tutorial')
def tutorial():
    return render_template('tutorial.html')

# Developers Page
@app.route('/developers')
def developers():
    return render_template('developers.html')

# Donate Page
@app.route('/donate')
def donate():
    return render_template('donate.html')

# Task execution logic (adapted from old tasks)
@app.route('/run_task', methods=['POST'])
def run_task():
    task = request.form.get('task')
    tasks_mapping = {
        'check_ports': check_ports,
        'monitor_network': monitor_network,
        'monitor_processes': monitor_processes,
        'scan_nikto': scan_nikto,
        'create_backup': create_backup,
        'start_scan': start_scan,
    }
    if task in tasks_mapping:
        result = tasks_mapping[task]()
    else:
        result = f"Unknown task: {task}"
    return render_template('result.html', result=result)

# Log attacks
def save_log(attack_type, log_data):
    with open(f'{attack_type}_log.txt', 'a') as log_file:
        log_file.write(log_data + '\n')

# Example: Old attack feature reworked
@app.route('/t50', methods=['POST'])
def t50_attack():
    data = request.json
    target = data.get('target')
    port = data.get('port', 80)
    packet_type = data.get('packetType', 'SYN')

    if not target:
        return jsonify({'message': 'IP или домен цели обязателен!'}), 400

    command = f"sudo t50 {target} --dport {port} --{packet_type}"

    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            save_log("t50", result.stdout + result.stderr)
            return jsonify({'message': 'T50 успешно запущен'})
        else:
            return jsonify({'message': f'Ошибка: {result.stderr}'})
    except Exception as e:
        return jsonify({'message': f'Ошибка: {e}'})

# Function to check open ports
def check_ports():
    ports_info = []
    for conn in psutil.net_connections(kind='inet'):
        if conn.status == psutil.CONN_LISTEN:
            ports_info.append(f"IP: {conn.laddr.ip}, Port: {conn.laddr.port}")
    return ports_info

@app.route('/scan_ports', methods=['POST'])
def scan_ports():
    data = request.get_json()
    ip = data.get('ip', '')

    if not is_valid_ip(ip):
        return jsonify({'error': 'Некорректный IP-адрес'}), 400
    
    # Основная логика для сканирования портов
    open_ports = run_port_scan(ip)
    return jsonify({'open_ports': open_ports})


# Monitor network connections
def monitor_network():
    network_info = []
    for net in psutil.net_if_addrs():
        network_info.append(str(net))
    return network_info

# Monitor system processes
def monitor_processes():
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'username']):
        processes.append(proc.info)
    return processes

# Create backup
def create_backup():
    source_dir = "/path/to/source"
    backup_dir = "/path/to/backup"
    shutil.copytree(source_dir, backup_dir)
    return f"Backup created from {source_dir} to {backup_dir}"

# Scan using Nikto
def scan_nikto():
    command = "nikto -h http://example.com"
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.stdout if result.returncode == 0 else f"Ошибка: {result.stderr}"
    except Exception as e:
        return f"Ошибка: {e}"

# Start scan
def start_scan():
    return "Scan started"

try:
    with open(f'{attack_type}_log.txt', 'a') as log_file:
        log_file.write(log_data + '\n')
except Exception as e:
    logging.error(f"Ошибка записи лога: {e}")



def geoip_lookup(ip):
    try:
        response = requests.post('https://geoip.example.com', json={'ip': ip}, timeout=10)
        return response.json()
    except Timeout:
        return {'error': 'Запрос превысил допустимое время ожидания'}

@app.route('/webapphook', methods=['POST'])
def webhook():
    data = request.get_json()
    if data:
        chat_id = data['message']['chat']['id']
        text = data['message']['text']
        # Ответ пользователю
        reply(chat_id, text)
    return 'ok', 200

def reply(chat_id, text):
    url = f"https://api.telegram.org/bot{os.getenv('BOT_TOKEN')}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': f"Вы сказали: {text}"
    }
    requests.post(url, json=payload)

if __name__ == '__main__':
    app.run(debug=True)
