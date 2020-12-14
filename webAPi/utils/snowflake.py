# !/usr/bin/env python
# -*-coding:utf-8 -*-
# PROJECT    : web-common-service
# Time       ：2020/12/14 22:48
# Warning    ：The Hard Way Is Easier
import time


class SnowFlakeId(object):
    WORKER_ID_BITS = 5
    DATACENTER_ID_BITS = 5
    SEQUENCE_BITS = 12

    MAX_WORKER_ID = -1 ^ (-1 << WORKER_ID_BITS)  # 2**5-1 0b11111
    MAX_DATACENTER_ID = -1 ^ (-1 << DATACENTER_ID_BITS)

    # 移位偏移计算
    WORKER_ID_SHIFT = SEQUENCE_BITS
    DATACENTER_ID_SHIFT = SEQUENCE_BITS + WORKER_ID_BITS
    TIMESTAMP_LEFT_SHIFT = SEQUENCE_BITS + WORKER_ID_BITS + DATACENTER_ID_BITS

    # 序号循环掩码
    SEQUENCE_MASK = -1 ^ (-1 << SEQUENCE_BITS)

    # Twitter元年时间戳
    TWEPOCH = 1288834974657

    def __init__(self, datacenter_id, worker_id, sequence=0):
        """
        :param datacenter_id: 数据中心ID
        :param worker_id: 机器ID
        :param sequence: 序列号
        """
        if worker_id > self.MAX_WORKER_ID or worker_id < 0:
            raise ValueError('worker_id值越界')

        if datacenter_id > self.MAX_DATACENTER_ID or datacenter_id < 0:
            raise ValueError('datacenter_id值越界')

        self.worker_id = worker_id
        self.datacenter_id = datacenter_id
        self.sequence = sequence

        self.last_timestamp = -1

    def _gen_timestamp(self):
        """生成整数时间戳"""
        return int(time.time() * 1000)

    def _til_next_millis(self, last_timestamp):
        """等到下一毫秒"""
        timestamp = self._gen_timestamp()
        while timestamp <= last_timestamp:
            timestamp = self._gen_timestamp()
        return timestamp

    def get_id(self):
        """获取新的ID"""
        timestamp = self._gen_timestamp()

        if timestamp < self.last_timestamp:
            raise Exception("时钟拨回异常： 拒绝请求直到{}".format(self.last_timestamp))

        if timestamp == self.last_timestamp:
            self.sequence = (self.sequence + 1) & self.SEQUENCE_MASK
            if self.sequence == 0:
                timestamp = self._til_next_millis(self.last_timestamp)
        else:
            self.sequence = 0
        self.last_timestamp = timestamp

        new_id = ((timestamp - self.TWEPOCH) << self.TIMESTAMP_LEFT_SHIFT) | \
                 (self.datacenter_id << self.DATACENTER_ID_SHIFT) | \
                 (self.worker_id << self.WORKER_ID_SHIFT) | self.sequence

        return new_id


snow_flake = SnowFlakeId(datacenter_id=1, worker_id=1)

if __name__ == '__main__':
    import time

    print(time.time())
    snow_flake_id = SnowFlakeId(datacenter_id=1, worker_id=1).get_id()  # 19位长度的数值id
    print(snow_flake_id)
