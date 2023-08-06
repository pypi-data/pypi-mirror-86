from os.path import dirname,join
def get_example_data(filename):
    """
    使用包中自带的数据集
    :param filename: 数据集名称
    :return: 包中数据集的真实文件路径
    """
    print("使用包中自带的数据集:",filename)
    if filename not in ['A1.csv',
                        'A2.csv',
                        'A3.csv',
                        'A4.csv',
                        'A5.csv',
                        'AS1.csv',
                        'AS2.csv']:
        raise Exception("文件不存在，样例数据集的文件名为'A1.csv','A2.csv',"
                        + "'A3.csv','A4.csv','A5.csv','AS1.csv','AS2.csv'")
    module_path = dirname(__file__)
    file_path = join(module_path,'data',filename)
    return file_path