#!/usr/bin/python

def getNixInterfaces():
    with open('/proc/net/dev') as f:
        allInterfaces = []
        for line in f:
            rawIface = line.split()[0]
            if 'Inter' not in rawIface:
                if 'face' not in rawIface:
                    if ':' in rawIface:
                        allInterfaces.append(rawIface[:-1])
                    else:
                        allInterfaces.append(rawIface)
        return allInterfaces

print getNixInterfaces()
