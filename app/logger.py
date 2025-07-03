import logging  
import sys  
  
# установка имени  
logger = logging.getLogger('logger')  
  
# установка уровня  
logger.setLevel(logging.DEBUG)  
  
# установка формата вывода сообщений  
formatter = logging.Formatter('[%(asctime)s] #%(levelname)-8s %(filename)s:'  
                '%(lineno)d - %(name)s - %(funcName)s - %(message)s')  
  
# Добавление хендлера  
stdout_handler = logging.StreamHandler(sys.stdout)  
file_handler = logging.FileHandler('app.log')
  
# Установка формата вывода сообщений для хендлера  
stdout_handler.setFormatter(formatter)  
  
# Добавление хендлера к логгеру  
logger.addHandler(stdout_handler)
logger.addHandler(file_handler)
