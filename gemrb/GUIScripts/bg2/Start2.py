#this is essentially Start.py from the SoA game, except for a very small change
import GemRB
from GUICommon import GameIsTOB

StartWindow = 0
TutorialWindow = 0
QuitWindow = 0
ExitButton = 0
SinglePlayerButton = 0
OptionsButton = 0
MultiPlayerButton = 0
MoviesButton = 0

def OnLoad():
	global StartWindow, TutorialWindow, QuitWindow
	global ExitButton, OptionsButton, MultiPlayerButton, MoviesButton, SinglePlayerButton
	global SinglePlayerButton

	skip_videos = GemRB.GetVar ("SkipIntroVideos")

	GemRB.LoadWindowPack("START", 640, 480)
#tutorial subwindow
	TutorialWindow = GemRB.LoadWindowObject (5)
	TextAreaControl = TutorialWindow.GetControl (1)
	CancelButton = TutorialWindow.GetControl (11)
	PlayButton = TutorialWindow.GetControl (10)
	TextAreaControl.SetText (44200)
	CancelButton.SetText (13727)
	PlayButton.SetText (33093)
	PlayButton.SetEvent (IE_GUI_BUTTON_ON_PRESS, "PlayPress")
	CancelButton.SetEvent (IE_GUI_BUTTON_ON_PRESS, "CancelTut")
	PlayButton.SetFlags (IE_GUI_BUTTON_DEFAULT, OP_OR)
	CancelButton.SetFlags (IE_GUI_BUTTON_CANCEL, OP_OR)
#quit subwindow
	QuitWindow = GemRB.LoadWindowObject (3)
	QuitTextArea = QuitWindow.GetControl (0)
	CancelButton = QuitWindow.GetControl (2)
	ConfirmButton = QuitWindow.GetControl (1)
	QuitTextArea.SetText (19532)
	CancelButton.SetText (13727)
	ConfirmButton.SetText (15417)
	ConfirmButton.SetEvent (0, "ExitConfirmed")
	CancelButton.SetEvent (0, "ExitCancelled")
	ConfirmButton.SetFlags (IE_GUI_BUTTON_DEFAULT, OP_OR)
	CancelButton.SetFlags (IE_GUI_BUTTON_CANCEL, OP_OR)
#main window
	StartWindow = GemRB.LoadWindowObject (0)
	StartWindow.SetFrame ()
	#this is the ToB specific part of Start.py
	if GemRB.GetVar("oldgame")==1:
		if GameIsTOB():
			StartWindow.SetPicture("STARTOLD")
		if not skip_videos:
			GemRB.PlayMovie ("INTRO15F", 1)
	else:
		if not skip_videos:
			GemRB.PlayMovie ("INTRO", 1)

	#end ToB specific part
	SinglePlayerButton = StartWindow.GetControl (0)
	ExitButton = StartWindow.GetControl (3)
	OptionsButton = StartWindow.GetControl (4)
	MultiPlayerButton = StartWindow.GetControl (1)
	MoviesButton = StartWindow.GetControl (2)
	BackButton = StartWindow.GetControl (5)
	StartWindow.CreateLabel(0x0fff0000, 0,450,640,30, "REALMS", "", 1)
	Label=StartWindow.GetControl (0x0fff0000)
	Label.SetText (GEMRB_VERSION)
	if not GameIsTOB():
		BackButton.SetState (IE_GUI_BUTTON_DISABLED)
		BackButton.SetText ("")
	else:
		BackButton.SetState (IE_GUI_BUTTON_ENABLED)
		BackButton.SetText (15416)
	SinglePlayerButton.SetState (IE_GUI_BUTTON_ENABLED)
	ExitButton.SetState (IE_GUI_BUTTON_ENABLED)
	OptionsButton.SetState (IE_GUI_BUTTON_ENABLED)
	MultiPlayerButton.SetState (IE_GUI_BUTTON_ENABLED)
	MoviesButton.SetState (IE_GUI_BUTTON_ENABLED)
	SinglePlayerButton.SetText (15413)
	ExitButton.SetText (15417)
	OptionsButton.SetText (13905)
	MultiPlayerButton.SetText (15414)
	MoviesButton.SetText (15415)
	SinglePlayerButton.SetEvent (IE_GUI_BUTTON_ON_PRESS, "SinglePlayerPress")
	ExitButton.SetEvent (IE_GUI_BUTTON_ON_PRESS, "ExitPress")
	OptionsButton.SetEvent (IE_GUI_BUTTON_ON_PRESS, "OptionsPress")
	MultiPlayerButton.SetEvent (IE_GUI_BUTTON_ON_PRESS, "MultiPlayerPress")
	MoviesButton.SetEvent (IE_GUI_BUTTON_ON_PRESS, "MoviesPress")
	BackButton.SetEvent (IE_GUI_BUTTON_ON_PRESS, "Restart")
	ExitButton.SetFlags (IE_GUI_BUTTON_CANCEL, OP_OR)
	QuitWindow.SetVisible (0)
	TutorialWindow.SetVisible (0)
	StartWindow.SetVisible (1)
	GemRB.LoadMusicPL("Theme.mus",1)
	return

def SinglePlayerPress():

	OptionsButton.SetText ("")
	SinglePlayerButton.SetText (13728)
	ExitButton.SetText (15416)
	MultiPlayerButton.SetText (13729)
	MoviesButton.SetText (33093)
	MultiPlayerButton.SetEvent (0, "LoadSingle")
	SinglePlayerButton.SetEvent (0, "NewSingle")
	MoviesButton.SetEvent (0, "Tutorial")
	ExitButton.SetEvent (0, "BackToMain")
	OptionsButton.SetState (IE_GUI_BUTTON_DISABLED)
	return

def MultiPlayerPress():

	OptionsButton.SetText ("")
	SinglePlayerButton.SetText (20642)
	ExitButton.SetText (15416)
	MultiPlayerButton.SetText ("")
	MoviesButton.SetText (11825)
	MultiPlayerButton.SetEvent (0, "")
	SinglePlayerButton.SetEvent (0, "ConnectPress")
	MoviesButton.SetEvent (0, "PregenPress")
	ExitButton.SetEvent (0, "BackToMain")
	MultiPlayerButton.SetState (IE_GUI_BUTTON_DISABLED)
	OptionsButton.SetState (IE_GUI_BUTTON_DISABLED)
	return

def ConnectPress():
#well...
	#GemRB.SetVar("PlayMode",2)
	return

def PregenPress():
	if StartWindow:
		StartWindow.Unload()
	if QuitWindow:
		QuitWindow.Unload()
	if TutorialWindow:
		TutorialWindow.Unload()
	#do not start game after chargen
	GemRB.SetVar("PlayMode",-1) #will allow export
	GemRB.SetVar("Slot",0)
	GemRB.LoadGame(-1)
	GemRB.SetNextScript ("CharGen")
	return

def LoadSingle():
	if StartWindow:
		StartWindow.Unload()
	if QuitWindow:
		QuitWindow.Unload()
	if TutorialWindow:
		TutorialWindow.Unload()
	GemRB.SetVar("PlayMode",0)
	GemRB.SetNextScript ("GUILOAD")
	return

def NewSingle():
	if StartWindow:
		StartWindow.Unload()
	if QuitWindow:
		QuitWindow.Unload()
	if TutorialWindow:
		TutorialWindow.Unload()
	GemRB.SetVar("PlayMode",0)
	GemRB.SetVar("Slot",1)
	GemRB.LoadGame(-1)
	GemRB.SetNextScript ("CharGen")
	return

def Tutorial():
	StartWindow.SetVisible (0)
	TutorialWindow.SetVisible (1)
	return

def PlayPress():
	if StartWindow:
		StartWindow.Unload()
	if QuitWindow:
		QuitWindow.Unload()
	if TutorialWindow:
		TutorialWindow.Unload()
	GemRB.SetVar("PlayMode",1) #tutorial
	GemRB.SetVar("Slot",1)
	GemRB.LoadGame(-1)
	GemRB.SetNextScript ("CharGen")
	return

def CancelTut():
	TutorialWindow.SetVisible (0)
	StartWindow.SetVisible (1)
	return

def ExitPress():
	StartWindow.SetVisible (0)
	QuitWindow.SetVisible (1)
	return

def ExitConfirmed():
	GemRB.Quit()
	return

def OptionsPress():
#apparently the order is important
	if StartWindow:
		StartWindow.Unload()
	if QuitWindow:
		QuitWindow.Unload()
	if TutorialWindow:
		TutorialWindow.Unload()
	GemRB.SetNextScript ("StartOpt")
	return

def MoviesPress():
#apparently the order is important
	if StartWindow:
		StartWindow.Unload()
	if QuitWindow:
		QuitWindow.Unload()
	if TutorialWindow:
		TutorialWindow.Unload()
	GemRB.SetNextScript ("GUIMOVIE")
	return

def ExitCancelled():
	QuitWindow.SetVisible (0)
	StartWindow.SetVisible (1)
	return

def BackToMain():
	SinglePlayerButton.SetState (IE_GUI_BUTTON_ENABLED)
	OptionsButton.SetState (IE_GUI_BUTTON_ENABLED)
	MultiPlayerButton.SetState (IE_GUI_BUTTON_ENABLED)
	SinglePlayerButton.SetText (15413)
	ExitButton.SetText (15417)
	OptionsButton.SetText (13905)
	MultiPlayerButton.SetText (15414)
	MoviesButton.SetText (15415)
	SinglePlayerButton.SetEvent (IE_GUI_BUTTON_ON_PRESS, "SinglePlayerPress")
	ExitButton.SetEvent (IE_GUI_BUTTON_ON_PRESS, "ExitPress")
	OptionsButton.SetEvent (IE_GUI_BUTTON_ON_PRESS, "OptionsPress")
	MultiPlayerButton.SetEvent (IE_GUI_BUTTON_ON_PRESS, "MultiPlayerPress")
	MoviesButton.SetEvent (IE_GUI_BUTTON_ON_PRESS, "MoviesPress")
	QuitWindow.SetVisible (0)
	StartWindow.SetVisible (1)
	return

def Restart():
	StartWindow.Unload()
	QuitWindow.Unload()
	GemRB.SetNextScript ("Start")
	return

