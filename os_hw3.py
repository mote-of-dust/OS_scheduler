import time

'''
to implement: arranging ready queue
preempting
quantum

'''
def turnaround(finish_time, schedules):
    sum = 0
    avg = 0
    for i in range(len(finish_time)):
        print('Process %d arrival time: %d' %(i, schedules[i][0]))
        print('Process %d finish time: %d' % (i, finish_time[i]))
        temp = finish_time[i] - schedules[i][0]
        print('turn around for Process %d is: %d time units' % (i, temp))
        sum += temp
    print()
    avg = sum / len(finish_time)
    print('Average turn around time: %d' % avg)

def sortqueue(ready_queue, schedules):
    if len(ready_queue) > 1:
        head = 0
        tail = len(ready_queue) - 1
        for i in range(tail, head, -1):
            # print('i is: %d' % i)
            for j in range(i):
                # print('j is: %d' % j)
                if schedules[ready_queue[j]][1] > schedules[ready_queue[j + 1]][1]:
                    ready_queue[j], ready_queue[j + 1] = ready_queue[j + 1], ready_queue[j]
                    print('swap happened')
    # print('new ready queue is: ')
    # print(ready_queue)
    return ready_queue


def premptive_prio(schedules):
    quantum = int(input("What is the desired Quantum: "))
    ready_queue = []
    print('----------------------')
    time_round = 0
    onCPUBool = False
    onCPU = ''
    runTime = 0
    arrivals = 0
    exits = 0
    finish_time = [0 for i in range(len(schedules))]

    while True:
        print("Time unit: %d ticks" % time_round)
        time.sleep(1)
        if arrivals < len(schedules):
            print('arrival check running')
            for i in range(len(schedules)):
                if schedules[i][0] == time_round:
                    if len(ready_queue) == 0:
                        ready_queue.append(i)
                    else:
                        ready_queue.append(i)
                        ready_queue = sortqueue(ready_queue, schedules)
                        print("new ready queue is:")
                        print(ready_queue)
                    print("Process at index %d arrives into ready queue" % i)
                    time.sleep(1)
                    arrivals += 1
                    if onCPUBool is False:
                        print("Process at index %d popped from queue and put on CPU" % i)
                        onCPU = ready_queue.pop(0)
                        onCPUBool = True
                        time.sleep(1)
                    # else:
                    #     if schedules[i][1] < schedules[onCPU][1]:
                    #         print("Process %d gets preempted and placed back on ready queue." % onCPU)
                    #         print("Process %d gets placed on the CPU." % i)
                    #         temp = schedules[onCPU][0]
                    #         onCPU = ready_queue.pop()
                    #         ready_queue.append(temp)
                    #         runTime = 0
                    #         time.sleep(1)
        elif onCPUBool is False:
            print("Process at index %d is placed on the CPU." % ready_queue[0])
            onCPU = ready_queue.pop(0)
            onCPUBool = True
            time.sleep(1)
        if len(ready_queue) > 0 and schedules[onCPU][1] > schedules[ready_queue[0]][1]:
            print("Process %d gets preempted and placed back on ready queue." % onCPU)
            print("Process %d gets placed on the CPU." % ready_queue[0])
            schedules[onCPU][2] -= runTime
            temp = schedules[onCPU][0]
            onCPU = ready_queue.pop(0)
            ready_queue.append(temp)
            ready_queue = sortqueue(ready_queue, schedules)
            runTime = 0
            time.sleep(1)
        elif len(ready_queue) > 0 and schedules[onCPU][1] == schedules[ready_queue[0]][1]:
            if runTime == quantum:
                print("Process %d gets preempted and placed back on ready queue due to quantum" % onCPU)
                print("Process %d gets placed on the CPU." % ready_queue[0])
                schedules[onCPU][2] -= runTime
                temp = onCPU
                onCPU = ready_queue.pop(0)
                ready_queue.append(temp)
                print("cur rdy q: ")
                print(ready_queue)
                ready_queue = sortqueue(ready_queue, schedules)
                runTime = 0
                time.sleep(1)
        if onCPUBool:
            runTime += 1
            print('Process %d has ran for %d time units currently.' % (onCPU, runTime))
            if runTime == schedules[onCPU][2]:
                print("Process %d has finished running and leaves CPU." % onCPU)
                finish_time[onCPU] = time_round + 1
                onCPU = ''
                onCPUBool = False
                exits += 1
                time.sleep(1)
                runTime = 0
                if exits == len(schedules):
                    print("All processes finished at time unit %d\n" % time_round)
                    print('---[Calculating turn around time]---')
                    turnaround(finish_time, schedules)
                    exit()
        time_round += 1

        print()


def create_array():
    schedFile = open("schedules.txt", "r")

    procNum = schedFile.readline()

    schedules = [[0 for i in range(3)] for j in range(int(procNum))]
    # print(schedules)

    rowStart = 0
    nextProc = schedFile.readline()
    while rowStart < int(procNum):
        temp = nextProc.split()
        for i in range(3):
            schedules[rowStart][i] = int(temp[i])
        print(schedules[rowStart])
        nextProc = schedFile.readline()
        rowStart += 1

    # print(schedules)
    schedFile.close()
    return schedules


schedules = create_array()
premptive_prio(schedules)
