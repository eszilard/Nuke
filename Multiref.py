############MULTIREF################


#Create matchmove or stabilize from tacker

def trackmatch():
    tracker = nuke.selectedNode()
    tracker = nuke.selectedNode()
    tracker.knob("cornerPinOptions").setValue("Transform (match-move)")
    button = tracker.knob("createCornerPin").execute()

def trackstab():
    tracker = nuke.selectedNode()
    tracker = nuke.selectedNode()
    tracker.knob("cornerPinOptions").setValue("Transform (stabilize)")
    button = tracker.knob("createCornerPin").execute()



#Turn a node multi-ref compatible

def makeMultiRef():

    tracker = nuke.selectedNode()
    
    X = createExpressionX(tracker)
    Y = createExpressionY(tracker)
    
    
    tracker.addKnob(nuke.XY_Knob("centerCurve", "Center Curve"))
    tracker["centerCurve"].setExpression(X, 0)
    tracker["centerCurve"].setExpression(Y, 1)



#Update when number of active translates change



def updateMultiRef():

    tracker = nuke.selectedNode()

    X = createExpressionX(tracker)
    Y = createExpressionY(tracker)
    
    tracker["centerCurve"].setExpression(X, 0)
    tracker["centerCurve"].setExpression(Y, 1)







#Create expressions



def createExpressionX(tracker):
    expX = ""
    activeNum = getActiveTranslate(tracker)
    activeNumCounter = getActiveTranslate(tracker)
    tracklist = getActiveTrackers(tracker)
    trackername = tracker.fullName()
    
    
    while activeNumCounter > 1:
        expX += trackername + "." + tracklist[activeNumCounter-1] + ".track_x +\n"
        activeNumCounter -= 1
    expX += trackername + "." + tracklist[activeNumCounter-1] + ".track_x\n"
    
    activenum = getActiveTranslate(tracker)
    
    
    expX = "(" + expX + ")/" + str(activeNum)
    return expX


def createExpressionY(tracker):
    expY = ""
    activeNum = getActiveTranslate(tracker)
    activeNumCounter = getActiveTranslate(tracker)
    tracklist = getActiveTrackers(tracker)
    trackername = tracker.fullName()
    
    
    while activeNumCounter > 1:
        expY += trackername + "." + tracklist[activeNumCounter-1] + ".track_y +\n"
        activeNumCounter -= 1
    expY += trackername + "." + tracklist[activeNumCounter-1] + ".track_y\n"
    
    activenum = getActiveTranslate(tracker)
    
    
    expY = "(" + expY + ")/" + str(activeNum)
    return expY





#Get Active Translate Knobs

def getActiveTranslate(tracker):
    trackers = []
    script = tracker["tracks"].toScript()
    
    count = 0
    active_transforms = 0
    
    trackers.append(script)
    
    for item in trackers:
        total_tracks = item.count('\"track ')
    
    while count <= int(total_tracks)-1:
        if tracker["tracks"].getValue(31 * count + 6) == 1:
            active_transforms += 1
        else:
            pass
        count +=1
    return active_transforms




#get active tracker names as tracks.x in a list


def getActiveTrackers(tracker):
    trackers = []
    script = tracker["tracks"].toScript()
    
    count = 0
    active_transforms = 0
    
    trackers.append(script)
    
    
    for item in trackers:
        total_tracks = item.count('\"track ')
    
    track_number = 0
    active_tracker_list = []
    
    while count <= int(total_tracks)-1:
        if tracker["tracks"].getValue(31 * count + 6) == 1:
            track_number += 1
            active_tracker_list.append("tracks."+str(track_number))
        elif tracker["tracks"].getValue(31 * count + 6) == 0:
            track_number += 1
        else:
            pass
        count +=1
    return active_tracker_list









#Create multiref matchmove

def createMultiMatchmove():
    #Create multiref matchmove
    
    
    
    
    refframe = int(nuke.frame())
    tracker = nuke.selectedNode()
    
    #Create transform node
    
    if tracker.knob('centerCurve') !=None:    
        
        #Define Tracker
        
        
        #Create Transform, set Pos
        transform = nuke.createNode("Transform")
        transform.setInput(0, None)
        transform.setXYpos(tracker.xpos(), tracker.ypos()+50)
        transform["label"].setValue("Matchmove \n Ref " + str(nuke.frame()))
        
        #Set X Translate
        transform.knob('translate').setExpression(
        tracker.fullName()
        + ".translate.x - " 
        + tracker.fullName() 
        + ".translate.x(" 
        + str(refframe) + ")" , 0
        )
        
        #Set Y Translate
        
        transform.knob('translate').setExpression(
        tracker.fullName()
        + ".translate.y - " 
        + tracker.fullName() 
        + ".translate.y(" 
        + str(refframe) + ")" , 1
        )
        
        #Set Rotate
        
        transform.knob('rotate').setExpression(
        tracker.fullName() 
        + ".rotate - " 
        + tracker.fullName()
        + ".rotate("
        + str(refframe) + ")"
        )
        
        #Set Scale
        transform.knob('scale').setExpression(
        tracker.fullName() 
        + ".scale / "
        + tracker.fullName()
        + ".scale("
        + str(refframe) + ")"
        )
        
        #Set Center
        transform.knob('center').setExpression(tracker.fullName() + ".centerCurve.x(" + str(refframe) + ")", 0)
        transform.knob('center').setExpression(tracker.fullName() + ".centerCurve.y(" + str(refframe) + ")", 1)
    else:
        trackmatch()






#Create multiref matchmove

def createMultiStabilize():
    #Create multiref matchmove
    
    
    
    
    refframe = int(nuke.frame())
    tracker = nuke.selectedNode()
    
    #Create transform node
    
    
    if tracker.knob('centerCurve') !=None:
        #Define Tracker
        
        
        #Create Transform, set Pos
        transform = nuke.createNode("Transform")
        transform.setInput(0, None)
        transform.setXYpos(tracker.xpos(), tracker.ypos()+50)
        transform["label"].setValue("Stabilize \n Ref " + str(nuke.frame()))
        
        #Set X Translate
        transform.knob('translate').setExpression("-("
        +tracker.fullName()
        + ".translate.x - " 
        + tracker.fullName() 
        + ".translate.x(" 
        + str(refframe) + "))" , 0
        )
        
        #Set Y Translate
        
        transform.knob('translate').setExpression("-("
        +tracker.fullName()
        + ".translate.y - " 
        + tracker.fullName() 
        + ".translate.y(" 
        + str(refframe) + "))" , 1
        )
        
        #Set Rotate
        
        transform.knob('rotate').setExpression("-("
        +tracker.fullName() 
        + ".rotate - " 
        + tracker.fullName()
        + ".rotate("
        + str(refframe) + "))"
        )
        
        #Set Scale
        transform.knob('scale').setExpression("1/("
        +tracker.fullName() 
        + ".scale / "
        + tracker.fullName()
        + ".scale("
        + str(refframe) + "))"
        )
        
        #Set Center
        transform.knob('center').setExpression(tracker.fullName() + ".centerCurve.x", 0)
        transform.knob('center').setExpression(tracker.fullName() + ".centerCurve.y", 1)
    else:
        trackstab()



nuke.menu("Nuke").addCommand("MultiTracker/Make node MultiTrack", "makeMultiRef()","Meta+G")
nuke.menu("Nuke").addCommand("MultiTracker/Update MultiTracker", "updateMultiRef()","Meta+F")
nuke.menu("Nuke").addCommand("MultiTracker/Create MultiMatchmove", "createMultiMatchmove()","Meta+A")
nuke.menu("Nuke").addCommand("MultiTracker/Create MultiStabilize", "createMultiStabilize()","Meta+S")


