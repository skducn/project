import os


def bluetooth_rssi_get():
    cmd = "system_profiler SPBluetoothDataType"
    devices = get_bluetooth_devices(cmd)

    print(devices)
    for device_name, device_info in devices.items():

        for key, value in device_info.items():
            if key == 'Connected':
                if value == 'Yes':
                    print(device_name, "连接中")
                else:
                    print(device_name, "未连接")
            if key == 'RSSI':
                print('RSSI:', value)


def get_bluetooth_devices(cmd):
    '''
    执行cmd命令获取所有蓝牙相关信息
    :param cmd: 命令行
    :return: 返回所有连接中或连接过的蓝牙设备
    '''
    r = os.popen(cmd)
    info = r.readlines()  # 读取命令行的输出到一个list
    level_map = process_info(info)
    r.close()
    return level_map2dict(level_map)["Bluetooth"]["Devices (Paired, Configured, etc.)"]


def process_info(info):
    '''
    处理命令行结果，生成根据缩进判定的层级
    :param info: 命令行结果，每行以数组形成存储
    :return: 带有层级的数组
    '''
    level_map = []
    for line in info:  # 按行遍历
        line = line.strip('\r\n')
        if len(line) > 0:  # 第二行是空行
            line_info = get_line_info(line)
            if line_info["level"] >= 0:  # 把第一行Bluetooth去除
                level_map.append(line_info)
    print(level_map)
    return level_map


def get_line_info(line):
    '''
    解析命令行每行信息
    :param line: 传入行
    :return: 根据冒号分割以及缩进，生成的每行信息(字典形式)
    '''
    split = line.split(':')
    name = split[0].lstrip(' ')
    value = split[1].lstrip(' ')
    level = (len(line) - len(line.lstrip(' ')) - 2) / 4
    if level < 0:
        level = 0  # 针对第一行

    line_info = {}
    line_info["name"] = name
    line_info["value"] = value
    line_info["level"] = level
    return line_info


def level_map2dict(ttree, level=0):
    '''
    根据层级信息转化成字典结构
    :param ttree:
    :param level:
    :return:
    '''
    result = {}
    for i in range(0, len(ttree)):
        current_node = ttree[i]
        try:
            next_node = ttree[i + 1]
        except:
            next_node = {'level': -1}

        # 边界条件，非当前层级
        if current_node['level'] > level:  # 已经作为整体插入，跳过
            continue
        if current_node['level'] < level:  # 当前是上一级的，直接返回现有结果
            return result


        # 递归生成
        if next_node['level'] == level:  # 同级
            dict_insert_or_append(result, current_node['name'], current_node['value'])
        elif next_node['level'] > level:  # 下一级，将下一级整体插入
            next_level = level_map2dict(ttree[i + 1:], level=next_node['level'])  # 剩下的进行处理
            dict_insert_or_append(result, current_node['name'], next_level)
        else:  # 下一个是上一级的，当前插入完成直接返回
            dict_insert_or_append(result, current_node['name'], current_node['value'])
            return result
    return result


def dict_insert_or_append(adict, key, val):
    '''
    针对key是否存在，新增或者添加
    :param adict:
    :param key:
    :param val:
    :return:
    '''
    if key in adict:  # 添加
        if type(adict[key]) != list:
            adict[key] = [adict[key]]  # 将单独存在的转化成list
        adict[key].append(val)
    else:  # 新增
        adict[key] = val

bluetooth_rssi_get()