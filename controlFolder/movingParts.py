# movingParts.py

import time

def s(serialInst):
    """Stop both motors."""
    cmd = 's\n'
    serialInst.write(cmd.encode('utf-8'))

def f(serialInst):
    """Forward: both motors."""
    cmd = 'f\n'
    serialInst.write(cmd.encode('utf-8'))

def b(serialInst):
    """Backward: both motors reverse."""
    cmd = 'b\n'
    serialInst.write(cmd.encode('utf-8'))

def fl(serialInst):
    """Pivot right: left motor only."""
    cmd = 'f1\n'
    serialInst.write(cmd.encode('utf-8'))

def fr(serialInst):
    """Pivot left: right motor only."""
    cmd = 'f2\n'
    serialInst.write(cmd.encode('utf-8'))

def r(serialInst):
    """Spin in place (both wheels opposite)."""
    cmd = 'r\n'
    serialInst.write(cmd.encode('utf-8'))

def l(serialInst):
    """Spin in place opposite direction."""
    cmd = 'l\n'
    serialInst.write(cmd.encode('utf-8'))
