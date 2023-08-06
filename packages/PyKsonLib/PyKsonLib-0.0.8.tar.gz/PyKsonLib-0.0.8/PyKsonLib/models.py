# coding=utf-8
import logging
from threading import Semaphore

import serial

"""
Works with KTHS-415BS Programmable Temperature Humidity Chamber from www.kson.com.tw
"""


class KTHS_415BS:
    def __init__(self, serial_port: str):
        logging.basicConfig(level=logging.DEBUG)
        self.port = serial.Serial(serial_port, baudrate=19200, parity=serial.PARITY_NONE,
                                  timeout=1)
        self.status_dict = {'0': "STOPPED", '1': "RUNNING", '2': "RESERVED"}
        self.pgm_list = list()
        self.pv = dict()
        self.sem = Semaphore()
        self.power_status = self.check_power_status()

    def check_power_status(self):
        self.sem.acquire()
        self.port.write('STX,0,1,A,END'.encode())
        re = self.port.read_until('END').decode().replace(" ", "")
        self.sem.release()
        if len(re) <= 10:
            return False
        return True

    def get_status(self):
        self.sem.acquire()
        self.port.write('STX,0,1,A,END'.encode())
        re = self.port.read_until('END').decode().replace(" ", "")
        self.sem.release()
        logging.debug("check status return:\n{}".format(re))
        re = re.split(",")[4:-1]
        self.pv['type'], self.pv['status'], self.pv['temperature'], self.pv['humidity'], self.pv['temp_sv'], self.pv[
            'humi_sv'] = re[0:6]

        self.pv['pgm_name'], self.pv['cycle'], self.pv['step'], self.pv['hour'], self.pv['min'], self.pv['error'] = re[
                                                                                                                    6:]

        self.pv['status'] = self.status_dict[self.pv['status']]
        logging.debug("Current Running Status:{}\n".format(self.pv['status']))
        logging.debug("Current Error Status:{}\n".format(self.pv['error']))
        return True

    def delete_pgm(self, pgm_name: str):
        self.sem.acquire()
        self.port.write('STX,0,1,D,{},END'.format(pgm_name).encode())
        re = self.port.read_until('END').decode().replace(" ", "")
        self.sem.release()
        logging.debug("delete program return:\n{}".format(re))
        return re == 'STX,1,0,D,END'

    def stop(self):
        self.sem.acquire()
        self.port.write('STX,0,1,E,END'.encode())
        re = self.port.read_until('END').decode().replace(" ", "")
        self.sem.release()
        logging.debug("stop return:\n{}".format(re))
        return re == 'STX,1,0,E,END'

    def pgm_jump_section(self, section):
        self.sem.acquire()
        self.port.write('STX,0,1,J,{},END'.format(section).encode())
        re = self.port.read_until('END').decode().replace(" ", "")
        self.sem.release()
        logging.debug("Jump section {} return:\n{}".format(section, re))
        return re == 'STX,1,0,J,END'

    def pgm_jump_next(self):
        """pgm_jump_next() funtion will jump by the next step,
        which means machine will jump from N to N+2 step and bypass N+1 step"""
        return self.pgm_jump_section('N')

    def list_all_pgm(self):
        self.sem.acquire()
        self.port.write('STX,0,1,O,END'.encode())
        re = self.port.read_until('END').decode().replace(" ", "")
        self.sem.release()
        logging.debug("Get all pgm return:\n{}".format(re))
        pgm_count = int(re.split(',')[4])
        if pgm_count >= 1:
            logging.debug("PGM count:{}".format(pgm_count))
            self.pgm_list = re.split(',')[5:-1]
            return self.pgm_list
        else:
            logging.debug("PGM count zero!")
            return None

    def load_pgm(self, pgm_name: str):
        self.get_status()
        if self.pv['status'] == 'STOPPED':
            self.sem.acquire()
            self.port.write('STX,0,1,L,{},END'.format(pgm_name).encode())
            re = self.port.read_until('END').decode().replace(" ", "")
            self.sem.release()
            logging.debug("Load program {} return:\n{}".format(pgm_name, re))
            return re == 'STX,1,0,L,END'
        else:
            return False

    def rename_pgm(self, src_pgm: str, dst_pgm: str):
        self.sem.acquire()
        self.port.write('STX,0,1,N,{},{},END'.format(src_pgm, dst_pgm).encode())
        re = self.port.read_until('END').decode().replace(" ", "")
        self.sem.release()
        logging.debug("Rename program {} to {} return:\n{}".format(src_pgm, dst_pgm, re))
        return re == 'STX,1,0,N,END'

    def view_pgm(self, pgm_name: str):
        self.sem.acquire()
        self.port.write('STX,0,1,R,{},END'.format(pgm_name).encode())
        re = self.port.read_until('END').decode().replace(" ", "")
        self.sem.release()
        logging.debug("View program {} return:\n{}".format(pgm_name, re))
        re = re.split(',')[5:-1]
        pgm_content = dict()
        pgm_content['cycle'], pgm_content['step'], pgm_content['high_limit'], pgm_content['low_limit'] = re[:4]
        steps = re[4:]
        # chunk the steps in to sections by size 8
        pgm_content['steps'] = [steps[x * 8:(x + 1) * 8] for x in range(0, int(pgm_content['step']))]
        return pgm_content

    def run_loaded_pgm(self):
        self.get_status()
        if self.pv['status'] == 'STOPPED':
            self.sem.acquire()
            self.port.write('STX,0,1,T,END'.encode())
            re = self.port.read_until('END').decode().replace(" ", "")
            self.sem.release()
            logging.debug("Run loaded program return:\n{}".format(re))
            return re == 'STX,1,0,T,END'
        else:
            logging.warning("Can only run loaded program when machine status is stopped!")
            return False

    def execute_pgm(self, pgm_name: str):
        self.get_status()
        if self.pv['status'] == 'STOPPED':
            self.sem.acquire()
            self.port.write('STX,0,1,S,{},END'.format(pgm_name).encode())
            re = self.port.read_until('END').decode().replace(" ", "")
            self.sem.release()
            logging.debug("Execute program return:\n{}".format(re))
            return re == 'STX,1,0,S,END'
        else:
            logging.warning("Can only execute program when machine status is stopped!")
            return False

    def write_pgm(self, pgm_name: str, target_temp: int, target_humi: int, target_hour: int, target_min: int):
        """due to function parameter complication,this function only support 1 target temperature and 1 target humidity
         in 2 steps,low limit and high limit setting not working,automatic set according to your temp setting,so
          we add two steps with 150 and -50C to set the limit range to -50~150"""
        cmd_str = 'STX,0,1,W,{pgm_name},1,4,{high_limit},{low_limit},{target_temp},' \
                  '{target_humi},0,0,0,0,0,0,{target_temp},{target_humi},{target_hour},' \
                  '{target_min},0,0,0,0,' \
                  '150,0,0,1,0,0,0,0,-50,0,0,1,0,0,0,0,END'.format(pgm_name=pgm_name, target_temp=target_temp,
                                                                   high_limit=100, low_limit=0, target_humi=target_humi,
                                                                   target_hour=target_hour, target_min=target_min)
        self.sem.acquire()
        self.port.write(cmd_str.encode())
        re = self.port.read_until('END').decode().replace(" ", "")
        self.sem.release()
        logging.debug("Write Program return:\n{}".format(re))
        return re == "STX,1,0,W,END"

    def close(self):
        self.port.close()
