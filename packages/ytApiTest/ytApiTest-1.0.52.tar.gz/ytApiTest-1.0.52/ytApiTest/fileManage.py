import os


class FileManage():

    def __init__(self):
        self._default_path = '.'

    def _get_obj_path(self):
        '''
        获取项目跟路径
        :return:
        '''
        yaml_file_path_list = []
        for dirpath, dirnames, filenames in os.walk(self._default_path):
            temp_obj = [yaml_file_name for yaml_file_name in filenames if yaml_file_name.endswith(".yaml")]
            if temp_obj:
                path = [os.path.join(dirpath, yaml_file_path) for yaml_file_path in temp_obj]
                yaml_file_path_list.extend(path)

        return yaml_file_path_list

    def get_obj_yaml_file_path(self):

        if self._get_obj_path():

            return self._get_obj_path()
        else:
            self._default_path = '..'
            return self._get_obj_path()


