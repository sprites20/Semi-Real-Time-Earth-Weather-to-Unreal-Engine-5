import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--latitude', dest='latitude', default='0', type=str, help='latitude in string')
parser.add_argument('--longitude', dest='longitude', default='0',type=str, help='longitude in string')
args = parser.parse_args()

print('cmd /c python capture2.py --prop "base" ' + '--latitude \"' + args.latitude + '\" --longitude \"' + args.longitude + '\"' + 
' && python capture2.py --prop "wind-speed"' + '--latitude \"' + args.latitude + '\" --latitude \"' + args.longitude + '\"')

while True:
    print("1")
    os.system('python capture2.py --prop "base" ' + '--latitude \"' + args.latitude + '\" --longitude \"' + args.longitude + '\"')
    print("2")
    os.system('python capture2.py --prop "wind-speed" ' + '--latitude \"' + args.latitude + '\" --longitude \"' + args.longitude + '\"')
    print("3")
    os.system('python capture2.py --prop "temperature" ' + '--latitude \"' + args.latitude + '\" --longitude \"' + args.longitude + '\"')