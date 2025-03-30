import time  # Import the time module
import serial


def s(serialInst):
    move = 's'
    serialInst.write(move.encode('utf-8'))

def f(serialInst):
    move = 'f'
    serialInst.write(move.encode('utf-8'))

def fl(serialInst):
    move = 'f1'
    serialInst.write(move.encode('utf-8'))

def fr(serialInst):
    move = 'f2'
    serialInst.write(move.encode('utf-8'))

def r(serialInst):
    move = 'r'
    serialInst.write(move.encode('utf-8'))

def rl(serialInst):
    move = 'r1'
    serialInst.write(move.encode('utf-8'))

def rr(serialInst):
    move = 'r2'
    serialInst.write(move.encode('utf-8'))


# def stop(serialInst):
#     stop = 's1'
#     serialInst.write(stop.encode('utf-8'))

def go_fwc(serialInst):
    fwc = ['f1','r1','f1','r1']
    for move in fwc:
        print(move)
        serialInst.write(move.encode('utf-8'))  # Encode the move as bytes
        time.sleep(5)  

def go_path(moves,serialInst):
    for move in moves:
        print(move)
        serialInst.write(move.encode('utf-8'))  # Encode the move as bytes
        time.sleep(5)  


def go_path_2(moves,serialInst,current):
    serialInst.write(moves[0].encode('utf-8'))  # Encode the move as bytes
    time.sleep(3)
    for move in moves[1:]:
        if current != move:
            current = move
            serialInst.write(move.encode('utf-8'))  # Encode the move as bytes
        time.sleep(3)    
        print(move)
    
       
