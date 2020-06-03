# An itunes playlist  is just an XML document, so we can parse through it and return information about the playlist
import plistlib, argparse
import numpy as np
import matplotlib.pyplot as plt

def findDuplicates(fileName):
    print("Finding duplicate tracks in {}...".format(fileName))
    plist = plistlib.readPlist(fileName)
    tracks = plist['Tracks']
    trackNames = {}
    for trackId, track in tracks.items():
        try:
            name = track['Name']
            duration = track['Total Time']
            if name in trackNames:
                if duration // 1000 == trackNames[name][0] // 1000:
                    count = trackNames[name][1]
                    trackNames[name] = (duration, count+1)
                else:
                    trackNames[name] = (duration, 1)
        except:
            pass
        
    dups = []
    for k, v in trackNames.items():
        if v[1] > 1:
            dups.append((v[1], k))
        if len(dups) > 0:
            print("Found {} duplicates. Track names saved to dup.txt".format(len(dups)))
        else:
            print("No duplicate tracks found!")
        
        f = open("dups.txt", "w")
        for val in dups:
            f.write("[%d] %s\n" % (val[0], val[1]))
        f.close()
        
def findCommonTracks(fileNames):
    trackNameSets = []
    #incorporate track duration as well
    for filename in fileNames:
        trackNames = set()
        plist = plistlib.readPlist(filename)
        tracks = plist['Tracks']
        for trackId, track in tracks.items():
            try:
                trackNames.add(track['Name'])
            except:
                pass
            trackNameSets.append(trackNames)
        commonTracks = set.intersection(*trackNameSets)
        if len(commonTracks) > 0:
            f = open("common.txt", "w")
            for val in commonTracks:
                s = "%s\n" % val
                f.write(s.encode("UTF-8"))
            f.close()
            print("{} common tracks found. Track names written to common.txt".format(len(commonTracks)))
        else:
            print("No common tracks found")
            
def plotStatistics(filename):
    plist = plistlib.readPlist(filename)
    tracks = plist['Tracks']
    ratings = []
    durations = []
    #add correlation value comparison and create scatter plot
    for trackId, track in tracks.items():
        try:
            ratings.append(track['Album Rating'])
            durations.append(track['Total Time'])
        except:
            pass
        
    if ratings == [] or durations == []:
        print("No ratings or total time results in {}".format(filename))
        return
    
    x = np.array(durations, np.int32)
    x = x/600000.0
    y = np.array(ratings, np.int32)
    plt.subplot(2, 1, 1)
    plt.plot(x, y, 'o')
    plt.axis([0, 1.05*np.max(x), -1, 110])
    plt.xlabel("Track Duration")
    plt.ylabel("Track Rating")
    
    plt.subplot(2, 1, 2)
    plt.hist(x, bins=20)
    plt.xlabel("Track Duration")
    plt.ylabel("Count")
    plt.show()
    
def main():
    desc = """ 
    An itunes playlist  is just an XML document, so we can parse through it and return information about the playlist.
    """
    
    parser = argparse.ArgumentParser(description=desc)
    group = parser.add_mututally_exclusive_group()
    group.add_argument('--common', nargs='*', dest='playlistFiles', required=False)
    group.add_argument('--stats', nargs='*', dest='playlistFile', required=False)
    group.add_argument('--dup', nargs='*', dest='playlistFileDups', required=False)
    
    args = parser.parse_args()
    if args.playlistFiles:
        findCommonTracks(args.playlistFiles)
    elif args.playlistFile:
        plotStatistics(args.playlistFile)
    elif args.playlistFileDups:
        findDuplicates(args.playlistFileDups)
    else:
        print("[ERROR] Check submission file. These are not the droids... tracks... you are looking for")
    
    
if __name__ == '__main__':
    main()
    
"""
Example use of program on command line: 
python playlist.py --common test-data/running.xml test-data/rating.xml
python playlist.py --stats test-data/workoutjams.xml

"""