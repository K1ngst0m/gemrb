/* GemRB - Infinity Engine Emulator
 * Copyright (C) 2003 The GemRB Project
 *
 * This program is free software; you can redistribute it and/or
 * modify it under the terms of the GNU General Public License
 * as published by the Free Software Foundation; either version 2
 * of the License, or (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
 *
 * $Header: /data/gemrb/cvs2svn/gemrb/gemrb/gemrb/plugins/Core/GameScript.h,v 1.74 2004/03/20 10:06:18 avenger_teambg Exp $
 *
 */

class GameScript;
class Action;

#ifndef GAMESCRIPT_H
#define GAMESCRIPT_H

#include "DataStream.h"
#include "Variables.h"
#include "SymbolMgr.h"
#include "Actor.h"
#include <list>

#define MAX_OBJECT_FIELDS	10
#define MAX_NESTING			5

#define GSASSERT(f,c) \
  if(!(f))  \
  {  \
  printf("Assertion failed: %s [0x%08X] Line %d",#f, c, __LINE__); \
		abort(); \
  }

#ifdef WIN32

#ifdef GEM_BUILD_DLL
#define GEM_EXPORT __declspec(dllexport)
#else
#define GEM_EXPORT __declspec(dllimport)
#endif

#else
#define GEM_EXPORT
#endif

class GEM_EXPORT Targets {
public:
	Targets()
	{
	};
	~Targets()
	{
		Clear();
	};
private:
	std::vector< Actor*> objects;
public:
	int Count()
	{
		return objects.size();
	};
	Actor* GetTarget(int index)
	{
		if (index >= objects.size()) {
			return NULL;
		}
		return objects.at( index );
	};
	void RemoveTargetAt(int index)
	{
		if(index>objects.size() ) {
			return;
		}
		std::vector< Actor*>::iterator m=objects.begin()+index;
		objects.erase(m);
	};
	void AddTarget(Actor* Target)
	{
		if(Target && !Target->DeleteMe) {
			objects.push_back( Target );
		}
	};
	void Clear()
	{
		objects.clear();
	};
	bool Contains(Actor* scr)
	{
		if (!objects.size()) {
			return false;
		}
		for (unsigned int i = 0; i < objects.size(); i++) {
			if (objects.at( i ) == scr) {
				return true;
			}
		}
		return false;
	};
};

class GEM_EXPORT Object {
public:
	Object()
	{
		RefCount = 1;
		objectName[0] = 0;

		memset( objectFields, 0, MAX_OBJECT_FIELDS * sizeof( int ) );
		memset( objectFilters, 0, MAX_NESTING * sizeof( int ) );
		memset( objectRect, 0, 4 * sizeof( int ) );

		canary = 0xdeadbeef;
	};
	~Object()
	{
	}
public:
	int objectFields[MAX_OBJECT_FIELDS];
	int objectFilters[MAX_NESTING];
	int objectRect[4];
	char objectName[65];
private:
	int RefCount;
	volatile unsigned long canary;
public:
	void Release()
	{
		GSASSERT( canary == 0xdeadbeef, canary );
		if (!RefCount) {
			printf( "WARNING!!! Double Freeing in %s: Line %d\n", __FILE__,
				__LINE__ );
			abort();
		}
		RefCount--;
		if (!RefCount) {
			delete this;
		}
	}
	void IncRef()
	{
		GSASSERT( canary == 0xdeadbeef, canary );
		RefCount++;
		printf( "IncRef(%d) called in Line %d\n", RefCount, __LINE__ );
		if (RefCount >= 4) {
			printf( "Refcount increased to: %d in object\n", RefCount );
			abort();
		}
	}
};

class GEM_EXPORT Trigger {
public:
	Trigger()
	{
		objectParameter = NULL;
		RefCount = 1;
		string0Parameter[0] = 0;
		string1Parameter[0] = 0;
		canary = 0xdeadbeef;
	};
	~Trigger()
	{
		if (objectParameter) {
			objectParameter->Release();
		}
	}
public:
	unsigned short triggerID;
	int int0Parameter;
	int flags;
	int int1Parameter;
	int int2Parameter;
	int XpointParameter;
	int YpointParameter;
	char string0Parameter[65];
	char string1Parameter[65];
	Object* objectParameter;
private:
	int RefCount;
	volatile unsigned long canary;
public:
	void Release()
	{
		GSASSERT( canary == 0xdeadbeef, canary );
		if (!RefCount) {
			printf( "WARNING!!! Double Freeing in %s: Line %d\n", __FILE__,
				__LINE__ );
			abort();
		}
		RefCount--;
		if (!RefCount) {
			delete this;
		}
	}
	void IncRef()
	{
		GSASSERT( canary == 0xdeadbeef, canary );
		RefCount++;
		printf( "IncRef(%d) called in Line %d\n", RefCount, __LINE__ );
		if (RefCount >= 4) {
			printf( "Refcount increased to: %d in trigger\n", RefCount );
			abort();
		}
	}
};

class GEM_EXPORT Condition {
public:
	Condition()
	{
		RefCount = 1;
		triggers = NULL;
		triggersCount = 0;
		canary = 0xdeadbeef;
	};
	~Condition()
	{
		if (!triggers) {
			return;
		}
		for (int c = 0; c < triggersCount; c++) {
			if (triggers[c]) {
				triggers[c]->Release();
			}
		}
		//delete[] triggers;
		delete triggers;
	}
public:
	unsigned short triggersCount;
	Trigger** triggers;
private:
	int RefCount;
	volatile unsigned long canary;
public:
	void Release()
	{
		GSASSERT( canary == 0xdeadbeef, canary );
		if (!RefCount) {
			printf( "WARNING!!! Double Freeing in %s: Line %d\n", __FILE__,
				__LINE__ );
			abort();
		}
		RefCount--;
		if (!RefCount) {
			delete this;
		}
	}
	void IncRef()
	{
		GSASSERT( canary == 0xdeadbeef, canary );
		RefCount++;
		printf( "IncRef(%d) called in Line %d\n", RefCount, __LINE__ );
		if (RefCount >= 4) {
			printf( "Refcount increased to: %d in condition\n", RefCount );
			abort();
		}
	}
};

class GEM_EXPORT Action {
public:
	Action()
	{
		actionID = 0;
		objects[0] = NULL;
		objects[1] = NULL;
		objects[2] = NULL;
		string0Parameter[0] = 0;
		string1Parameter[0] = 0;
		int0Parameter = 0;
		XpointParameter = 0;
		YpointParameter = 0;
		int1Parameter = 0;
		int2Parameter = 0;
		RefCount = 1;
		canary = 0xdeadbeef;
	};
	~Action()
	{
		for (int c = 0; c < 3; c++) {
			if (objects[c]) {
				objects[c]->Release();
			}
		}
	}
public:
	unsigned short actionID;
	Object* objects[3];
	int int0Parameter;
	int XpointParameter;
	int YpointParameter;
	int int1Parameter;
	int int2Parameter;
	char string0Parameter[65];
	char string1Parameter[65];
private:
	int RefCount;
	volatile unsigned long canary;
public:
	void Release()
	{
		GSASSERT( canary == 0xdeadbeef, canary );
		if (!RefCount) {
			printf( "WARNING!!! Double Freeing in %s: Line %d\n", __FILE__,
				__LINE__ );
			abort();
		}
		RefCount--;
		if (!RefCount) {
			delete this;
		}
	}
	void IncRef()
	{
		GSASSERT( canary == 0xdeadbeef, canary );
		RefCount++;
		printf( "IncRef(%d) called in Line %d\n", RefCount, __LINE__ );
		if (RefCount >= 4) {
			printf( "Refcount increased to: %d in action %d\n", RefCount,
				actionID );
			abort();
		}
	}
};

class GEM_EXPORT Response {
public:
	Response()
	{
		RefCount = 1;
		actions = NULL;
		weight = 0;
		actionsCount = 0;
		canary = 0xdeadbeef;
	};
	~Response()
	{
		if (!actions) {
			return;
		}
		for (int c = 0; c < actionsCount; c++) {
			if (actions[c]) {
				actions[c]->Release();
			}
		}
		delete actions;
	}
public:
	unsigned char weight;
	unsigned char actionsCount;
	Action** actions;
private:
	int RefCount;
	volatile unsigned long canary;
public:
	void Release()
	{
		GSASSERT( canary == 0xdeadbeef, canary );
		if (!RefCount) {
			printf( "WARNING!!! Double Freeing in %s: Line %d\n", __FILE__,
				__LINE__ );
			abort();
		}
		RefCount--;
		if (!RefCount) {
			delete this;
		}
	}
	void IncRef()
	{
		GSASSERT( canary == 0xdeadbeef, canary );
		RefCount++;
		printf( "IncRef(%d) called in Line %d\n", RefCount, __LINE__ );
		if (RefCount >= 4) {
			printf( "Refcount increased to: %d in response\n", RefCount );
			abort();
		}
	}
};

class GEM_EXPORT ResponseSet {
public:
	ResponseSet()
	{
		RefCount = 1;
		responses = NULL;
		responsesCount = 0;
		canary = 0xdeadbeef;
	};
	~ResponseSet()
	{
		if (!responses) {
			return;
		}
		for (int b = 0; b < responsesCount; b++) {
			Response* rP = responses[b];
			rP->Release();
		}
		//delete[] responses;
		delete responses;
	}
public:
	unsigned short responsesCount;
	Response** responses;
private:
	int RefCount;
	volatile unsigned long canary;
public:
	void Release()
	{
		GSASSERT( canary == 0xdeadbeef, canary );
		if (!RefCount) {
			printf( "WARNING!!! Double Freeing in %s: Line %d\n", __FILE__,
				__LINE__ );
			abort();
		}
		RefCount--;
		if (!RefCount) {
			delete this;
		}
	}
	void IncRef()
	{
		GSASSERT( canary == 0xdeadbeef, canary );
		RefCount++;
		printf( "IncRef(%d) called in Line %d\n", RefCount, __LINE__ );
		if (RefCount >= 4) {
			printf( "Refcount increased to: %d\n", RefCount );
			abort();
		}
	}
};

class GEM_EXPORT ResponseBlock {
public:
	ResponseBlock()
	{
		RefCount = 1;
		condition = NULL;
		responseSet = NULL;
		canary = 0xdeadbeef;
	};
	~ResponseBlock()
	{
		if (condition) {
			condition->Release();
		}
		if (responseSet) {
			responseSet->Release();
		}
	}
public:
	Condition* condition;
	ResponseSet* responseSet;
private:
	int RefCount;
	volatile unsigned long canary;
public:
	void Release()
	{
		GSASSERT( canary == 0xdeadbeef, canary );
		if (!RefCount) {
			printf( "WARNING!!! Double Freeing in %s: Line %d\n", __FILE__,
				__LINE__ );
			abort();
		}
		RefCount--;
		if (!RefCount) {
			delete this;
		}
	}
	void IncRef()
	{
		GSASSERT( canary == 0xdeadbeef, canary );
		RefCount++;
		printf( "IncRef(%d) called in Line %d\n", RefCount, __LINE__ );
		if (RefCount >= 4) {
			printf( "Refcount increased to: %d\n", RefCount );
			abort();
		}
	}
};

class GEM_EXPORT Script {
public:
	Script(const char* ScriptName)
	{
		canary = 0xdeadbeef;
		RefCount = 1;
		responseBlocks = NULL;
		responseBlocksCount = 0;
		if (!Name) {
			this->Name[0] = 0;
			return;
		}
		strncpy( Name, ScriptName, 8 );
		Name[8] = 0;
	};
	~Script()
	{
		FreeResponseBlocks();
		printf( "Freeing Script: %s\n", GetName() );
	}
	const char* GetName()
	{
		return this ? Name : "<none>";
	}
	void AllocateBlocks(unsigned int count)
	{
		if (!count) {
			FreeResponseBlocks();
			responseBlocks = NULL;
			responseBlocksCount = 0;
		}
		responseBlocks = new ResponseBlock * [count];
		responseBlocksCount = count;
	}
private:
	void FreeResponseBlocks()
	{
		if (!responseBlocks) {
			return;
		}
		for (unsigned int i = 0; i < responseBlocksCount; i++) {
			if (responseBlocks[i]) {
				responseBlocks[i]->Release();
			}
		}
		//delete[] responseBlocks;
		delete responseBlocks;
	}
public:
	unsigned int responseBlocksCount;
	ResponseBlock** responseBlocks;
	char Name[9];
private:
	int RefCount;
	volatile unsigned long canary;
public:
	void Release()
	{
		GSASSERT( canary == 0xdeadbeef, canary );
		if (!RefCount) {
			printf( "WARNING!!! Double Freeing in %s: Line %d\n", __FILE__,
				__LINE__ );
			abort();
		}
		RefCount--;
		if (!RefCount) {
			delete this;
		}
	}
	void IncRef()
	{
		GSASSERT( canary == 0xdeadbeef, canary );
		RefCount++;
		printf( "IncRef(%d) called in Line %d\n", RefCount, __LINE__ );
		if (RefCount >= 4) {
			printf( "Refcount increased to: %d\n", RefCount );
			abort();
		}
	}
};

typedef int (* TriggerFunction)(Scriptable*, Trigger*);
typedef void (* ActionFunction)(Scriptable*, Action*);
typedef Targets* (* ObjectFunction)(Scriptable *, Targets*);
typedef int (* IDSFunction)(Actor *, int parameter);

struct TriggerLink {
	const char* Name;
	TriggerFunction Function;
};

//createcreature flags
#define CC_OFFSET    1  //add the position of Sender to the coordinates
#define CC_OBJECT    2  //use object instead of sender
#define CC_MASK      3

//begindialog flags
#define BD_STRING0   0
#define BD_TARGET    1
#define BD_SOURCE    2
#define BD_RESERVED  3
#define BD_LOCMASK   3  //where is the dialog resref
#define BD_INTERRUPT 4  //interrupts action
#define BD_TALKCOUNT 8  //increases talkcount
#define BD_SETDIALOG 16 //also sets dialog (for string0)
#define BD_CHECKDIST 32 //checks distance, if needs, walks up
#define BD_OWN  	 64 //source == target, works for player only

#define AF_NONE 	 0
#define AF_INSTANT   1
#define AF_CONTINUE  2
#define AF_MASK 	 3   //none, instant or continue
#define AF_BLOCKING  4

struct ActionLink {
	const char* Name;
	ActionFunction Function;
	int Flags;
};

struct ObjectLink {
	const char* Name;
	ObjectFunction Function;
};

struct IDSLink {
	const char* Name;
	IDSFunction Function;
};

#define IE_SCRIPT_ALWAYS		0
#define IE_SCRIPT_AREA			1
#define IE_SCRIPT_TRIGGER		2

#define MAX_TRIGGERS			0xFF
#define MAX_ACTIONS			400
#define MAX_OBJECTS			128

class GEM_EXPORT GameScript {
public:
	Variables* locals;
	Script* script;
	Scriptable* MySelf;
	unsigned long scriptRunDelay;
	bool endReached;
	void Update();
	void EvaluateAllBlocks();
private: //Internal Functions
	Script* CacheScript(DataStream* stream, const char* Context);
	ResponseBlock* ReadResponseBlock(DataStream* stream);
	Condition* ReadCondition(DataStream* stream);
	ResponseSet* ReadResponseSet(DataStream* stream);
	Response* ReadResponse(DataStream* stream);
	Trigger* ReadTrigger(DataStream* stream);
	Object* DecodeObject(const char* line);
	bool EvaluateCondition(Scriptable* Sender, Condition* condition);
	static bool EvaluateTrigger(Scriptable* Sender, Trigger* trigger);
	int ExecuteResponseSet(Scriptable* Sender, ResponseSet* rS);
	int ExecuteResponse(Scriptable* Sender, Response* rE);
	static Targets* EvaluateObject(Object* oC);
	static int ParseInt(const char*& src);
	static void ParseString(const char*& src, char* tmp);

public:
	static void ExecuteAction(Scriptable* Sender, Action* aC);
	static Action* CreateAction(char* string, bool autoFree = true);
private:
	static Action* GenerateAction(char* String);
	static Trigger* GenerateTrigger(char* String);
	/* returns the number of actors matching the IDS targeting */
	static int GetObjectCount(Scriptable* Sender, Object* oC);
	static Scriptable* GetActorFromObject(Scriptable* Sender, Object* oC);
	static int GetHappiness(Scriptable* Sender, int reputation);
	static int GetHPPercent(Scriptable* Sender);
	static int SeeCore(Scriptable* Sender, Trigger* parameters, int flags);
	static void BeginDialog(Scriptable* Sender, Action* parameters, int flags);
	static void CreateCreatureCore(Scriptable* Sender, Action* parameters,
		int flags);
	static Targets *XthNearestOf(Scriptable *Sender, Targets *parameters, int count);
	static Targets *XthNearestEnemyOf(Scriptable *Sender, Targets *parameters, int count);

	static unsigned char GetOrient(short sX, short sY, short dX, short dY);
private: //Internal variables
	unsigned long lastRunTime;
	unsigned long scriptType;
private: //Script Internal Variables
	bool continueExecution;
	std::list< Action*> programmedActions;
	char Name[9];
	bool freeLocals;
public:
	GameScript(const char* ResRef, unsigned char ScriptType,
		Variables* local = NULL);
	~GameScript();
	static void ReplaceMyArea(Scriptable* Sender, char* newVarName);
	static unsigned long CheckVariable(Scriptable* Sender,
		const char* VarName, const char* Context);
	static unsigned long CheckVariable(Scriptable* Sender, const char* VarName);

	static void SetVariable(Scriptable* Sender, const char* VarName,
		const char* Context, int value);
	static void SetVariable(Scriptable* Sender, const char* VarName, int value);
	static void ExecuteString(Scriptable* Sender, char* String);
	static bool EvaluateString(Scriptable* Sender, char* String);
public: //Script Functions
	static int ID_Alignment(Actor *actor, int parameter);
	static int ID_Allegiance(Actor *actor, int parameter);
	static int ID_AVClass(Actor *actor, int parameter);
	static int ID_Class(Actor *actor, int parameter);
	static int ID_ClassMask(Actor *actor, int parameter);
	static int ID_Faction(Actor *actor, int parameter);
	static int ID_Gender(Actor *actor, int parameter);
	static int ID_General(Actor *actor, int parameter);
	static int ID_Race(Actor *actor, int parameter);
	static int ID_Specific(Actor *actor, int parameter);
	static int ID_Subrace(Actor *actor, int parameter);
	static int ID_Team(Actor *actor, int parameter);

	//Triggers
	static int ActionListEmpty(Scriptable* Sender, Trigger* parameters);
	static int Alignment(Scriptable* Sender, Trigger* parameters);
	static int Allegiance(Scriptable* Sender, Trigger* parameters);
	static int AreaCheck(Scriptable* Sender, Trigger* parameter);
	static int AreaFlag(Scriptable* Sender, Trigger* parameter);
	static int AreaType(Scriptable* Sender, Trigger* parameter);
	static int BitCheck(Scriptable* Sender, Trigger* parameters);
	static int BreakingPoint(Scriptable* Sender, Trigger* parameters);
	static int CheckStat(Scriptable* Sender, Trigger* parameters);
	static int CheckStatGT(Scriptable* Sender, Trigger* parameters);
	static int CheckStatLT(Scriptable* Sender, Trigger* parameters);
	static int Class(Scriptable* Sender, Trigger* parameters);
	static int Clicked(Scriptable* Sender, Trigger* parameters);
	static int Dead(Scriptable* Sender, Trigger* parameters);
	static int Entered(Scriptable* Sender, Trigger* parameters);
	static int Exists(Scriptable* Sender, Trigger* parameters);
	static int False(Scriptable* Sender, Trigger* parameters);
	static int Gender(Scriptable* Sender, Trigger* parameters);
	static int General(Scriptable* Sender, Trigger* parameters);
	static int Global(Scriptable* Sender, Trigger* parameters);
	static int GlobalLT(Scriptable* Sender, Trigger* parameters);
	static int GlobalGT(Scriptable* Sender, Trigger* parameters);
	static int GlobalsEqual(Scriptable* Sender, Trigger* parameters);
	static int GlobalTimerExact(Scriptable* Sender, Trigger* parameters);
	static int GlobalTimerExpired(Scriptable* Sender, Trigger* parameters);
	static int GlobalTimerNotExpired(Scriptable* Sender, Trigger* parameters);
	static int Happiness(Scriptable* Sender, Trigger* parameters);
	static int HappinessGT(Scriptable* Sender, Trigger* parameters);
	static int HappinessLT(Scriptable* Sender, Trigger* parameters);
	static int HP(Scriptable* Sender, Trigger* parameters);
	static int HPGT(Scriptable* Sender, Trigger* parameters);
	static int HPLT(Scriptable* Sender, Trigger* parameters);
	static int HPPercent(Scriptable* Sender, Trigger* parameters);
	static int HPPercentGT(Scriptable* Sender, Trigger* parameters);
	static int HPPercentLT(Scriptable* Sender, Trigger* parameters);
	static int InActiveArea(Scriptable* Sender, Trigger* parameter);
	static int InMyArea(Scriptable* Sender, Trigger* parameter);
	static int InParty(Scriptable* Sender, Trigger* parameters);
	static int InPartyAllowDead(Scriptable* Sender, Trigger* parameters);
	static int InPartySlot(Scriptable* Sender, Trigger* parameters);
	static int IsValidForPartyDialog(Scriptable* Sender, Trigger* parameters);
	static int Level(Scriptable* Sender, Trigger* parameters);
	static int LevelGT(Scriptable* Sender, Trigger* parameters);
	static int LevelLT(Scriptable* Sender, Trigger* parameters);
	static int LOS(Scriptable* Sender, Trigger* parameters);
	static int Morale(Scriptable* Sender, Trigger* parameters);
	static int MoraleGT(Scriptable* Sender, Trigger* parameters);
	static int MoraleLT(Scriptable* Sender, Trigger* parameters);
	static int NotStateCheck(Scriptable* Sender, Trigger* parameters);
	static int NumCreatures(Scriptable* Sender, Trigger* parameters);
	static int NumCreaturesGT(Scriptable* Sender, Trigger* parameters);
	static int NumCreaturesLT(Scriptable* Sender, Trigger* parameters);
	static int NumTimesTalkedTo(Scriptable* Sender, Trigger* parameters);
	static int NumTimesTalkedToGT(Scriptable* Sender, Trigger* parameters);
	static int NumTimesTalkedToLT(Scriptable* Sender, Trigger* parameters);
	static int ObjectActionListEmpty(Scriptable* Sender, Trigger* parameters);
	static int OnCreation(Scriptable* Sender, Trigger* parameters);
	static int OpenState(Scriptable* Sender, Trigger* parameters);
	static int Or(Scriptable* Sender, Trigger* parameters);
	static int PartyHasItem(Scriptable* Sender, Trigger* parameters);
	static int Race(Scriptable* Sender, Trigger* parameters);
	static int RandomNum(Scriptable* Sender, Trigger* parameters);
	static int RandomNumGT(Scriptable* Sender, Trigger* parameters);
	static int RandomNumLT(Scriptable* Sender, Trigger* parameters);
	static int Range(Scriptable* Sender, Trigger* parameters);
	static int Reputation(Scriptable* Sender, Trigger* parameters);
	static int ReputationGT(Scriptable* Sender, Trigger* parameters);
	static int ReputationLT(Scriptable* Sender, Trigger* parameters);
	static int See(Scriptable* Sender, Trigger* parameters);
	static int Specific(Scriptable* Sender, Trigger* parameters);
	static int StateCheck(Scriptable* Sender, Trigger* parameters);
	static int True(Scriptable* Sender, Trigger* parameters);
	static int UnselectableVariable(Scriptable* Sender, Trigger* parameters);
	static int UnselectableVariableGT(Scriptable* Sender, Trigger* parameters);
	static int UnselectableVariableLT(Scriptable* Sender, Trigger* parameters);
	static int XP(Scriptable* Sender, Trigger* parameters);
	static int XPGT(Scriptable* Sender, Trigger* parameters);
	static int XPLT(Scriptable* Sender, Trigger* parameters);
public:
	//Actions
	static void Activate(Scriptable* Sender, Action* parameters);
	static void AddAreaFlag(Scriptable* Sender, Action* parameters);
	static void AddAreaType(Scriptable* Sender, Action* parameters);
	static void AddExperienceParty(Scriptable *Sender, Action* parameters);
	static void AddExperiencePartyGlobal(Scriptable *Sender, Action* parameters);
	static void AddGlobals(Scriptable* Sender, Action* parameters);
	static void AddWayPoint(Scriptable* Sender, Action* parameters);
	static void AddXP2DA(Scriptable *Sender, Action* parameters);
	static void AddXPObject(Scriptable *Sender, Action* parameters);
	static void Ally(Scriptable* Sender, Action* parameters);
	static void AmbientActivate(Scriptable* Sender, Action* parameters);
	static void BitClear(Scriptable* Sender, Action* parameters);
	static void CloseDoor(Scriptable* Sender, Action* parameters);
	static void CreateCreature(Scriptable* Sender, Action* parameters);
	static void CreateCreatureAtLocation(Scriptable* Sender, Action* parameters);
	static void CreateCreatureObject(Scriptable* Sender, Action* parameters);
	static void CreateCreatureObjectOffset(Scriptable* Sender, Action* parameters);
	static void CreateCreatureOffset(Scriptable* Sender, Action* parameters);
	static void CreatePartyGold(Scriptable *Sender, Action *parameters);
	static void ChangeAIScript(Scriptable* Sender, Action* parameters);
	static void ChangeAlignment(Scriptable* Sender, Action* parameters);
	static void ChangeAllegiance(Scriptable* Sender, Action* parameters);
	static void ChangeClass(Scriptable* Sender, Action* parameters);
	static void ChangeGender(Scriptable* Sender, Action* parameters);
	static void ChangeGeneral(Scriptable* Sender, Action* parameters);
	static void ChangeRace(Scriptable* Sender, Action* parameters);
	static void ChangeSpecifics(Scriptable* Sender, Action* parameters);
	static void ChangeStat(Scriptable* Sender, Action* parameters);
	static void ClearActions(Scriptable* Sender, Action* parameters);
	static void ClearAllActions(Scriptable* Sender, Action* parameters);
	static void Continue(Scriptable* Sender, Action* parameters);
	static void CreateVisualEffect(Scriptable* Sender, Action* parameters);
	static void CreateVisualEffectObject(Scriptable* Sender,
		Action* parameters);
	static void CutSceneID(Scriptable* Sender, Action* parameters);
	static void Deactivate(Scriptable* Sender, Action* parameters);
	static void DestroyPartyGold(Scriptable* Sender, Action* parameters);
	static void DestroySelf(Scriptable* Sender, Action* parameters);
	static void Dialogue(Scriptable* Sender, Action* parameters);
	static void DialogueForceInterrupt(Scriptable* Sender, Action* parameters);
	static void DisplayString(Scriptable* Sender, Action* parameters);
	static void DisplayStringHead(Scriptable* Sender, Action* parameters);
	static void DisplayStringNoNameHead(Scriptable* Sender, Action* parameters);
	static void DisplayStringWait(Scriptable* Sender, Action* parameters);
	static void EndCutSceneMode(Scriptable* Sender, Action* parameters);
	static void Enemy(Scriptable* Sender, Action* parameters);
	static void Face(Scriptable* Sender, Action* parameters);
	static void FaceObject(Scriptable* Sender, Action* parameters);
	static void FadeFromColor(Scriptable* Sender, Action* parameters);
	static void FadeToColor(Scriptable* Sender, Action* parameters);
	static void ForceAIScript(Scriptable* Sender, Action* parameters);
	static void ForceSpell(Scriptable* Sender, Action* parameters);
	static void GivePartyGold(Scriptable* Sender, Action* parameters);
	static void GivePartyGoldGlobal(Scriptable* Sender, Action* parameters);
	static void GlobalAddGlobal(Scriptable* Sender, Action* parameters);
	static void GlobalAndGlobal(Scriptable* Sender, Action* parameters);
	static void GlobalBAnd(Scriptable* Sender, Action* parameters);
	static void GlobalBAndGlobal(Scriptable* Sender, Action* parameters);
	static void GlobalBOr(Scriptable* Sender, Action* parameters);
	static void GlobalBOrGlobal(Scriptable* Sender, Action* parameters);
	static void GlobalMax(Scriptable* Sender, Action* parameters);
	static void GlobalMaxGlobal(Scriptable* Sender, Action* parameters);
	static void GlobalMin(Scriptable* Sender, Action* parameters);
	static void GlobalMinGlobal(Scriptable* Sender, Action* parameters);
	static void GlobalOrGlobal(Scriptable* Sender, Action* parameters);
	static void GlobalSetGlobal(Scriptable* Sender, Action* parameters);
	static void GlobalShL(Scriptable* Sender, Action* parameters);
	static void GlobalShLGlobal(Scriptable* Sender, Action* parameters);
	static void GlobalShR(Scriptable* Sender, Action* parameters);
	static void GlobalShRGlobal(Scriptable* Sender, Action* parameters);
	static void GlobalSubGlobal(Scriptable* Sender, Action* parameters);
	static void GlobalXor(Scriptable* Sender, Action* parameters);
	static void GlobalXorGlobal(Scriptable* Sender, Action* parameters);
	static void HideGUI(Scriptable* Sender, Action* parameters);
	static void IncrementGlobal(Scriptable* Sender, Action* parameters);
	static void IncrementGlobalOnce(Scriptable* Sender, Action* parameters);
	static void JoinParty(Scriptable* Sender, Action* parameters);
	static void JumpToPoint(Scriptable* Sender, Action* parameters);
	static void JumpToPointInstant(Scriptable* Sender, Action* parameters);
	static void JumpToObject(Scriptable* Sender, Action* parameters);
	static void LeaveAreaLUA(Scriptable* Sender, Action* parameters);
	static void LeaveAreaLUAPanic(Scriptable* Sender, Action* parameters);
	static void LeaveParty(Scriptable* Sender, Action* parameters);
	static void Lock(Scriptable* Sender, Action* parameters);
	static void MakeGlobal(Scriptable* Sender, Action* parameters);
	static void MoraleDec(Scriptable* Sender, Action* parameters);
	static void MoraleInc(Scriptable* Sender, Action* parameters);
	static void MoraleSet(Scriptable* Sender, Action* parameters);
	static void MoveBetweenAreas(Scriptable* Sender, Action* parameters);
	static void MoveToPoint(Scriptable* Sender, Action* parameters);
	static void MoveToObject(Scriptable* Sender, Action* parameters);
	static void MoveToOffset(Scriptable* Sender, Action* parameters);
	static void MoveViewPoint(Scriptable* Sender, Action* parameters);
	static void MoveViewObject(Scriptable* Sender, Action* parameters);
	static void NoAction(Scriptable* Sender, Action* parameters);
	static void OpenDoor(Scriptable* Sender, Action* parameters);
	static void PlayDead(Scriptable* Sender, Action* parameters);
	static void PlayerDialogue(Scriptable* Sender, Action* parameters);
	static void PlaySequence(Scriptable* Sender, Action* parameters);
	static void PlaySound(Scriptable* Sender, Action* parameters);
	static void SaveLocation(Scriptable* Sender, Action* parameters);
	static void Recoil(Scriptable* Sender, Action* parameters);
	static void RemoveAreaFlag(Scriptable* Sender, Action* parameters);
	static void RemoveAreaType(Scriptable* Sender, Action* parameters);
	static void RunAwayFrom(Scriptable* Sender, Action* parameters);
	static void RunAwayFromNoInterrupt(Scriptable* Sender, Action* parameters);
	static void SaveObjectLocation(Scriptable* Sender, Action* parameters);
	static void ScreenShake(Scriptable* Sender, Action* parameters);
	static void SetAnimState(Scriptable* Sender, Action* parameters);
	static void SetAreaRestFlag(Scriptable* Sender, Action* parameters);
	static void SetDialogue(Scriptable* Sender, Action* parameters);
	static void SetGlobal(Scriptable* Sender, Action* parameters);
	static void SetGlobalTimer(Scriptable* Sender, Action* parameters);
	static void SetLeavePartyDialogFile(Scriptable* Sender, Action* parameters);
	static void SetNumTimesTalkedTo(Scriptable* Sender, Action* parameters);
	static void SetPlayerSound(Scriptable* Sender, Action* parameters);
	static void SetTokenGlobal(Scriptable* Sender, Action* parameters);
	static void SG(Scriptable* Sender, Action* parameters);
	static void SmallWait(Scriptable* Sender, Action* parameters);
	static void StartCutSceneMode(Scriptable* Sender, Action* parameters);
	static void StartCutScene(Scriptable* Sender, Action* parameters);
	static void StartDialogue(Scriptable* Sender, Action* parameters);
	static void StartDialogueInterrupt(Scriptable* Sender, Action* parameters);
	static void StartDialogueNoSet(Scriptable* Sender, Action* parameters);
	static void StartDialogueNoSetInterrupt(Scriptable* Sender,
		Action* parameters);
	static void StartDialogueOverride(Scriptable* Sender, Action* parameters);
	static void StartDialogueOverrideInterrupt(Scriptable* Sender,
		Action* parameters);
	static void StartMovie(Scriptable* Sender, Action* parameters);
	static void StartSong(Scriptable* Sender, Action* parameters);
	static void Swing(Scriptable* Sender, Action* parameters);
	static void TakePartyGold(Scriptable* Sender, Action* parameters);
	static void TriggerActivation(Scriptable* Sender, Action* parameters);
	static void UnhideGUI(Scriptable* Sender, Action* parameters);
	static void Unlock(Scriptable* Sender, Action* parameters);
	static void VerbalConstant(Scriptable* Sender, Action* parameters);
	static void Wait(Scriptable* Sender, Action* parameters);
	static void WaitRandom(Scriptable* Sender, Action* parameters);
public:
	//Objects
	static Targets *BestAC(Scriptable *Sender, Targets *parameters);
	static Targets *EighthNearest(Scriptable *Sender, Targets *parameters);
	static Targets *EighthNearestEnemyOf(Scriptable *Sender, Targets *parameters);
	static Targets *FifthNearest(Scriptable *Sender, Targets *parameters);
	static Targets *FifthNearestEnemyOf(Scriptable *Sender, Targets *parameters);
	static Targets *FourthNearest(Scriptable *Sender, Targets *parameters);
	static Targets *FourthNearestEnemyOf(Scriptable *Sender, Targets *parameters);
	static Targets *Gabber(Scriptable *Sender, Targets *parameters);
	static Targets *LastSeenBy(Scriptable *Sender, Targets *parameters);
	static Targets *LastTalkedToBy(Scriptable *Sender, Targets *parameters);
	static Targets *Myself(Scriptable *Sender, Targets *parameters);
	static Targets *Nearest(Scriptable *Sender, Targets *parameters);
	static Targets *NearestEnemyOf(Scriptable *Sender, Targets *parameters);
	static Targets *NinthNearest(Scriptable *Sender, Targets *parameters);
	static Targets *NinthNearestEnemyOf(Scriptable *Sender, Targets *parameters);
	static Targets *Player1(Scriptable *Sender, Targets *parameters);
	static Targets *Player1Fill(Scriptable *Sender, Targets *parameters);
	static Targets *Player2(Scriptable *Sender, Targets *parameters);
	static Targets *Player2Fill(Scriptable *Sender, Targets *parameters);
	static Targets *Player3(Scriptable *Sender, Targets *parameters);
	static Targets *Player3Fill(Scriptable *Sender, Targets *parameters);
	static Targets *Player4(Scriptable *Sender, Targets *parameters);
	static Targets *Player4Fill(Scriptable *Sender, Targets *parameters);
	static Targets *Player5(Scriptable *Sender, Targets *parameters);
	static Targets *Player5Fill(Scriptable *Sender, Targets *parameters);
	static Targets *Player6(Scriptable *Sender, Targets *parameters);
	static Targets *Player6Fill(Scriptable *Sender, Targets *parameters);
	static Targets *Protagonist(Scriptable *Sender, Targets *parameters);
	static Targets *SecondNearest(Scriptable *Sender, Targets *parameters);
	static Targets *SecondNearestEnemyOf(Scriptable *Sender, Targets *parameters);
	static Targets *SeventhNearest(Scriptable *Sender, Targets *parameters);
	static Targets *SeventhNearestEnemyOf(Scriptable *Sender, Targets *parameters);
	static Targets *SixthNearest(Scriptable *Sender, Targets *parameters);
	static Targets *SixthNearestEnemyOf(Scriptable *Sender, Targets *parameters);
	static Targets *StrongestOf(Scriptable *Sender, Targets *parameters);
	static Targets *TenthNearest(Scriptable *Sender, Targets *parameters);
	static Targets *TenthNearestEnemyOf(Scriptable *Sender, Targets *parameters);
	static Targets *ThirdNearest(Scriptable *Sender, Targets *parameters);
	static Targets *ThirdNearestEnemyOf(Scriptable *Sender, Targets *parameters);
	static Targets *WeakestOf(Scriptable *Sender, Targets *parameters);
	static Targets *WorstAC(Scriptable *Sender, Targets *parameters);

public:
	/*GemRB extensions/actions*/
	static void RunAwayFromPoint(Scriptable* Sender, Action* parameters);
	static void UnMakeGlobal(Scriptable* Sender, Action* parameters);
	/*GemRB extensions/objects*/
	static Targets *Player7(Scriptable *Sender, Targets *parameters);
	static Targets *Player7Fill(Scriptable *Sender, Targets *parameters);
	static Targets *Player8(Scriptable *Sender, Targets *parameters);
	static Targets *Player8Fill(Scriptable *Sender, Targets *parameters);
};

#endif
