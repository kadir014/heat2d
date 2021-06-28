#  This file is a part of the Heat2D Project and  #
#  distributed under the GPL 3 license            #
#                                                 #
#           HEAT2D Game Engine Project            #
#            Copyright © Kadir Aksoy              #
#       https://github.com/kadir014/heat2d        #


import sys
import platform
import psutil
import cpuinfo
import pygame

#This instance has to be created before creating a window
pygame.display.init()
DISPLAYINFO = pygame.display.Info()


class OS:
    name = str()
    full_name = str()
    simple_name = str()
    network_name = str()
    bit = int()

    def update_info():
        if   sys.platform == "win32": OS.name = "Windows"
        elif sys.platform == "darwin": OS.name = "MacOS"
        elif sys.platform.startswith("linux"): OS.name = "Linux"
        elif sys.platform.startswith("freebsd"): OS.name = "FreeBSD"

        OS.full_name     = platform.platform()
        OS.simple_name   = platform.platform(terse=True)
        OS.network_name  = platform.node()

        # NOTE: Debian-64 returns x86_64
        if platform.machine().endswith("64"): OS.bit = 64
        elif platform.machine().endswith("86"): OS.bit = 32


class Monitor:
    width = int()
    height = int()
    bitsize = int()
    bytesize = int()

    def update_info():
        Monitor.width = DISPLAYINFO.current_w
        Monitor.height = DISPLAYINFO.current_h
        Monitor.bitsize = DISPLAYINFO.bitsize
        Monitor.bytesize = DISPLAYINFO.bytesize


class RAM:
    total        = int()
    total_gb     = int()
    available    = int()
    available_gb = int()
    percent      = float()
    used         = int()
    used_gb      = int()
    free         = int()
    free_gb      = int()

    def update_info():
        vm = psutil.virtual_memory()

        RAM.total        = vm.total
        RAM.total_gb     = int(vm.total / 1073741824)
        RAM.available    = vm.available
        RAM.available_gb = int(vm.available / 1073741824)
        RAM.percent      = vm.percent
        RAM.used         = vm.used
        RAM.used_gb      = int(vm.used / 1073741824)
        RAM.free         = vm.free
        RAM.free_gb      = int(vm.free / 1073741824)


class CPU:
    family =        str()
    brand  =        str()
    hz     =        str()
    hz_advertised = str()
    cores =         int()
    percent =       float()

    def update_info():
        cpi = cpuinfo.get_cpu_info()

        CPU.family        = platform.processor()
        CPU.brand         = cpi["brand_raw"]
        CPU.hz            = cpi["hz_actual_friendly"]
        CPU.hz_advertised = cpi["hz_advertised_friendly"]
        CPU.cores         = psutil.cpu_count()
        CPU.percent       = psutil.cpu_percent()


class GPU:
    vram = int()
    #TODO: Graphics Card brand, name, producer, usage, ram etc...

    def update_info():
        GPU.vram = DISPLAYINFO.video_mem


class Disk:
    device     = str()
    filesystem = str()
    total      = int()
    total_gb   = int()
    percent    = float()
    used       = int()
    used_gb    = int()
    free       = int()
    free_gb    = int()

    def update_info():
        d = psutil.disk_partitions()[0]
        ds = psutil.disk_usage(d.mountpoint)

        Disk.device     = d.device
        Disk.filesystem = d.fstype
        Disk.total      = ds.total
        Disk.total_gb   = int(ds.total / 1073741824)
        Disk.percent    = ds.percent
        Disk.used       = ds.used
        Disk.used_gb    = int(ds.used / 1073741824)
        Disk.free       = ds.free
        Disk.free_gb    = int(ds.free / 1073741824)


def print_specs(update=False):
    if update:
        OS.update_info()
        Monitor.update_info()
        RAM.update_info()
        CPU.update_info()
        Disk.update_info()

    print("Operating System")
    print(f"  Name       : {OS.name}")
    print(f"  Full name  : {OS.full_name}")
    print(f"  Simple na  : {OS.simple_name}")
    print(f"  Network n  : {OS.network_name}")
    print(f"  Bit        : {OS.bit}")
    print("")
    print("Monitor")
    print(f"  Width      : {Monitor.width} px")
    print(f"  Height     : {Monitor.height} px")
    print(f"  Bit-size   : {Monitor.bitsize}")
    print(f"  Byte-size  : {Monitor.bytesize}")
    print("")
    print("Memory")
    print(f"  Usage      : {RAM.percent}%")
    print(f"  Total      : {RAM.total_gb} GB")
    print(f"  Available  : {RAM.available_gb} GB")
    print(f"  Used       : {RAM.used_gb} GB")
    print(f"  Free       : {RAM.free_gb} GB")
    print("")
    print("Processor")
    print(f"  Usage      : {CPU.percent}%")
    print(f"  Hz         : {CPU.hz}")
    print(f"  Cores      : {CPU.cores}")
    print(f"  Family     : {CPU.family}")
    print(f"  Brand      : {CPU.brand}")
    print("")
    print("Disk")
    print(f"  Usage      : {Disk.percent}")
    print(f"  Filesystem : {Disk.filesystem}")
    print(f"  Total      : {Disk.total_gb} GB")
    print(f"  Used       : {Disk.used_gb} GB")
    print(f"  Free       : {Disk.free_gb} GB")
