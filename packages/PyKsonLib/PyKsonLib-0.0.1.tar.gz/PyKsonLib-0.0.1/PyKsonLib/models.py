# coding=utf-8
import logging
import serial

"""
Works with KTHS-415BS Programmable Temperature Humidity Chamber from www.kson.com.tw
"""


class KTHS_415BS:
    def __init__(self, serial_port: str):
        logging.basicConfig(level=logging.DEBUG)
        self.port = serial.Serial(serial_port, baudrate=19200, parity=serial.PARITY_NONE,
                                  timeout=1)
        self.type = self.status = self.temp_pv = self.humi_pv = self.temp_sv = self.humi_sv = '0'
        self.pgm_name = self.cycle = self.step = self.hour = self.min = self.error = '0'
        self.status_dict = {'0': "STOPPED", '1': "RUNNING", '2': "RESERVED"}
        self.error_dict = {'0': 'No Error', '1': 'Temp sensor error', '2': 'Humid sensor error',
                           '3': 'Temp&Humid converter error',
                           '4': 'Communication off', '5': 'Internal over high temp', '6': 'Internal over low temp',
                           '7': 'Low humid sensor error', '8': 'Environment over high temp',
                           '9': 'Environment sensor error',
                           '10': 'Low humid converter error', '11': 'External over high temp', '12': 'Water shortage',
                           '13': 'C1 compressor error', '14': 'C2 compressor error', '15': 'Gas/Water pressure',
                           '16': 'C1 compressor over load', '17': 'C2 compressor over load', '18': 'Fan over load'}
        self.pgm_list = list()

    def get_status(self):
        self.port.write('STX,0,1,A,END'.encode())
        re = self.port.read(100).decode().replace(" ", "")
        logging.debug("check status return:\n{}".format(re))
        re = re.split(",")[4:-1]
        self.type, self.status, self.temp_pv, self.humi_pv, self.temp_sv, self.humi_sv = re[0:6]
        self.pgm_name, self.cycle, self.step, self.hour, self.min, self.error = re[6:]
        logging.info("Current Running Status:{}\n".format(self.status_dict[self.status]))
        logging.info("Current Error Status:{}\n".format(self.error_dict[self.error]))
        return None

    def delete_pgm(self, pgm_name: str):
        self.port.write('STX,0,1,D,{},END'.format(pgm_name).encode())
        re = self.port.read(100).decode().replace(" ", "")
        logging.debug("delete program return:\n{}".format(re))
        return re == 'STX,1,0,D,END'

    def stop(self):
        self.port.write('STX,0,1,E,END'.encode())
        re = self.port.read(100).decode().replace(" ", "")
        logging.debug("stop return:\n{}".format(re))
        return re == 'STX,1,0,E,END'

    def pgm_jump_section(self, section):
        self.port.write('STX,0,1,J,{},END'.format(section).encode())
        re = self.port.read(100).decode().replace(" ", "")
        logging.debug("Jump section {} return:\n{}".format(section, re))
        return re == 'STX,1,0,J,END'

    def pgm_jump_next(self):
        """pgm_jump_next() funtion will jump by the next step,
        which means machine will jump from N to N+2 step and bypass N+1 step"""
        return self.pgm_jump_section('N')

    def list_all_pgm(self):
        self.port.write('STX,0,1,O,END'.encode())
        re = self.port.read(1000).decode().replace(" ", "")
        logging.debug("Get all pgm return:\n{}".format(re))
        pgm_count = int(re.split(',')[4])
        if pgm_count >= 1:
            logging.debug("PGM count:{}".format(pgm_count))
            self.pgm_list = re.split(',')[5:-1]
        else:
            logging.debug("PGM count zero!")
            return None

    def load_pgm(self, pgm_name: str):
        self.port.write('STX,0,2,L,{},END'.format(pgm_name).encode())
        re = self.port.read(100).decode().replace(" ", "")
        logging.debug("Load program {} return:\n{}".format(pgm_name, re))
        return re == 'STX,1,0,L,END'

    def rename_pgm(self, src_pgm: str, dst_pgm: str):
        self.port.write('STX,0,1,N,{},{},END'.format(src_pgm, dst_pgm).encode())
        re = self.port.read(100).decode().replace(" ", "")
        logging.debug("Rename program {} to {} return:\n{}".format(src_pgm, dst_pgm, re))
        return re == 'STX,1,0,N,END'

    def view_pgm(self, pgm_name: str):
        self.port.write('STX,0,1,R,{},END'.format(pgm_name).encode())
        re = self.port.read(1000).decode().replace(" ", "")
        logging.debug("View program {} return:\n{}".format(pgm_name, re))
        re = re.split(',')[5:-1]
        pgm_content = dict()
        pgm_content['cycle'], pgm_content['step'], pgm_content['high_limit'], pgm_content['low_limit'] = re[:4]
        steps = re[4:]
        print(pgm_content['step'])
        # chunk the steps in to sections by size 8
        pgm_content['steps'] = [steps[x * 8:(x + 1) * 8] for x in range(0, int(pgm_content['step']))]
        return pgm_content

    def run_loaded_pgm(self):
        self.get_status()
        if self.status_dict[self.status] == 'STOPPED':
            self.port.write('STX,0,1,T,END'.encode())
            re = self.port.read(100).decode().replace(" ", "")
            logging.debug("Run loaded program return:\n{}".format(re))
            return re == 'STX,1,0,T,END'
        else:
            logging.warning("Can only run loaded program when machine status is stopped!")
            return False

    def execute_pgm(self, pgm_name: str):
        self.get_status()
        if self.status_dict[self.status] == 'STOPPED':
            self.port.write('STX,0,1,S,{},END'.format(pgm_name).encode())
            re = self.port.read(100).decode().replace(" ", "")
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
        print(cmd_str)
        self.port.write(cmd_str.encode())
        re = self.port.read(100).decode().replace(" ", "")
        logging.debug("Write Program return:\n{}".format(re))
        return re == "STX,1,0,W,END"

    def close(self):
        self.port.close()
