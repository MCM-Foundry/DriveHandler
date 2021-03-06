# Part of DriveHandler
# Author: Ryan Pavlik

# https://github.com/rpavlik/DriveHandler

#          Copyright Iowa State University 2011.
# Distributed under the Boost Software License, Version 1.0.
#    (See accompanying file LICENSE_1_0.txt or copy at
#          http://www.boost.org/LICENSE_1_0.txt)

import dbus
import subprocess

class USBDrive(object):
  def __init__(self, dev):
    self.dev = dev
    self.device_obj = dbus.SystemBus().get_object("org.freedesktop.UDisks", dev)
    self.dev_methods = dbus.Interface(self.device_obj, dbus_interface='org.freedesktop.UDisks.Device')
    #self.dev_props = dbus.Interface(self.device_obj, dbus.PROPERTIES_IFACE)

  def mount(self):
    print "Waiting for udisks to settle..."
    # See these links for why we do this:
    # http://cgit.freedesktop.org/udisks/tree/tests/run#n55
    # http://cgit.freedesktop.org/udisks/tree/tests/run#n147
    subprocess.call(['udevadm', 'settle'])

    print "Mounting %s" % self.dev
    self.mountpoint = self.dev_methods.FilesystemMount('', [])

  def unmount(self):
    print "Unmounting %s" % self.dev
    self.dev_methods.FilesystemUnmount(dbus.Array([], 's'))
    self.mountpoint = None

  def eject(self):
    print "Ejecting %s" % self.dev
    self.dev_methods.DriveEject(dbus.Array([], 's'))

