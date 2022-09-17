import subprocess
import sys
import os

def install(package):
    #subprocess.check_call([sys.executable, "-m", "pip", "install", str(package)])
    os.system("pip install " + str(package))
    reqs = subprocess.check_output([sys.executable, '-m', 'pip', 'show', str(package)])

    print(str(reqs) + "\n")
    print("Installed " + package.upper() + "\n")

install("scrapy")   # En caso de no andar, fijate en los marcadores de JSPY de google que ahi hay un link para bajar
# el Twisted de forma manual, y ahi podes poner "pip install Twisted-20.3.0-cp39-cp39-win_amd64.whl" o algo asi y
# despues instalas el pip scrapy y listo y tendria que andar
install("requests")
install("mysql-connector-python")
install("pandas")
install("xlrd")
install("xlwt")
install("selenium")
install("fake_useragent")
install("beautifulsoup4")
install("auto-py-to-exe")
install("openpyxl")
#install("requests")

# install("beautifulsoup4")
# install("ruamel.yaml")
# install("selenium")
# install("webdriver_manager")