#Brute_Force_Admin_Fonctionnal by 3xtr3mX ⚔️💻

🚨 Description
Welcome to the ultimate brute-force tool, Brute_Force_Admin_Fonctionnal! This Python script is designed to test admin passwords for penetration testing purposes. Use this code wisely... or not, at your own risk 😈

On powerful machines, this script can test up to 1000 passwords per second with 4 cores and 500 passwords per second with 2 cores. The number of cores to use can be adjusted at line 138 of the code according to your preferences.

Important reminders:

Use it only in a legal and ethical context.
Hacking without permission is illegal. 😈
⚡ Features
Fast brute-force attack, really fast. 🚀
Supports multi-core usage to improve performance.
Easy to configure: simply change the number of cores at line 138.
Ideal for penetration testing on admin systems (in a legitimate context).
🛠️ Prerequisites
Before diving into the brute force power of this code, make sure you have the following:

Python 3.x: Ensure Python is installed on your system.
Required Libraries:
os: For handling file systems and processes.
win32security: For managing security and permissions on Windows.
time: For handling delays and timing within the script.
multiprocessing: For managing core usage (Pool, cpu_count, Manager, Lock).

⚙️ Installation
Clone the repository or download the source code:
git clone https://github.com/3xtr3mX/Brute_Force_Admin_Fonctionnal.git
Navigate to the project directory:
cd Brute_Force_Admin_Fonctionnal
Make sure Python 3.x is installed. If not, download it here.

📄 Requirements
-pywin32
-Other libraries (os, time, multiprocessing) are included by default in Python, so no need to install them separately.

🧠 Configuration
Adjusting the number of cores:
Go to line 138 in the code and set the number of cores based on your machine. The more cores you set, the faster the execution will be. 🧨
# Line 138
cpu_cores = 4  # Change this number according to your CPU cores
Customizing the password list:
You can customize the password list by editing the password_list.txt file.

🚀 Usage
Simply run the script:
-python brute_force_admin.py
⚠️ Warning: Make sure you have explicit permission to test the target site or service with this brute-force tool. Unauthorized hacking attempts are punishable by law. ⚖️

💥 Disclaimer
This code is extremely powerful and should be used responsibly.
Never use it on systems without the explicit consent of the owners.
Malicious usage may result in legal consequences. ⚠️

🔒 License
This project is provided as-is and should be used for legitimate purposes only.
The creator (3xtr3mX) disclaims any responsibility for misuse of the script.
