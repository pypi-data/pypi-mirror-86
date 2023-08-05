_indent = '    '
_change_line = '\n'
_func_define = 'def '
_func_return = 'return'


class frame_constructor(object):
    def __init__(self,db_name,table_struct,file_path,file_name):
        self.table_struct = table_struct
        self.db_name = db_name
        self.file_path = file_path
        self.file_name = file_name
        self.fh = open(self.file_path+self.file_name,'w')


    def dump(self):
        self.add_file_title()
        for table_name,table_frame in self.table_struct.items():
            self.construct_table(table_name,table_frame)

        self.fh.close()

    def add_file_title(self):
        self.fh.write('from anduin.server import Data')
        self.changeline()
        self.changeline()

    def construct_table(self,table_name,table_frame):
        self.construct_func_def(table_name)
        self.changeline()
        self.indent()
        self.write_drop_table(table_name)
        self.changeline()
        self.indent()
        self.write_table_frame(table_frame)
        self.write_create_table(table_name)
        self.changeline()
        self.indent()
        self.add_return()
        self.changeline(2)
    def construct_func_def(self,func_name):
        self.fh.write(_func_define + func_name + '():')

    def add_return(self):
        self.fh.write(_func_return)

    def indent(self,indent_multi = 1):
        self.fh.write(_indent*indent_multi)

    def changeline(self,change_mult = 1):
        self.fh.write(_change_line*change_mult)

    def write_comment(self,content):
        for i in content.split('\n'):
            self.fh.write('#'+i)

    def write_drop_table(self,table_name):
        self.fh.write('Data.query("drop table %s.%s")' % (self.db_name, table_name))

    def write_table_frame(self, table_frame):
        self.fh.write('column = [')
        self.changeline()
        for line in table_frame:
            self.indent(2)
            self.fh.write('(')
            # for word in line:
            self.fh.write('"%s", "%s", '%(line[0],line[1]))
            if line[4] != None:
                self.fh.write('"default \'%s\'"'%line[4])
            if 'PRI' in line:
                self.fh.write('"%s", "%s", '%('AUTO_INCREMENT','primary key'))
            self.fh.write('),')
            self.changeline(2)
            pass
        self.indent()
        self.fh.write(']')
        self.changeline()

    def write_create_table(self, table_name):
        self.indent()
        self.fh.write('Data.create(%s , column)'%table_name)








