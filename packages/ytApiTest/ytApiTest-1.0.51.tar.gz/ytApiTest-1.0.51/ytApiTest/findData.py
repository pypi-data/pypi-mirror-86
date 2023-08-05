import jsonpath

class FindData():


    def find_expr_value(self, json_expr,find_obj):
        '''
        查找yaml文件数据
        :param json_expr:
        :return:
        '''
        new_json_expr = self.get_json_expr_find_expr(json_expr)

        # print('-------------')
        # print(new_json_expr)
        # print('-------------')
        # print(find_obj)


        index = self.get_json_expr_index(json_expr)
        json_value = jsonpath.jsonpath(find_obj, new_json_expr)
        if json_value == False: return json_expr
        if index != -1 and json_value:
            return json_value[index]
        return json_value


    def get_json_expr_index(self, json_expr):
        '''
        截取json_expr 下标
        :param json_expr:
        :return:
        '''
        if json_expr.find('/') == -1: return -1
        return int(json_expr.split('/')[-1])


    def get_json_expr_find_expr(self, json_expr):
        '''
        分割查找表达式
        :param json_expr:
        :return:
        '''
        if json_expr.find('/') == -1: return json_expr

        expr = json_expr.split('/')[0]

        if expr.find('-') == -1:
            expr_list = expr.split('.')
            expr_list.insert(1,'[*]')
            new_expr = '.'.join(expr_list)
            return new_expr

        return expr

if __name__ == '__main__':
    FindData().get_json_expr_find_expr('$.adminTenantCreate_data.adminTenantCreate_data.req_data.tenantName/0',True)