import os
import threading
import time
import wave


def getTimestamp():
    return time.strftime('%Y-%m-%d_%H-%M-%S')

class SoundReader:
    def __init__(self, soundSaveFolder, interval, length):
        self.saveFolder = soundSaveFolder
        self.sampleInterval = interval
        self.sampleLength = length
        self.isRecording = False
        self.recordingLoopActive = False
        self.threadsStarted = False
        self.nextTimer = None

    def startRecording(self):
        self.recordingLoopActive = True
        if (self.threadsStarted == False):
            print 'inside here'
            threading.Timer(0, self.sampleAudioWithInterval, ()).start()
            self.threadsStarted = True

    def stopRecording(self):
        self.recordingLoopActive = False

        # used if there is an error with stopping the recording thread

    def resetIsRecording(self):
        self.isRecording = False

    def sampleAudioWithInterval(self):
            #setting up next recording timer thread
            self.nextTimer = threading.Timer(self.sampleInterval, self.sampleAudioWithInterval, ())
            self.nextTimer.start()
            if(self.recordingLoopActive == True):
                self.isRecording = True
                #line below ensures that, even when there is an error recording sound, isRecording won't stay on
                #The pi has 15 seconds more than the sample length to finish saving the data
                threading.Timer(self.sampleLength + 15, self.resetIsRecording, ()).start()
                timestamp = getTimestamp()
                try:
                    print '[SoundReader] Started recording audio'
                    self.recordAudio(self.sampleLength, self.saveFolder, timestamp+'.wav')
                    print '[SoundReader] Recorded audio'
                except Exception as e:
                    print 'sound recording error'
                self.isRecording = False


    def recordAudio(self, sampleSeconds, filepath, filename):
        recordString = self.getRecordString(sampleSeconds, filepath, filename)
        # excecutes system call
        os.system(recordString)


    def getRecordString(self, sampleSeconds, filepath, filename):
        # records raw audio with arecord and pipes it to lame mp3 encoder to convert to mp3
        # edit "--preset medium -mm" section if you would like to change recorded audio quality
        # learn about presets by calling "man lame" in console
        print os.path.join(filepath,filename)
        return "arecord -Dplug:card0 -f S16_LE -c2 -d " + str(sampleSeconds) + " -t wav | lame --preset medium -mm - " + os.path.join(filepath,filename)

    # cancels recording threads, used when quitting application
    def quit(self):
        if self.nextTimer != None:
            self.nextTimer.cancel()

    def setLogger(self, logger):
        self.logger = logger

    def setStorage(self, storage):
        self.storage = storage

x = SoundReader('/home/pi/BeeSounds/',20,10)
x.startRecording()
