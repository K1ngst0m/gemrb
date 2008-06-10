# -*-python-*-
# GemRB - Infinity Engine Emulator
# Copyright (C) 2003-2004 The GemRB Project
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
# $Id$
# character generation, mage spells (GUICG7)

import GemRB
from GUIDefines import *
from GUICommon import GetMageSpells, GetLearnableMageSpells

MageSpellsWindow = 0
MageSpellsTextArea = 0
DoneButton = 0
Random = 1
MageSpells = []
KitValue = 0
Class = 0
Slot = GemRB.GetVar ("Slot")

def OnLoad():
	global MageSpellsWindow, MageSpellsTextArea, DoneButton
	global MageSpellsSelectPointsLeft, MageSpells, Class, KitValue
	
	AlignmentTable = GemRB.LoadTable("aligns")
	ClassTable = GemRB.LoadTable("classes")
	KitTable = GemRB.LoadTable("magesch")
	ClassRow = GemRB.GetVar("Class")-1
	Class = GemRB.GetTableValue(ClassTable, ClassRow, 5)
	TmpTable = GemRB.LoadTable("clskills")
	TableName = GemRB.GetTableValue(TmpTable, Class, 2)
	if TableName == "*":
		GemRB.SetNextScript("GUICG6")
		return

	MageSpellsSelectPointsLeft = 2
	GemRB.LoadWindowPack("GUICG", 640, 480)
	MageSpellsWindow = GemRB.LoadWindow(7)
	v = GemRB.GetVar("Alignment")
	KitIndex = GemRB.GetVar("Class Kit")
	if KitIndex:
		KitValue = GemRB.GetTableValue(KitTable, KitIndex - 21, 3)

		# bards have kits too
		if KitValue == -1:
			KitValue = 0x4000 # we only need it for the spells, so this is ok
		#this is an ugly hack, to exclude bards from specialisation (and bonus spell)
		if GemRB.GetTableValue(TmpTable, Class, 4)=='*':
			MageSpellsSelectPointsLeft = MageSpellsSelectPointsLeft + 1
		# TODO make the random Pick method enforce a specialist selection too?
	else:
		KitValue = 0x4000

	MageSpells = GetMageSpells (KitValue, v, 1)
	GemRB.SetVar("MageSpellBook", 0)
	SpellMask = 0
	GemRB.SetVar("SpellMask", 0)

	RemoveKnownSpells (IE_SPELL_TYPE_WIZARD)

	PointsLeftLabel = GemRB.GetControl(MageSpellsWindow, 0x1000001b)
	GemRB.SetLabelUseRGB(MageSpellsWindow, PointsLeftLabel, 1)
	GemRB.SetText(MageSpellsWindow, PointsLeftLabel, str(MageSpellsSelectPointsLeft))

	for i in range (24):
		SpellButton = GemRB.GetControl(MageSpellsWindow, i + 2)
		if i >=  len(MageSpells):
			GemRB.SetButtonState(MageSpellsWindow, SpellButton, IE_GUI_BUTTON_DISABLED)
			continue

		Spell = GemRB.GetSpell(MageSpells[i][0])
		GemRB.SetTooltip(MageSpellsWindow, SpellButton, Spell['SpellName'])
		GemRB.SetSpellIcon(MageSpellsWindow, SpellButton, MageSpells[i][0], 1)
		GemRB.SetVarAssoc(MageSpellsWindow, SpellButton, "ButtonPressed", i)
		GemRB.SetEvent(MageSpellsWindow, SpellButton, IE_GUI_BUTTON_ON_PRESS, "MageSpellsSelectPress")
		GemRB.SetButtonSprites(MageSpellsWindow, SpellButton, "GUIBTBUT", 0,0,1,2,3)
		GemRB.SetButtonFlags(MageSpellsWindow, SpellButton, IE_GUI_BUTTON_PICTURE, OP_OR)
		if MageSpells[i][1] == 0:
			GemRB.SetButtonState(MageSpellsWindow, SpellButton, IE_GUI_BUTTON_LOCKED)
			# shade red
			GemRB.SetButtonBorder (MageSpellsWindow, SpellButton, 0, 0,0, 0,0, 200,0,0,100, 1,1)
		elif MageSpells[i][1] == 1:
			GemRB.SetButtonState (MageSpellsWindow, SpellButton, IE_GUI_BUTTON_ENABLED)
		else:
			# use the green border state for matching specialist spells
			GemRB.SetButtonState (MageSpellsWindow, SpellButton, IE_GUI_BUTTON_THIRD)

	GemRB.SetToken("number", str(MageSpellsSelectPointsLeft))
	MageSpellsTextArea = GemRB.GetControl(MageSpellsWindow, 27)
	GemRB.SetText(MageSpellsWindow, MageSpellsTextArea, 17250)

	DoneButton = GemRB.GetControl(MageSpellsWindow, 0)
	GemRB.SetButtonState(MageSpellsWindow, DoneButton, IE_GUI_BUTTON_DISABLED)
	GemRB.SetEvent(MageSpellsWindow, DoneButton, IE_GUI_BUTTON_ON_PRESS, "MageSpellsDonePress")
	GemRB.SetText(MageSpellsWindow, DoneButton, 11973)
	GemRB.SetButtonFlags(MageSpellsWindow, DoneButton, IE_GUI_BUTTON_DEFAULT, OP_OR)

	MageSpellsCancelButton = GemRB.GetControl(MageSpellsWindow, 29)
	GemRB.SetButtonState(MageSpellsWindow, MageSpellsCancelButton, IE_GUI_BUTTON_ENABLED)
	GemRB.SetEvent(MageSpellsWindow, MageSpellsCancelButton, IE_GUI_BUTTON_ON_PRESS, "MageSpellsCancelPress")
	GemRB.SetText(MageSpellsWindow, MageSpellsCancelButton, 13727)

	MageSpellsPickButton = GemRB.GetControl(MageSpellsWindow, 30)
	GemRB.SetButtonState(MageSpellsWindow, MageSpellsPickButton, IE_GUI_BUTTON_ENABLED)
	GemRB.SetEvent(MageSpellsWindow, MageSpellsPickButton, IE_GUI_BUTTON_ON_PRESS, "MageSpellsPickPress")
	GemRB.SetText(MageSpellsWindow, MageSpellsPickButton, 34210)

	GemRB.SetVisible(MageSpellsWindow,1)
	return

def MageSpellsSelectPress():
	global MageSpellsSelectPointsLeft, MageSpells, Class, KitValue

	MageSpellBook = GemRB.GetVar("MageSpellBook")
	i = GemRB.GetVar("ButtonPressed")
	SpellMask = 1 << i

	Spell = GemRB.GetSpell(MageSpells[i][0])
	GemRB.SetText(MageSpellsWindow, MageSpellsTextArea, Spell["SpellDesc"])
	if MageSpells[i][1]:
		if SpellMask & MageSpellBook:
			MageSpellsSelectPointsLeft = MageSpellsSelectPointsLeft + 1
			MageSpellBook = MageSpellBook ^ SpellMask
			GemRB.SetButtonState(MageSpellsWindow, DoneButton, IE_GUI_BUTTON_DISABLED)
		else:
			if MageSpellsSelectPointsLeft == 0:
				MarkButton(i,0)
				return

			# specialists need to pick at least one specialist spell
			if Class == 1 and KitValue != 0x4000 and \
			MageSpellsSelectPointsLeft == 1 and MageSpells[i][1] != 2:
				HasSpecialistSpell = 0
				# check if the current selection contains a specialist spell
				for j in range (len(MageSpells)):
					if (MageSpellBook & (1 << j)) and MageSpells[j][1] == 2:
						HasSpecialistSpell = 1

				if HasSpecialistSpell == 0:
					GemRB.SetText (MageSpellsWindow, MageSpellsTextArea, 33381)
					MarkButton (i,0)
					return

			MageSpellsSelectPointsLeft = MageSpellsSelectPointsLeft - 1
			MageSpellBook = MageSpellBook | SpellMask
			if MageSpellsSelectPointsLeft == 0:
				GemRB.SetButtonState(MageSpellsWindow, DoneButton, IE_GUI_BUTTON_ENABLED)

	for j in range (len(MageSpells)):
		if MageSpellBook & (1 << j):
			MarkButton(j,1)
		else:
			MarkButton(j,0)

	PointsLeftLabel = GemRB.GetControl(MageSpellsWindow, 0x1000001b)
	GemRB.SetText(MageSpellsWindow, PointsLeftLabel, str(MageSpellsSelectPointsLeft))
	GemRB.SetVar("MageSpellBook", MageSpellBook)
	return

def MarkButton(i,select):
	if select:
		type = IE_GUI_BUTTON_SELECTED
	else:
		if MageSpells[i][1] == 1:
			type = IE_GUI_BUTTON_ENABLED
		elif MageSpells[i][1] == 2:
			# specialist spell
			type = IE_GUI_BUTTON_THIRD
		else:
			type = IE_GUI_BUTTON_LOCKED

	SpellButton = GemRB.GetControl(MageSpellsWindow, i + 2)
	GemRB.SetButtonState(MageSpellsWindow, SpellButton, type)
	return

def MageSpellsCancelPress():
	GemRB.UnloadWindow(MageSpellsWindow)
	GemRB.SetNextScript("CharGen6") #haterace
	return

def MageSpellsDonePress():
	global KitValue, Slot
	MageSpellBook = GemRB.GetVar ("MageSpellBook")
	j=1
	for level in range(1, 10):
		for i in range (len(MageSpells)):
			if MageSpellBook & j:
				GemRB.LearnSpell (Slot, MageSpells[i][0])
			j=j<<1

	GemRB.UnloadWindow(MageSpellsWindow)
	GemRB.SetNextScript("GUICG6") #abilities
	return

def RemoveKnownSpells(type):
	global Slot
	for level in range(0, 9):
		for j in range(GemRB.GetKnownSpellsCount (Slot, type, level)-1, -1, -1):
			GemRB.RemoveSpell (Slot, type, level, j)

def MageSpellsPickPress():
	global MageSpellsSelectPointsLeft, MageSpells

	MageSpellBook = GemRB.GetVar("MageSpellBook")
	Range = 0
	for i in range (len(MageSpells)):
		if MageSpells[i][1]:
			Range+=1

	if MageSpellsSelectPointsLeft > Range:
		MageSpellsSelectPointsLeft = Range
	if MageSpellsSelectPointsLeft:
		for i in range(MageSpellsSelectPointsLeft):
			if Random:
				j = RandomPick(Range)
			else:
				j = AutoPick(Range)
			MageSpellBook = MageSpellBook | (1<<j)
		GemRB.SetVar("MageSpellBook", MageSpellBook)
	MageSpellsDonePress()
	return

def RandomPick (Range):
	MageSpellBook = GemRB.GetVar("MageSpellBook")

	j = GemRB.Roll(1,Range,-1)
	while MageSpellBook & (1<<j):
		j = j - 1
		if j<0:
			j=Range-1
	return j

def AutoPick (Range):
	return j

