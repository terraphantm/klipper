#!/usr/bin/env python3

import sys, os, re, subprocess, optparse, time, fcntl, struct

class error(Exception):
    pass

def find_canboot_serial_path():
    if not os.path.exists('/dev/serial/by-id/'):
        return None
    for fname in os.listdir('/dev/serial/by-id/'):
        if 'usb-CanBoot' in fname:
            return '/dev/serial/by-id/' + fname
    return None

def call_flashcan(uuid, interface, binfile):
    args = [sys.executable, "lib/canboot/flash_can.py", "-u",
            uuid, "-i", interface, "-r"]
    sys.stderr.write(" ".join(args) + '\n\n')
    res = subprocess.call(args)
    if res != 0:
        sys.stderr.write("Error running flash_can.py\n")

    time.sleep(1)

    serialpath = find_canboot_serial_path()
    
    if serialpath is None:
        args = [sys.executable, "lib/canboot/flash_can.py", "-u",
            uuid, "-i", interface, "-f", binfile]
        
    if serialpath is not None:            
        args = [sys.executable, "lib/canboot/flash_can.py", "-d",
                serialpath, "-f", binfile]
        
    sys.stderr.write(" ".join(args) + '\n\n')
    res = subprocess.call(args)
    if res != 0:
        sys.stderr.write("Errorna running flash_can.py\n")
        sys.exit(-1)


def main():
    usage = "%prog [options] -i <interface> -u <uuid> <binary>"
    opts = optparse.OptionParser(usage)
    opts.add_option("-u", "--uuid", type="string", dest="uuid",
                    help="device uuid")
    opts.add_option("-i", "--interface", type="string", dest="interface",
                    help="CAN Bus Interface")

                    
    options, args = opts.parse_args()
    if len(args) != 1:
        opts.error("Incorrect number of arguments")
    if not options.uuid:
        sys.stderr.write("\nPlease specify UUID\n\n")
        sys.exit(-1)
    if not options.interface:
        options.interface = 'can0'


    call_flashcan(options.uuid, options.interface, args[0])
    

if __name__ == '__main__':
    main()
