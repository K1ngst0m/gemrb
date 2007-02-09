# -*-python-*-
# GemRB - Infinity Engine Emulator
# Copyright (C) 2003 The GemRB Project
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
# $Header: /data/gemrb/cvs2svn/gemrb/gemrb/gemrb/GUIScripts/iwd/GUIREC.py,v 1.11 2007/02/09 17:23:48 avenger_teambg Exp $


# GUIREC.py - scripts to control stats/records windows from GUIREC winpack
###################################################
import string
import GemRB
import GUICommonWindows
from GUIDefines import *
from ie_stats import *
from GUICommon import CloseOtherWindow
from GUICommonWindows import *
from GUIWORLD import OpenReformPartyWindow

###################################################
RecordsWindow = None
InformationWindow = None
BiographyWindow = None
PortraitWindow = None
OptionsWindow = None
OldPortraitWindow = None
OldOptionsWindow = None

###################################################
def OpenRecordsWindow ():
	global RecordsWindow, PortraitWindow, OptionsWindow
	global OldPortraitWindow, OldOptionsWindow

	if CloseOtherWindow (OpenRecordsWindow):
		if InformationWindow: OpenInformationWindow ()
	
		GemRB.UnloadWindow (RecordsWindow)
		GemRB.UnloadWindow (OptionsWindow)
		GemRB.UnloadWindow (PortraitWindow)
		RecordsWindow = None
		GemRB.SetVar ("OtherWindow", -1)
		GemRB.SetVisible (0,1)
		GemRB.UnhideGUI ()
		GUICommonWindows.PortraitWindow = OldPortraitWindow
		OldPortraitWindow = None
		GUICommonWindows.OptionsWindow = OldOptionsWindow
		OldOptionsWindow = None
		SetSelectionChangeHandler (None)
		return

	GemRB.HideGUI ()
	GemRB.SetVisible (0,0)

	GemRB.LoadWindowPack ("GUIREC", 640, 480)
	RecordsWindow = Window = GemRB.LoadWindow (2)
	GemRB.SetVar ("OtherWindow", RecordsWindow)
	#saving the original portrait window
	OldOptionsWindow = GUICommonWindows.OptionsWindow
	OptionsWindow = GemRB.LoadWindow (0)
	SetupMenuWindowControls (OptionsWindow, 0, "OpenRecordsWindow")
	GemRB.SetWindowFrame (OptionsWindow)
	OldPortraitWindow = GUICommonWindows.PortraitWindow
	PortraitWindow = OpenPortraitWindow (0)

	# dual class
	Button = GemRB.GetControl (Window, 0)
	GemRB.SetText (Window, Button, 7174)
	GemRB.SetEvent (Window, Button, IE_GUI_BUTTON_ON_PRESS, "DualClassWindow")

	# levelup
	Button = GemRB.GetControl (Window, 37)
	GemRB.SetText (Window, Button, 7175)
	GemRB.SetEvent (Window, Button, IE_GUI_BUTTON_ON_PRESS, "LevelupWindow")

	# information
	Button = GemRB.GetControl (Window, 1)
	GemRB.SetText (Window, Button, 11946)
	GemRB.SetEvent (Window, Button, IE_GUI_BUTTON_ON_PRESS, "OpenInformationWindow")

	# reform party
	Button = GemRB.GetControl (Window, 51)
	GemRB.SetText (Window, Button, 16559)
	GemRB.SetEvent (Window, Button, IE_GUI_BUTTON_ON_PRESS, "OpenReformPartyWindow")

	# customize
	Button = GemRB.GetControl (Window, 50)
	GemRB.SetText (Window, Button, 10645)
	GemRB.SetEvent (Window, Button, IE_GUI_BUTTON_ON_PRESS, "CustomizeWindow")

	# export
	Button = GemRB.GetControl (Window, 36)
	GemRB.SetText (Window, Button, 13956)
	GemRB.SetEvent (Window, Button, IE_GUI_BUTTON_ON_PRESS, "OpenExportWindow")

## 	# kit info
## 	Button = GemRB.GetControl (Window, 52)
## 	GemRB.SetText (Window, Button, 61265)
## 	GemRB.SetEvent (Window, Button, IE_GUI_BUTTON_ON_PRESS, "KitInfoWindow")

	SetSelectionChangeHandler (UpdateRecordsWindow)
	UpdateRecordsWindow ()
	GemRB.SetVisible (OptionsWindow, 1)
	GemRB.SetVisible (Window, 3)
	GemRB.SetVisible (PortraitWindow, 1)


def UpdateRecordsWindow ():
	global stats_overview, alignment_help

	Window = RecordsWindow
	if not RecordsWindow:
		print "SelectionChange handler points to non existing window\n"
		return

	pc = GemRB.GameGetSelectedPCSingle ()

	# exportable
	Button = GemRB.GetControl (Window, 36)
	if GemRB.GetPlayerStat (pc, IE_MC_FLAGS)&MC_EXPORTABLE:
		GemRB.SetButtonState (Window, Button, IE_GUI_BUTTON_ENABLED)
	else:
		GemRB.SetButtonState (Window, Button, IE_GUI_BUTTON_DISABLED)

	# name
	Label = GemRB.GetControl (Window, 0x1000000e)
	GemRB.SetText (Window, Label, GemRB.GetPlayerName (pc, 0))

	# portrait
	Button = GemRB.GetControl (Window, 2)
	GemRB.SetButtonState (Window, Button, IE_GUI_BUTTON_LOCKED)
	GemRB.SetButtonFlags (Window, Button, IE_GUI_BUTTON_NO_IMAGE | IE_GUI_BUTTON_PICTURE, OP_SET)
	GemRB.SetButtonPicture (Window, Button, GemRB.GetPlayerPortrait (pc,0), "NOPORTMD")

	# armorclass
	Label = GemRB.GetControl (Window, 0x10000028)
	GemRB.SetText (Window, Label, str (GemRB.GetPlayerStat (pc, IE_ARMORCLASS)))
	GemRB.SetTooltip (Window, Label, 4197)

	# hp now
	Label = GemRB.GetControl (Window, 0x10000029)
	GemRB.SetText (Window, Label, str (GemRB.GetPlayerStat (pc, IE_HITPOINTS)))
	GemRB.SetTooltip (Window, Label, 4198)

	# hp max
	Label = GemRB.GetControl (Window, 0x1000002a)
	GemRB.SetText (Window, Label, str (GemRB.GetPlayerStat (pc, IE_MAXHITPOINTS)))
	GemRB.SetTooltip (Window, Label, 4199)

	# stats

	sstr = GemRB.GetPlayerStat (pc, IE_STR)
	sstrx = GemRB.GetPlayerStat (pc, IE_STREXTRA)
	cstr = GetStatColor(pc, IE_STR)
	if sstrx > 0 and sstr==18:
		sstr = "%d/%02d" %(sstr, sstrx % 100)
	else:
		sstr = str(sstr)
	sint = str(GemRB.GetPlayerStat (pc, IE_INT))
	cint = GetStatColor(pc, IE_INT)
	swis = str(GemRB.GetPlayerStat (pc, IE_WIS))
	cwis = GetStatColor(pc, IE_WIS)
	sdex = str(GemRB.GetPlayerStat (pc, IE_DEX))
	cdex = GetStatColor(pc, IE_DEX)
	scon = str(GemRB.GetPlayerStat (pc, IE_CON))
	ccon = GetStatColor(pc, IE_CON)
	schr = str(GemRB.GetPlayerStat (pc, IE_CHR))
	cchr = GetStatColor(pc, IE_CHR)

	Label = GemRB.GetControl (Window, 0x1000002f)
	GemRB.SetText (Window, Label, sstr)
	GemRB.SetLabelTextColor (Window, Label, cstr[0], cstr[1], cstr[2])

	Label = GemRB.GetControl (Window, 0x10000009)
	GemRB.SetText (Window, Label, sdex)
	GemRB.SetLabelTextColor (Window, Label, cdex[0], cdex[1], cdex[2])

	Label = GemRB.GetControl (Window, 0x1000000a)
	GemRB.SetText (Window, Label, scon)
	GemRB.SetLabelTextColor (Window, Label, ccon[0], ccon[1], ccon[2])

	Label = GemRB.GetControl (Window, 0x1000000b)
	GemRB.SetText (Window, Label, sint)
	GemRB.SetLabelTextColor (Window, Label, cint[0], cint[1], cint[2])

	Label = GemRB.GetControl (Window, 0x1000000c)
	GemRB.SetText (Window, Label, swis)
	GemRB.SetLabelTextColor (Window, Label, cwis[0], cwis[1], cwis[2])

	Label = GemRB.GetControl (Window, 0x1000000d)
	GemRB.SetText (Window, Label, schr)
	GemRB.SetLabelTextColor (Window, Label, cchr[0], cchr[1], cchr[2])

	# class
	ClassTitle = GetActorClassTitle (pc)
	Label = GemRB.GetControl (Window, 0x10000030)
	GemRB.SetText (Window, Label, ClassTitle)

	# race
	Table = GemRB.LoadTable ("races")
	text = GemRB.GetTableValue (Table, GemRB.GetPlayerStat (pc, IE_RACE) - 1, 0)
	GemRB.UnloadTable (Table)

	Label = GemRB.GetControl (Window, 0x1000000f)
	GemRB.SetText (Window, Label, text)

	Table = GemRB.LoadTable ("aligns")

	text = GemRB.GetTableValue (Table, GemRB.FindTableValue( Table, 3, GemRB.GetPlayerStat (pc, IE_ALIGNMENT) ), 0)
	GemRB.UnloadTable (Table)
	Label = GemRB.GetControl (Window, 0x10000010)
	GemRB.SetText (Window, Label, text)

	Label = GemRB.GetControl (Window, 0x10000011)
	if GemRB.GetPlayerStat (pc, IE_SEX) ==  1:
		GemRB.SetText (Window, Label, 7198)
	else:
		GemRB.SetText (Window, Label, 7199)

	#collecting tokens for stat overview
	ClassTitle = GemRB.GetString (GetActorClassTitle (pc) )

	GemRB.SetToken("CLASS", ClassTitle)
	GemRB.SetToken("LEVEL", str (GemRB.GetPlayerStat (pc, IE_LEVEL) ) )
	GemRB.SetToken("EXPERIENCE", str (GemRB.GetPlayerStat (pc, IE_XP) ) )

	# help, info textarea
	stats_overview = GetStatOverview (pc)
	Text = GemRB.GetControl (Window, 45)
	GemRB.SetText (Window, Text, stats_overview)
	#if player is inaccessible make this grey
	GemRB.SetVisible (Window, 1)


def GetStatColor (pc, stat):
	a = GemRB.GetPlayerStat(pc, stat)
	b = GemRB.GetPlayerStat(pc, stat, 1)
	if a==b:
		return (255,255,255)
	if a<b:
		return (255,255,0)
	return (0,255,0)

def GetStatOverview (pc):
	won = "[color=FFFFFF]"
	woff = "[/color]"
	StateTable = GemRB.LoadTable ("statdesc")
	str_None = GemRB.GetString (41275)

	GS = lambda s, pc=pc: GemRB.GetPlayerStat (pc, s)

	stats = []
	# 16480 <CLASS>: Level <LEVEL>
	# Experience: <EXPERIENCE>
	# Next Level: <NEXTLEVEL>

	Main = GemRB.GetString (16480)

	# 59856 Current State
	CurrentState = won + GemRB.GetString (59856) + woff + "\n\n"
	stats.append (None)
	effects = GemRB.GetPlayerStates (pc)
	for c in effects:
		tmp = GemRB.GetTableValue (StateTable, ord(c)-65, 0)
		print c, GemRB.GetString(tmp)
		stats.append (tmp)

	stats.append (None)

	# 67049 AC Bonuses
	stats.append (67049)
	#   67204 AC vs. Slashing
	stats.append ((67204, GS (IE_ACSLASHINGMOD), ''))
	#   67205 AC vs. Piercing
	stats.append ((67205, GS (IE_ACPIERCINGMOD), ''))
	#   67206 AC vs. Crushing
	stats.append ((67206, GS (IE_ACCRUSHINGMOD), ''))
	#   67207 AC vs. Missile
	stats.append ((67207, GS (IE_ACMISSILEMOD), ''))
	stats.append (None)


	# 67208 Resistances
	stats.append (67208)
	#   67209 Normal Fire
	stats.append ((67209, GS (IE_RESISTFIRE), '%'))
	#   67210 Magic Fire
	stats.append ((67210, GS (IE_RESISTMAGICFIRE), '%'))
	#   67211 Normal Cold
	stats.append ((67211, GS (IE_RESISTCOLD), '%'))
	#   67212 Magic Cold
	stats.append ((67212, GS (IE_RESISTMAGICCOLD), '%'))
	#   67213 Electricity
	stats.append ((67213, GS (IE_RESISTELECTRICITY), '%'))
	#   67214 Acid
	stats.append ((67214, GS (IE_RESISTACID), '%'))
	#   67215 Magic
	stats.append ((67215, GS (IE_RESISTMAGIC), '%'))
	#   67216 Slashing Attacks
	stats.append ((67216, GS (IE_RESISTSLASHING), '%'))
	#   67217 Piercing Attacks
	stats.append ((67217, GS (IE_RESISTPIERCING), '%'))
	#   67218 Crushing Attacks
	stats.append ((67218, GS (IE_RESISTCRUSHING), '%'))
	#   67219 Missile Attacks
	stats.append ((67219, GS (IE_RESISTMISSILE), '%'))
	stats.append (None)

	# 4220 Proficiencies
	stats.append (4220)
	#   4208 THAC0
	stats.append ((4208, GS (IE_THAC0), ''))
	#   4209 Number of Attacks
	tmp = GS (IE_NUMBEROFATTACKS)
	if (tmp&1):
		tmp2 = str(tmp/2) + chr(188)
	else:
		tmp2 = str(tmp/2)

	stats.append ((4209, tmp2, ''))
	#   4210 Lore
	stats.append ((4210, GS (IE_LORE), ''))
	#   4211 Open Locks
	stats.append ((4211, GS (IE_LOCKPICKING), ''))
	#   4212 Stealth
	stats.append ((4212, GS (IE_STEALTH), ''))
	#   4213 Find/Remove Traps
	stats.append ((4213, GS (IE_TRAPS), ''))
	#   4214 Pick Pockets
	stats.append ((4214, GS (IE_PICKPOCKET), ''))
	#   4215 Tracking
	stats.append ((4215, GS (IE_TRACKING), ''))
	#   4216 Reputation
	stats.append ((4216, GS (IE_REPUTATION), ''))
	#   4217 Turn Undead Level
	stats.append ((4217, GS (IE_TURNUNDEADLEVEL), ''))
	#   4218 Lay on Hands Amount
	stats.append ((4218, GS (IE_LAYONHANDSAMOUNT), ''))
	#   4219 Backstab Damage
	stats.append ((4219, GS (IE_BACKSTABDAMAGEMULTIPLIER), ''))
	stats.append (None)

	# 4221 Saving Throws
	stats.append (4221)
	#   4222 Paralyze/Poison/Death
	stats.append ((4222, GS (IE_SAVEVSDEATH), ''))
	#   4223 Rod/Staff/Wand
	stats.append ((4223, GS (IE_SAVEVSWANDS), ''))
	#   4224 Petrify/Polymorph
	stats.append ((4224, GS (IE_SAVEVSPOLY), ''))
	#   4225 Breath Weapon
	stats.append ((4225, GS (IE_SAVEVSBREATH), ''))
	#   4226 Spells
	stats.append ((4226, GS (IE_SAVEVSSPELL), ''))
	stats.append (None)

	# 4227 Weapon Proficiencies
	stats.append (4227)
	#   55011 Unused Slots
	#   33642 Fist
	#   33649 Edged Weapon
	#   33651 Hammer
	#   44990 Axe
	stats.append ((44990, GS (IE_PROFICIENCYAXE), ''))
	#   33653 Club
	#   33655 Bow
	stats.append (None)

	# 4228 Ability Bonuses
	stats.append (4228)
	#   4229 To Hit
	#   4230 Damage
	#   4231 Open Doors
	#   4232 Weight Allowance
	#   4233 Armor Class Bonus
	#   4234 Missile Adjustment
	stats.append ((4234, GS (IE_ACMISSILEMOD), ''))
	#   4236 CON HP Bonus/Level
	#   4240 Reaction
	stats.append (None)

	# 4238 Magical Defense Adjustment
	stats.append (4238)
	#   4239 Bonus Priest Spells
	stats.append ((4239, GS (IE_CASTINGLEVELBONUSCLERIC), ''))
	stats.append (None)

	# 4237 Chance to learn spell
	#SpellLearnChance = won + GemRB.GetString (4237) + woff

	# ??? 4235 Reaction Adjustment

	res = []
	lines = 0
	for s in stats:
		try:
			strref, val, type = s
			if val == 0 and type != '0':
				continue
			res.append (GemRB.GetString (strref) + ': ' + str (val) + type)
			lines = 1
		except:
			if s != None:
				res.append (won + GemRB.GetString (s) + woff)
				lines = 0
			else:
				if not lines:
					res.append (str_None)
				res.append ("")
				lines = 0

	return Main + CurrentState + string.join (res, "\n")


def OpenInformationWindow ():
	global InformationWindow

	GemRB.HideGUI ()

	if InformationWindow != None:
		if BiographyWindow: OpenBiographyWindow ()

		GemRB.UnloadWindow (InformationWindow)
		InformationWindow = None
		GemRB.SetVar ("FloatWindow", -1)
	
		GemRB.UnhideGUI()
		return

	InformationWindow = Window = GemRB.LoadWindow (4)
	GemRB.SetVar ("FloatWindow", InformationWindow)


	# Biography
	Button = GemRB.GetControl (Window, 26)
	GemRB.SetText (Window, Button, 18003)
	GemRB.SetEvent (Window, Button, IE_GUI_BUTTON_ON_PRESS, "OpenBiographyWindow")

	# Done
	Button = GemRB.GetControl (Window, 24)
	GemRB.SetText (Window, Button, 11973)
	GemRB.SetEvent (Window, Button, IE_GUI_BUTTON_ON_PRESS, "OpenInformationWindow")

	GemRB.UnhideGUI ()
	GemRB.ShowModal (Window, MODAL_SHADOW_GRAY)


def OpenBiographyWindow ():
	global BiographyWindow

	GemRB.HideGUI ()

	if BiographyWindow != None:
		GemRB.UnloadWindow (BiographyWindow)
		BiographyWindow = None
		GemRB.SetVar ("FloatWindow", InformationWindow)
	
		GemRB.UnhideGUI()
		GemRB.ShowModal (InformationWindow, MODAL_SHADOW_GRAY)
		return

	BiographyWindow = Window = GemRB.LoadWindow (12)
	GemRB.SetVar ("FloatWindow", BiographyWindow)

	TextArea = GemRB.GetControl (Window, 0)
	GemRB.SetText (Window, TextArea, 39424)

	# Done
	Button = GemRB.GetControl (Window, 2)
	GemRB.SetText (Window, Button, 11973)
	GemRB.SetEvent (Window, Button, IE_GUI_BUTTON_ON_PRESS, "OpenBiographyWindow")

	GemRB.UnhideGUI ()
	GemRB.ShowModal (Window, MODAL_SHADOW_GRAY)
	return

def OpenExportWindow ():
	global ExportWindow, NameField, ExportDoneButton

	ExportWindow = GemRB.LoadWindow(13)

	TextArea = GemRB.GetControl(ExportWindow, 2)
	GemRB.SetText(ExportWindow, TextArea, 10962)

	TextArea = GemRB.GetControl(ExportWindow,0)
	GemRB.GetCharacters (ExportWindow, TextArea)

	ExportDoneButton = GemRB.GetControl(ExportWindow, 4)
	GemRB.SetText(ExportWindow, ExportDoneButton, 11973)
	GemRB.SetButtonState(ExportWindow, ExportDoneButton, IE_GUI_BUTTON_DISABLED)

	CancelButton = GemRB.GetControl(ExportWindow,5)
	GemRB.SetText(ExportWindow, CancelButton, 13727)

	NameField = GemRB.GetControl(ExportWindow,6)

	GemRB.SetEvent(ExportWindow, ExportDoneButton, IE_GUI_BUTTON_ON_PRESS, "ExportDonePress")
	GemRB.SetEvent(ExportWindow, CancelButton, IE_GUI_BUTTON_ON_PRESS, "ExportCancelPress")
	GemRB.SetEvent(ExportWindow, NameField, IE_GUI_EDIT_ON_CHANGE, "ExportEditChanged")
	GemRB.ShowModal (ExportWindow, MODAL_SHADOW_GRAY)
	GemRB.SetControlStatus (ExportWindow, NameField,IE_GUI_CONTROL_FOCUSED)
	return

def ExportDonePress():
	GemRB.UnloadWindow(ExportWindow)
	#save file under name from EditControl
	return

def ExportCancelPress():
	GemRB.UnloadWindow(ExportWindow)
	return

def ExportEditChanged():
	ExportFileName = GemRB.QueryText(ExportWindow, NameField)
	if ExportFileName == "":
		GemRB.SetButtonState(ExportWindow, ExportDoneButton, IE_GUI_BUTTON_DISABLED)
	else:
		GemRB.SetButtonState(ExportWindow, ExportDoneButton, IE_GUI_BUTTON_ENABLED)
	return


###################################################
# End of file GUIREC.py
