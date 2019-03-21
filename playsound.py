from __future__ import print_function

import sys
import wave
import getopt
import alsaaudio

def play(devicename, f):

    print('%d channels, %d sampling rate\n, %d sampwidth' % (f.getnchannels(),
                                               f.getframerate(), f.getsampwidth()))
    # Set attributes
    device = alsaaudio.PCM(device=devicename)
    device.setchannels(f.getnchannels())
    device.setrate(f.getframerate())
    mixer = alsaaudio.Mixer(control = 'PCM', device = devicename)
    channel = alsaaudio.MIXER_CHANNEL_ALL
    mixer.setvolume(80, channel)
    # 8bit is unsigned in wav files
    if f.getsampwidth() == 1:
        device.setformat(alsaaudio.PCM_FORMAT_U8)
    # Otherwise we assume signed data, little endian
    elif f.getsampwidth() == 2:
        device.setformat(alsaaudio.PCM_FORMAT_S16_LE)
    elif f.getsampwidth() == 3:
        device.setformat(alsaaudio.PCM_FORMAT_S24_LE)
    elif f.getsampwidth() == 4:
        device.setformat(alsaaudio.PCM_FORMAT_S32_LE)
    else:
        raise ValueError('Unsupported format')

    device.setperiodsize(4096)

    data = f.readframes(4096)
    while data:
        # Read data from stdin
        device.write(data)
        data = f.readframes(4096)

def usage():
    print('usage: playwav.py [-d <device>] <file>', file=sys.stderr)
    sys.exit(2)

if __name__ == '__main__':





    f = wave.open('beep1.wav', 'rb')
    devicename = 'hw:'+ sys.argv[1]


    play(devicename, f)

    f.close()
