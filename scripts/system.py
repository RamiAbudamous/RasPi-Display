import os
import psutil

def calcPercBar(part, whole, segments=20):
    percentage = part/whole
    filledSegments = int(percentage*segments)
    bar = "█" * filledSegments + "-" * (segments-filledSegments)
    return f"[{bar}]"


def getCPUStats():
    cpuCount = psutil.cpu_count()
    cpuPercent = psutil.cpu_percent(.99)
    cpuUptime = psutil.cpu_times().system

    os.system('cls')
    print("CPU STATS\n")

    print("CPU count: ", cpuCount, "cores")
    print("CPU usage: ", cpuPercent, "%")
    # apparently the last one here is minutes, so maybe remove the first one? or the second one? no clue. one of them isnt needed.
    print(f"CPU Uptime: {int(cpuUptime/(60*60*24))}:{int(cpuUptime/(60*60))%24}:{int((cpuUptime/60)%60)}:{int(cpuUptime%60)}")
    print("\n")


def getMemStats():
    os.system('cls')
    print("MEMORY STATS\n")

    memUsage = psutil.virtual_memory()
    print("Mem Total:", int(memUsage.total/(1024*1024)), "MB")
    print("Mem Used:", int(memUsage.used/(1024*1024)), "MB")
    print("Mem Available:", int(memUsage.available/(1024*1024)), "MB")
    memBar = calcPercBar(memUsage.used, memUsage.total)
    print(f"{memBar} {memUsage.percent}%\n")
    print("Swap Usage %:", psutil.swap_memory().percent, "%")
    print("\n")


def getDiskStats():
    os.system('cls')
    print("DISK STATS\n")

    for dp in psutil.disk_partitions():
        print("Disk usage of partition ", dp.mountpoint, ": ") 
        diskUsage = psutil.disk_usage(dp.mountpoint)
        print("Total: ", int(diskUsage.total/(1024*1024)), "MB")
        print("Used: ", int(diskUsage.used/(1024*1024)), "MB")
        print("Free: ", int(diskUsage.free/(1024*1024)), "MB")
        diskBar = calcPercBar(diskUsage.used, diskUsage.total)
        print(f"{diskBar} {diskUsage.percent}%")
        print("\n")


def getNetStats():
    os.system('cls')
    print("NETWORK STATS\n")

    netUsage = psutil.net_io_counters()
    print(f"Total data sent: {round((netUsage.bytes_sent/(1024*1024*1024)), 2)} Gigabytes")
    print(f"Total data received: {round((netUsage.bytes_recv/(1024*1024*1024)), 2)} Gigabytes")
    print(f"Total packets sent: {round(netUsage.packets_sent/1000000, 2)}M Packets")
    print(f"Total packets received: {round(netUsage.packets_recv/1000000, 2)}M Packets")
    print("Total incoming packets dropped:", netUsage.dropin, "Packets")
    print("Total outgoing packets dropped:", netUsage.dropout, "Packets")
    print("\n")


def getStats():
    cpuCount = psutil.cpu_count()
    cpuPercent = psutil.cpu_percent(.99)
    cpuUptime = psutil.cpu_times().system

    os.system('cls')
    print("SYSTEM OVERVIEW\n")

    print("CPU STATS")
    print("CPU count: ", cpuCount, "cores")
    print("CPU usage: ", cpuPercent, "%")
    print(f"CPU Uptime: {int(cpuUptime/(60*60*24))}:{int(cpuUptime/(60*60))%24}:{int((cpuUptime/60)%60)}:{int(cpuUptime%60)}\n")


    print("MEMORY STATS")
    memUsage = psutil.virtual_memory()
    print("Mem Total:", int(memUsage.total/(1024*1024)), "MB")
    print("Mem Used:", int(memUsage.used/(1024*1024)), "MB")
    
    memBar = calcPercBar(memUsage.used, memUsage.total)
    print(f"{memBar} {memUsage.percent}%\n")
    

    print("DISK STATS")
    for dp in psutil.disk_partitions():
        print("Disk usage of partition ", dp.mountpoint, ": ") 
        diskUsage = psutil.disk_usage(dp.mountpoint)
        print("Total: ", int(diskUsage.total/(1024*1024)), "MB")
        print("Used: ", int(diskUsage.used/(1024*1024)), "MB")

        diskBar = calcPercBar(diskUsage.used, diskUsage.total)
        print(f"{diskBar} {diskUsage.percent}%")

if __name__ == "__main__":
    getStats()