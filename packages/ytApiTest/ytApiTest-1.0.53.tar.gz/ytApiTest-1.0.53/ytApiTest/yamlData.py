
from ytApiTest.singleton import Singleton
from ytApiTest.fileManage import FileManage
from ytApiTest.findData import FindData
from ytApiTest.yamlKey import YAML_CONFIG_KEY

import yaml,jsonpath,copy


class YamlData(Singleton):
    _yaml_data_list = []
    def __init__(self):

        self._file = FileManage()
        self.find_data = FindData()

    def collect_skip_obj_yaml_data(self):

        '''
        查找项目所有yaml文件数据
        :return:
        '''

        if len(self._yaml_data_list):return self._yaml_data_list

        for path in self._file.get_obj_yaml_file_path():

            temp_dic = {}

            with open(path,encoding='UTF-8') as file:

                for yaml_dic in yaml.load_all(file,Loader=yaml.FullLoader):

                    temp_dic.update(yaml_dic)

            self._yaml_data_list.append(temp_dic)
        print('-------加载yaml文件数据--------')
        return self._yaml_data_list

    def get_interface_all_case_data(self,interface_name):
        '''
        获取接口所有用例数据
        :param interface_name:
        :return:
        '''
        interface_json_expr = '$.{}/0'.format(interface_name)
        find_value = self.find_data.find_expr_value(json_expr=interface_json_expr,find_obj=self.collect_skip_obj_yaml_data())
        return copy.deepcopy(find_value)

    def get_singleton_interface_case_data(self,interface_name,case_name):
        '''
        获取单个用例数据
        :param interface_name:
        :param case_name:
        :return:
        '''
        return self.get_interface_all_case_data(interface_name=interface_name).get(case_name)

    def get_case_interface_name(self,case_name):
        '''
        获取接口名
        :param case_name: 用例名
        :return:
        '''
        temp_value = copy.deepcopy(self.collect_skip_obj_yaml_data())
        for value in temp_value:
            if value.__contains__(YAML_CONFIG_KEY.OBJECT_HOST):
                value.pop(YAML_CONFIG_KEY.OBJECT_HOST)
            interface = [key for key ,v in value.items() if v != None and v.__contains__(case_name)]
            if len(interface):
                 return interface[0]

    def update_case_data(self,interface,case_name,req_data,update_key):
        '''请求数据
         更新用例
        :param interface:
        :param case_name:
        :param req_data:
        :return:
        '''

        if update_key == YAML_CONFIG_KEY.INTERFACE_REQUEST_DATA:
            
            expr = '$.{}.{}.{}'.format(interface,case_name,YAML_CONFIG_KEY.INTERFACE_REQUEST_DATA)

            for index,value in enumerate(self.collect_skip_obj_yaml_data()):

                find_value = jsonpath.jsonpath(value,expr)
                if find_value and find_value != None:
                    find_value = find_value[0]
                if isinstance(find_value,dict):
                    
                    find_value.update(req_data)
                
                elif find_value != False:
                    
                    self.collect_skip_obj_yaml_data()[index][interface][case_name][YAML_CONFIG_KEY.INTERFACE_REQUEST_DATA] = req_data
         
        elif case_name == YAML_CONFIG_KEY.INTERFACE_JSON_PATH:
            expr = '$.{}.{}.{}/0'.format(interface, case_name, YAML_CONFIG_KEY.INTERFACE_JSON_PATH)
            for index, value in enumerate(self.collect_skip_obj_yaml_data()):
                find_value = self.find_data.find_expr_value(find_obj=value, json_expr=expr)
                if find_value != False:
                    find_value.format(**req_data)

if __name__ == '__main__':
    pass