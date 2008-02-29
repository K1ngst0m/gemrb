#character generation (GUICG 0)
import GemRB
from CharGenCommon import *
from ie_stats import *
from GUICommon import *

CharGenWindow = 0

def OnLoad():
	global CharGenWindow
	DisplayOverview (9)

	return

# we need to redefine this or we're stuck in an include loop with CharGenCommon
def NextPress():
	FinishCharGen()
	return

def FinishCharGen():
	#set my character up
	MyChar = GemRB.GetVar ("Slot")
	GemRB.CreatePlayer ("charbase", MyChar | 0x8000 )
	GemRB.SetPlayerStat (MyChar, IE_SEX, GemRB.GetVar ("Gender") )
	KitTable = GemRB.LoadTable ("kitlist")
	RaceTable = GemRB.LoadTable ("races")
	Race = GemRB.GetVar ("Race")-1
	GemRB.SetPlayerStat (MyChar, IE_RACE, GemRB.GetTableValue (RaceTable, Race, 3) )
	t = GemRB.GetVar ("Alignment")
	GemRB.SetPlayerStat (MyChar, IE_ALIGNMENT, t)

	#a little explanation for the different handling of mage kit values:
	#Originally, the IE had only mage schools, and the kit field
	#was simply an unusability field (with a single bit set)
	#then BG2 crammed in a lot more kits, and 32 bits were not enough.
	#They solved this by making the generalist value 0x4000 to hold
	#the kit index in the lower portions.
	#When you see 0x4000 in a kit value, you need to translate
	#the kit index to unusability value, using the kitlist
	#So, for mages, the kit equals to the unusability value
	#but for others there is an additional mapping by kitlist.2da

	ClassTable = GemRB.LoadTable ("classes")
	ClassIndex = GemRB.GetVar ("Class")-1
	Class = GemRB.GetTableValue (ClassTable, ClassIndex, 5)
	GemRB.SetPlayerStat (MyChar, IE_CLASS, Class)
	KitIndex = GemRB.GetVar ("Class Kit")
	TmpTable = GemRB.LoadTable ("clskills")
	#mage spells
	TableName = GemRB.GetTableValue (TmpTable, Class, 2, 0)

	if TableName != "*":
		KitValue = GemRB.GetTableValue(KitTable, KitIndex, 6)
		if KitValue == "*":
			KitValue = 0x4000
		SetupSpellLevels(MyChar, TableName, IE_SPELL_TYPE_WIZARD, 1)
		Learnable = GetLearnableMageSpells( KitValue, t, 1)
		SpellBook = GemRB.GetVar ("MageSpellBook")
		j=1
		for i in range(len(Learnable) ):
			if SpellBook & j:
				GemRB.LearnSpell (MyChar, Learnable[i], 0)
			j=j<<1
	else:
		KitValue = (0x4000 + KitIndex)<<16

	print "KitValue**********:",KitValue
	GemRB.SetPlayerStat (MyChar, IE_KIT, KitValue)

	#priest spells
	TableName = GemRB.GetTableValue (TmpTable, Class, 1, 0)
	if TableName != "*":
		SetupSpellLevels(MyChar, TableName, IE_SPELL_TYPE_PRIEST, 1)
		ClassFlag = 0 #set this according to class
		Learnable = GetLearnablePriestSpells( ClassFlag, t, 1)
		for i in range(len(Learnable) ):
			GemRB.LearnSpell (MyChar, Learnable[i], 0)

	GemRB.UnloadTable (TmpTable)
	TmpTable=GemRB.LoadTable ("repstart")
	AlignmentTable = GemRB.LoadTable ("aligns")
	t = GemRB.FindTableValue (AlignmentTable, 3, t)
	t = GemRB.GetTableValue (TmpTable,t,0) * 10
	GemRB.SetPlayerStat (MyChar, IE_REPUTATION, t)

	#slot 1 is the protagonist
	if MyChar == 1:
		GemRB.GameSetReputation( t )

	GemRB.UnloadTable (TmpTable)
	TmpTable=GemRB.LoadTable ("strtgold")
	t = GemRB.Roll (GemRB.GetTableValue (TmpTable,Class,1),GemRB.GetTableValue (TmpTable,Class,0), GemRB.GetTableValue (TmpTable,Class,2) )
	GemRB.SetPlayerStat (MyChar, IE_GOLD, t*GemRB.GetTableValue (TmpTable,Class,3) )
	GemRB.UnloadTable (AlignmentTable)
	GemRB.UnloadTable (ClassTable)
	GemRB.UnloadTable (RaceTable)
	GemRB.UnloadTable (TmpTable)

	GemRB.SetPlayerStat (MyChar, IE_HATEDRACE, GemRB.GetVar ("HatedRace") )
	TmpTable=GemRB.LoadTable ("ability")
	AbilityCount = GemRB.GetTableRowCount (TmpTable)
	for i in range(AbilityCount):
		StatID=GemRB.GetTableValue (TmpTable, i,4)
		GemRB.SetPlayerStat (MyChar, StatID, GemRB.GetVar ("Ability "+str(i) ) )
	GemRB.UnloadTable (TmpTable)

	TmpTable=GemRB.LoadTable ("weapprof")
	ProfCount = GemRB.GetTableRowCount (TmpTable)
	#bg2 weapprof.2da contains the bg1 proficiencies too, skipping those
	for i in range(ProfCount-8):
		StatID = GemRB.GetTableValue (TmpTable, i+8, 0)
		Value = GemRB.GetVar ("Prof "+str(i) )
		if Value:
			GemRB.ApplyEffect (MyChar, "Proficiency", Value, StatID )
	GemRB.UnloadTable (TmpTable)

	SetColorStat (MyChar, IE_HAIR_COLOR, GemRB.GetVar ("HairColor") )
	SetColorStat (MyChar, IE_SKIN_COLOR, GemRB.GetVar ("SkinColor") )
	SetColorStat (MyChar, IE_MAJOR_COLOR, GemRB.GetVar ("MajorColor") )
	SetColorStat (MyChar, IE_MINOR_COLOR, GemRB.GetVar ("MinorColor") )
	#SetColorStat (MyChar, IE_METAL_COLOR, 0x1B )
	#SetColorStat (MyChar, IE_LEATHER_COLOR, 0x16 )
	#SetColorStat (MyChar, IE_ARMOR_COLOR, 0x17 )
	GemRB.SetPlayerStat (MyChar, IE_EA, 2 )
	Str=GemRB.GetVar ("Ability 0")
	GemRB.SetPlayerStat (MyChar, IE_STR, Str)
	if Str==18:
		GemRB.SetPlayerStat (MyChar,IE_STREXTRA,GemRB.GetVar ("StrExtra"))
	else:
		GemRB.SetPlayerStat (MyChar, IE_STREXTRA,0)

	GemRB.SetPlayerStat (MyChar, IE_DEX, GemRB.GetVar ("Ability 1"))
	GemRB.SetPlayerStat (MyChar, IE_CON, GemRB.GetVar ("Ability 2"))
	GemRB.SetPlayerStat (MyChar, IE_INT, GemRB.GetVar ("Ability 3"))
	GemRB.SetPlayerStat (MyChar, IE_WIS, GemRB.GetVar ("Ability 4"))
	GemRB.SetPlayerStat (MyChar, IE_CHR, GemRB.GetVar ("Ability 5"))

	#setting skills (thieving/ranger)
	TmpTable = GemRB.LoadTable ("skills")
	RowCount = GemRB.GetTableRowCount (TmpTable)-2

	for i in range(RowCount):
		stat = GemRB.GetTableValue (TmpTable, i+2, 2)
		value = GemRB.GetVar ("Skill "+str(i) )
		GemRB.SetPlayerStat (MyChar, stat, value )
 	GemRB.UnloadTable (TmpTable)

	GemRB.SetPlayerName (MyChar, GemRB.GetToken ("CHARNAME"), 0)
	TmpTable = GemRB.LoadTable ("clskills")
	GemRB.SetPlayerStat (MyChar, IE_XP, GemRB.GetTableValue (TmpTable, Class, 3) )  #this will also set the level (automatically)
	GemRB.UnloadTable (TmpTable)

	#does all the rest
	LargePortrait = GemRB.GetToken ("LargePortrait")
	SmallPortrait = GemRB.GetToken ("SmallPortrait")
	GemRB.FillPlayerInfo (MyChar, LargePortrait, SmallPortrait)

	playmode = GemRB.GetVar ("PlayMode")
	if playmode >=0:
		#LETS PLAY!!
		GemRB.EnterGame()
	else:
		#leaving multi player pregen
		GemRB.UnloadWindow (CharGenWindow)
		#when export is done, go to start
		if GameIsTOB():
			GemRB.SetToken ("NextScript","Start2")
		else:
			GemRB.SetToken ("NextScript","Start")
		GemRB.SetNextScript ("ExportFile") #export
	return

