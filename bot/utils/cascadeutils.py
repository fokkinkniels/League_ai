import os

    

def generate_negative_description_file():
    ## open the output file for writing. will overwrite all existing data in there
    with open('neg.txt', 'w') as f:
        ## loop over all the filenames
        for filename in os.listdir('opencv_classifier/Dataset/Negative/'):
            f.write('Dataset/Negative/' + filename + '\n')

generate_negative_description_file()


# $ C:\Users\fokki\Documents\opencv\build\x64\vc15\bin\opencv_annotation.exe --annotations=pos.txt --images=Dataset/positive/

# You click once to set the upper left corner, then again to set the lower right corner.
# Press 'c' to confirm.
# Or 'd' to undo the previous confirmation.
# When done, click 'n' to move to the next image.
# Press 'esc' to exit.
# Will exit automatically when you've annotated all of the images


# C:\Users\fokki\Documents\opencv\build\x64\vc15\bin\opencv_createsamples.exe -info opencv_classifier/pos_minion.txt -w 24 -h 24 -num 10000 -vec pos.vec

# cd opencv_classifier

# C:/Users/fokki/Documents/opencv/build/x64/vc15/bin/opencv_traincascade.exe -data cascade/ -vec pos.vec -bg neg.txt -precalcValBufSize 12000 -precalcIdxBufSize 12000 -numPos 2500 -numNeg 5000 -numStages 10 -w 24 -h 24 -maxFalseAlarmRate 0.4 -minHitRate 0.9999