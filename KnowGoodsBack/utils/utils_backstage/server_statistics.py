import psutil

# 获取本机磁盘使用率和剩余空间G信息
def get_disk_info():
    # 循环磁盘分区
    content = ""
    for disk in psutil.disk_partitions():
        # 读写方式 光盘 or 有效磁盘类型
        if 'cdrom' in disk.opts or disk.fstype == '':
            continue
        disk_name_arr = disk.device.split(':')
        disk_name = disk_name_arr[0]
        disk_info = psutil.disk_usage(disk.device)
        # 磁盘剩余空间，单位G
        free_disk_size = disk_info.free//1024//1024//1024
        # 当前磁盘使用率和剩余空间G信息
        info = "%s盘使用率:%s%%， 剩余空间:%iG" % (disk_name, str(disk_info.percent), free_disk_size)
        # print(info)
        # 拼接多个磁盘的信息
        content = content + info+','
    return content

# cpu信息
def get_cpu_info():
    cpu_percent = psutil.cpu_percent(interval=1)
    cpu_info =  cpu_percent
    return cpu_info

# 内存信息
def get_memory_info():
    virtual_memory = psutil.virtual_memory()
    used_memory = virtual_memory.used/1024/1024/1024
    free_memory = virtual_memory.free/1024/1024/1024
    memory_percent = virtual_memory.percent
    memory_info = "内存使用:%0.2fG，使用率%0.1f%%，剩余内存:%0.2fG" % (used_memory, memory_percent, free_memory)
    return memory_info



