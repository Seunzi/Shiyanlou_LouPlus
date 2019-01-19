import sys,os

startpoint = 3500.00

class ArgError(Exception):
    pass
def get_dir(mark):
    try:
            args = sys.argv[1:]
            index = args.index(str(mark))
            fdir = str(args[index+1])
            return fdir
    except (IndexError,ValueError):
        raise  ArgError('missing arg {}'.format(mark))

class Config(object):
    _config = {}
    def __init__(self,configfile):
        try:
            if os.path.exists(configfile):
                with open(configfile,'r') as file:
                    for line in file:
                        line = line.split('=')
                        self._config[line[0].strip()] = float(line[1].strip())
            else:
                print('Configfile Error')
                exit()
        except Exception:
                print('parameter error')
                exit()

    def get_config(self,key):
        try:
            value = self._config[str(key)]
            return value
        except Exception:
            print('parameter error')
            exit()

class UserData(object):
    config = Config(get_dir('-c'))
    _userdata = {}
    result = []
    def __init__(self,userdatafile):
        try:
            if os.path.exists(userdatafile):
                with open(userdatafile,'r') as file:
                    for line in file:
                        line = line.split(',')
                        self._userdata[int(line[0].strip())] = float(line[1].strip())
            else:
                print('parameter error')
                exit()
        except Exception:
            print('userdata wrong')
            exit()

    def cal_ins(self,cnum):
        config = self.config
        insurance_rate = config.get_config('YangLao') + config.get_config('YiLiao') + config.get_config('ShiYe') + config.get_config('GongShang') + config.get_config('ShengYu') + config.get_config('GongJiJin')
        insurance = cnum * insurance_rate
        return float(insurance)

    def cal_tax(self,cnum,startpoint=startpoint):
        tax_base = cnum - self.cal_ins(cnum) - startpoint
        tax = float()
        if tax_base < 0:
            tax_base = 0
        elif tax_base <= 1500:
            tax = tax_base * 0.03 - 0
        elif tax_base <= 4500:
            tax = tax_base * 0.10 - 105
        elif tax_base <= 9000:
            tax = tax_base * 0.20 - 555
        elif tax_base <= 35000:
            tax = tax_base * 0.25 - 1005
        elif tax_base <= 55000:
            tax = tax_base * 0.30 - 2755
        elif tax_base <= 80000:
            tax = tax_base * 0.35 - 5505
        elif tax_base > 8000:
            tax = tax_base * 0.45 - 13505
        return float(tax)

    def gen_result(self,cnum,id,salary):
        insurance = self.cal_ins(cnum)
        tax = self.cal_tax(cnum)
        self.result.append('%i,%i,%.2f,%.2f,%.2f' % (id,salary,insurance,tax,(salary - insurance - tax)))

    def calculator(self):
        config = self.config
        for id,salary in self._userdata.items():
            if salary < config.get_config('JiShuL'):
                cnum = config.get_config('JiShuL') 
                self.gen_result(cnum,id,salary)

            elif salary < config.get_config('JiShuH'):
                cnum = salary
                self.gen_result(cnum,id,salary)

            elif salary >= config.get_config('JiShuH'):
                cnum = config.get_config('JiShuH')
                self.gen_result(cnum,id,salary)

        return self.result

    def dumptofile(self,outputfile):
        self.calculator()
        self.result = sorted(self.result,key = lambda list1: list1[0])
        with open(outputfile,'w') as file:
            for res in self.result:
                file.write(str(res))
                file.write('\n')
        print('Dump Done')

if __name__ == '__main__':
    run = UserData(get_dir('-d'))
    run.dumptofile(get_dir('-o'))
