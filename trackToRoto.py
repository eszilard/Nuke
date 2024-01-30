def trackToRoto():
    
    
    tracks = nuke.selectedNodes()
    
    for tracker in tracks:
        if tracker.Class() == "Tracker4":

            roto = nuke.createNode("Roto")

            roto.setInput(0, None)
            roto.setXYpos(tracker.xpos(), tracker.ypos()+50)

            roto.knob('scale').setExpression(tracker.fullName() + ".scale")
            roto.knob('rotate').setExpression(tracker.fullName() + ".rotate")
            roto.knob('translate').setExpression(tracker.fullName() + ".translate")
    
    
        else:
            pass

nuke.menu("Nuke").addCommand("Tools/Create Linked Tracker", "trackToRoto()","Alt+R")
