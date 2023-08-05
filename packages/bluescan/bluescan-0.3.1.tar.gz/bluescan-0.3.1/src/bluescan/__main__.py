#!/usr/bin/env python3

import os
import sys
import logging
import traceback
import subprocess
from pathlib import PosixPath

from bthci import HCI
from pyclui import Logger
from bluepy.btle import BTLEException
from bluetooth.btcommon import BluetoothError

from .ui import parse_cmdline
from .helper import find_rfkill_devid
from .br_scan import BRScanner
from .le_scan import LEScanner
from .gatt_scan import GATTScanner
from .sdp_scan import SDPScanner
from .stack_scan import StackScanner
from .vuln_scan import VulnScanner
from .lmp_scan import LMPScanner


logger = Logger(__name__, logging.INFO)


def init(iface='hci0'):
    hci = HCI(iface)

    exitcode, output = subprocess.getstatusoutput(
        'rfkill unblock %d' % find_rfkill_devid(iface))
    if exitcode != 0:
        logger.error('rfkill: ' + output)
        sys.exit(exitcode)

    # hci.reset()
    hci.inquiry_cancel()
    hci.exit_periodic_inquiry_mode()

    hci.write_scan_enable() # No scan enabled

    event_params = hci.le_set_advertising_enable() # Advertising is disabled
    if event_params['Status'] != 0x00:
        #print(WARNING, 'Status of HCI_LE_Set_Advertising_Enable command: 0x%02x'%event_params['Status'])
        pass
    
    try:
        hci.le_set_scan_enable({
            'LE_Scan_Enable': 0x00, # Scanning disabled
            'Filter_Duplicates': 0x01 # Ignored
        })
    except RuntimeError as e:
        #print(WARNING, e)
        pass

    hci.set_event_filter({'Filter_Type': 0x00}) # Clear All Filters

    event_params = hci.read_bdaddr()
    if event_params['Status'] != 0:
        raise RuntimeError
    else:
        local_bd_addr = event_params['BD_ADDR'].upper()

    # Clear bluetoothd cache
    cache_path = PosixPath('/var/lib/bluetooth/') / local_bd_addr / 'cache'
    if cache_path.exists():
        for file in cache_path.iterdir():
            os.remove(file)


def main():
    try:
        args = parse_cmdline()
        logger.debug('args: {}'.format(args))

        if args['-i'] == 'The first HCI device':
            args['-i'] = HCI.get_default_hcistr() # May raise IndexError

        init(args['-i'])

        if args['-m'] == 'br':
            br_scanner = BRScanner(args['-i'])
            br_scanner.inquiry(inquiry_len=args['--inquiry-len'])
        elif args['-m'] == 'lmp':
            LMPScanner(args['-i']).scan(args['BD_ADDR'])
        elif args['-m'] == 'le':
            LEScanner(args['-i']).scan(args['--timeout'], 
                args['--scan-type'], args['--sort'], 
                args['BD_ADDR'], args['--addr-type'])
        elif args['-m'] == 'sdp':
            SDPScanner(args['-i']).scan(args['BD_ADDR'])
        elif args['-m'] == 'gatt':
            GATTScanner(args['-i']).scan(args['BD_ADDR'], args['--addr-type'],
                args['--include-descriptor'])
        elif args['-m'] == 'stack':
            StackScanner(args['-i']).scan(args['BD_ADDR'])
        elif args['-m'] == 'vuln':
            VulnScanner(args['-i']).scan(args['BD_ADDR'], args['--addr-type'])
        else:
            logger.error('Invalid scan mode')
    except IndexError:
        logger.error('There is no available HCI device')
    except BluetoothError as e:
        logger.error('{}'.format(e))
    except RuntimeError as e:
        logger.error('{}'.format(e))
    except (BTLEException, ValueError) as e:
        logger.error('{}'.format(e))
        if 'le on' in str(e):
            print('        No BLE adapter? or missing sudo ?')
    except KeyboardInterrupt:
        logger.info(args['-m'].upper() + " scan canceled\n")
    # except Exception as e:
    #     #traceback.print_exc()
    #     print(ERROR, e)


if __name__ == '__main__':
    main()
