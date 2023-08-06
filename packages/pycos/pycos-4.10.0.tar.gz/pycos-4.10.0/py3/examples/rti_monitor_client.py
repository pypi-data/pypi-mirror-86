#!/usr/bin/env python

# to be used with 'rti_monitor_server.py'
# client requests execution of tasks on (remote) server.

import random
import pycos
# import netpycos to use distributed version of Pycos
import pycos.netpycos


def monitor_proc(n, task=None):
    # this task gets exceptions (notifications of exit status) for (remote)
    # tasks created in rti_test
    done = 0
    while done < n:
        msg = yield task.receive()
        if isinstance(msg, pycos.MonitorStatus):
            rtask = msg.info
            if msg.type == StopIteration:
                pycos.logger.debug('RTI %s finished with: %s', rtask, msg.value)
            else:
                pycos.logger.debug('RTI %s failed with: %s', rtask, msg.type)
            done += 1
        else:
            pycos.logger.warning('ignoring invalid message')


def rti_test(task=None):
    # if server is on remote network, automatic discovery won't work,
    # so add it explicitly
    # yield scheduler.peer(pycos.Location('192.168.21.5', 9705))

    # get reference to RTI at server
    rti1 = yield pycos.RTI.locate('rti_1')
    print('RTI is at %s' % rti1.location)

    # 5 (remote) tasks are created with rti1
    n = 5
    # set monitor (monitor_proc task) for tasks created for this RTI
    yield rti1.monitor(pycos.Task(monitor_proc, n))

    for i in range(n):
        rtask = yield rti1('test%s' % i, b=i)
        pycos.logger.debug('RTI %s created' % rtask)
        # If necessary, each rtask can also be set (different) 'monitor'
        rtask.send('msg:%s' % i)
        yield task.sleep(random.uniform(0, 1))


pycos.logger.setLevel(pycos.Logger.DEBUG)
# use 'test' secret so peers that use same secret are recognized
scheduler = pycos.Pycos(name='client', secret='test')
pycos.Task(rti_test)
