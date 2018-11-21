#!/usr/bin/env python

import pygame, sys, random, os, subprocess, threading, time, copy, csv
from pygame.locals import *

def randomWithRemove(myList):
    # removes and returns random element from list
    # list is modified
    choice = random.choice(myList)
    myList.remove(choice)
    return choice

def uniqueShuffleList(myList):
    # shuffles elements in a list with condition that no element can be
    # in the same position as its original position after the shuffle
    # returns new list of shuffled elements
    newList = list(myList)
    while True:
        random.shuffle(newList)
        for a, b in zip(myList, newList):
            if a == b:
                break
        else:
            return newList

def repeatElem(li, n):
    # repeat an element n times in a list
    # to build lists with repeated elements
    return ([i for x in li for i in n*[x]])

def chunkList(theList, n):
    # splits list into chunks of size n
    for i in range(0, len(theList), n):
        yield theList[i:i+n]

def preExperimentScreen():
    instText = "Press the return key to start the experiment."
    instFontSize = 40
    displayTextMultiline(canvas, instText, instFontSize, (0.4*xc, 0.3*yc), (1.6*xc, yc))
    pygame.display.update()
    wait(10)
    waitForKeypress()
    clearCanvas()

def instructions(phase):
    pygame.mouse.set_visible(0)
    if phase=='NounTrain1':
        instText = "Gude! Nem bilong mi emi Samson.\n\nI am here to help you learn my native language. It is called: Panitok.\n\nIf you can learn to speak just like me, then you will have learned Panitok successfully.\n\nWe will start with something easy."
        instAudio = pygame.mixer.Sound('audio/instructions/NounExposure1.wav')
        instFontSize = 40
    elif phase=='NounTrain2':
        instText = "First, I will teach you some simple words in Panitok\n\nI will show you pictures and say their name in my language.\n\nYou must REPEAT the names aloud after me.\n\nAfter each word, press the return key to move on to the next one.\n\nPress the return key when you're ready to get started."
        instAudio = pygame.mixer.Sound('audio/instructions/NounExposure2.wav')
        instFontSize = 40
    elif phase=='NounTest':
        instText = "Ok. Now it is time to take a short test on what you have learned so far.\n\nI will show you pictures or names in Panitok.\n\nWhen I show you a picture, you have to select the correct name; when I show you a name, you have to select the correct picture.\n\nUse the mouse to CLICK ON THE CORRECT NAME OR PICTURE.\n\nPress the return key when you're ready to start the test."
        instFontSize = 36
        instAudio = pygame.mixer.Sound('audio/instructions/NounSelection.wav')
    elif phase=='NounProductionTest':
        instText = "Good job! Before we move on to the next training phase, I want to see how well you can speak Panitok so far.\n\nI will now show you some pictures, and you will have to SAY THEIR NAME in Panitok.\n\nSpeak clearly into the microphone in front of you, and press the return key when you finish naming each picture.\n\nPress the return key when you're ready to start speaking."
        instFontSize = 36
        instAudio = pygame.mixer.Sound('audio/instructions/NounProduction.wav')
    elif phase=='SpeakerFamiliarisation':
        instText = "Well done! You have made it through your first tests!\n\nIn the next phase, you will get to know some of my friends, who also speak Panitok.\n\nThey will teach you some more complex features of the language.\n\nBut first, they will introduce themselves to you in Panitok.\n\nAfter each introduction, you have to tell me who you have just met.\n\nUse the mouse to CLICK ON THE CORRECT PICTURE of the speaker.\n\nPress the return key when you are ready to meet them."
        instFontSize = 30
        instAudio = pygame.mixer.Sound('audio/instructions/SpeakerFam.wav')
    elif phase=='GroupCategorisation':
        instText = "Ok, now I want to see how well you know my friends.\n\nYou will hear each speaker introduce themselves once again.\n\nAfter each introduction, you have to choose the group of speakers you think that speaker belongs to.\n\nUse the mouse to CLICK ON THE CORRECT GROUP each time.\n\nPress the return key when you are ready to begin."
        instFontSize = 36
        instAudio = pygame.mixer.Sound('audio/instructions/GroupCategorisation.wav')
    # elif phase=='Learning':
    #     instText = "Great! Now my friends will teach you some more complex features of Panitok.\n\nThey will do this through two simple tasks.\n\nIn the first task, they will take turns to say phrases in Panitok that you have not heard before, and you have to select the picture you think the phrase describes.\n\nIn the second task, you will hear one of them describe a picture in Panitok, and you have to select the group of speakers you think the current speaker belongs to.\n\nUse the mouse to CLICK ON THE CORRECT PICTURE OR GROUP OF SPEAKERS each time.\n\nPress the return key when you are ready to start."
    #     instFontSize = 30
    #     instAudio = pygame.mixer.Sound('audio/instructions/PhraseLearning.wav')
    elif phase=='Learning':
        instText = "Great! Now my friends will teach you some more complex features of Panitok.\n\nThey will take turns to say phrases in Panitok that you have not heard before, and you have to select the picture you think the phrase describes.\n\nUse the mouse to CLICK ON THE CORRECT PICTURE each time.\n\nPress the return key when you are ready to start."
        instFontSize = 30
        instAudio = pygame.mixer.Sound('audio/instructions/PhraseLearningOneTask.wav')
    elif phase=='CueTesting':
        instText = "Good job! You are now ready for testing.\n\nIn this following task, you will see some phrases in Panitok that my friends use to describe pictures.\n\nFor each phrase, you have to select who you think said it.\n\nUse the mouse to CLICK ON THE CORRECT SPEAKER each time.\n\nPress the return key when you are ready to start the test."
        instFontSize = 36
        instAudio = pygame.mixer.Sound('audio/instructions/CueCategorisation.wav')
    elif phase=='ProductionTest':
        instText = "Ok, you are ready for your final test: you will now play a simple game of describing pictures to my friends!\n\nI will show you some pictures alongside one of my friends.\n\nEach time, you have to describe the picture in Panitok to my friend, so that he or she will be able to recognise it.\n\nYou will be provided with feedback every now and then to help refresh your memory.\n\nPress the return key when you are ready to start speaking."
        instFontSize = 36
        instAudio = pygame.mixer.Sound('audio/instructions/Production.wav')
    elif phase=='Questionnaire':
        instText = "Well done!\n\nThat is all the Panitok you will learn today. Thank you very much for your interest in my language.\n\nBefore you leave, I would like to ask you some questions about certain features of Panitok.\n\nUse the keyboard to type in your answers.\n\nPress the return key to start answering the questions."
        instFontSize = 36
        instAudio = pygame.mixer.Sound('audio/instructions/Questionnaire.wav')
    displayTextMultiline(canvas, instText, instFontSize, (0.4*xc, 0.3*yc), (1.6*xc, yc))
    pygame.display.update()
    wait(10)
    pygame.mixer.Sound.play(instAudio)
    while pygame.mixer.get_busy():
       pass
    if phase != 'NounTrain1':
        waitForKeypress()
    clearCanvas()
    
def displayText(text, fontSize, xyCoords, colour=(0,0,0)):
    # displays text string centred on xyCoords
    font = pygame.font.SysFont('Arial', fontSize)
    text = font.render(text, 1, colour)
    text_rect = text.get_rect(center=(xyCoords))
    canvas.blit(text, text_rect)
    return text_rect

def displayTextMultiline(surface, text, fontSize, textPos, textSize, colour=(0,0,0)):
    # function to blit multiline text to surface because there is no easy way to do this in pygame
    # textPos specifies position of top left corner of textarea within the surface
    # textSize specifies size of the textarea
    font = pygame.font.SysFont('Arial', fontSize)
    words = [word.split(' ') for word in text.splitlines()]
    space = font.size(' ')[0]  # specify space width
    maxWidth, maxHeight = textSize    # specify textarea size
    x, y = textPos
    for line in words:
        for word in line:
            wordSurface = font.render(word, 1, colour)
            wordWidth, wordHeight = wordSurface.get_size()
            if x + wordWidth >= maxWidth:
                x = textPos[0]      # reset x pos
                y += wordHeight     # start on new row
            surface.blit(wordSurface, (x, y))
            x += wordWidth + space
        x = textPos[0]
        y += wordHeight
    
def clearCanvas():
    pygame.mouse.set_visible(0)
    canvas.fill((255,255,255))
    pygame.display.update()
    
def displayOptionBoxes(selectionTask):
    if selectionTask == 'image':
        pygame.draw.rect(canvas, (0,0,0), [0.4*xc-150, 1.2*yc-150, 300, 300], 2)
        pygame.draw.rect(canvas, (0,0,0), [1.6*xc-150, 1.2*yc-150, 300, 300], 2)
    elif selectionTask == 'label':
        pygame.draw.rect(canvas, (0,0,0), [0.4*xc-150, 1.2*yc-40, 300, 80], 2)
        pygame.draw.rect(canvas, (0,0,0), [1.6*xc-150, 1.2*yc-40, 300, 80], 2)
    elif selectionTask == 'category':
        pygame.draw.circle(canvas, (211,211,211), (int(0.4*xc), int(1.2*yc)), 150)
        pygame.draw.circle(canvas, (211,211,211), (int(1.6*xc), int(1.2*yc)), 150)

def wait(timeInMs):
    # waits for a specified duration (ms)
    t0 = pygame.time.get_ticks()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(), pygame.quit()
        tE = pygame.time.get_ticks() - t0
        pygame.display.update()
        if tE > timeInMs:
            break

def waitForKeypress():
    waiting = True
    while waiting:
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    waiting = False
                    break
            elif event.type == pygame.QUIT:
                sys.exit(), pygame.quit()
    
def waitForClick(leftObjDims, rightObjDims):
    # wait for mouse click on comprehension trials
    # object dimensions must be in the form of a tuple corresponding to
    # object x centre, object y centre, object width, object height
    
    leftObjXC, leftObjYC, leftObjW, leftObjH = leftObjDims[0], leftObjDims[1], leftObjDims[2], leftObjDims[3]
    rightObjXC, rightObjYC, rightObjW, rightObjH = rightObjDims[0], rightObjDims[1], rightObjDims[2], rightObjDims[3]
    
    clicked = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        x,y = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0]==1:
            if leftObjXC-0.5*leftObjW<x<leftObjXC+0.5*leftObjW and leftObjYC-0.5*leftObjH<y<leftObjYC+0.5*leftObjH:
                clicked = 'L'
                break
            elif rightObjXC-0.5*rightObjW<x<rightObjXC+0.5*rightObjW and rightObjYC-0.5*rightObjH<y<rightObjYC+0.5*rightObjH:
                clicked = 'R'
                break
    
    return clicked

def record(recordingsDirPath, expPhase, globalTrialNo):
    rec = subprocess.Popen(['sox -d -c 1 -b 16 -r 44100 {0}/{1}_{2}_{3}_{4}.wav'.format(recordingsDirPath, subjNo, condition, expPhase, globalTrialNo)], shell=True)
  
def displayFeedback(targPos, clickPos):
    # display feedback post-click on comprehension trials
    if targPos == 'L':
        canvas.blit(whitePNG, (1.6*xc-250, yc-150))
    elif targPos == 'R':
        canvas.blit(whitePNG, (0.4*xc-250, yc-150))
    pygame.display.update()
    if targPos == clickPos:
        pygame.mixer.Sound.play(correct)
    else:
        pygame.mixer.Sound.play(wrong)
    while pygame.mixer.get_busy():
        pass
    wait(10)

def selectSpeakers(condition):
    speakersMale = ['m1', 'm2', 'm3', 'm4', 'm5', 'm6']
    speakersFemale = ['f1', 'f2', 'f3', 'f4', 'f5', 'f6']
    conditionsList = [1,2,3,4,5,6]
    genderDict = {}
    if condition in conditionsList:
        if condition==3 or condition==4 or condition==6:
            genderDict['female'] = [randomWithRemove(speakersFemale) for i in range(4)]
            genderDict['male'] = [randomWithRemove(speakersMale) for i in range(4)]
            genderDict['extras'] = speakersFemale + speakersMale
        else:
            if majorityGroup == 'f':
                genderDict['female'] = speakersFemale
                genderDict['male'] = [randomWithRemove(speakersMale) for i in range(2)]
                genderDict['extras'] = speakersMale     # for selecting target group speakers on group categorisation trials in conditions 1, 2, 5
            elif majorityGroup == 'm':
                genderDict['female'] = [randomWithRemove(speakersFemale) for i in range(2)]
                genderDict['male'] = speakersMale
                genderDict['extras'] = speakersFemale   # for selecting target group speakers on group categorisation trials in conditions 1, 2, 5
    else:
        raise Exception('Please enter a valid condition (1-6)')
    print genderDict
    return genderDict


def generateSpeakerItemDicts(condition, speakerIDs):
    # integrating Kenny's counterbalancing code (with slight modifications) to experiment
    # this code now returns a list object containing five sublists, one for each of the four learning blocks and one for the cue test block
    # elements within each sublist are dictionaries corresponding to individual trials
    # note that cueSkew, varSkew and conditioning here are specific to this function and
    # are not equivalent to cueDist, varDist and conditioning in the rest of the script
    # (varSkew for Kenny refers to the overall distribution of markers across the experiment, as opposed to distribution with each cue)
    # but the mapping of conditions (1-6) to cueSkew, varSkew and conditioning in the final conditional of the function should sort this out

    def shuffle(l):
        return random.sample(l, len(l))  
    
    #builds a new list with n occurences of each element of a_list, 
    #like rep(a_list,each=n) in R
    def rep_each(a_list,n):
        if a_list==[]:
            return []
        else:
            return [a_list[0]]*n + rep_each(a_list[1:],n)
            
    # builds a new list containing n copies of a_list, each shuffled
    #equovalent to replicate(n,sample(a_list)) in R
    def shuffle_build(a_list,n):
        if n==0:
            return []
        else:
            return shuffle(a_list) + shuffle_build(a_list,n-1)
    
    #fuggly, but needed for numbers - need to dadd duplicate numbers, want to balance
    #occurence of numbers as much as possible
    def shuffle_build_special(a_list,spares_list,n):
        if n==0:
            return []
        else:
            return shuffle(a_list + [spares_list[n-1]]) + shuffle_build_special(a_list,spares_list,n-1)
        
    #data is a list of categories [c1,c2,c1,c2,c2,...]
    #distributes ids from category1_ids,category2_ids in order based on this
    def interleave_categorical(categories,category1,category2,category1_ids,category2_ids):
        c1_counter = 0
        c2_counter = 0
        interleaved_list = []
        for c in categories:
            if (c==category1):
                interleaved_list.append(category1_ids[c1_counter])
                c1_counter += 1
            elif (c==category2):
                interleaved_list.append(category2_ids[c2_counter])
                c2_counter += 1 
        return interleaved_list
            
    def add_categorical_cue(data,cueSkew,variantSkew,conditioning):
        ## group categories (m/f) either have 4/4 or 6/2 members
        if (cueSkew=='balanced'):
            majorityGroup_n = 4
            minorityGroup_n = 4
            cues = [c1]*2 + [c2]*2
        elif (cueSkew=='skewed'):
            majorityGroup_n = 6
            minorityGroup_n = 2
            cues = [c1]*3 + [c2]*1
        
        if (conditioning=='unconditioned' and variantSkew=='balanced'):
            desired_c1_marker_count = 2 #every member of c1 should appear twice with V1 (and twice with V2) 
            desired_c2_marker_count = 2 #ditto c2
        elif (conditioning=='unconditioned' and variantSkew=='skewed'):
            desired_c1_marker_count = 3 #every member of c1 should appear thrice with V1 (and once with V2) 
            desired_c2_marker_count = 3 #ditto c2
        elif (conditioning=='conditioned' and variantSkew=='balanced'):
            desired_c1_marker_count = 3 #every member of c1 should appear thrice with V1 (and once with V2) 
            desired_c2_marker_count = 1 #and vice versa for the other category
        elif (conditioning=='conditioned' and variantSkew=='skewed'):
            desired_c1_marker_count = 3 #every member of c1 should appear thrice with V1 (and once with V2) 
            desired_c2_marker_count = 1 #and vice versa for the other category
    
        #this ensure each single category instance exemplifies the correct proportion of cues
        #e.g. ensures that each noun exemplifies the appropriate distribution over speaker genders
        #what this doesn't do is ensure that e.g. each gender automatically uses the desired proportion of markers
        #so I will have to check that afterwards
        valid_cue_assignment = False
        while not(valid_cue_assignment):
            #do the assignment
            for trial,cue in zip(data,shuffle_build(cues,8)):
                trial['gender'] = cue
            #check the assignment - does each cue occur with the desired marker frequency?
            c1_count = len([d for d in data if d['gender']==c1 and d['marker']==v1])
            c2_count = len([d for d in data if d['gender']==c2 and d['marker']==v1])
            print c1_count,c2_count
            if (c1_count == desired_c1_marker_count*majorityGroup_n) and (c2_count == desired_c2_marker_count*minorityGroup_n):
                valid_cue_assignment=True
        
    def add_categorical_cue_instances(data,cueSkew,variantSkew,conditioning):
        ## group categories (m/f) either have 4/4 or 6/2 members
        c1_cue_instances = [sp for sp in speakerIDs if c1 in sp]
        c2_cue_instances = [sp for sp in speakerIDs if c2 in sp]
        if (conditioning=='unconditioned' and variantSkew=='balanced'):
            desired_c1_marker_count = 2 #every member of c1 should appear twice with V1 (and twice with V2) 
            desired_c2_marker_count = 2 #ditto c2
        elif (conditioning=='unconditioned' and variantSkew=='skewed'):
            desired_c1_marker_count = 3 #every member of c1 should appear thrice with V1 (and once with V2) 
            desired_c2_marker_count = 3 #ditto c2
        elif (conditioning=='conditioned' and variantSkew=='balanced'):
            desired_c1_marker_count = 3 #every member of c1 should appear thrice with V1 (and once with V2) 
            desired_c2_marker_count = 1 #and vice versa for the other category
        elif (conditioning=='conditioned' and variantSkew=='skewed'):
            desired_c1_marker_count = 3 #every member of c1 should appear thrice with V1 (and once with V2) 
            desired_c2_marker_count = 1 #and vice versa for the other category
        
        print c1_cue_instances
        print c2_cue_instances
        
        #OK, once we have a working assignment there, can add in instances of the cues - 
        #doing this randomised, so again no guarantee that e.g. each speaker 
        #exemplifies the marker proportion correctly
        valid_cue_instance_assignment = False
        counter=0
        while not(valid_cue_instance_assignment):
            print counter
            counter+=1
            data_categories = [d['gender'] for d in data]
            cue_instances = interleave_categorical(data_categories,c1,c2,
                                                    shuffle(c1_cue_instances*4),
                                                    shuffle(c2_cue_instances*4))
            #do the assignment
            for trial,cue_instance in zip(data,cue_instances):
                trial['speaker'] = cue_instance
            #check the assignment
            c1_instance_counts = [len([d for d in data if d['marker']==v1 and d['speaker']==cci]) for cci in c1_cue_instances]
            c2_instance_counts = [len([d for d in data if d['marker']==v1 and d['speaker']==cci]) for cci in c2_cue_instances]
            print c1_instance_counts
            print c2_instance_counts
            if (all([c==desired_c1_marker_count for c in c1_instance_counts]) and 
                all([c==desired_c2_marker_count for c in c2_instance_counts])):
                valid_cue_instance_assignment=True
    
    #want each number to appear roughly equally often with each marker
    #want each number to appear at least once with each irrelevant feature instance
    #want each number to appear at least once with each cue category instance
    def add_numbers(data): 
        valid_number_assignment = False
        counter=0
        while not(valid_number_assignment):
            print counter
            counter+=1
            #do assignment randomly
            #this is pretty ugly, but life will be easier if I ensure numbers are approximately balanced
            spare_numbers = [2,3,4]*2+shuffle([2,3,4])[:2]
            numbers = shuffle_build_special([2,3,4],spare_numbers,8)
            for trial,n in zip(data,numbers):
                trial['number'] = n
            #check that each number occurs at the desired frequency for each variant
            number_counts_v1 = [len([d for d in data if d['marker']==v1 and d['number']==n]) for n in [2,3,4]]
            number_counts_v2 = [len([d for d in data if d['marker']==v2 and d['number']==n]) for n in [2,3,4]]
            print number_counts_v1
            print number_counts_v2
            #count how often each number occurs with each irrelevant instance
            irrelevant_instances = set([d['label'] for d in data])
            number_counts_by_irrelevant_instance = [len([d for d in data if d['label']==i and d['number']==n]) 
            for n in [2,3,4] for i in irrelevant_instances]
            print number_counts_by_irrelevant_instance
            
            #count how often each number occurs with each cue category instance
            cue_category_instances = set([d['speaker'] for d in data])
            number_counts_by_cue_category_instance = [len([d for d in data if d['speaker']==i and d['number']==n]) 
            for n in [2,3,4] for i in cue_category_instances]
            print number_counts_by_cue_category_instance
            
            if (#check each number to occur approx equally frequently with each variant
                (max(number_counts_v1)-min(number_counts_v1))<=1 and 
                (max(number_counts_v2)-min(number_counts_v2))<=1 and
                #check each number occurs at least once with each irrelevant and cue instance
                all([c>0 for c in number_counts_by_irrelevant_instance]) and
                all([c>0 for c in number_counts_by_cue_category_instance])
                ):
                    valid_number_assignment = True
    
    ################################################################
    ### jia's new bits to facilitate adding filler trial stims #####
    
    def add_trialtype(data):
        trialTypes = ['critical']*32
        for trial,trialType in zip(data,trialTypes):
            trial['trialType'] = trialType
    
    def generate_filler_trials():
        # generates a block of 8 filler trials where
        # each speaker occurs once, each lexical item occurs once, speaker-item pairing is random,
        # and each lexical item occurs with number 1 (singular)
        
        labels = uniqueShuffleList(['stoa', 'kontena', 'kilok', 'tebol', 'winim', 'golo', 'lukluk', 'sindaun'])
        speakers = uniqueShuffleList(speakerIDs)
        numbers = [1]*8
        trialTypes = ['filler']*8
        markers = [None]*8
        cueCats = [s[0] for s in speakers]
        
        fillerData = [{'gender': c, 'label': l, 'marker': m, 'speaker': s, 'number': n, 'trialType': tt} for c,l,m,s,n,tt in
            zip(cueCats, labels, markers, speakers, numbers, trialTypes)]
    
        return fillerData
    
    #######################################################################
    ### jia's new bits to add cue cat test dict ###########################
        
    def generate_cuetest_block(condition):
        # generates a block of 32 critical trials where
        # each speaker occurs 4 times, each lexical item occurs four times, speaker-item pairing is random,
        # lexical items are always plural with each item appearing with quantity 2, 3, 4 and random 2/3/4,
        # and each marker occurs with each speaker at the appropriate (50-50/75-25) frequency
        
        # list of labels, each label occurs 4x
        labels = rep_each(['stoa', 'kontena', 'kilok', 'tebol', 'winim', 'golo', 'lukluk', 'sindaun'], 4)
        
        # sublists of [2,3,4,x] where x is a random 2/3/4, flatten into 1d list
        numbers = reduce(lambda x,y: x+y, [[2,3,4] + [random.choice([2,3,4])] for x in range(8)])
        
        # zip labels and numbers to create label-number pairing (to ensure lexical items appear with appropriate quantity distribution)
        # shuffle so we get randomised order (because we will zip with speaker list later)
        labels_numbers = uniqueShuffleList(zip(labels, numbers))
        
        # unzip for label and number lists
        labels = [x[0] for x in labels_numbers]
        numbers = [x[1] for x in labels_numbers]
        
        if condition==2 or condition==3:
            # cue skew, variant skew
            majoritySpeakers = [s for s in speakerIDs if c1 in s]
            minoritySpeakers = [s for s in speakerIDs if c2 in s]
            majoritySpeakers_n = len(majoritySpeakers)
            minoritySpeakers_n = len(minoritySpeakers)
            speakers = [s for s in majoritySpeakers for s in 4*[s]] + [s for s in minoritySpeakers for s in 4*[s]]
            markerDist_c1 = [v1]*3 + [v2]*1
            markerDist_c2 = [v1]*1 + [v2]*3
            markers = markerDist_c1 * majoritySpeakers_n + markerDist_c2 * minoritySpeakers_n
        else:
            speakers = rep_each(speakerIDs, 4)
            if condition==1 or condition==4:
                # variant skew
                markerDist = [v1]*3 + [v2]*1
            elif condition==5 or condition==6:
                # variant uniform
                markerDist = [v1]*2 + [v2]*2
            markers = markerDist * len(speakerIDs)
        
        cueCats = [g[0] for g in speakers]
        
        cueTestData = [{'gender': c, 'label': l, 'marker': m, 'speaker': s, 'number': n} for c,l,m,s,n in
            zip(cueCats, labels, markers, speakers, numbers)]
        
        return cueTestData
    
    #######################################################################
    ### jia's new bits to add production test dict ########################
    
    def generate_production_block():
        # generates a block of 80 trials with:
        # 64 critical trials where
        # each speaker appears 8 times, each with one of the eight lexical items
        # lexical items are always plural with each item appearing with quantity 2 (x2), 3 (x2), 4 (x2) and random 2/3/4 (x2)
        # + 16 filler trials where
        # each speaker appears twice, each lexical item appears twice
        # lexical items are always singular
        
        # list of speakers, each speaker occurs 8x
        # where each speaker occurs once within each block of 8 (shuffled for random order to facilitate zipping with item-number pairing later)
        speakers = []
        [speakers.extend(uniqueShuffleList(speakerIDs)) for i in range(8)]
        
        # sublists of [2,3,4,x] where x is a random 2/3/4, flatten into 1d list
        numbers = reduce(lambda x,y: x+y, [[2]*2 + [3]*2 + [4]*2 + random.sample([2,3,4], 2) for x in range(8)])
        
        # list of labels, each label occurs 8x
        labels = rep_each(['stoa', 'kontena', 'kilok', 'tebol', 'winim', 'golo', 'lukluk', 'sindaun'], 8)
        
        cueCats = [g[0] for g in speakers]
        trialTypes = ['critical']*len(speakers)
        markers = [None]*len(speakers)
        
        productionData = [{'gender': c, 'label': l, 'marker': m, 'speaker': s, 'number': n, 'trialType': tt} for c,l,m,s,n,tt in
            zip(cueCats, labels, markers, speakers, numbers, trialTypes)]
        
        productionData += generate_filler_trials()
        productionData += generate_filler_trials()
        
        return productionData
        
    #######################################################################
    #######################################################################
    
    #each block consists of 32 trials
    #cue is either gender or semantic category
    #variant is the plural marker
    #there is an irrelevant category (nouns when cue is gender, speaker when cue is semantics)
    def generate_single_block(cueSkew,variantSkew,conditioning,write=False):
        if (conditioning=='conditioned' and cueSkew=='balanced' and variantSkew=='skewed'):
            print("This cannot be achieved!")
            return []
        elif (conditioning=='conditioned' and cueSkew=='skewed' and variantSkew=='balanced'):
            print("This cannot be achieved!")
            return []
        elif (conditioning=='conditioned' and variantSkew=='skewed'):
            print("This cannot be achieved in a single block!")
        else:
            #marker is either skewed 3-1 or balanced 2-2
            if (variantSkew=='balanced'):
                markers = [v1]*2 + [v2]*2
            elif (variantSkew=='skewed'):
                markers = [v1]*3 + [v2]*1
                
            ## 8 lexical items
            labels = uniqueShuffleList(['stoa', 'kontena', 'kilok', 'tebol', 'winim', 'golo', 'lukluk', 'sindaun'])
            
            #OK, start building trial list
            #First, ensure that each item from the irrelevant category exemplifies the target proportion
            #e.g. each noun exemplifies the appropriate distirbution
            data = [{'label':l,'marker':m} for l,m in 
                    zip(rep_each(labels,4), markers*8)]
                            
            #Next, add the categorical cue - spinning this out to a general function
            add_categorical_cue(data,cueSkew,variantSkew,conditioning)
            add_categorical_cue_instances(data,cueSkew,variantSkew,conditioning)
            add_numbers(data)
            add_trialtype(data)
            if write:
                filename = 'PythonCue'+cueSkew+'Variant'+variantSkew+'Conditioning'+conditioning+'.csv'
                with open(filename, 'ab') as csvfile:
                    csvwriter = csv.DictWriter(csvfile, 
                                    fieldnames=['label','gender',
                                                'speaker','marker','number'],
                                    restval='NA',extrasaction='ignore')
                    csvwriter.writeheader()
                    csvwriter.writerows(data)
            return data
    
    
    #this is only required when we want skewed cues and conditioned variation, 
    #in which case we need 5/8 items marked with V1, which isn't possible in a single block
    def generate_paired_blocks(write=False):
        markers = [v1]*5 + [v2]*3
        ## 8 lexical items
        labels = uniqueShuffleList(['stoa', 'kontena', 'kilok', 'tebol', 'winim', 'golo', 'lukluk', 'sindaun'])
        
        #ensures that both variants are at the correct frequency in each block - 
        #for each e.g. noun, odd numbers will occur 3 times with v1 in block 1, 2 times in block 2
        #for odd numbers, other way around
        blocks = ([1,2]*4+[2,1]*4)*4
        
        #build basic data list
        data = [{'label':l,'marker':m,'block':b} for l,m,b in zip(rep_each(labels,8), markers*8, blocks)]
        #now split into blocks
        data_block1 = [d for d in data if d['block']==1]
        data_block2 = [d for d in data if d['block']==2]
        
        #allocate cues for each block as in the single block case
        add_categorical_cue(data_block1,'skewed','skewed','conditioned')
        add_categorical_cue_instances(data_block1,'skewed','skewed','conditioned')
        add_numbers(data_block1)
        add_trialtype(data_block1)
        add_categorical_cue(data_block2,'skewed','skewed','conditioned')
        add_categorical_cue_instances(data_block2,'skewed','skewed','conditioned')
        add_numbers(data_block2)
        add_trialtype(data_block2)
        if write:
            filename = 'PythonCueskewedVariantskewedConditioningconditioned.csv'
            with open(filename, 'ab') as csvfile:
                csvwriter = csv.DictWriter(csvfile, 
                                    fieldnames=['label','gender',
                                                'speaker','marker','number'],
                                    restval='NA',extrasaction='ignore')
                csvwriter.writeheader()
                csvwriter.writerows(data_block1+data_block2)
        return data_block1,data_block2
        
    def generate_trial_blocks(params):
        # first unpack the params which are fed in as a tuple
        cueSkew, variantSkew, conditioning = params[0], params[1], params[2]
        if cueSkew=='skewed' and variantSkew=='skewed' and conditioning=='conditioned':
            block1,block2 = generate_paired_blocks()
            block3,block4 = generate_paired_blocks()
            for b in [block1,block2,block3,block4]:
                b += generate_filler_trials()
        else:
            block1=generate_single_block(cueSkew,variantSkew,conditioning) + generate_filler_trials()
            block2=generate_single_block(cueSkew,variantSkew,conditioning) + generate_filler_trials()
            block3=generate_single_block(cueSkew,variantSkew,conditioning) + generate_filler_trials()
            block4=generate_single_block(cueSkew,variantSkew,conditioning) + generate_filler_trials()
        return [block1,block2,block3,block4]
    
    paramList = [('skewed', 'skewed', 'unconditioned'), ('skewed', 'skewed', 'conditioned'), ('balanced', 'balanced', 'conditioned'), ('balanced', 'skewed', 'unconditioned'), ('skewed', 'balanced', 'unconditioned'), ('balanced', 'balanced', 'unconditioned')]
    
    learningDicts = generate_trial_blocks(paramList[condition-1])
    cueTestDict = generate_cuetest_block(condition)
    productionTestDict = generate_production_block()
    
    trialDicts = learningDicts + [cueTestDict] + [productionTestDict]
    
    return trialDicts

def loadItems():
    # pre-load images, labels and audio files
    # returns dict of key (meaning) - value (list of [image, image (small), label, audio]) mappings
    # for each lexical item
    
    itemsDict = {}
    for i in range(len(meanings)):
        img = pygame.image.load('{}images/items/large/{}.png'.format(filePath, meanings[i]))    # 350x350 px
        imgSmall1 = pygame.image.load('{}images/items/small/{}_1.png'.format(filePath, meanings[i]))    # 200x200 px
        imgSmall2 = pygame.image.load('{}images/items/small/{}_2.png'.format(filePath, meanings[i]))
        imgSmall3 = pygame.image.load('{}images/items/small/{}_3.png'.format(filePath, meanings[i]))
        imgSmall4 = pygame.image.load('{}images/items/small/{}_4.png'.format(filePath, meanings[i]))
        imgMed = pygame.image.load('{}images/items/medium/{}.png'.format(filePath, meanings[i]))    # 300x300 px
        imgLarge1 = pygame.image.load('{}images/items/large/{}_1.png'.format(filePath, meanings[i]))    # 350x350px
        imgLarge2 = pygame.image.load('{}images/items/large/{}_2.png'.format(filePath, meanings[i]))
        imgLarge3 = pygame.image.load('{}images/items/large/{}_3.png'.format(filePath, meanings[i]))
        imgLarge4 = pygame.image.load('{}images/items/large/{}_4.png'.format(filePath, meanings[i]))
        label = labels[i]
        audio = pygame.mixer.Sound('{}audio/{}.wav'.format(filePath, meanings[i]))
        key = meanings[i]
        itemsDict[key] = [img, imgSmall1, imgSmall2, imgSmall3 ,imgSmall4, imgMed, imgLarge1, imgLarge2, imgLarge3, imgLarge4, label, audio]
    
    return itemsDict

def loadSpeakers(genderDict):
    # pre-load avatar images (small = 150x150px; regular = 300x300px)
    # and audio files for each speaker
    # returns dict of key (speakerID) - value (list of [avatar img, small avatar img, intro audio]) mappings
    namesDict = {'m1': 'Danny', 'm2': 'Jack', 'm3': 'Caleb', 'm4': 'Silas', 'm5': 'Viktor', 'm6': 'Iven',
                 'f1': 'Laila', 'f2': 'Tessie', 'f3': 'Rosalind', 'f4': 'Kina', 'f5': 'Arisa', 'f6': 'Nancy'}
    speakerIDs = genderDict['male'] + genderDict['female']
    speakersDict = {}
    for i in speakerIDs:
        avatar = pygame.image.load('{}images/avatars/{}.png'.format(filePath, i))
        avatarMed = pygame.image.load('{}images/avatars/medium/{}.png'.format(filePath, i))
        avatarSmall = pygame.image.load('{}images/avatars/small/{}.png'.format(filePath, i))
        audioIntro = pygame.mixer.Sound('{}audio_speakers/introsscaled/intro_{}.wav'.format(filePath, i))
        audioIntroShort = pygame.mixer.Sound('{}audio_speakers/introsscaled/introshort_{}.wav'.format(filePath, i))
        name = namesDict[i]
        key = i
        speakersDict[key] = [avatar, avatarMed, avatarSmall, audioIntro, audioIntroShort, name]
        
    # adding a dict of extra speakers (outside of the 8 regular speakers in the expt)
    # expt will draw from these speakers when choosing avatars to display for the target group
    # on group categorisation trials since in some conditions (1/2/5) there is only one
    # other speaker of the target gender besides the target speaker
    extraSpeakerIDs = genderDict['extras']
    extraSpeakersDict = {}
    for i in extraSpeakerIDs:
        avatarSmall = pygame.image.load('{}images/avatars/small/{}.png'.format(filePath, i))
        key = i
        extraSpeakersDict[key] = [avatarSmall]

    return speakersDict, extraSpeakersDict

def loadMiscObjects():
    global whitePNG, bubble, correct, wrong
    whitePNG = pygame.transform.scale(pygame.image.load('{}images/white.png'.format(filePath)), (500,500))
    bubble = pygame.image.load('{}images/bubble.png'.format(filePath))
    correct = pygame.mixer.Sound('{}audio/correct.wav'.format(filePath))
    wrong = pygame.mixer.Sound('{}audio/wrong.wav'.format(filePath))
    
def createDataFile(filePath, subjNo):
    dataFilePath = filePath + 'data/'
    if not os.path.exists(dataFilePath):
        os.makedirs(dataFilePath)
    dataFile = '{0}sub{1}.csv'.format(dataFilePath, subjNo)
    header = ['ID', 'study', 'experiment', 'condition', 'cueDist', 'varDist', 'varType', 'markers', 'majCat', 'majVar', 'phase', 'selectionTask', 'trialType', 'globalTrial', 'localTrial', 'nounItem', 'number', 'inputMarker', 'inputNoun', 'targetPosition', 'clickPosition', 'foilItem', 'foilNumber', 'category', 'foilCategory', 'speaker', 'targetSpeaker', 'foilSpeaker', 'spokenResponse', 'answerQuest', 'timeStamp']
    with open(dataFile, 'wb') as f:
        writer = csv.writer(f)
        writer.writerow(header)
    return dataFile

def writeDataToFile(dataToLog):
    with open(dataFile, 'ab') as f:
        writer = csv.writer(f)
        writer.writerow(dataToLog)

class NounTrain:
    '''Build trial for Noun Training Phase'''
    
    def __init__(self, itemName):
        # create instance of lexical item
        self.itemName = itemName
        self.itemImage = itemsDict[itemName][0]
        self.itemLabel = itemsDict[itemName][10]
        self.itemAudio = itemsDict[itemName][11]
        self.inputNoun = self.itemLabel   # for logging
    
    def returnTrialStim(self):
        # return trial stim to log
        return [self.itemName, self.inputNoun]
    
    def showImage(self):
        # blit image to screen for duration of timeInMs
        canvas.blit(self.itemImage, (xc-imgWL/2, yc-imgHL/2))
        pygame.display.update()
        wait(1000)
    
    def showLabel(self):
        # display label on screen for duration of timeInMs
        displayText(self.itemLabel, 50, (xc, 0.4*yc))
        wait(5)
    
    def playAudio(self):
        # play sound file for current label
        pygame.mixer.Sound.play(self.itemAudio)
        while pygame.mixer.get_busy():
            pass
        
    def startRecording(self, recDirPath, expPhase, globalTrialNo):
        # start recording, stop recording 500ms after space press
        recording = True
        threading.Thread(target = record(recDirPath, expPhase, globalTrialNo))
        while recording:
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        wait(500)
                        recording = False
                        os.system('pkill sox')
                        break
    
    def clear(self):
        clearCanvas()
        
class NounTest:
    '''Build trial for Noun Testing Phase'''
    
    def __init__(self, itemName):
        # create instance of lexical item
        self.itemName = itemName
        self.itemImage = itemsDict[itemName][5]
        self.itemLabel = itemsDict[itemName][10]
        self.itemAudio = itemsDict[itemName][11]
        self.distItemName = random.choice(filter(lambda x: x != itemName, meanings))
        self.distItemLabel = itemsDict[self.distItemName][10]
        self.inputNoun = self.itemLabel   # for logging
        
    def returnTrialStim(self):
        # return trial stim to log
        return [self.itemName, self.inputNoun, self.distItemName, self.distItemLabel]

    def showImage(self):
        # display image on label selection trials
        pygame.display.set_caption('Click on the correct word')
        pygame.mouse.set_pos(mousePos)
        pygame.mouse.set_visible(1)
        canvas.blit(self.itemImage, (xc-imgWM/2, 0.7*yc-imgHM/2))
        pygame.display.update()
    
    def showLabel(self):
        # display label on image selection trials
        pygame.display.set_caption('Click on the correct object')
        pygame.mouse.set_pos(mousePos)
        pygame.mouse.set_visible(1)
        displayText(self.itemLabel, 50, (xc, 0.4*yc))
        pygame.display.update()
    
    def showLabelOptions(self, targPos):
        # display target and distractor labels on label selection trials
        displayOptionBoxes('label')
        targLabel = self.itemLabel
        if targPos=='R':
            displayText(targLabel, 60, (1.6*xc, 1.2*yc))
            displayText(self.distItemLabel, 60, (0.4*xc, 1.2*yc))
        elif targPos=='L':
            displayText(targLabel, 60, (0.4*xc, 1.2*yc))
            displayText(self.distItemLabel, 60, (1.6*xc, 1.2*yc))
        pygame.display.update()
        
    def showImageOptions(self, targPos):
        # display target and distractor images on image selection trials
        displayOptionBoxes('image')
        targImg = self.itemImage
        distImg = itemsDict[self.distItemName][5]
        if targPos=='L':
            canvas.blit(targImg, (0.4*xc-imgWM/2, 1.2*yc-imgHM/2))
            canvas.blit(distImg, (1.6*xc-imgWM/2, 1.2*yc-imgHM/2))
        elif targPos=='R':
            canvas.blit(targImg, (1.6*xc-imgWM/2, 1.2*yc-imgHM/2))
            canvas.blit(distImg, (0.4*xc-imgWM/2, 1.2*yc-imgHM/2))
        pygame.display.update()
    
    def feedback(self, targPos, clickPos):
        # display feedback
        displayFeedback(targPos, clickPos)
    
    def playAudio(self):
        # play audio associated with correct label/image during feedback
        # wait(1500)
        pygame.mixer.Sound.play(self.itemAudio)
        wait(1500)
    
    def getClick(self, leftObjDims, rightObjDims):
        # check for click on either object
        clickPos = waitForClick(leftObjDims, rightObjDims)
        return clickPos
    
    def clear(self):
        clearCanvas()
        
class NounProductionTest:
    '''Build trial for Noun Production Testing Phase'''
    
    def __init__(self, itemName):
        # create instance of lexical item
        self.itemName = itemName
        self.itemImage = itemsDict[itemName][0]
        self.itemLabel = itemsDict[itemName][10]
        self.itemAudio = itemsDict[itemName][11]
        
    def returnTrialStim(self):
        # return trial stim to log
        return [self.itemName]
        
    def showImage(self):
        # display image on production trials
        wait(500)
        canvas.blit(self.itemImage, (xc-imgWL/2, yc-imgHL/2))
    
    def showHyphens(self):
        # display string of hyphens corresponding to the number of letters in label
        hyphensToDisplay = '-'* len(self.itemLabel)
        displayText(hyphensToDisplay, 50, (xc, 0.4*yc))
        pygame.display.update()
        
    def startRecording(self, recDirPath, expPhase, globalTrialNo):
        # start recording, stop recording 500ms space press
        recording = True
        threading.Thread(target = record(recDirPath, expPhase, globalTrialNo))
        while recording:
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        wait(500)
                        recording = False
                        os.system('pkill sox')
                        break
    
    def feedback(self):
        # display label for each item post participant production
        clearCanvas()
        canvas.blit(self.itemImage, (xc-imgWL/2, yc-imgHL/2))
        displayText(self.itemLabel, 50, (xc, 0.4*yc))
        pygame.display.update()
        wait(0)
    
    def playAudio(self):
        # play audio associated with each item post participant production
        # wait(1000) before moving on to next trial
        pygame.mixer.Sound.play(self.itemAudio)
        while pygame.mixer.get_busy():
            pass
        wait(1000)
    
    def clear(self):
        clearCanvas()

class SpeakerFamiliarisation:
    '''Build trial for Speaker Familiarisation Phase'''
    
    def __init__(self, speakerID):
        # create instance of a speaker
        self.speakerID = speakerID
        self.speakerAvatar = speakersDict[speakerID][0]
        self.speakerIntro = speakersDict[speakerID][3]
        self.speakerName = speakersDict[speakerID][5]
        self.distSpeakerID = random.choice(filter(lambda x: x != self.speakerID and x[0] != self.speakerID[0], speakersDict.keys()))    # randomly select distractor speaker avatar on constraint that it is a different gender by filtering by first char of speakerID
    
    def returnTrialStim(self):
        return [self.speakerID, self.distSpeakerID]
        
    def showAvatar(self):
        # display speaker avatar during speaker introduction
        pygame.display.set_caption('Speaker introduction')
        pygame.mouse.set_visible(0)
        canvas.blit(self.speakerAvatar, (xc-imgWL/2, yc-imgHL/2))
        pygame.display.update()
        wait(1000)
        
    def showGloss(self):
        # diplay gloss of speaker introduction
        introText = "Good day! My name is {}.\nToday, I will teach you my language, Panitok.\nNice to meet you!".format(self.speakerName)
        displayText('"', 100, (0.4*xc, 0.25*yc))
        displayText('"', 100, (1.6*xc, 0.45*yc))
        displayTextMultiline(canvas, introText, 36, (0.5*xc, 0.2*yc), (2*xc, yc), (125,125,125))
        pygame.display.update()
        wait(10)
    
    def playIntro(self):
        # wait 1000ms after avatar appears, play speaker intro
        pygame.mixer.Sound.play(self.speakerIntro)
        while pygame.mixer.get_busy():
            pass
    
    def showOptions(self, targPos):
        # wait 100ms after intro playback offset, display target and distractor speakers
        wait(100)
        clearCanvas()
        pygame.display.set_caption('Click on the speaker you just met')
        pygame.mouse.set_pos(mousePos)
        pygame.mouse.set_visible(1)
        displayOptionBoxes('image')
        allSpeakers = speakersDict.keys()
        targAvatar = speakersDict[self.speakerID][0]
        distAvatar = speakersDict[self.distSpeakerID][0]
        if targPos=='L':
            canvas.blit(targAvatar, (0.4*xc-imgWM/2, 1.2*yc-imgHM/2))
            canvas.blit(distAvatar, (1.6*xc-imgWM/2, 1.2*yc-imgHM/2))
        elif targPos=='R':
            canvas.blit(targAvatar, (1.6*xc-imgWM/2, 1.2*yc-imgHM/2))
            canvas.blit(distAvatar, (0.4*xc-imgWM/2, 1.2*yc-imgHM/2))
        displayText('Who did you just meet?', 20, (xc, 0.2*yc))
        pygame.display.update()
    
    def getClick(self, leftObjDims, rightObjDims):
        # check for click on either object
        clickPos = waitForClick(leftObjDims, rightObjDims)
        return clickPos
    
    def feedback(self, targPos, clickPos):
        # display feedback
        displayFeedback(targPos, clickPos)
        wait(1000)

    def clear(self):
        clearCanvas()
        wait(100)

class GroupCategorisation:
    '''Build trial for Group Categorisation Phase'''
    
    def __init__(self, speakerID):
        # create instance of a speaker
        self.speakerID = speakerID
        self.speakerIntroShort = speakersDict[speakerID][4]
        self.speakerName = speakersDict[speakerID][5]
        self.category = speakerID[0]
        genders = ['m', 'f']
        self.distCategory = filter(lambda x: x != self.category, genders)[0]
        
        # create target speakers and distractor speakers lists to use when displaying options on categorisation trials
        self.targGender = speakerID[0]
        self.distGender = self.distCategory
        if self.targGender == minorityGroup:
            extraSpeaker = random.choice([speaker for speaker in extraSpeakersDict.keys() if self.targGender in speaker])
            self.targSpeakers =  [random.choice([speaker for speaker in speakersDict.keys() if self.targGender in speaker and speaker != speakerID])] + [extraSpeaker]
            self.targGroup = [speakersDict[speakerID][2]] + [extraSpeakersDict[extraSpeaker][0]]
        else:
            self.targSpeakers = random.sample([speaker for speaker in speakersDict.keys() if self.targGender in speaker and speaker != speakerID], 2)
            self.targGroup = [speakersDict[i][2] for i in self.targSpeakers]
        self.distSpeakers = random.sample([speaker for speaker in speakersDict.keys() if self.distGender in speaker], 2)
        self.distGroup = [speakersDict[i][2] for i in self.distSpeakers]
    
    def returnTrialStim(self):
        return [self.speakerID, self.targSpeakers, self.distSpeakers, self.category, self.distCategory]

    def showGloss(self):
        # diplay gloss of speaker introduction
        pygame.mouse.set_visible(0)
        introText = " My name is {}.".format(self.speakerName)
        displayText('"', 100, (0.6*xc, 0.4*yc))
        displayText('"', 100, (1.4*xc, 0.4*yc))
        displayText(introText, 36, (xc, 0.4*yc), colour=(125,125,125))
        pygame.display.update()
        wait(10)
    
    def playIntro(self):
        # wait 1000ms after avatar appears, play speaker intro
        pygame.mixer.Sound.play(self.speakerIntroShort)
        while pygame.mixer.get_busy():
            pass

    def showOptions(self, targPos):
        # wait 100ms after intro playback offset, display target and distractor speakers
        clearCanvas()
        pygame.display.set_caption('Click on the correct group')
        pygame.mouse.set_pos(mousePos)
        pygame.mouse.set_visible(1)
        displayOptionBoxes('category')
        if targPos == 'L':
            for i in range(2):
                canvas.blit(self.targGroup[i], (0.4*xc-imgWS/2+imgWS/2*i, 1.2*yc-50))
            for i in range(2):
                canvas.blit(self.distGroup[i], (1.6*xc-imgWS/2+imgWS/2*i, 1.2*yc-50))
        elif targPos == 'R':
            for i in range(2):
                canvas.blit(self.targGroup[i], (1.6*xc-imgWS/2+imgWS/2*i, 1.2*yc-50))
            for i in range(2):
                canvas.blit(self.distGroup[i], (0.4*xc-imgWS/2+imgWS/2*i, 1.2*yc-50))
        displayText('Click on the group the speaker belongs to', 20, (xc, 0.2*yc))
        pygame.display.update()
        
    def getClick(self, leftObjDims, rightObjDims):
        # check for click on either object
        clickPos = waitForClick(leftObjDims, rightObjDims)
        return clickPos

    def feedback(self, targPos, clickPos):
        displayFeedback(targPos, clickPos)
        wait(1000)
    
    def clear(self):
        clearCanvas()
        wait(100)
    
class VariantLearning:
    '''Build variant learning trial'''
    
    def __init__(self, speakerID, label, marker, quantity, category, trialType):
        # create instance of variant learning trial stim
        self.speakerID = speakerID
        self.avatarMed = speakersDict[speakerID][1]
        self.label = label
        self.marker = marker
        self.quantity = quantity
        self.category = category
        self.trialType = trialType
        
        if trialType == 'critical':
            self.itemName = meanings[labels.index(self.label)]
            self.itemImage = itemsDict[self.itemName][0]
            self.distItemName = self.itemName
            self.distItemQuantity = 1
            self.targImg = itemsDict[self.itemName][self.quantity]
            self.distImg = itemsDict[self.itemName][1]
            self.inputNoun = self.label    # for logging
            self.itemAudio = pygame.mixer.Sound('{}audio_speakers/{}scaled/{}{}_{}.wav'.format(filePath, speakerID, self.marker, self.itemName, speakerID))
        elif trialType == 'filler':
            self.itemName = meanings[labels.index(self.label)]
            self.distItemName = self.itemName #random.choice(filter(lambda x: x != self.itemName, meanings))
            self.distItemQuantity = random.choice([2,3,4])
            self.targImg = itemsDict[self.itemName][1]
            self.distImg = itemsDict[self.distItemName][self.distItemQuantity]
            self.marker = 'NA'
            self.inputNoun = self.label        # for logging
            self.itemAudio = pygame.mixer.Sound('{}audio_speakers/{}scaled/{}_{}.wav'.format(filePath, speakerID, self.itemName, speakerID))
        genders = ['m', 'f']
        self.distCategory = filter(lambda x: x != self.category, genders)[0]
        
    def returnTrialStim(self):
        # return trial stim to log
        return [self.itemName, self.quantity, self.marker, self.inputNoun, self.distItemName, self.distItemQuantity, self.category, self.distCategory]
            
    def showInstruction(self):
        pygame.display.set_caption('Click on the correct image')
        displayText('Click on the image that matches the phrase', 20, (xc, 0.2*yc))
        pygame.display.update()
        
    def showNounPhrase(self):
        # display NP in speech bubble on screen
        pygame.mouse.set_visible(0)
        canvas.blit(bubble, (xc-200, 0.3*yc))
        if self.trialType == 'critical':
            displayText('{} {}'.format(self.marker, self.label), 50, (xc, 0.4*yc))
        elif self.trialType == 'filler':
            displayText(self.label, 50, (xc, 0.4*yc))
        pygame.display.update()
    
    def showAvatar(self):
        # display avatar associated with current speaker
        #displayText('speaker:', 36, (xc, 0.2*yc))
        canvas.blit(self.avatarMed, (xc-75, 0.7*yc-75))
        pygame.display.update()
    
    def playAudio(self):
        # play sound file for current NP
        wait(250)
        pygame.mixer.Sound.play(self.itemAudio)
        while pygame.mixer.get_busy():
            pass
        
    def feedback(self, targPos, clickPos):
        displayFeedback(targPos, clickPos)
        wait(1000)
    
    def showOptions(self, targPos):
        # show options (singular and plural items) for variant learning trial
        pygame.mouse.set_pos([xc, 0.3*yc])
        pygame.mouse.set_visible(1)
        displayOptionBoxes('image')
        if targPos=='L':
            canvas.blit(self.targImg, (0.4*xc-imgWS/2, 1.2*yc-imgHS/2))
            canvas.blit(self.distImg, (1.6*xc-imgWS/2, 1.2*yc-imgHS/2))
        elif targPos=='R':
            canvas.blit(self.distImg, (0.4*xc-imgWS/2, 1.2*yc-imgHS/2))
            canvas.blit(self.targImg, (1.6*xc-imgWS/2, 1.2*yc-imgHS/2))
        pygame.display.update()

    def getClick(self, leftObjDims, rightObjDims):
        # check for click on either object
        clickPos = waitForClick(leftObjDims, rightObjDims)
        return clickPos
        
    def clear(self):
        clearCanvas()
        wait(100)
        
class CueCategorisation:
    '''Build cue categorisation trial'''
    
    def __init__(self, speakerID, label, marker, quantity, category, trialType):
        # create instance of cue categorisation trial stim
        # initialise with speakerItemCueDict for learning trials and speakerItemCueTestDict for testing trials
        self.speakerID = speakerID
        self.label = label
        self.marker = marker
        self.quantity = quantity
        self.category = category
        self.trialType = trialType
        
        if trialType == 'critical':
            self.itemName = meanings[labels.index(self.label)]
            if self.quantity == 2:
                self.itemImg = itemsDict[self.itemName][2]
            elif self.quantity == 3:
                self.itemImg = itemsDict[self.itemName][3]
            elif self.quantity == 4:
                self.itemImg = itemsDict[self.itemName][4]
            self.inputNoun = self.label    # for logging
            self.itemAudio = pygame.mixer.Sound('{}audio_speakers/{}scaled/{}{}_{}.wav'.format(filePath, speakerID, self.marker, self.itemName, speakerID))
        elif trialType == 'filler':
            self.itemName = meanings[labels.index(self.label)]
            self.itemImg = itemsDict[self.itemName][1]
            self.inputNoun = self.label       # for logging
            self.itemAudio = pygame.mixer.Sound('{}audio_speakers/{}scaled/{}_{}.wav'.format(filePath, speakerID, self.itemName, speakerID))
        genders = ['m', 'f']
        self.distCategory = filter(lambda x: x != self.category, genders)[0]
        
        # create target speakers and distractor speakers lists to use when displaying options on categorisation trials
        self.targGender = self.category
        self.distGender = self.distCategory
        if self.targGender == minorityGroup:
            extraSpeaker = random.choice([speaker for speaker in extraSpeakersDict.keys() if self.targGender in speaker])
            self.targSpeakers =  [random.choice([speaker for speaker in speakersDict.keys() if self.targGender in speaker and speaker != speakerID])] + [extraSpeaker]
            self.targGroup = [speakersDict[speakerID][2]] + [extraSpeakersDict[extraSpeaker][0]]
        else:
            self.targSpeakers = random.sample([speaker for speaker in speakersDict.keys() if self.targGender in speaker and speaker != speakerID], 2)
            self.targGroup = [speakersDict[i][2] for i in self.targSpeakers]
        self.distSpeakers = random.sample([speaker for speaker in speakersDict.keys() if self.distGender in speaker], 2)
        self.distGroup = [speakersDict[i][2] for i in self.distSpeakers]
        
        # select distractor speaker to use when displaying options on categorisation test trials
        self.distSpeakerID = random.choice([speaker for speaker in speakersDict.keys() if self.distGender in speaker])

    def returnTrialStim(self, phase):
        # return trial stim to log
        if phase == 'learning':
            return [self.itemName, self.quantity, self.marker, self.inputNoun, self.targSpeakers, self.distSpeakers, self.category, self.distCategory]
        elif phase == 'testing':
            return [self.itemName, self.quantity, self.marker, self.inputNoun, self.distSpeakerID, self.category, self.distCategory]

    def showInstruction(self):
        pygame.display.set_caption('Click on the correct group')
        displayText('Click on the group this speaker belongs to', 20, (xc, 0.2*yc))
        pygame.display.update()
    
    def showNounPhrase(self):
        # display NP on screen
        canvas.blit(self.itemImg, (xc-imgWS/2, 0.7*yc-imgHS/2))
        if self.trialType == 'critical':
            displayText('{} {}'.format(self.marker, self.label), 50, (xc, 0.4*yc))
        elif self.trialType == 'filler':
            displayText(self.label, 50, (xc, 0.4*yc))
        pygame.display.update()
    
    def showOptions(self, targPos):
        # show speaker groups (male and female) for cue categorisation trials
        pygame.mouse.set_pos(mousePos)
        pygame.mouse.set_visible(1)
        displayOptionBoxes('category')
        if targPos == 'L':
            for i in range(2):
                canvas.blit(self.targGroup[i], (0.4*xc-imgWS/2+imgWS/2*i, 1.2*yc-50))
            for i in range(2):
                canvas.blit(self.distGroup[i], (1.6*xc-imgWS/2+imgWS/2*i, 1.2*yc-50))
        elif targPos == 'R':
            for i in range(2):
                canvas.blit(self.targGroup[i], (1.6*xc-imgWS/2+imgWS/2*i, 1.2*yc-50))
            for i in range(2):
                canvas.blit(self.distGroup[i], (0.4*xc-imgWS/2+imgWS/2*i, 1.2*yc-50))
        pygame.display.update()
    
    def showTestOptions(self, targPos):
        # show target and distractor speakers for cue categorisation test trials
        pygame.display.set_caption('Click on the correct speaker')
        pygame.mouse.set_pos(mousePos)
        pygame.mouse.set_visible(1)
        displayOptionBoxes('image')
        targAvatar = speakersDict[self.speakerID][1]
        distAvatar = speakersDict[self.distSpeakerID][1]
        if targPos == 'L':
            canvas.blit(targAvatar, (0.4*xc-75, 1.2*yc-75))
            canvas.blit(distAvatar, (1.6*xc-75, 1.2*yc-75))
        elif targPos == 'R':
            canvas.blit(targAvatar, (1.6*xc-75, 1.2*yc-75))
            canvas.blit(distAvatar, (0.4*xc-75, 1.2*yc-75))
        pygame.display.update()     

    def getClick(self, leftObjDims, rightObjDims):
        # check for click on either object
        clickPos = waitForClick(leftObjDims, rightObjDims)
        return clickPos
    
    def playAudio(self):
        # play sound file for speaker associated with NP
        wait(250)
        pygame.mixer.Sound.play(self.itemAudio)
        while pygame.mixer.get_busy():
            pass

    def feedback(self, targPos, clickPos):
        displayFeedback(targPos, clickPos)
        wait(1000)
    
    def clear(self):
        clearCanvas()
        wait(100)
        
class ProductionTest():
    '''Build production test trial'''
    
    def __init__(self, speakerID, label, quantity, category, trialType):
        # create instance of production test trial stim
        self.speakerID = speakerID
        self.avatarMed = speakersDict[speakerID][1]
        self.label = label
        self.quantity = quantity
        self.category = category
        self.trialType = trialType
        self.itemName = meanings[labels.index(self.label)]
        
        if self.trialType == 'critical':
            if self.quantity == 2:
                self.itemImg = itemsDict[self.itemName][7]
            elif self.quantity == 3:
                self.itemImg = itemsDict[self.itemName][8]
            elif self.quantity == 4:
                self.itemImg = itemsDict[self.itemName][9]
        elif self.trialType == 'filler':
            self.itemImg = itemsDict[self.itemName][6]
            self.itemAudio = pygame.mixer.Sound('{}audio_speakers/{}scaled/{}_{}.wav'.format(filePath, speakerID, self.itemName, speakerID))
        genders = ['m', 'f']
        self.distCategory = filter(lambda x: x != self.category, genders)[0]

    def returnTrialStim(self):
        # return trial stim to log
        return [self.itemName, self.quantity, self.category, self.distCategory]
    
    def showAvatar(self):
        # display speaker avatar on production test trial
        pygame.mouse.set_visible(0)
        canvas.blit(self.avatarMed, (xc-75, 0.4*yc-75))
        displayText('Tell me the name of the image below:', 20, (xc, 0.2*yc))
        pygame.display.update()
    
    def showImage(self):
        # display image to name on screen
        wait(1000)
        canvas.blit(self.itemImg, (xc-imgWL/2, yc-imgHL/2))
        pygame.display.update()

    def showHyphens(self):
        # display string of hyphens corresponding to the number of letters in label
        hyphensToDisplay = '-'* len(self.label)
        if self.trialType == 'critical':
            hyphensToDisplay = ' '.join(['-'*3, hyphensToDisplay])
        displayText(hyphensToDisplay, 50, (xc, 1.5*yc))
        pygame.display.update()

    def startRecording(self, recDirPath, expPhase, globalTrialNo):
        # start recording, stop recording 500ms after space press
        recording = True
        threading.Thread(target = record(recDirPath, expPhase, globalTrialNo))
        while recording:
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        wait(500)
                        recording = False
                        os.system('pkill sox')
                        break
    
    def feedback(self):
        # display label for each item post production (only on filler (bare noun) trials)
        clearCanvas()
        canvas.blit(self.itemImg, (xc-imgWL/2, yc-imgHL/2))
        canvas.blit(self.avatarMed, (xc-75, 0.4*yc-75))
        displayText('Tell me the name of the image below:', 20, (xc, 0.2*yc))
        displayText(self.label, 50, (xc, 1.55*yc))
        pygame.display.update()
        wait(0)
        
    def playAudio(self):
        # play audio associated with item (only on filler (bare noun) trials)
        # wait 500ms before moving on to next trial
        pygame.mixer.Sound.play(self.itemAudio)
        while pygame.mixer.get_busy():
            pass
        wait(500)

    def clear(self):
        clearCanvas()
        wait(500)
        
def begin():
    global canvas, xc, yc, imgWL, imgHL, imgWM, imgHM, imgWS, imgHS, mousePos, exp, withinStudyExp, subjNo, condition, cueDist, varDist, varType, globalTrialNo, meanings, labels, markers, markersToUse, majorityMarker, minorityMarker, majorityGroup, minorityGroup, c1, c2, v1, v2, filePath, recordingsDirPath, dataFile
    
    exp = 'B'   # for logging
    condition = int(sys.argv[1])
    subjNo = exp + str(condition) + sys.argv[2]
    
    conditions = [('skewed', 'skewed', 'unconditioned'), ('skewed', 'skewed', 'conditioned'), ('uniform', 'skewed', 'conditioned'), ('uniform', 'skewed', 'unconditioned'), ('skewed', 'uniform', 'unconditioned'), ('uniform', 'uniform', 'unconditioned')]
    conditionsIdx = condition - 1
    cueDist, varDist, varType = conditions[conditionsIdx][0], conditions[conditionsIdx][1], conditions[conditionsIdx][2]
    meanings = ['bookcase', 'bucket', 'clock', 'drawer', 'fan', 'lamp', 'mirror', 'sofa']
    labels = ['stoa', 'kontena', 'kilok', 'tebol', 'winim', 'golo', 'lukluk', 'sindaun']
    markers = ['nim', 'hap', 'tog']
    markersToUse = random.sample(markers, 2)
    #markersCopy = markers[:]
    groups = ['m', 'f']
    groupsCopy = groups[:]
    
    # adding this because Carmen wants to log it
    # note that because of this 'exp' in script now corresponds to 'study' column in logfile, and 'withinStudyExp' in script corresponds to 'exp' column in logfile
    if condition==5 or condition==6:
        withinStudyExp = 1
    elif condition==1 or condition==4:
        withinStudyExp = 2
    elif condition==2 or condition==3:
        withinStudyExp = 3
    
    # majorityGroup, minorityGroup, majorityMarker, minorityMarker are just for logging purposes
    # c1, c2 (two speaker categories) and v1, v2 (two markers) are for use in generateSpeakerItemDicts()
    if condition == 1 or condition == 2 or condition == 5:
        majorityGroup, minorityGroup = random.sample(groups, 2)
    else:
        majorityGroup, minorityGroup = 'NA', 'NA'
    
    if condition == 1 or condition == 2 or condition == 4:
        majorityMarker, minorityMarker = markersToUse[0], markersToUse[1]
    else:
        majorityMarker, minorityMarker = 'NA', 'NA'
    
    if majorityGroup == 'NA':
        c1, c2 = random.sample(groups, 2)
    else:
        c1, c2 = majorityGroup, minorityGroup
    
    if majorityMarker == 'NA':
        v1, v2 = random.sample(markersToUse, 2)
    else:
        v1, v2 = majorityMarker, minorityMarker
        
    print c1, c2
    print v1, v2
    
    
    filePath = os.path.expanduser("~/Desktop/cuelearning/")
    recordingsDirPath = '{}{}/'.format(filePath, subjNo)
    if not os.path.exists(recordingsDirPath):
        os.makedirs(recordingsDirPath)
    
    dataFile = createDataFile(filePath, subjNo)
    
    globalTrialNo = 0   # for logging across exp phases
    
    imgWL, imgHL = 350, 350
    imgWM, imgHM = 300, 300
    imgWS, imgHS = 200, 200
    
    pygame.init()
    pygame.mixer.init(44100, -16, 2, 2048)
    
    scrRes = pygame.display.Info()
    scrWidth = scrRes.current_w
    scrHeight = scrRes.current_h
    xc = scrWidth/2
    yc = scrHeight/2
    mousePos = [xc, 0.3*yc]
    
    canvas = pygame.display.set_mode((scrWidth, scrHeight), 0, 32)
    canvas.fill((255, 255, 255))
    
def buildNounTrainBlock(itemsDict):
    global globalTrialNo
    if not os.path.exists(recordingsDirPath):
        os.makedirs(recordingsDirPath)
    pygame.display.set_caption('Learn and repeat')
    currPhase = 'NounExposure'
    itemsList = itemsDict.keys()*3
    pygame.mouse.set_visible(0)
    for i in range(len(itemsList)):
        timeStamp = time.asctime()
        globalTrialNo += 1
        trialNo = i+1
        currSpeaker = 'default'
        currItem = random.choice(itemsList)
        itemsList.remove(currItem)
        currTrialStim = NounTrain(currItem)
        currTrialStim.showImage()
        currTrialStim.showLabel()
        currTrialStim.playAudio()
        currTrialStim.startRecording(recordingsDirPath, currPhase, globalTrialNo)
        stimToLog = currTrialStim.returnTrialStim()
        lexItem, inputNoun = stimToLog[0], stimToLog[1]
        lexItemQuantity = 1
        trialType = 'critical'
        selectionTask, inputMarker, targPos, clickPos, distItem, distItemQuantity, answerQuest, category, distCategory, targSpeaker, distSpeaker =  'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA'
        spokenResp = ''
        dataToLog = [subjNo, exp, withinStudyExp, condition, cueDist, varDist, varType, markersToUse, majorityGroup, majorityMarker, currPhase, selectionTask, trialType, globalTrialNo, trialNo, lexItem, lexItemQuantity, inputMarker, inputNoun, targPos, clickPos, distItem,  distItemQuantity, category, distCategory, currSpeaker, targSpeaker, distSpeaker, spokenResp, answerQuest, timeStamp, '\n']
        writeDataToFile(dataToLog)
        currTrialStim.clear()
        wait(100)
        
def buildNounTestBlock(itemsDict):
    global globalTrialNo
    selectionTaskList = ['image']*8 + ['label']*8
    imageItemsList = itemsDict.keys()
    imageTargPosList = ['R']*(len(imageItemsList)/2) + ['L']*(len(imageItemsList)/2)
    labelItemsList = itemsDict.keys()
    labelTargPosList = ['R']*(len(labelItemsList)/2) + ['L']*(len(labelItemsList)/2)
    currPhase = 'NounSelection'
    
    for i in range(len(selectionTaskList)):
        timeStamp = time.asctime()
        globalTrialNo += 1
        trialNo = i+1
        selectionTask = random.choice(selectionTaskList)
        selectionTaskList.remove(selectionTask)
        currSpeaker = 'default'
        
        if selectionTask == 'label':
            # label selection trial
            wait(500)
            currItem = random.choice(imageItemsList)
            targPos = random.choice(imageTargPosList)
            imageItemsList.remove(currItem)
            imageTargPosList.remove(targPos)
            currTrialStim = NounTest(currItem)
            currTrialStim.showImage()
            currTrialStim.showLabelOptions(targPos)
            clickPos = currTrialStim.getClick((xc-400, 1.2*yc, 300, 80), (xc+400, 1.2*yc, 300, 80))
        elif selectionTask == 'image':
            # image selection trial
            wait(500)
            currItem = random.choice(labelItemsList)
            targPos = random.choice(labelTargPosList)
            labelItemsList.remove(currItem)
            labelTargPosList.remove(targPos)
            currTrialStim = NounTest(currItem)
            currTrialStim.showLabel()
            currTrialStim.showImageOptions(targPos)
            clickPos = currTrialStim.getClick((0.4*xc, 1.2*yc, imgWM, imgHM), (1.6*xc, 1.2*yc, imgWM, imgHM))
        
        currTrialStim.feedback(targPos, clickPos)
        currTrialStim.playAudio()
        stimToLog = currTrialStim.returnTrialStim()
        lexItem = stimToLog[0]
        if selectionTask == 'label':
            inputNoun = stimToLog[1]
            distItem = stimToLog[3]
        elif selectionTask == 'image':
            inputNoun = 'NA'
            distItem = stimToLog[2]
        trialType = 'critical'
        spokenResp = ''
        lexItemQuantity, distItemQuantity = 1, 1
        inputMarker, targPos, clickPos, targSpeaker, distSpeaker, answerQuest, category, distCategory = 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA'
        dataToLog = [subjNo, exp, withinStudyExp, condition, cueDist, varDist, varType, markersToUse, majorityGroup, majorityMarker, currPhase, selectionTask, trialType, globalTrialNo, trialNo, lexItem, lexItemQuantity, inputMarker, inputNoun, targPos, clickPos, distItem, distItemQuantity, category, distCategory, currSpeaker, targSpeaker, distSpeaker, spokenResp, answerQuest, timeStamp, '\n']
        writeDataToFile(dataToLog)
        currTrialStim.clear()

def buildNounProductionTestBlock(itemsDict):
    global globalTrialNo
    if not os.path.exists(recordingsDirPath):
        os.makedirs(recordingsDirPath)
    pygame.display.set_caption('Say the name of this object')
    itemsList = itemsDict.keys()*2
    pygame.mouse.set_visible(0)
    currPhase = 'NounProduction'
    
    for i in range(len(itemsList)):
        timeStamp = time.asctime()
        globalTrialNo += 1
        trialNo = i+1
        currItem = random.choice(itemsList)
        itemsList.remove(currItem)
        currTrialStim = NounProductionTest(currItem)
        currTrialStim.showImage()
        currTrialStim.showHyphens()
        currTrialStim.startRecording(recordingsDirPath, currPhase, globalTrialNo)
        currTrialStim.feedback()
        currTrialStim.playAudio()
        stimToLog = currTrialStim.returnTrialStim()
        lexItem = stimToLog[0]
        lexItemQuantity = 1
        trialType = 'critical'
        spokenResp = ''
        selectionTask, inputMarker, inputNoun, targPos, clickPos, distItem, distItemQuantity, answerQuest, category, distCategory, currSpeaker, targSpeaker, distSpeaker = 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA'
        dataToLog = [subjNo, exp, withinStudyExp, condition, cueDist, varDist, varType, markersToUse, majorityGroup, majorityMarker, currPhase, selectionTask, trialType, globalTrialNo, trialNo, lexItem, lexItemQuantity, inputMarker, inputNoun, targPos, clickPos, distItem, distItemQuantity, category, distCategory, currSpeaker, targSpeaker, distSpeaker, spokenResp, answerQuest, timeStamp, '\n']
        writeDataToFile(dataToLog)
        currTrialStim.clear()
    
def buildSpeakerFamiliarisationBlock():
    global globalTrialNo
    speakersList = genderDict['female'] + genderDict['male']
    random.shuffle(speakersList)
    speakerTargPosList = ['R']*(len(speakersList)/2) + ['L']*(len(speakersList)/2)
    currPhase = 'SpeakerFam'
    
    for i in range(len(speakersList)):
        timeStamp = time.asctime()
        globalTrialNo += 1
        trialNo = i+1
        currSpeaker = speakersList.pop(random.randrange(len(speakersList)))
        targPos = speakerTargPosList.pop(random.randrange(len(speakerTargPosList)))
        currTrialStim = SpeakerFamiliarisation(currSpeaker)
        currTrialStim.showAvatar()
        currTrialStim.showGloss()
        currTrialStim.playIntro()
        currTrialStim.showOptions(targPos)
        clickPos = currTrialStim.getClick((0.4*xc, 1.2*yc, imgWM, imgHM), (1.6*xc, 1.2*yc, imgWM, imgHM))
        currTrialStim.feedback(targPos, clickPos)
        stimToLog = currTrialStim.returnTrialStim()
        targSpeaker, distSpeaker = stimToLog[0], stimToLog[1]
        trialType = 'critical'
        spokenResp = ''
        selectionTask, lexItem, lexItemQuantity, inputMarker, inputNoun, distItem, distItemQuantity, answerQuest, category, distCategory = 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA'
        dataToLog = [subjNo, exp, withinStudyExp, condition, cueDist, varDist, varType, markersToUse, majorityGroup, majorityMarker, currPhase, selectionTask, trialType, globalTrialNo, trialNo, lexItem, lexItemQuantity, inputMarker, inputNoun, targPos, clickPos, distItem, distItemQuantity, category, distCategory, currSpeaker, targSpeaker, distSpeaker, spokenResp, answerQuest, timeStamp, '\n']
        writeDataToFile(dataToLog)
        currTrialStim.clear()

def buildGroupCategorisationBlock():
    global globalTrialNo
    speakersList = genderDict['female'] + genderDict['male']
    random.shuffle(speakersList)
    speakerGroupTargPosList = ['R']*(len(speakersList)/2) + ['L']*(len(speakersList)/2)
    currPhase = 'GroupCategorisation'
    
    for i in range(len(speakersList)):
        timeStamp = time.asctime()
        globalTrialNo += 1
        trialNo = i+1
        currSpeaker = speakersList.pop(random.randrange(len(speakersList)))
        targPos = speakerGroupTargPosList.pop(random.randrange(len(speakerGroupTargPosList)))
        currTrialStim = GroupCategorisation(currSpeaker)
        currTrialStim.showGloss()
        currTrialStim.playIntro()
        currTrialStim.showOptions(targPos)
        clickPos = currTrialStim.getClick((0.4*xc, 1.2*yc, imgWM, imgHM), (1.6*xc, 1.2*yc, imgWM, imgHM))
        currTrialStim.feedback(targPos, clickPos)
        stimToLog = currTrialStim.returnTrialStim()
        targSpeaker, distSpeaker, category, distCategory = (stimToLog[1][0], stimToLog[1][1]), (stimToLog[2][0], stimToLog[2][1]), stimToLog[3], stimToLog[4]
        trialType = 'critical'
        spokenResp = ''
        selectionTask, lexItem, lexItemQuantity, inputMarker, inputNoun, distItem, distItemQuantity, answerQuest = 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA'
        dataToLog = [subjNo, exp, withinStudyExp, condition, cueDist, varDist, varType, markersToUse, majorityGroup, majorityMarker, currPhase, selectionTask, trialType, globalTrialNo, trialNo, lexItem, lexItemQuantity, inputMarker, inputNoun, targPos, clickPos, distItem, distItemQuantity, category, distCategory, currSpeaker, targSpeaker, distSpeaker, spokenResp, answerQuest, timeStamp, '\n']
        writeDataToFile(dataToLog)
        currTrialStim.clear()
    
def buildLearningBlock():
    global globalTrialNo
    blockList = range(1,5)      # [2,1,4,3] -> for debugging cue cat block
    numTrialsPerBlock = 40      # 32 x critical + 8 x filler trials
    currPhase = 'PhraseLearning'
    
    for block in blockList:
        currBlock = block
        targPosList = ['R']*20 + ['L']*20
        for i in range(numTrialsPerBlock):
            timeStamp = time.asctime()
            globalTrialNo += 1
            trialNo = i + 1 + ((currBlock-1) * numTrialsPerBlock)
            targPos = targPosList.pop(random.randrange(len(targPosList)))
            selectionTask = 'image'
            if currBlock == 1:
                currTrial = varLearningTrials1.pop(random.randrange(len(varLearningTrials1)))
                currSpeaker, label, marker, quantity, category, trialType = currTrial['speaker'], currTrial['label'], currTrial['marker'], currTrial['number'], currTrial['gender'], currTrial['trialType']
                currTrialStim = VariantLearning(currSpeaker, label, marker, quantity, category, trialType)
            elif currBlock == 3:
                currTrial = varLearningTrials2.pop(random.randrange(len(varLearningTrials2)))
                currSpeaker, label, marker, quantity, category, trialType = currTrial['speaker'], currTrial['label'], currTrial['marker'], currTrial['number'], currTrial['gender'], currTrial['trialType']
                currTrialStim = VariantLearning(currSpeaker, label, marker, quantity, category, trialType)
            elif currBlock == 2:
                currTrial = cueCatTrials1.pop(random.randrange(len(cueCatTrials1)))
                currSpeaker, label, marker, quantity, category, trialType = currTrial['speaker'], currTrial['label'], currTrial['marker'], currTrial['number'], currTrial['gender'], currTrial['trialType']
                currTrialStim = VariantLearning(currSpeaker, label, marker, quantity, category, trialType)
            elif currBlock == 4:
                currTrial = cueCatTrials2.pop(random.randrange(len(cueCatTrials2)))
                currSpeaker, label, marker, quantity, category, trialType = currTrial['speaker'], currTrial['label'], currTrial['marker'], currTrial['number'], currTrial['gender'], currTrial['trialType']            
            currTrialStim = VariantLearning(currSpeaker, label, marker, quantity, category, trialType)
            currTrialStim.showAvatar()
            currTrialStim.showNounPhrase()
            currTrialStim.playAudio()
            currTrialStim.showInstruction()
            currTrialStim.showOptions(targPos)
            clickPos = currTrialStim.getClick((0.4*xc, 1.2*yc, imgWM, imgHM), (1.6*xc, 1.2*yc, imgWM, imgHM))
            currTrialStim.feedback(targPos, clickPos)
            stimToLog = currTrialStim.returnTrialStim()
            lexItem, lexItemQuantity, inputMarker, inputNoun, distItem, distItemQuantity, category, distCategory = stimToLog[0], stimToLog[1], stimToLog[2], stimToLog[3], stimToLog[4], stimToLog[5], stimToLog[6], stimToLog[7]
            answerQuest, targSpeaker, distSpeaker = 'NA', 'NA', 'NA'
                        
            spokenResp = ''
            
            dataToLog = [subjNo, exp, withinStudyExp, condition, cueDist, varDist, varType, markersToUse, majorityGroup, majorityMarker, currPhase, selectionTask, trialType, globalTrialNo, trialNo, lexItem, lexItemQuantity, inputMarker, inputNoun, targPos, clickPos, distItem, distItemQuantity, category, distCategory, currSpeaker, targSpeaker, distSpeaker, spokenResp, answerQuest, timeStamp, '\n']
            writeDataToFile(dataToLog)
            currTrialStim.clear()

def buildCueCategorisationTestBlock():
    global globalTrialNo
    targPosList = ['R']*16 + ['L']*16
    currPhase = 'PhraseCategorsation'
    trialType = 'critical'
    numTrials = len(cueTestTrials)
    
    for i in range(numTrials):
        timeStamp = time.asctime()
        globalTrialNo += 1
        trialNo = i+1
        targPos = targPosList.pop(random.randrange(len(targPosList)))
        currTrial = cueTestTrials.pop(random.randrange(len(cueTestTrials)))
        currSpeaker, label, marker, quantity, category = currTrial['speaker'], currTrial['label'], currTrial['marker'], currTrial['number'], currTrial['gender']
        currTrialStim = CueCategorisation(currSpeaker, label, marker, quantity, category, trialType)
        currTrialStim.showNounPhrase()
        currTrialStim.showTestOptions(targPos)
        clickPos = currTrialStim.getClick((0.4*xc, 1.2*yc, imgWM, imgHM), (1.6*xc, 1.2*yc, imgWM, imgHM))
        stimToLog = currTrialStim.returnTrialStim('testing')
        lexItem, lexItemQuantity, inputMarker, inputNoun, distSpeaker, category, distCategory = stimToLog[0], stimToLog[1], stimToLog[2], stimToLog[3], stimToLog[4], stimToLog[5], stimToLog[6]
        targSpeaker = currSpeaker
        distItem, distItemQuantity, answerQuest = 'NA', 'NA', 'NA'
        spokenResp = ''
        selectionTask = 'prediction'
        dataToLog = [subjNo, exp, withinStudyExp, condition, cueDist, varDist, varType, markersToUse, majorityGroup, majorityMarker, currPhase, selectionTask, trialType, globalTrialNo, trialNo, lexItem, lexItemQuantity, inputMarker, inputNoun, targPos, clickPos, distItem, distItemQuantity, category, distCategory, currSpeaker, targSpeaker, distSpeaker, spokenResp, answerQuest, timeStamp, '\n']
        writeDataToFile(dataToLog)
        currTrialStim.clear()

def buildProductionTestBlock():
    global globalTrialNo
    if not os.path.exists(recordingsDirPath):
        os.makedirs(recordingsDirPath)
    pygame.display.set_caption('Name the image for the addressee')
    currPhase = 'PhraseProduction'
    numTrials = len(productionTestTrials)
    
    for i in range(numTrials):
        timeStamp = time.asctime()
        globalTrialNo += 1
        trialNo = i+1
        currTrial = productionTestTrials.pop(random.randrange(len(productionTestTrials)))
        currSpeaker, label, quantity, category, trialType = currTrial['speaker'], currTrial['label'], currTrial['number'], currTrial['gender'], currTrial['trialType']
        currTrialStim = ProductionTest(currSpeaker, label, quantity, category, trialType)
        currTrialStim.showAvatar()
        currTrialStim.showImage()
        currTrialStim.showHyphens()
        currTrialStim.startRecording(recordingsDirPath, currPhase, globalTrialNo)
        if trialType == 'filler':
            currTrialStim.feedback()
            currTrialStim.playAudio()
        stimToLog = currTrialStim.returnTrialStim()
        lexItem, lexItemQuantity, category, distCategory = stimToLog[0], stimToLog[1], stimToLog[2], stimToLog[3]
        selectionTask, inputMarker, inputNoun, targPos, clickPos, distItem, distItemLabel, distItemQuantity, targSpeaker, distSpeaker, answerQuest = 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA'
        spokenResp = ''
        dataToLog = [subjNo, exp, withinStudyExp, condition, cueDist, varDist, varType, markersToUse, majorityGroup, majorityMarker, currPhase, selectionTask, trialType, globalTrialNo, trialNo, lexItem, lexItemQuantity, inputMarker, inputNoun, targPos, clickPos, distItem, distItemQuantity, category, distCategory, currSpeaker, targSpeaker, distSpeaker, spokenResp, answerQuest, timeStamp, '\n']
        writeDataToFile(dataToLog)
        currTrialStim.clear()
        
def buildQuestionnaire():
    pygame.mouse.set_visible(1)
    linkRect = displayText('Questionnaire will open in browser. Please wait.', 30, (xc, yc))
    linkRect[0], linkRect[1] = xc, yc
    pygame.display.update()
    wait(2000)
    import webbrowser
    webbrowser.open_new_tab("https://blake4.ppls.ed.ac.uk/jloy/cuelearning/postquest.html?id={}&cond={}&cd={}&vd={}&vt={}&mg={}&mj={}&mn={}".format(subjNo, condition, cueDist, varDist, varType, majorityGroup, v1, v2))
    

    

if __name__ == "__main__":
    
    begin()
    
    loadMiscObjects()
    
    itemsDict = loadItems()
    
    genderDict = selectSpeakers(condition)
    speakersDict = loadSpeakers(genderDict)[0]
    extraSpeakersDict = loadSpeakers(genderDict)[1]
    
    trialDicts = generateSpeakerItemDicts(condition, speakersDict.keys())

    varLearningTrials1, cueCatTrials1, varLearningTrials2, cueCatTrials2, cueTestTrials, productionTestTrials = trialDicts[0], trialDicts[1], trialDicts[2], trialDicts[3], trialDicts[4], trialDicts[5]
    
    print '############################'
    print varLearningTrials1, '\n'
    print cueCatTrials1, '\n'
    print varLearningTrials2, '\n'
    print cueCatTrials2, '\n'
    print cueTestTrials, '\n'
    print productionTestTrials
    
    preExperimentScreen()
    
    instructions('NounTrain1')
    instructions('NounTrain2')
    buildNounTrainBlock(itemsDict)
    
    instructions('NounTest')
    buildNounTestBlock(itemsDict)
    
    instructions('NounProductionTest')
    buildNounProductionTestBlock(itemsDict)
    
    instructions('SpeakerFamiliarisation')
    buildSpeakerFamiliarisationBlock()
    
    instructions('Learning')
    buildLearningBlock()
    
    instructions('CueTesting')
    buildCueCategorisationTestBlock()
    
    instructions('ProductionTest')
    buildProductionTestBlock()
    
    instructions('Questionnaire')
    buildQuestionnaire()
