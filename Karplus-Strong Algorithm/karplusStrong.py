import wave, math, pygame, argparse, os, random, time
import numpy as np
from collections import deque
import matplotlib.pyplot as plt

showPlot = False
#Pentatonic Minor Scale (piano C4-E(b)-F-G-B(b)-C5)
pmNotes = {'C4': 262, 'Eb': 311, 'F': 249, 'G': 391, 'Bb': 466}

def generateNotes(freq):
    sampleRate = 44100
    numSamples = 44100
    N = int(sampleRate/freq)
    buffer = deque([random.random() - 0.5 for i in range(N)])
    if showPlot:
        axline = plt.plot(buffer)
    samples = np.array([0]*numSamples, 'float32')
    for i in range(numSamples):
        samples[i] = buffer[0]
        average = 0.996 * 0.5 * (buffer[0] + buffer[1])
        buffer.append(average)
        buffer.popleft()
        if showPlot:
            if i % 1000 == 0:
                axline.set_ydata(buffer)
                plt.draw()
        
    samples = np.array(samples*32767, 'int16')
    return samples.tostring()

def writeWAV(fileName, data):
    file = wave.open(fileName, 'wb')
    numChannels = 1
    sampleWidth = 2
    frameRate = 44100
    numFrames = 44100
    file.setparams((numChannels, sampleWidth, frameRate, numFrames, 'NONE', 'noncompressed'))
    file.writeframes(data)
    file.close()
    
class Piano():
    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 1, 2048)
        pygame.init()
        self.notes = {}
    
    def add(self, fileName):
        self.notes[fileName] = pygame.mixer.Sound(fileName)
    
    def play(self, fileName):
        try:
            self.notes[fileName].play()
        except:
            print(fileName + " not found!")
    
    def playRandomNotes(self):
        index = random.randint(0, len(self.notes)-1)
        note = list(self.notes.values())[index]
        note.play()

def main():
    global showPlot
    
    #parser = argparse.ArgumentParser(description="Generating sounds with Karplus String Algorithm")
    #parser.add_argument('--display', action='store_true', required=False)
    #parser.add_argument('--play', action='store_true', required=False)
    #parser.add_argument('--piano', action='store_true', required=False)
    
    play = input("Press enter to run, or type 'display', 'play'  or 'paino' to see/hear fun other options: ")
    
    #args = parser.parse_args()
    #if args.display:
    if play.lower() == 'display':
        showPlot = True
        plt.ion()
        
    piano = Piano()
    
    print("Creating notes...")
    for name, freq in list(pmNotes.items()):
        fileName = name + '.wav'
        if not os.path.exists(fileName):
            data = generateNote(freq)
            print("Creating " + fileName + "...")
            writeWAV(fileName, data)
        else:
            print(fileName + ' already created. Skipping...')
            
        piano.add(name + '.wav')
        
        #if args.display:
        if play.lower == 'display':
            piano.play(name + '.wav')
            time.sleep(0.5)
            
    #if args.play:
    if play.lower() == 'play':
        while True:
            try:
                piano.playRandomNotes()
                rest = np.random.choice([1, 2, 4, 8], 1, p=[0.15, 0.7, 0.1, 0.05])
                time.sleep(0.25 * rest[0])
            except KeyboardInterrupt:
                exit()
    
    #if args.piano:
    if play.lower() == 'piano':
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYUP:
                    print("Key Pressed")
                    piano.playRandomNotes()
                    time.sleep(0.5)

if __name__ == '__main__':
    main()