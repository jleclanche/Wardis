from struct import unpack_from, calcsize
from StringIO import StringIO
from constants import *
from binascii import hexlify
from operator import attrgetter
import re


def read_string(buf, offset=0):
	"""Read from string or StringIO buffer until EOF or a null char is encountered."""
	tmp = ""
	index = offset
	while True:
		if type(buf) in (str, unicode):
			c = buf[index]
		else:
			c = buf.read(1)

		if len(c) == 0:
			return tmp

		if c == chr(0):
			return tmp

		tmp += c
		index = index + 1


def unpack_buffer(format, buf):
	"""Wrapper for struct.unpack_from which can operate on StringIO buffers."""
	return unpack_from(format, buf.read(calcsize(format)))


class Message(object):
	"""Unknown Message"""
	def __repr__(self):
		if type(self) == Message:
			if len(self.data):
				return "<%s, Opcode = 0x%X, %d bytes data>" % (self.name, self.opcode, len(self.data))
			else:
				return "<%s, Opcode = 0x%X>" % (self.name, self.opcode)
		else:
			if len(self.data):
				return "<%s, %d bytes data>" % (self.name, len(self.data))
			else:
				return "<%s>" % (self.name)

	def unpack(self, format, offset=0):
		"""Shortcut for struct.unpack() which uses the message data in little endian order"""
		unpack_result = unpack_from("<" + format, self.data, offset)

		if len(unpack_result) == 1:
			return unpack_result[0]
		else:
			return unpack_result

	def getdata(self):
		return self._data

	def setdata(self, newval):
		self._data = newval
		self.setdata_hook(newval)

	def setdata_hook(self, newval):
		"""Function that can be hooked to watch for new data."""
		pass

	data = property(getdata, setdata, doc="Raw data")

	@property
	def name(self):
		if type(self).__doc__:
			return type(self).__doc__.partition("\n")[0]
		else:
			return " ".join(match.group(1) for match in re.finditer("([A-Z][a-z]+|[UCS]MSG|PVP|GUID|[A-Z]+(?![a-z]))", type(self).__name__))

	@property
	def opcode(self):
		"""Unrecognized opcode

		This opcode has no meaning associated with it in the code."""
		return self._opcode

	def __unicode__(self):
		return hexlify(self.data)


class MSGNullAction(Message):
	opcode = 0x0

class CMSGBootMe(Message):
	opcode = 0x1

class CMSGDbLookup(Message):
	opcode = 0x2

class SMSGDbLookup(Message):
	opcode = 0x3

class CMSGQueryObjectPosition(Message):
	opcode = 0x4

class SMSGQueryObjectPosition(Message):
	opcode = 0x5

class CMSGQueryObjectRotation(Message):
	opcode = 0x6

class SMSGQueryObjectRotation(Message):
	opcode = 0x7

class CMSGWorldTeleport(Message):
	opcode = 0x8

class CMSGTeleportToUnit(Message):
	opcode = 0x9

class CMSGZoneMap(Message):
	opcode = 0xA

class SMSGZoneMap(Message):
	opcode = 0xB

class CMSGDebugChangeCellZone(Message):
	opcode = 0xC

class CMSGEmblazonTabardObsolete(Message):
	opcode = 0xD

class CMSGUnemblazonTabardObsolete(Message):
	opcode = 0xE

class CMSGRecharge(Message):
	opcode = 0xF

class CMSGLearnSpell(Message):
	opcode = 0x10

class CMSGCreateMonster(Message):
	opcode = 0x11

class CMSGDestroyMonster(Message):
	opcode = 0x12

class CMSGCreateItem(Message):
	opcode = 0x13

class CMSGCreateGameObject(Message):
	opcode = 0x14

class SMSGCheckForBots(Message):
	opcode = 0x15

class CMSGMakeMonsterAttackGUID(Message):
	opcode = 0x16

class CMSGBotDetected2(Message):
	opcode = 0x17

class CMSGForceAction(Message):
	opcode = 0x18

class CMSGForceActionOnOther(Message):
	opcode = 0x19

class CMSGForceActionShow(Message):
	opcode = 0x1A

class SMSGForceActionShow(Message):
	opcode = 0x1B

class CMSGPetGodMode(Message):
	opcode = 0x1C

class SMSGPetGodMode(Message):
	opcode = 0x1D

class SMSGDebugInfoSpellMissObsolete(Message):
	opcode = 0x1E

class CMSGWeatherSpeedCheat(Message):
	opcode = 0x1F

class CMSGUndressPlayer(Message):
	opcode = 0x20

class CMSGBeastMaster(Message):
	opcode = 0x21

class CMSGGodMode(Message):
	opcode = 0x22

class SMSGGodMode(Message):
	opcode = 0x23

class CMSGCheatSetmoney(Message):
	opcode = 0x24

class CMSGLevelCheat(Message):
	opcode = 0x25

class CMSGPetLevelCheat(Message):
	opcode = 0x26

class CMSGSetWorldstate(Message):
	opcode = 0x27

class CMSGCooldownCheat(Message):
	opcode = 0x28

class CMSGUseSkillCheat(Message):
	opcode = 0x29

class CMSGFlagQuest(Message):
	opcode = 0x2A

class CMSGFlagQuestFinish(Message):
	opcode = 0x2B

class CMSGClearQuest(Message):
	opcode = 0x2C

class CMSGSendEvent(Message):
	opcode = 0x2D

class CMSGDebugAIState(Message):
	opcode = 0x2E

class SMSGDebugAIState(Message):
	opcode = 0x2F

class CMSGDisablePVPCheat(Message):
	opcode = 0x30

class CMSGAdvanceSpawnTime(Message):
	opcode = 0x31

class CMSGPVPPortObsolete(Message):
	opcode = 0x32

class CMSGAuthSRP6Begin(Message):
	opcode = 0x33

class CMSGAuthSRP6Proof(Message):
	opcode = 0x34

class CMSGAuthSRP6Recode(Message):
	opcode = 0x35

class CMSGCharCreate(Message):
	opcode = 0x36

class CMSGCharEnum(Message):
	"""Enumerate Characters (Request)

	Requests the character list."""
	opcode = 0x37

class CMSGCharDelete(Message):
	opcode = 0x38

class SMSGAuthSRP6Response(Message):
	opcode = 0x39

class SMSGCharCreate(Message):
	opcode = 0x3A

class SMSGCharEnum(Message):
	"""Enumerate Characters (Response)

	Character list response."""
	opcode = 0x3B

	class Character(object):
		def __init__(self, buf):
			self._guid, = unpack_buffer("<Q", buf)
			self._name = read_string(buf)
			self._race, = unpack_buffer("B", buf)
			self._class, = unpack_buffer("B", buf)
			self._gender, = unpack_buffer("B", buf)
			buf.read(5)
			self._level, = unpack_buffer("B", buf)
			self._zoneID, = unpack_buffer("<L", buf)
			self._mapID, = unpack_buffer("<L", buf)
			self._x, self._y, self._z = unpack_buffer("<fff", buf)
			self._guildID, = unpack_buffer("<L", buf)
			self._flags, = unpack_buffer("<L", buf)
			buf.read(5)
			self._petDisplayID, = unpack_buffer("<L", buf)
			self._petLevel, = unpack_buffer("<L", buf)
			self._petFamily, = unpack_buffer("<L", buf)
			buf.read(20*9)

		def __unicode__(self):
			return "<%s, Level %d %s %s>" % (self.name, self.level, self.race, self.character_class)

		@property
		def guid(self):
			"""GUID"""
			return self._guid

		name = property(attrgetter("_name"))

		@property
		def race(self):
			return player_races[self._race]

		@property
		def character_class(self):
			"""Character Class"""
			return player_classes[self._class]

		@property
		def gender(self):
			return genders[self._gender]

		level = property(attrgetter("_level"))
		zoneID = property(attrgetter("_zoneID"), doc="Zone ID")
		mapID = property(attrgetter("_mapID"), doc="Map ID")

		@property
		def coordinates(self):
			"""Coordinates"""
			return {"X": self._x, "Y": self._y, "Z": self._z}

		guildID = property(attrgetter("_guildID"), doc="Guild ID")
		flags = property(attrgetter("_flags"), doc="Flags")

		@property
		def pet(self):
			"""Pet"""
			return {"Display ID": self._petDisplayID, "Level": self._petLevel, "Family": self._petFamily}

	@property
	def character_count(self):
		"""Character count"""
		return self.unpack("B")

	def __iter__(self):
		buf = StringIO(self.data)
		buf.read(1)
		for i in range(0, self.character_count):
			yield SMSGCharEnum.Character(buf)

class SMSGCharDelete(Message):
	opcode = 0x3C

class CMSGPlayerLogin(Message):
	opcode = 0x3D

class SMSGNewWorld(Message):
	opcode = 0x3E

class SMSGTransferPending(Message):
	opcode = 0x3F

class SMSGTransferAborted(Message):
	opcode = 0x40

class SMSGCharacterLoginFailed(Message):
	opcode = 0x41

class SMSGLoginSetTimeSpeed(Message):
	opcode = 0x42

class SMSGGameTimeUpdate(Message):
	opcode = 0x43

class CMSGGameTimeSet(Message):
	opcode = 0x44

class SMSGGameTimeSet(Message):
	opcode = 0x45

class CMSGGameSpeedSet(Message):
	opcode = 0x46

class SMSGGameSpeedSet(Message):
	opcode = 0x47

class CMSGServerTime(Message):
	opcode = 0x48

class SMSGServerTime(Message):
	opcode = 0x49

class CMSGPlayerLogout(Message):
	opcode = 0x4A

class CMSGLogoutRequest(Message):
	opcode = 0x4B

class SMSGLogoutResponse(Message):
	opcode = 0x4C

class SMSGLogoutComplete(Message):
	opcode = 0x4D

class CMSGLogoutCancel(Message):
	opcode = 0x4E

class SMSGLogoutCancelAck(Message):
	opcode = 0x4F

class CMSGNameQuery(Message):
	"""Name Query (Request)

	Asks the server to resolve a GUID to a name."""
	opcode = 0x50

	@property
	def guid(self):
		"""GUID"""
		return self.unpack("Q")

class SMSGNameQueryResponse(Message):
	"""Name Query (Response)

	Maps a GUID to a name and other data"""
	opcode = 0x51

	def setdata_hook(self, data):
		buf = StringIO(data)
		self._guid, = unpack_buffer("<Q", buf)
		self._character_name = unicode(read_string(buf), "utf-8")
		self._realm = unicode(read_string(buf), "utf-8")
		self._race, self._gender, self._class = unpack_buffer("<3L", buf)

	guid = property(attrgetter("_guid"), doc="GUID")
	character_name = property(attrgetter("_character_name"), doc="Character Name")

	@property
	def realm(self):
		"""Realm Name

		Used in the case of cross-realm battlegrounds."""
		return self._realm

	@property
	def race(self):
		"""Race"""
		return player_races[self._race]

	@property
	def gender(self):
		"""Gender"""
		return genders[self._gender]

	@property
	def character_class(self):
		"""Class"""
		return player_classes[self._class]

class CMSGPetNameQuery(Message):
	opcode = 0x52

class SMSGPetNameQueryResponse(Message):
	opcode = 0x53

class CMSGGuildQuery(Message):
	opcode = 0x54

class SMSGGuildQueryResponse(Message):
	opcode = 0x55

class CMSGItemQuerySingle(Message):
	opcode = 0x56

class CMSGItemQueryMultiple(Message):
	opcode = 0x57

class SMSGItemQuerySingleResponse(Message):
	opcode = 0x58

class SMSGItemQueryMultipleResponse(Message):
	opcode = 0x59

class CMSGPageTextQuery(Message):
	opcode = 0x5A

class SMSGPageTextQueryResponse(Message):
	opcode = 0x5B

class CMSGQuestQuery(Message):
	opcode = 0x5C

class SMSGQuestQueryResponse(Message):
	opcode = 0x5D

class CMSGGameObjectQuery(Message):
	opcode = 0x5E

class SMSGGameObjectQueryResponse(Message):
	opcode = 0x5F

class CMSGCreatureQuery(Message):
	opcode = 0x60

class SMSGCreatureQueryResponse(Message):
	opcode = 0x61

class CMSGWho(Message):
	opcode = 0x62

class SMSGWho(Message):
	opcode = 0x63

class CMSGWhois(Message):
	opcode = 0x64

class SMSGWhois(Message):
	opcode = 0x65

class CMSGContactList(Message):
	opcode = 0x66

class SMSGContactList(Message):
	opcode = 0x67

class SMSGFriendStatus(Message):
	opcode = 0x68

class CMSGAddFriend(Message):
	opcode = 0x69

class CMSGDelFriend(Message):
	opcode = 0x6A

class CMSGSetContactNotes(Message):
	opcode = 0x6B

class CMSGAddIgnore(Message):
	opcode = 0x6C

class CMSGDelIgnore(Message):
	opcode = 0x6D

class CMSGGroupInvite(Message):
	opcode = 0x6E

class SMSGGroupInvite(Message):
	opcode = 0x6F

class CMSGGroupCancel(Message):
	opcode = 0x70

class SMSGGroupCancel(Message):
	opcode = 0x71

class CMSGGroupAccept(Message):
	opcode = 0x72

class CMSGGroupDecline(Message):
	opcode = 0x73

class SMSGGroupDecline(Message):
	opcode = 0x74

class CMSGGroupUnInvite(Message):
	opcode = 0x75

class CMSGGroupUnInviteGUID(Message):
	opcode = 0x76

class SMSGGroupUnInvite(Message):
	opcode = 0x77

class CMSGGroupSetLeader(Message):
	opcode = 0x78

class SMSGGroupSetLeader(Message):
	opcode = 0x79

class CMSGLootMethod(Message):
	opcode = 0x7A

class CMSGGroupDisband(Message):
	opcode = 0x7B

class SMSGGroupDestroyed(Message):
	opcode = 0x7C

class SMSGGroupList(Message):
	opcode = 0x7D

class SMSGPartyMemberStats(Message):
	opcode = 0x7E

class SMSGPartyCommandResult(Message):
	opcode = 0x7F

class UMSGUpdateGroupMembers(Message):
	opcode = 0x80

class CMSGGuildCreate(Message):
	opcode = 0x81

class CMSGGuildInvite(Message):
	opcode = 0x82

class SMSGGuildInvite(Message):
	opcode = 0x83

class CMSGGuildAccept(Message):
	opcode = 0x84

class CMSGGuildDecline(Message):
	opcode = 0x85

class SMSGGuildDecline(Message):
	opcode = 0x86

class CMSGGuildInfo(Message):
	opcode = 0x87

class SMSGGuildInfo(Message):
	opcode = 0x88

class CMSGGuildRoster(Message):
	opcode = 0x89

class SMSGGuildRoster(Message):
	opcode = 0x8A

class CMSGGuildPromote(Message):
	opcode = 0x8B

class CMSGGuildDemote(Message):
	opcode = 0x8C

class CMSGGuildLeave(Message):
	opcode = 0x8D

class CMSGGuildRemove(Message):
	opcode = 0x8E

class CMSGGuildDisband(Message):
	opcode = 0x8F

class CMSGGuildLeader(Message):
	opcode = 0x90

class CMSGGuildMotd(Message):
	opcode = 0x91

class SMSGGuildEvent(Message):
	opcode = 0x92

class SMSGGuildCommandResult(Message):
	opcode = 0x93

class UMSGUpdateGuild(Message):
	opcode = 0x94

class CMSGChatMessage(Message):
	"""Chat Message Sent

	The client wants to send a chat message."""
	opcode = 0x95

	def setdata_hook(self, data):
		buf = StringIO(data)
		self._type, self._language = unpack_buffer("<LL", buf)

		if self._type in (0x07, 0x11): # whisper or channel
			self._recipient = unicode(read_string(buf), "utf-8")

		self._text = unicode(read_string(buf), "utf-8")

	@property
	def message_type(self):
		"""Message Type"""
		return message_types[self._type]

	@property
	def language(self):
		return languages[self._language]

	@property
	def recipient(self):
		if hasattr(self, "_recipient"):
			return self._recipient

	def __unicode__(self):
		return self._text

class SMSGChatMessage(Message):
	"""Chat Message Received/Ack

	The server has sent a new message for the client or acknowledged the
	client's request to send."""
	opcode = 0x96

	def setdata_hook(self, data):
		buf = StringIO(data)
		self._type, self._language = unpack_buffer("<BL", buf)

		self._guid1, = unpack_buffer("<Q", buf)
		buf.read(4)

		if self._type in range(0x0c, 0x10) or self._type in (0x29, 0x2a):
			name_length, = unpack_buffer("<L", buf)
			self._npc_name = unicode(buf.read(name_length), "utf-8")

		self._guid2, = unpack_buffer("<Q", buf)
		length, = unpack_buffer("<L", buf)
		self._text = unicode(buf.read(length-1), "utf-8")
		self._flags, = unpack_buffer("B", buf)

	@property
	def message_type(self):
		"""Message Type"""
		return message_types[self._type]

	@property
	def language(self):
		return languages[self._language]

	guid1 = property(attrgetter("_guid1"), doc="GUID 1")
	guid2 = property(attrgetter("_guid2"), doc="GUID 2")

	def __unicode__(self):
		return self._text

	@property
	def npc_name(self):
		if hasattr(self, "_npc_name"):
			return self._npc_name

	@property
	def flags(self):
		return { "AFK": self._flags & 0x1>0, "DND": self._flags & 0x2>0, "GM": self._flags & 0x4>0 }

class CMSGJoinChannel(Message):
	opcode = 0x97

class CMSGLeaveChannel(Message):
	opcode = 0x98

class SMSGChannelNotify(Message):
	opcode = 0x99

class CMSGChannelList(Message):
	opcode = 0x9A

class SMSGChannelList(Message):
	opcode = 0x9B

class CMSGChannelPassword(Message):
	opcode = 0x9C

class CMSGChannelSetOwner(Message):
	opcode = 0x9D

class CMSGChannelOwner(Message):
	opcode = 0x9E

class CMSGChannelModerator(Message):
	opcode = 0x9F

class CMSGChannelUnModerator(Message):
	opcode = 0xA0

class CMSGChannelMute(Message):
	opcode = 0xA1

class CMSGChannelUnmute(Message):
	opcode = 0xA2

class CMSGChannelInvite(Message):
	opcode = 0xA3

class CMSGChannelKick(Message):
	opcode = 0xA4

class CMSGChannelBan(Message):
	opcode = 0xA5

class CMSGChannelUnban(Message):
	opcode = 0xA6

class CMSGChannelAnnouncements(Message):
	opcode = 0xA7

class CMSGChannelModerate(Message):
	opcode = 0xA8

class SMSGUpdateObject(Message):
	opcode = 0xA9

class SMSGDestroyObject(Message):
	opcode = 0xAA

class CMSGUseItem(Message):
	opcode = 0xAB

class CMSGOpenItem(Message):
	opcode = 0xAC

class CMSGReadItem(Message):
	opcode = 0xAD

class SMSGReadItemOk(Message):
	opcode = 0xAE

class SMSGReadItemFailed(Message):
	opcode = 0xAF

class SMSGItemCooldown(Message):
	opcode = 0xB0

class CMSGGameObjectUse(Message):
	opcode = 0xB1

class CMSGGameObjectChairUseObsolete(Message):
	opcode = 0xB2

class SMSGGameObjectCustomAnim(Message):
	opcode = 0xB3

class CMSGAreaTrigger(Message):
	opcode = 0xB4

class MSGMoveStartForward(Message):
	opcode = 0xB5

class MSGMoveStartBackward(Message):
	opcode = 0xB6

class MSGMoveStop(Message):
	opcode = 0xB7

class MSGMoveStartStrafeLeft(Message):
	opcode = 0xB8

class MSGMoveStartStrafeRight(Message):
	opcode = 0xB9

class MSGMoveStopStrafe(Message):
	opcode = 0xBA

class MSGMoveJump(Message):
	opcode = 0xBB

class MSGMoveStartTurnLeft(Message):
	opcode = 0xBC

class MSGMoveStartTurnRight(Message):
	opcode = 0xBD

class MSGMoveStopTurn(Message):
	opcode = 0xBE

class MSGMoveStartPitchUp(Message):
	opcode = 0xBF

class MSGMoveStartPitchDown(Message):
	opcode = 0xC0

class MSGMoveStopPitch(Message):
	opcode = 0xC1

class MSGMoveSetRunMode(Message):
	opcode = 0xC2

class MSGMoveSetWalkMode(Message):
	opcode = 0xC3

class MSGMoveToggleLogging(Message):
	opcode = 0xC4

class MSGMoveTeleport(Message):
	opcode = 0xC5

class MSGMoveTeleportCheat(Message):
	opcode = 0xC6

class MSGMoveTeleportAck(Message):
	opcode = 0xC7

class MSGMoveToggleFallLogging(Message):
	opcode = 0xC8

class MSGMoveFallLand(Message):
	opcode = 0xC9

class MSGMoveStartSwim(Message):
	opcode = 0xCA

class MSGMoveStopSwim(Message):
	opcode = 0xCB

class MSGMoveSetRunSpeedCheat(Message):
	opcode = 0xCC

class MSGMoveSetRunSpeed(Message):
	opcode = 0xCD

class MSGMoveSetRunBackSpeedCheat(Message):
	opcode = 0xCE

class MSGMoveSetRunBackSpeed(Message):
	opcode = 0xCF

class MSGMoveSetWalkSpeedCheat(Message):
	opcode = 0xD0

class MSGMoveSetWalkSpeed(Message):
	opcode = 0xD1

class MSGMoveSetSwimSpeedCheat(Message):
	opcode = 0xD2

class MSGMoveSetSwimSpeed(Message):
	opcode = 0xD3

class MSGMoveSetSwimBackSpeedCheat(Message):
	opcode = 0xD4

class MSGMoveSetSwimBackSpeed(Message):
	opcode = 0xD5

class MSGMoveSetAllSpeedCheat(Message):
	opcode = 0xD6

class MSGMoveSetTurnRateCheat(Message):
	opcode = 0xD7

class MSGMoveSetTurnRate(Message):
	opcode = 0xD8

class MSGMoveToggleCollisionCheat(Message):
	opcode = 0xD9

class MSGMoveSetFacing(Message):
	opcode = 0xDA

class MSGMoveSetPitch(Message):
	opcode = 0xDB

class MSGMoveWorldportAck(Message):
	opcode = 0xDC

class SMSGMonsterMove(Message):
	opcode = 0xDD

class SMSGMoveWaterWalk(Message):
	opcode = 0xDE

class SMSGMoveLandWalk(Message):
	opcode = 0xDF

class MSGMoveSetRawPositionAck(Message):
	opcode = 0xE0

class CMSGMoveSetRawPosition(Message):
	opcode = 0xE1

class SMSGForceRunSpeedChange(Message):
	opcode = 0xE2

class CMSGForceRunSpeedChangeAck(Message):
	opcode = 0xE3

class SMSGForceRunBackSpeedChange(Message):
	opcode = 0xE4

class CMSGForceRunBackSpeedChangeAck(Message):
	opcode = 0xE5

class SMSGForceSwimSpeedChange(Message):
	opcode = 0xE6

class CMSGForceSwimSpeedChangeAck(Message):
	opcode = 0xE7

class SMSGForceMoveRoot(Message):
	opcode = 0xE8

class CMSGForceMoveRootAck(Message):
	opcode = 0xE9

class SMSGForceMoveUnroot(Message):
	opcode = 0xEA

class CMSGForceMoveUnrootAck(Message):
	opcode = 0xEB

class MSGMoveRoot(Message):
	opcode = 0xEC

class MSGMoveUnroot(Message):
	opcode = 0xED

class MSGMoveHeartbeat(Message):
	opcode = 0xEE

class SMSGMoveKnockBack(Message):
	opcode = 0xEF

class CMSGMoveKnockBackAck(Message):
	opcode = 0xF0

class MSGMoveKnockBack(Message):
	opcode = 0xF1

class SMSGMoveFeatherFall(Message):
	opcode = 0xF2

class SMSGMoveNormalFall(Message):
	opcode = 0xF3

class SMSGMoveSetHover(Message):
	opcode = 0xF4

class SMSGMoveUnsetHover(Message):
	opcode = 0xF5

class CMSGMoveHoverAck(Message):
	opcode = 0xF6

class MSGMoveHover(Message):
	opcode = 0xF7

class CMSGTriggerCinematicCheat(Message):
	opcode = 0xF8

class CMSGOpeningCinematic(Message):
	opcode = 0xF9

class SMSGTriggerCinematic(Message):
	opcode = 0xFA

class CMSGNextCinematicCamera(Message):
	opcode = 0xFB

class CMSGCompleteCinematic(Message):
	opcode = 0xFC

class SMSGTutorialFlags(Message):
	opcode = 0xFD

class CMSGTutorialFlag(Message):
	opcode = 0xFE

class CMSGTutorialClear(Message):
	opcode = 0xFF

class CMSGTutorialReset(Message):
	opcode = 0x100

class CMSGStandstatechange(Message):
	opcode = 0x101

class CMSGEmote(Message):
	opcode = 0x102

class SMSGEmote(Message):
	opcode = 0x103

class CMSGTextEmote(Message):
	opcode = 0x104

class SMSGTextEmote(Message):
	opcode = 0x105

class CMSGAutoEquipGroundItem(Message):
	opcode = 0x106

class CMSGAutoStoreGroundItem(Message):
	opcode = 0x107

class CMSGAutoStoreLootItem(Message):
	opcode = 0x108

class CMSGStoreLootInSlot(Message):
	opcode = 0x109

class CMSGAutoEquipItem(Message):
	opcode = 0x10A

class CMSGAutoStoreBagItem(Message):
	opcode = 0x10B

class CMSGSwapItem(Message):
	opcode = 0x10C

class CMSGSwapInvItem(Message):
	opcode = 0x10D

class CMSGSplitItem(Message):
	opcode = 0x10E

class CMSGAutoEquipItemSlot(Message):
	opcode = 0x10F

class CMSGDestroyItem(Message):
	opcode = 0x111

class SMSGInventoryChangeFailure(Message):
	opcode = 0x112

class SMSGOpenContainer(Message):
	opcode = 0x113

class CMSGInspect(Message):
	opcode = 0x114

class SMSGInspect(Message):
	opcode = 0x115

class CMSGInitiateTrade(Message):
	opcode = 0x116

class CMSGBeginTrade(Message):
	opcode = 0x117

class CMSGBusyTrade(Message):
	opcode = 0x118

class CMSGIgnoreTrade(Message):
	opcode = 0x119

class CMSGAcceptTrade(Message):
	opcode = 0x11A

class CMSGUnacceptTrade(Message):
	opcode = 0x11B

class CMSGCancelTrade(Message):
	opcode = 0x11C

class CMSGSetTradeItem(Message):
	opcode = 0x11D

class CMSGClearTradeItem(Message):
	opcode = 0x11E

class CMSGSetTradeGold(Message):
	opcode = 0x11F

class SMSGTradeStatus(Message):
	opcode = 0x120

class SMSGTradeStatusExtended(Message):
	opcode = 0x121

class SMSGInitializeFactions(Message):
	opcode = 0x122

class SMSGSetFactionVisible(Message):
	opcode = 0x123

class SMSGSetFactionStanding(Message):
	opcode = 0x124

class CMSGSetFactionAtwar(Message):
	opcode = 0x125

class CMSGSetFactionCheat(Message):
	opcode = 0x126

class SMSGSetProficiency(Message):
	opcode = 0x127

class CMSGSetActionButton(Message):
	opcode = 0x128

class SMSGActionButtons(Message):
	opcode = 0x129

class SMSGInitialSpells(Message):
	opcode = 0x12A

class SMSGLearnedSpell(Message):
	opcode = 0x12B

class SMSGSupercededSpell(Message):
	opcode = 0x12C

class CMSGNewSpellSlot(Message):
	opcode = 0x12D

class CMSGCastSpell(Message):
	opcode = 0x12E

class CMSGCancelCast(Message):
	opcode = 0x12F

class SMSGCastFailed(Message):
	opcode = 0x130

class SMSGSpellStart(Message):
	opcode = 0x131

class SMSGSpellGo(Message):
	opcode = 0x132

class SMSGSpellFailure(Message):
	opcode = 0x133

class SMSGSpellCooldown(Message):
	opcode = 0x134

class SMSGCooldownEvent(Message):
	opcode = 0x135

class CMSGCancelAura(Message):
	opcode = 0x136

class SMSGUpdateAuraDuration(Message):
	opcode = 0x137

class SMSGPetCastFailed(Message):
	opcode = 0x138

class MSGChannelStart(Message):
	opcode = 0x139

class MSGChannelUpdate(Message):
	opcode = 0x13A

class CMSGCancelChannelling(Message):
	opcode = 0x13B

class SMSGAIReaction(Message):
	opcode = 0x13C

class CMSGSetSelection(Message):
	opcode = 0x13D

class CMSGSetTargetObsolete(Message):
	opcode = 0x13E

class CMSGUnused(Message):
	opcode = 0x13F

class CMSGUnused2(Message):
	opcode = 0x140

class CMSGAttackSwing(Message):
	opcode = 0x141

class CMSGAttackStop(Message):
	opcode = 0x142

class SMSGAttackStart(Message):
	opcode = 0x143

class SMSGAttackStop(Message):
	opcode = 0x144

class SMSGAttackSwingNotInRange(Message):
	opcode = 0x145

class SMSGAttackSwingBadFacing(Message):
	opcode = 0x146

class SMSGAttackSwingNotStanding(Message):
	opcode = 0x147

class SMSGAttackSwingDeadTarget(Message):
	opcode = 0x148

class SMSGAttackSwingCantAttack(Message):
	opcode = 0x149

class SMSGAttackerStateUpdate(Message):
	opcode = 0x14A

class SMSGVictimStateUpdateObsolete(Message):
	opcode = 0x14B

class SMSGDamageDoneObsolete(Message):
	opcode = 0x14C

class SMSGDamageTakenObsolete(Message):
	opcode = 0x14D

class SMSGCancelCombat(Message):
	opcode = 0x14E

class SMSGPlayerCombatXPGainObsolete(Message):
	opcode = 0x14F

class SMSGSpellHealLog(Message):
	opcode = 0x150

class SMSGSpellEnergizeLog(Message):
	opcode = 0x151

class CMSGSheatheObsolete(Message):
	opcode = 0x152

class CMSGSavePlayer(Message):
	opcode = 0x153

class CMSGSetDeathBindPoint(Message):
	opcode = 0x154

class SMSGBindPointUpdate(Message):
	opcode = 0x155

class CMSGGetDeathBindZone(Message):
	opcode = 0x156

class SMSGBindZoneReply(Message):
	opcode = 0x157

class SMSGPlayerBound(Message):
	opcode = 0x158

class SMSGClientControlUpdate(Message):
	opcode = 0x159

class CMSGRepopRequest(Message):
	opcode = 0x15A

class SMSGResurrectRequest(Message):
	opcode = 0x15B

class CMSGResurrectResponse(Message):
	opcode = 0x15C

class CMSGLoot(Message):
	opcode = 0x15D

class CMSGLootMoney(Message):
	opcode = 0x15E

class CMSGLootRelease(Message):
	opcode = 0x15F

class SMSGLootResponse(Message):
	opcode = 0x160

class SMSGLootReleaseResponse(Message):
	opcode = 0x161

class SMSGLootRemoved(Message):
	opcode = 0x162

class SMSGLootMoneyNotify(Message):
	opcode = 0x163

class SMSGLootItemNotify(Message):
	opcode = 0x164

class SMSGLootClearMoney(Message):
	opcode = 0x165

class SMSGItemPushResult(Message):
	opcode = 0x166

class SMSGDuelRequested(Message):
	opcode = 0x167

class SMSGDuelOutOfBounds(Message):
	opcode = 0x168

class SMSGDuelInBounds(Message):
	opcode = 0x169

class SMSGDuelComplete(Message):
	opcode = 0x16A

class SMSGDuelWinner(Message):
	opcode = 0x16B

class CMSGDuelAccepted(Message):
	opcode = 0x16C

class CMSGDuelCancelled(Message):
	opcode = 0x16D

class SMSGMountResult(Message):
	opcode = 0x16E

class SMSGDismountResult(Message):
	opcode = 0x16F

class SMSGPureMountCancelledObsolete(Message):
	opcode = 0x170

class CMSGMountSpecialAnim(Message):
	opcode = 0x171

class SMSGMountSpecialAnim(Message):
	opcode = 0x172

class SMSGPetTameFailure(Message):
	opcode = 0x173

class CMSGPetSetAction(Message):
	opcode = 0x174

class CMSGPetAction(Message):
	opcode = 0x175

class CMSGPetAbandon(Message):
	opcode = 0x176

class CMSGPetRename(Message):
	opcode = 0x177

class SMSGPetNameInvalid(Message):
	opcode = 0x178

class SMSGPetSpells(Message):
	opcode = 0x179

class SMSGPetMode(Message):
	opcode = 0x17A

class CMSGGossipHello(Message):
	opcode = 0x17B

class CMSGGossipSelectOption(Message):
	opcode = 0x17C

class SMSGGossipMessage(Message):
	opcode = 0x17D

class SMSGGossipComplete(Message):
	opcode = 0x17E

class CMSGNPCTextQuery(Message):
	opcode = 0x17F

class SMSGNPCTextUpdate(Message):
	opcode = 0x180

class SMSGNPCWontTalk(Message):
	opcode = 0x181

class CMSGQuestGiverStatusQuery(Message):
	opcode = 0x182

class SMSGQuestGiverStatus(Message):
	opcode = 0x183

class CMSGQuestGiverHello(Message):
	opcode = 0x184

class SMSGQuestGiverQuestList(Message):
	opcode = 0x185

class CMSGQuestGiverQueryQuest(Message):
	opcode = 0x186

class CMSGQuestGiverQuestAutolaunch(Message):
	opcode = 0x187

class SMSGQuestGiverQuestDetails(Message):
	opcode = 0x188

class CMSGQuestGiverAcceptQuest(Message):
	opcode = 0x189

class CMSGQuestGiverCompleteQuest(Message):
	opcode = 0x18A

class SMSGQuestGiverRequestItems(Message):
	opcode = 0x18B

class CMSGQuestGiverRequestReward(Message):
	opcode = 0x18C

class SMSGQuestGiverOfferReward(Message):
	opcode = 0x18D

class CMSGQuestGiverChooseReward(Message):
	opcode = 0x18E

class SMSGQuestGiverQuestInvalid(Message):
	opcode = 0x18F

class CMSGQuestGiverCancel(Message):
	opcode = 0x190

class SMSGQuestGiverQuestComplete(Message):
	opcode = 0x191

class SMSGQuestGiverQuestFailed(Message):
	opcode = 0x192

class CMSGQuestLogSwapQuest(Message):
	opcode = 0x193

class CMSGQuestLogRemoveQuest(Message):
	opcode = 0x194

class SMSGQuestLogFull(Message):
	opcode = 0x195

class SMSGQuestUpdateFailed(Message):
	opcode = 0x196

class SMSGQuestUpdateFailedtimer(Message):
	opcode = 0x197

class SMSGQuestUpdateComplete(Message):
	opcode = 0x198

class SMSGQuestUpdateAddKill(Message):
	opcode = 0x199

class SMSGQuestUpdateAddItem(Message):
	opcode = 0x19A

class CMSGQuestConfirmAccept(Message):
	opcode = 0x19B

class SMSGQuestConfirmAccept(Message):
	opcode = 0x19C

class CMSGPushQuestToParty(Message):
	opcode = 0x19D

class CMSGListInventory(Message):
	opcode = 0x19E

class SMSGListInventory(Message):
	opcode = 0x19F

class CMSGSellItem(Message):
	opcode = 0x1A0

class SMSGSellItem(Message):
	opcode = 0x1A1

class CMSGBuyItem(Message):
	opcode = 0x1A2

class CMSGBuyItemInSlot(Message):
	opcode = 0x1A3

class SMSGBuyItem(Message):
	opcode = 0x1A4

class SMSGBuyFailed(Message):
	opcode = 0x1A5

class CMSGTaxiClearAllNodes(Message):
	opcode = 0x1A6

class CMSGTaxiEnableAllNodes(Message):
	opcode = 0x1A7

class CMSGTaxiShowNodes(Message):
	opcode = 0x1A8

class SMSGShowTaxiNodes(Message):
	opcode = 0x1A9

class CMSGTaxiNodeStatusQuery(Message):
	opcode = 0x1AA

class SMSGTaxiNodeStatus(Message):
	opcode = 0x1AB

class CMSGTaxiQueryAvailableNodes(Message):
	opcode = 0x1AC

class CMSGActivateTaxi(Message):
	opcode = 0x1AD

class SMSGActivateTaxiReply(Message):
	opcode = 0x1AE

class SMSGNewTaxiPath(Message):
	opcode = 0x1AF

class CMSGTrainerList(Message):
	opcode = 0x1B0

class SMSGTrainerList(Message):
	opcode = 0x1B1

class CMSGTrainerBuySpell(Message):
	opcode = 0x1B2

class SMSGTrainerBuySucceeded(Message):
	opcode = 0x1B3

class SMSGTrainerBuyFailed(Message):
	opcode = 0x1B4

class CMSGBinderActivate(Message):
	opcode = 0x1B5

class SMSGPlayerBindError(Message):
	opcode = 0x1B6

class CMSGBankerActivate(Message):
	opcode = 0x1B7

class SMSGShowBank(Message):
	opcode = 0x1B8

class CMSGBuyBankSlot(Message):
	opcode = 0x1B9

class SMSGBuyBankSlotResult(Message):
	opcode = 0x1BA

class CMSGPetitionShowList(Message):
	opcode = 0x1BB

class SMSGPetitionShowList(Message):
	opcode = 0x1BC

class CMSGPetitionBuy(Message):
	opcode = 0x1BD

class CMSGPetitionShowSignatures(Message):
	opcode = 0x1BE

class SMSGPetitionShowSignatures(Message):
	opcode = 0x1BF

class CMSGPetitionSign(Message):
	opcode = 0x1C0

class SMSGPetitionSignResults(Message):
	opcode = 0x1C1

class MSGPetitionDecline(Message):
	opcode = 0x1C2

class CMSGOfferPetition(Message):
	opcode = 0x1C3

class CMSGTurnInPetition(Message):
	opcode = 0x1C4

class SMSGTurnInPetitionResults(Message):
	opcode = 0x1C5

class CMSGPetitionQuery(Message):
	opcode = 0x1C6

class SMSGPetitionQueryResponse(Message):
	opcode = 0x1C7

class SMSGFishNotHooked(Message):
	opcode = 0x1C8

class SMSGFishEscaped(Message):
	opcode = 0x1C9

class CMSGBug(Message):
	opcode = 0x1CA

class SMSGNotification(Message):
	opcode = 0x1CB

class CMSGPlayedTime(Message):
	opcode = 0x1CC

class SMSGPlayedTime(Message):
	opcode = 0x1CD

class CMSGQueryTime(Message):
	opcode = 0x1CE

class SMSGQueryTimeResponse(Message):
	opcode = 0x1CF

class SMSGLogXPGain(Message):
	opcode = 0x1D0

class SMSGAuraCastLog(Message):
	opcode = 0x1D1

class CMSGReclaimCorpse(Message):
	opcode = 0x1D2

class CMSGWrapItem(Message):
	opcode = 0x1D3

class SMSGLevelUpInfo(Message):
	opcode = 0x1D4

class MSGMinimapPing(Message):
	opcode = 0x1D5

class SMSGResistLog(Message):
	opcode = 0x1D6

class SMSGEnchantmentLog(Message):
	opcode = 0x1D7

class CMSGSetSkillCheat(Message):
	opcode = 0x1D8

class SMSGStartMirrorTimer(Message):
	opcode = 0x1D9

class SMSGPauseMirrorTimer(Message):
	opcode = 0x1DA

class SMSGStopMirrorTimer(Message):
	opcode = 0x1DB

class CMSGPing(Message):
	opcode = 0x1DC

class SMSGPong(Message):
	opcode = 0x1DD

class SMSGClearCooldown(Message):
	opcode = 0x1DE

class SMSGGameObjectPageText(Message):
	opcode = 0x1DF

class CMSGSetSheathed(Message):
	opcode = 0x1E0

class SMSGCooldownCheat(Message):
	opcode = 0x1E1

class SMSGSpellDelayed(Message):
	opcode = 0x1E2

class CMSGPlayerMacroObsolete(Message):
	opcode = 0x1E3

class SMSGPlayerMacroObsolete(Message):
	opcode = 0x1E4

class CMSGGhost(Message):
	opcode = 0x1E5

class CMSGGMInvis(Message):
	opcode = 0x1E6

class SMSGInvalidPromotionCode(Message):
	opcode = 0x1E7

class MSGGMBindOther(Message):
	opcode = 0x1E8

class MSGGMSummon(Message):
	opcode = 0x1E9

class SMSGItemTimeUpdate(Message):
	opcode = 0x1EA

class SMSGItemEnchantTimeUpdate(Message):
	opcode = 0x1EB

class SMSGAuthChallenge(Message):
	"""Auth Challenge

	Asks the client to identify itself. Always the first packet exchanged in a
	game connection."""
	opcode = 0x1EC

class CMSGAuthSession(Message):
	"""Auth Session

	Provides the server with identity information."""
	opcode = 0x1ED

	@property
	def client_build(self):
		"""Client Build"""
		return self.unpack("H", 0)

	@property
	def account_name(self):
		"""Account Name"""
		return read_string(self.data, 8)

class SMSGAuthResponse(Message):
	opcode = 0x1EE

class MSGGMShowlabel(Message):
	opcode = 0x1EF

class CMSGPetCastSpell(Message):
	opcode = 0x1F0

class MSGSaveGuildEmblem(Message):
	opcode = 0x1F1

class MSGTabardVendorActivate(Message):
	opcode = 0x1F2

class SMSGPlaySpellVisual(Message):
	opcode = 0x1F3

class CMSGZoneUpdate(Message):
	opcode = 0x1F4

class SMSGPartyKillLog(Message):
	opcode = 0x1F5

class SMSGCompressedUpdateObject(Message):
	opcode = 0x1F6

class SMSGPlaySpellImpact(Message):
	opcode = 0x1F7

class SMSGExplorationExperience(Message):
	opcode = 0x1F8

class CMSGGMSetSecurityGroup(Message):
	opcode = 0x1F9

class CMSGGMNuke(Message):
	opcode = 0x1FA

class MSGRandomRoll(Message):
	opcode = 0x1FB

class SMSGEnvironmentaldamagelog(Message):
	opcode = 0x1FC

class CMSGRWhoisObsolete(Message):
	opcode = 0x1FD

class SMSGRWhois(Message):
	opcode = 0x1FE

class MSGLookingForGroup(Message):
	opcode = 0x1FF

class CMSGSetLookingForGroup(Message):
	opcode = 0x200

class CMSGUnlearnSpell(Message):
	opcode = 0x201

class CMSGUnlearnSkill(Message):
	opcode = 0x202

class SMSGRemovedSpell(Message):
	opcode = 0x203

class CMSGDeCharge(Message):
	opcode = 0x204

class CMSGGMTicketCreate(Message):
	opcode = 0x205

class SMSGGMTicketCreate(Message):
	opcode = 0x206

class CMSGGMTicketUpdatetext(Message):
	opcode = 0x207

class SMSGGMTicketUpdatetext(Message):
	opcode = 0x208

class SMSGAccountDataTimes(Message):
	opcode = 0x209

class CMSGRequestAccountData(Message):
	opcode = 0x20A

class CMSGUpdateAccountData(Message):
	opcode = 0x20B

class SMSGUpdateAccountData(Message):
	opcode = 0x20C

class SMSGClearFarSightImmediate(Message):
	opcode = 0x20D

class SMSGPowerGainLogObsolete(Message):
	opcode = 0x20E

class CMSGGMTeach(Message):
	opcode = 0x20F

class CMSGGMCreateItemTarget(Message):
	opcode = 0x210

class CMSGGMTicketGetTicket(Message):
	opcode = 0x211

class SMSGGMTicketGetTicket(Message):
	opcode = 0x212

class CMSGUnlearnTalents(Message):
	opcode = 0x213

class SMSGGameObjectSpawnAnimObsolete(Message):
	opcode = 0x214

class SMSGGameObjectDespawnAnim(Message):
	opcode = 0x215

class MSGCorpseQuery(Message):
	opcode = 0x216

class CMSGGMTicketDeleteticket(Message):
	opcode = 0x217

class SMSGGMTicketDeleteticket(Message):
	opcode = 0x218

class SMSGChatWrongFaction(Message):
	opcode = 0x219

class CMSGGMTicketSystemStatus(Message):
	opcode = 0x21A

class SMSGGMTicketSystemStatus(Message):
	opcode = 0x21B

class CMSGSpiritHealerActivate(Message):
	opcode = 0x21C

class CMSGSetStatCheat(Message):
	opcode = 0x21D

class SMSGSetRestStart(Message):
	opcode = 0x21E

class CMSGSkillBuyStep(Message):
	opcode = 0x21F

class CMSGSkillBuyRank(Message):
	opcode = 0x220

class CMSGXPCheat(Message):
	opcode = 0x221

class SMSGSpiritHealerConfirm(Message):
	opcode = 0x222

class CMSGCharacterPointCheat(Message):
	opcode = 0x223

class SMSGGossipPOI(Message):
	opcode = 0x224

class CMSGChatIgnored(Message):
	opcode = 0x225

class CMSGGMVision(Message):
	opcode = 0x226

class CMSGServerCommand(Message):
	opcode = 0x227

class CMSGGMSilence(Message):
	opcode = 0x228

class CMSGGMRevealto(Message):
	opcode = 0x229

class CMSGGMResurrect(Message):
	opcode = 0x22A

class CMSGGMSummonMob(Message):
	opcode = 0x22B

class CMSGGMMoveCorpse(Message):
	opcode = 0x22C

class CMSGGMFreeze(Message):
	opcode = 0x22D

class CMSGGMUberInvis(Message):
	opcode = 0x22E

class CMSGGMRequestPlayerInfo(Message):
	opcode = 0x22F

class SMSGGMPlayerInfo(Message):
	opcode = 0x230

class CMSGGuildRank(Message):
	opcode = 0x231

class CMSGGuildAddRank(Message):
	opcode = 0x232

class CMSGGuildDelRank(Message):
	opcode = 0x233

class CMSGGuildSetPublicNote(Message):
	opcode = 0x234

class CMSGGuildSetOfficerNote(Message):
	opcode = 0x235

class SMSGLoginVerifyWorld(Message):
	opcode = 0x236

class CMSGClearExploration(Message):
	opcode = 0x237

class CMSGSendMail(Message):
	opcode = 0x238

class SMSGSendMailResult(Message):
	opcode = 0x239

class CMSGGetMailList(Message):
	opcode = 0x23A

class SMSGMailListResult(Message):
	opcode = 0x23B

class CMSGBattlefieldList(Message):
	opcode = 0x23C

class SMSGBattlefieldList(Message):
	opcode = 0x23D

class CMSGBattlefieldJoin(Message):
	opcode = 0x23E

class SMSGBattlefieldWinObsolete(Message):
	opcode = 0x23F

class SMSGBattlefieldLoseObsolete(Message):
	opcode = 0x240

class CMSGTaxiClearNode(Message):
	opcode = 0x241

class CMSGTaxiEnableNode(Message):
	opcode = 0x242

class CMSGItemTextQuery(Message):
	opcode = 0x243

class SMSGItemTextQueryResponse(Message):
	opcode = 0x244

class CMSGMailTakeMoney(Message):
	opcode = 0x245

class CMSGMailTakeItem(Message):
	opcode = 0x246

class CMSGMailMarkAsRead(Message):
	opcode = 0x247

class CMSGMailReturnToSender(Message):
	opcode = 0x248

class CMSGMailDelete(Message):
	opcode = 0x249

class CMSGMailCreateTextItem(Message):
	opcode = 0x24A

class SMSGSpellLogMiss(Message):
	opcode = 0x24B

class SMSGSpellLogExecute(Message):
	opcode = 0x24C

class SMSGDebugAuraProc(Message):
	opcode = 0x24D

class SMSGPeriodicAuraLog(Message):
	opcode = 0x24E

class SMSGSpellDamageShield(Message):
	opcode = 0x24F

class SMSGSpellNonMeleeDamageLog(Message):
	opcode = 0x250

class CMSGLearnTalent(Message):
	opcode = 0x251

class SMSGResurrectFailed(Message):
	opcode = 0x252

class CMSGTogglePVP(Message):
	opcode = 0x253

class SMSGZoneUnderAttack(Message):
	opcode = 0x254

class MSGAuctionHello(Message):
	opcode = 0x255

class CMSGAuctionSellItem(Message):
	opcode = 0x256

class CMSGAuctionRemoveItem(Message):
	opcode = 0x257

class CMSGAuctionListItems(Message):
	opcode = 0x258

class CMSGAuctionListOwnerItems(Message):
	opcode = 0x259

class CMSGAuctionPlaceBid(Message):
	opcode = 0x25A

class SMSGAuctionCommandResult(Message):
	opcode = 0x25B

class SMSGAuctionListResult(Message):
	opcode = 0x25C

class SMSGAuctionOwnerListResult(Message):
	opcode = 0x25D

class SMSGAuctionBidderNotification(Message):
	opcode = 0x25E

class SMSGAuctionOwnerNotification(Message):
	opcode = 0x25F

class SMSGProcResist(Message):
	opcode = 0x260

class SMSGStandStateChangeFailureObsolete(Message):
	opcode = 0x261

class SMSGDispelFailed(Message):
	opcode = 0x262

class SMSGSpellOrDamageImmune(Message):
	opcode = 0x263

class CMSGAuctionListBidderItems(Message):
	opcode = 0x264

class SMSGAuctionBidderListResult(Message):
	opcode = 0x265

class SMSGSetFlatSpellModifier(Message):
	opcode = 0x266

class SMSGSetPctSpellModifier(Message):
	opcode = 0x267

class CMSGSetAmmo(Message):
	opcode = 0x268

class SMSGCorpseReclaimDelay(Message):
	opcode = 0x269

class CMSGSetActiveMover(Message):
	opcode = 0x26A

class CMSGPetCancelAura(Message):
	opcode = 0x26B

class CMSGPlayerAICheat(Message):
	opcode = 0x26C

class CMSGCancelAutoRepeatSpell(Message):
	opcode = 0x26D

class MSGGMAccountOnline(Message):
	opcode = 0x26E

class MSGListStabledPets(Message):
	opcode = 0x26F

class CMSGStablePet(Message):
	opcode = 0x270

class CMSGUnstablePet(Message):
	opcode = 0x271

class CMSGBuyStableSlot(Message):
	opcode = 0x272

class SMSGStableResult(Message):
	opcode = 0x273

class CMSGStableRevivePet(Message):
	opcode = 0x274

class CMSGStableSwapPet(Message):
	opcode = 0x275

class MSGQuestPushResult(Message):
	opcode = 0x276

class SMSGPlayMusic(Message):
	opcode = 0x277

class SMSGPlayObjectSound(Message):
	opcode = 0x278

class CMSGRequestPetInfo(Message):
	opcode = 0x279

class CMSGFarSight(Message):
	opcode = 0x27A

class SMSGSpellDispelLog(Message):
	opcode = 0x27B

class SMSGDamageCalcLog(Message):
	opcode = 0x27C

class CMSGEnableDamageLog(Message):
	opcode = 0x27D

class CMSGGroupChangeSubGroup(Message):
	opcode = 0x27E

class CMSGRequestPartyMemberStats(Message):
	opcode = 0x27F

class CMSGGroupSwapSubGroup(Message):
	opcode = 0x280

class CMSGResetFactionCheat(Message):
	opcode = 0x281

class CMSGAutoStoreBankItem(Message):
	opcode = 0x282

class CMSGAutoBankItem(Message):
	opcode = 0x283

class MSGQueryNextMailTime(Message):
	opcode = 0x284

class SMSGReceivedMail(Message):
	opcode = 0x285

class SMSGRaidGroupOnly(Message):
	opcode = 0x286

class CMSGSetDurabilityCheat(Message):
	opcode = 0x287

class CMSGSetPVPRankCheat(Message):
	opcode = 0x288

class CMSGAddPVPMedalCheat(Message):
	opcode = 0x289

class CMSGDelPVPMedalCheat(Message):
	opcode = 0x28A

class CMSGSetPVPTitle(Message):
	opcode = 0x28B

class SMSGPVPCredit(Message):
	opcode = 0x28C

class SMSGAuctionRemovedNotification(Message):
	opcode = 0x28D

class CMSGGroupRaidConvert(Message):
	opcode = 0x28E

class CMSGGroupAssistantLeader(Message):
	opcode = 0x28F

class CMSGBuyBackItem(Message):
	opcode = 0x290

class SMSGServerMessage(Message):
	opcode = 0x291

class CMSGMeetingStoneJoin(Message):
	opcode = 0x292

class CMSGMeetingStoneLeave(Message):
	opcode = 0x293

class CMSGMeetingStoneCheat(Message):
	opcode = 0x294

class SMSGMeetingStoneSetqueue(Message):
	opcode = 0x295

class CMSGMeetingStoneInfo(Message):
	opcode = 0x296

class SMSGMeetingStoneComplete(Message):
	opcode = 0x297

class SMSGMeetingStoneInProgress(Message):
	opcode = 0x298

class SMSGMeetingStoneMemberAdded(Message):
	opcode = 0x299

class CMSGGMTicketSystemToggle(Message):
	opcode = 0x29A

class CMSGCancelGrowthAura(Message):
	opcode = 0x29B

class SMSGCancelAutoRepeat(Message):
	opcode = 0x29C

class SMSGStandStateUpdate(Message):
	opcode = 0x29D

class SMSGLootAllPassed(Message):
	opcode = 0x29E

class SMSGLootRollWon(Message):
	opcode = 0x29F

class CMSGLootRoll(Message):
	opcode = 0x2A0

class SMSGLootStartRoll(Message):
	opcode = 0x2A1

class SMSGLootRoll(Message):
	opcode = 0x2A2

class CMSGLootMasterGive(Message):
	opcode = 0x2A3

class SMSGLootMasterList(Message):
	opcode = 0x2A4

class SMSGSetForcedReactions(Message):
	opcode = 0x2A5

class SMSGSpellFailedOther(Message):
	opcode = 0x2A6

class SMSGGameObjectResetState(Message):
	opcode = 0x2A7

class CMSGRepairItem(Message):
	opcode = 0x2A8

class SMSGChatPlayerNotFound(Message):
	opcode = 0x2A9

class MSGTalentWipeConfirm(Message):
	opcode = 0x2AA

class SMSGSummonRequest(Message):
	opcode = 0x2AB

class CMSGSummonResponse(Message):
	opcode = 0x2AC

class MSGMoveToggleGravityCheat(Message):
	opcode = 0x2AD

class SMSGMonsterMoveTransport(Message):
	opcode = 0x2AE

class SMSGPetBroken(Message):
	opcode = 0x2AF

class MSGMoveFeatherFall(Message):
	opcode = 0x2B0

class MSGMoveWaterWalk(Message):
	opcode = 0x2B1

class CMSGServerBroadcast(Message):
	opcode = 0x2B2

class CMSGSelfRes(Message):
	opcode = 0x2B3

class SMSGFeignDeathResisted(Message):
	opcode = 0x2B4

class CMSGRunScript(Message):
	opcode = 0x2B5

class SMSGScriptMessage(Message):
	opcode = 0x2B6

class SMSGDuelCountdown(Message):
	opcode = 0x2B7

class SMSGAreaTriggerMessage(Message):
	opcode = 0x2B8

class CMSGToggleHelm(Message):
	opcode = 0x2B9

class CMSGToggleCloak(Message):
	opcode = 0x2BA

class SMSGMeetingStoneJoinFailed(Message):
	opcode = 0x2BB

class SMSGPlayerSkinned(Message):
	opcode = 0x2BC

class SMSGDurabilityDamageDeath(Message):
	opcode = 0x2BD

class CMSGSetExploration(Message):
	opcode = 0x2BE

class CMSGSetActionbarToggles(Message):
	opcode = 0x2BF

class UMSGDeleteGuildCharter(Message):
	opcode = 0x2C0

class MSGPetitionRename(Message):
	opcode = 0x2C1

class SMSGInitWorldStates(Message):
	opcode = 0x2C2

class SMSGUpdateWorldState(Message):
	opcode = 0x2C3

class CMSGItemNameQuery(Message):
	opcode = 0x2C4

class SMSGItemNameQueryResponse(Message):
	opcode = 0x2C5

class SMSGPetActionFeedback(Message):
	opcode = 0x2C6

class CMSGCharRename(Message):
	opcode = 0x2C7

class SMSGCharRename(Message):
	opcode = 0x2C8

class CMSGMoveSplineDone(Message):
	opcode = 0x2C9

class CMSGMoveFallReset(Message):
	opcode = 0x2CA

class SMSGInstanceSaveCreated(Message):
	opcode = 0x2CB

class SMSGRaidInstanceInfo(Message):
	opcode = 0x2CC

class CMSGRequestRaidInfo(Message):
	opcode = 0x2CD

class CMSGMoveTimeSkipped(Message):
	opcode = 0x2CE

class CMSGMoveFeatherFallAck(Message):
	opcode = 0x2CF

class CMSGMoveWaterWalkAck(Message):
	opcode = 0x2D0

class CMSGMoveNotActiveMover(Message):
	opcode = 0x2D1

class SMSGPlaySound(Message):
	opcode = 0x2D2

class CMSGBattlefieldStatus(Message):
	opcode = 0x2D3

class SMSGBattlefieldStatus(Message):
	opcode = 0x2D4

class CMSGBattlefieldPort(Message):
	opcode = 0x2D5

class MSGInspectHonorStats(Message):
	opcode = 0x2D6

class CMSGBattleMasterHello(Message):
	opcode = 0x2D7

class CMSGMoveStartSwimCheat(Message):
	opcode = 0x2D8

class CMSGMoveStopSwimCheat(Message):
	opcode = 0x2D9

class SMSGForceWalkSpeedChange(Message):
	opcode = 0x2DA

class CMSGForceWalkSpeedChangeAck(Message):
	opcode = 0x2DB

class SMSGForceSwimBackSpeedChange(Message):
	opcode = 0x2DC

class CMSGForceSwimBackSpeedChangeAck(Message):
	opcode = 0x2DD

class SMSGForceTurnRateChange(Message):
	opcode = 0x2DE

class CMSGForceTurnRateChangeAck(Message):
	opcode = 0x2DF

class MSGPVPLogData(Message):
	opcode = 0x2E0

class CMSGLeaveBattlefield(Message):
	opcode = 0x2E1

class CMSGAreaSpiritHealerQuery(Message):
	opcode = 0x2E2

class CMSGAreaSpiritHealerQueue(Message):
	opcode = 0x2E3

class SMSGAreaSpiritHealerTime(Message):
	opcode = 0x2E4

class CMSGGMUnteach(Message):
	opcode = 0x2E5

class SMSGWardenData(Message):
	opcode = 0x2E6

class CMSGWardenData(Message):
	opcode = 0x2E7

class SMSGGroupJoinedBattleground(Message):
	opcode = 0x2E8

class MSGBattlegroundPlayerPositions(Message):
	opcode = 0x2E9

class CMSGPetStopAttack(Message):
	opcode = 0x2EA

class SMSGBinderConfirm(Message):
	opcode = 0x2EB

class SMSGBattlegroundPlayerJoined(Message):
	opcode = 0x2EC

class SMSGBattlegroundPlayerLeft(Message):
	opcode = 0x2ED

class CMSGBattlemasterJoin(Message):
	opcode = 0x2EE

class SMSGAddonInfo(Message):
	opcode = 0x2EF

class CMSGPetUnlearn(Message):
	opcode = 0x2F0

class SMSGPetUnlearnConfirm(Message):
	opcode = 0x2F1

class SMSGPartyMemberStatsFull(Message):
	opcode = 0x2F2

class CMSGPetSpellAutocast(Message):
	opcode = 0x2F3

class SMSGWeather(Message):
	opcode = 0x2F4

class SMSGPlayTimeWarning(Message):
	opcode = 0x2F5

class SMSGMinigameSetup(Message):
	opcode = 0x2F6

class SMSGMinigameState(Message):
	opcode = 0x2F7

class CMSGMinigameMove(Message):
	opcode = 0x2F8

class SMSGMinigameMoveFailed(Message):
	opcode = 0x2F9

class SMSGRaidInstanceMessage(Message):
	opcode = 0x2FA

class SMSGCompressedMoves(Message):
	opcode = 0x2FB

class CMSGGuildInfoText(Message):
	opcode = 0x2FC

class SMSGChatRestricted(Message):
	opcode = 0x2FD

class SMSGSplineSetRunSpeed(Message):
	opcode = 0x2FE

class SMSGSplineSetRunBackSpeed(Message):
	opcode = 0x2FF

class SMSGSplineSetSwimSpeed(Message):
	opcode = 0x300

class SMSGSplineSetWalkSpeed(Message):
	opcode = 0x301

class SMSGSplineSetSwimBackSpeed(Message):
	opcode = 0x302

class SMSGSplineSetTurnRate(Message):
	opcode = 0x303

class SMSGSplineMoveUnroot(Message):
	opcode = 0x304

class SMSGSplineMoveFeatherFall(Message):
	opcode = 0x305

class SMSGSplineMoveNormalFall(Message):
	opcode = 0x306

class SMSGSplineMoveSetHover(Message):
	opcode = 0x307

class SMSGSplineMoveUnsetHover(Message):
	opcode = 0x308

class SMSGSplineMoveWaterWalk(Message):
	opcode = 0x309

class SMSGSplineMoveLandWalk(Message):
	opcode = 0x30A

class SMSGSplineMoveStartSwim(Message):
	opcode = 0x30B

class SMSGSplineMoveStopSwim(Message):
	opcode = 0x30C

class SMSGSplineMoveSetRunMode(Message):
	opcode = 0x30D

class SMSGSplineMoveSetWalkMode(Message):
	opcode = 0x30E

class CMSGGMNukeAccount(Message):
	opcode = 0x30F

class MSGGMDestroyCorpse(Message):
	opcode = 0x310

class CMSGGMDestroyOnlineCorpse(Message):
	opcode = 0x311

class CMSGActivatetaxiexpress(Message):
	opcode = 0x312

class SMSGSetFactionAtWar(Message):
	opcode = 0x313

class SMSGGameTimeBiasSet(Message):
	opcode = 0x314

class CMSGDebugActionsStart(Message):
	opcode = 0x315

class CMSGDebugActionsStop(Message):
	opcode = 0x316

class CMSGSetFactionInactive(Message):
	opcode = 0x317

class CMSGSetWatchedFaction(Message):
	opcode = 0x318

class MSGMoveTimeSkipped(Message):
	opcode = 0x319

class SMSGSplineMoveRoot(Message):
	opcode = 0x31A

class CMSGSetExplorationAll(Message):
	opcode = 0x31B

class SMSGInvalidatePlayer(Message):
	opcode = 0x31C

class CMSGResetInstances(Message):
	opcode = 0x31D

class SMSGInstanceReset(Message):
	opcode = 0x31E

class SMSGInstanceResetFailed(Message):
	opcode = 0x31F

class SMSGUpdateLastInstance(Message):
	opcode = 0x320

class MSGRaidTargetUpdate(Message):
	opcode = 0x321

class MSGRaidReadyCheck(Message):
	opcode = 0x322

class CMSGLuaUsage(Message):
	opcode = 0x323

class SMSGPetActionSound(Message):
	opcode = 0x324

class SMSGPetDismissSound(Message):
	opcode = 0x325

class SMSGGhosteeGone(Message):
	opcode = 0x326

class CMSGGMUpdateTicketStatus(Message):
	opcode = 0x327

class SMSGGMTicketStatusUpdate(Message):
	opcode = 0x328

class MSGSetDungeonDifficulty(Message):
	opcode = 0x329

class CMSGGMSurveySubmit(Message):
	opcode = 0x32A

class SMSGUpdateInstanceOwnership(Message):
	opcode = 0x32B

class CMSGIgnoreKnockbackCheat(Message):
	opcode = 0x32C

class SMSGChatPlayerAmbiguous(Message):
	opcode = 0x32D

class MSGDelayGhostTeleport(Message):
	opcode = 0x32E

class SMSGSpellInstaKillLog(Message):
	opcode = 0x32F

class SMSGSpellUpdateChainTargets(Message):
	opcode = 0x330

class CMSGChatFiltered(Message):
	opcode = 0x331

class SMSGExpectedSpamRecords(Message):
	opcode = 0x332

class SMSGSpellStealLog(Message):
	opcode = 0x333

class CMSGLotteryQueryObsolete(Message):
	opcode = 0x334

class SMSGLotteryQueryResultObsolete(Message):
	opcode = 0x335

class CMSGBuyLotteryTicketObsolete(Message):
	opcode = 0x336

class SMSGLotteryResultObsolete(Message):
	opcode = 0x337

class SMSGCharacterProfile(Message):
	opcode = 0x338

class SMSGCharacterProfileRealmConnected(Message):
	opcode = 0x339

class SMSGDefenseMessage(Message):
	opcode = 0x33A

class SMSGInstanceDifficulty(Message):
	opcode = 0x33B

class MSGGMResetInstanceLimit(Message):
	opcode = 0x33C

class SMSGMOTD(Message):
	opcode = 0x33D

class SMSGMoveSetFlightObsolete(Message):
	opcode = 0x33E

class SMSGMoveUnsetFlightObsolete(Message):
	opcode = 0x33F

class CMSGMoveFlightAckObsolete(Message):
	opcode = 0x340

class MSGMoveStartSwimCheat(Message):
	opcode = 0x341

class MSGMoveStopSwimCheat(Message):
	opcode = 0x342

class SMSGMoveSetCanFly(Message):
	opcode = 0x343

class SMSGMoveUnsetCanFly(Message):
	opcode = 0x344

class CMSGMoveSetCanFlyAck(Message):
	opcode = 0x345

class CMSGMoveSetFly(Message):
	opcode = 0x346

class CMSGSocketGems(Message):
	opcode = 0x347

class CMSGArenaTeamCreate(Message):
	opcode = 0x348

class SMSGArenaTeamCommandResult(Message):
	opcode = 0x349

class UMSGUpdateArenaTeamObsolete(Message):
	opcode = 0x34A

class CMSGArenaTeamQuery(Message):
	opcode = 0x34B

class SMSGArenaTeamQueryResponse(Message):
	opcode = 0x34C

class CMSGArenaTeamRoster(Message):
	opcode = 0x34D

class SMSGArenaTeamRoster(Message):
	opcode = 0x34E

class CMSGArenaTeamInvite(Message):
	opcode = 0x34F

class SMSGArenaTeamInvite(Message):
	opcode = 0x350

class CMSGArenaTeamAccept(Message):
	opcode = 0x351

class CMSGArenaTeamDecline(Message):
	opcode = 0x352

class CMSGArenaTeamLeave(Message):
	opcode = 0x353

class CMSGArenaTeamRemove(Message):
	opcode = 0x354

class CMSGArenaTeamDisband(Message):
	opcode = 0x355

class CMSGArenaTeamLeader(Message):
	opcode = 0x356

class SMSGArenaTeamEvent(Message):
	opcode = 0x357

class CMSGBattlemasterJoinArena(Message):
	opcode = 0x358

class MSGMoveStartAscend(Message):
	opcode = 0x359

class MSGMoveStopAscend(Message):
	opcode = 0x35A

class SMSGArenaTeamStats(Message):
	opcode = 0x35B

class CMSGLFGSetAutoJoin(Message):
	opcode = 0x35C

class CMSGLFGClearAutoJoin(Message):
	opcode = 0x35D

class CMSGLFMSetAutoFill(Message):
	opcode = 0x35E

class CMSGLFMClearAutoFill(Message):
	opcode = 0x35F

class CMSGAcceptLFGMatch(Message):
	opcode = 0x360

class CMSGDeclineLFGMatch(Message):
	opcode = 0x361

class CMSGCancelPendingLFG(Message):
	opcode = 0x362

class CMSGClearLookingForGroup(Message):
	opcode = 0x363

class CMSGClearLookingForMore(Message):
	opcode = 0x364

class CMSGSetLookingForMore(Message):
	opcode = 0x365

class CMSGSetLFGComment(Message):
	opcode = 0x366

class SMSGLFGTimedOut(Message):
	opcode = 0x367

class SMSGLFGOtherTimedOut(Message):
	opcode = 0x368

class SMSGLFGAutoJoinFailed(Message):
	opcode = 0x369

class SMSGLFGAutoJoinFailedNoPlayer(Message):
	opcode = 0x36A

class SMSGLFGLeaderIsLFM(Message):
	opcode = 0x36B

class SMSGLFGUpdate(Message):
	opcode = 0x36C

class SMSGLFGUpdateLFM(Message):
	opcode = 0x36D

class SMSGLFGUpdateLFG(Message):
	opcode = 0x36E

class SMSGLFGUpdateQueued(Message):
	opcode = 0x36F

class SMSGLFGPendingInvite(Message):
	opcode = 0x370

class SMSGLFGPendingMatch(Message):
	opcode = 0x371

class SMSGLFGPendingMatchDone(Message):
	opcode = 0x372

class SMSGTitleEarned(Message):
	opcode = 0x373

class CMSGSetTitle(Message):
	opcode = 0x374

class CMSGCancelMountAura(Message):
	opcode = 0x375

class SMSGArenaError(Message):
	opcode = 0x376

class MSGInspectArenaTeams(Message):
	opcode = 0x377

class SMSGDeathReleaseLoc(Message):
	opcode = 0x378

class CMSGCancelTempEnchantment(Message):
	opcode = 0x379

class SMSGForcedDeathUpdate(Message):
	opcode = 0x37A

class CMSGCheatSetHonorCurrency(Message):
	opcode = 0x37B

class CMSGCheatSetArenaCurrency(Message):
	opcode = 0x37C

class MSGMoveSetFlightSpeedCheat(Message):
	opcode = 0x37D

class MSGMoveSetFlightSpeed(Message):
	opcode = 0x37E

class MSGMoveSetFlightBackSpeedCheat(Message):
	opcode = 0x37F

class MSGMoveSetFlightBackSpeed(Message):
	opcode = 0x380

class SMSGForceFlightSpeedChange(Message):
	opcode = 0x381

class CMSGForceFlightSpeedChangeAck(Message):
	opcode = 0x382

class SMSGForceFlightBackSpeedChange(Message):
	opcode = 0x383

class CMSGForceFlightBackSpeedChangeAck(Message):
	opcode = 0x384

class SMSGSplineSetFlightSpeed(Message):
	opcode = 0x385

class SMSGSplineSetFlightBackSpeed(Message):
	opcode = 0x386

class CMSGMaelstromInvalidateCache(Message):
	opcode = 0x387

class SMSGFlightSplineSync(Message):
	opcode = 0x388

class CMSGSetTaxiBenchmarkMode(Message):
	opcode = 0x389

class SMSGJoinedBattlegroundQueue(Message):
	opcode = 0x38A

class SMSGRealmSplit(Message):
	"""Realm Split Information (Response)

	Information about the current or last realm split."""
	opcode = 0x38B

	@property
	def splitState(self):
		"""Split State

		Whether a realm split is in progress or not."""
		return ["Normal", "Split", "Split pending"][self.unpack("L", 4)]

	@property
	def splitDate(self):
		"""Split Date

		The realm split date."""
		return self.data[8:16]

class CMSGRealmSplit(Message):
	"""Realm Split Information (Request)

	Queries information about a realm split (character transfer) for this realm."""
	opcode = 0x38C

class CMSGMoveChngTransport(Message):
	opcode = 0x38D

class MSGPartyAssignment(Message):
	opcode = 0x38E

class SMSGOfferPetitionError(Message):
	opcode = 0x38F

class SMSGTimeSync(Message):
	"""Time Sync (Request)"""
	opcode = 0x390

class CMSGTimeSync(Message):
	"""Time Sync (Response)"""
	opcode = 0x391

class CMSGSendLocalEvent(Message):
	opcode = 0x392

class CMSGSendGeneralTrigger(Message):
	opcode = 0x393

class CMSGSendCombatTrigger(Message):
	opcode = 0x394

class CMSGMaelstromGMSentMail(Message):
	opcode = 0x395

class SMSGResetFailedNotify(Message):
	opcode = 0x396

class SMSGRealGroupUpdate(Message):
	opcode = 0x397

class SMSGLFGDisabled(Message):
	opcode = 0x398

class CMSGActivePVPCheat(Message):
	opcode = 0x399

class CMSGCheatDumpItemsDebugOnly(Message):
	opcode = 0x39A

class SMSGCheatDumpItemsDebugOnlyResponse(Message):
	opcode = 0x39B

class SMSGCheatDumpItemsDebugOnlyResponseWriteFile(Message):
	opcode = 0x39C

class SMSGUpdateComboPoints(Message):
	opcode = 0x39D

class SMSGVoiceSessionRosterUpdate(Message):
	opcode = 0x39E

class SMSGVoiceSessionLeave(Message):
	opcode = 0x39F

class SMSGVoiceSessionAdjustPriority(Message):
	opcode = 0x3A0

class CMSGVoiceSetTalkerMutedRequest(Message):
	opcode = 0x3A1

class SMSGVoiceSetTalkerMuted(Message):
	opcode = 0x3A2

class SMSGInitExtraAuraInfo(Message):
	opcode = 0x3A3

class SMSGSetExtraAuraInfo(Message):
	opcode = 0x3A4

class SMSGSetExtraAuraInfoNeedUpdate(Message):
	opcode = 0x3A5

class SMSGClearExtraAuraInfo(Message):
	opcode = 0x3A6

class MSGMoveStartDescend(Message):
	opcode = 0x3A7

class CMSGIgnoreRequirementsCheat(Message):
	opcode = 0x3A8

class SMSGIgnoreRequirementsCheat(Message):
	opcode = 0x3A9

class SMSGSpellChanceProcLog(Message):
	opcode = 0x3AA

class CMSGMoveSetRunSpeed(Message):
	opcode = 0x3AB

class SMSGDismount(Message):
	opcode = 0x3AC

class MSGMoveUpdateCanFly(Message):
	opcode = 0x3AD

class MSGRaidReadyCheckConfirm(Message):
	opcode = 0x3AE

class CMSGVoiceSessionEnable(Message):
	opcode = 0x3AF

class SMSGVoiceParentalControls(Message):
	opcode = 0x3B0

class CMSGGMWhisper(Message):
	opcode = 0x3B1

class SMSGGMMessageChat(Message):
	opcode = 0x3B2

class MSGGMGearRating(Message):
	opcode = 0x3B3

class CMSGCommentatorEnable(Message):
	opcode = 0x3B4

class SMSGCommentatorStateChanged(Message):
	opcode = 0x3B5

class CMSGCommentatorGetMapInfo(Message):
	opcode = 0x3B6

class SMSGCommentatorMapInfo(Message):
	opcode = 0x3B7

class CMSGCommentatorGetPlayerInfo(Message):
	opcode = 0x3B8

class SMSGCommentatorGetPlayerInfo(Message):
	opcode = 0x3B9

class SMSGCommentatorPlayerInfo(Message):
	opcode = 0x3BA

class CMSGCommentatorEnterInstance(Message):
	opcode = 0x3BB

class CMSGCommentatorExitInstance(Message):
	opcode = 0x3BC

class CMSGCommentatorInstanceCommand(Message):
	opcode = 0x3BD

class SMSGClearTarget(Message):
	opcode = 0x3BE

class CMSGBotDetected(Message):
	opcode = 0x3BF

class SMSGCrossedInebriationThreshold(Message):
	opcode = 0x3C0

class CMSGCheatPlayerLogin(Message):
	opcode = 0x3C1

class CMSGCheatPlayerLookup(Message):
	opcode = 0x3C2

class SMSGCheatPlayerLookup(Message):
	opcode = 0x3C3

class SMSGKickReason(Message):
	opcode = 0x3C4

class MSGRaidReadyCheckFinished(Message):
	opcode = 0x3C5

class CMSGComplain(Message):
	opcode = 0x3C6

class SMSGComplainResult(Message):
	opcode = 0x3C7

class SMSGFeatureSystemStatus(Message):
	opcode = 0x3C8

class CMSGGMShowComplaints(Message):
	opcode = 0x3C9

class CMSGGMUnsquelch(Message):
	opcode = 0x3CA

class CMSGChannelSilenceVoice(Message):
	opcode = 0x3CB

class CMSGChannelSilenceAll(Message):
	opcode = 0x3CC

class CMSGChannelUnsilenceVoice(Message):
	opcode = 0x3CD

class CMSGChannelUnsilenceAll(Message):
	opcode = 0x3CE

class CMSGTargetCast(Message):
	opcode = 0x3CF

class CMSGTargetScriptCast(Message):
	opcode = 0x3D0

class CMSGChannelDisplayList(Message):
	opcode = 0x3D1

class CMSGSetActiveVoiceChannel(Message):
	opcode = 0x3D2

class CMSGGetChannelMemberCount(Message):
	opcode = 0x3D3

class SMSGChannelMemberCount(Message):
	opcode = 0x3D4

class CMSGChannelVoiceOn(Message):
	opcode = 0x3D5

class CMSGChannelVoiceOff(Message):
	opcode = 0x3D6

class CMSGDebugListTargets(Message):
	opcode = 0x3D7

class SMSGDebugListTargets(Message):
	opcode = 0x3D8

class SMSGAvailableVoiceChannel(Message):
	opcode = 0x3D9

class CMSGAddVoiceIgnore(Message):
	opcode = 0x3DA

class CMSGDelVoiceIgnore(Message):
	opcode = 0x3DB

class CMSGPartySilence(Message):
	opcode = 0x3DC

class CMSGPartyUnsilence(Message):
	opcode = 0x3DD

class MSGNotifyPartySquelch(Message):
	opcode = 0x3DE

class SMSGComsatReconnectTry(Message):
	opcode = 0x3DF

class SMSGComsatDisconnect(Message):
	opcode = 0x3E0

class SMSGComsatConnectFail(Message):
	opcode = 0x3E1

class SMSGVoiceChatStatus(Message):
	opcode = 0x3E2

class CMSGReportPVPAFK(Message):
	opcode = 0x3E3

class CMSGReportPVPAFKResult(Message):
	opcode = 0x3E4

class CMSGGuildBankerActivate(Message):
	opcode = 0x3E5

class CMSGGuildBankQueryTab(Message):
	opcode = 0x3E6

class SMSGGuildBankList(Message):
	opcode = 0x3E7

class CMSGGuildBankSwapItems(Message):
	opcode = 0x3E8

class CMSGGuildBankBuyTab(Message):
	opcode = 0x3E9

class CMSGGuildBankUpdateTab(Message):
	opcode = 0x3EA

class CMSGGuildBankDepositMoney(Message):
	opcode = 0x3EB

class CMSGGuildBankWithdrawMoney(Message):
	opcode = 0x3EC

class MSGGuildBankLogQuery(Message):
	opcode = 0x3ED

class CMSGSetChannelWatch(Message):
	opcode = 0x3EE

class SMSGUserListAdd(Message):
	opcode = 0x3EF

class SMSGUserListRemove(Message):
	opcode = 0x3F0

class SMSGUserListUpdate(Message):
	opcode = 0x3F1

class CMSGClearChannelWatch(Message):
	opcode = 0x3F2

class SMSGInspectTalent(Message):
	opcode = 0x3F3

class SMSGGoGoGoObsolete(Message):
	opcode = 0x3F4

class SMSGEchoPartySquelch(Message):
	opcode = 0x3F5

class CMSGSetTitleSuffix(Message):
	opcode = 0x3F6

class CMSGSpellClick(Message):
	opcode = 0x3F7

class SMSGLootList(Message):
	opcode = 0x3F8

class CMSGGMCharacterRestore(Message):
	opcode = 0x3F9

class CMSGGMCharacterSave(Message):
	opcode = 0x3FA

class SMSGVoiceSessionFull(Message):
	opcode = 0x3FB

class MSGGuildPermissions(Message):
	opcode = 0x3FC

class MSGGuildBankMoneyWithdrawn(Message):
	opcode = 0x3FD

class MSGGuildEventLogQuery(Message):
	opcode = 0x3FE

class CMSGMaelstromRenameGuild(Message):
	opcode = 0x3FF

class CMSGGetMirrorImageData(Message):
	opcode = 0x400

class SMSGMirrorImageData(Message):
	opcode = 0x401

class SMSGForceDisplayUpdate(Message):
	opcode = 0x402

class SMSGSpellChanceResistPushback(Message):
	opcode = 0x403

class CMSGIgnoreDiminishingReturnsCheat(Message):
	opcode = 0x404

class SMSGIgnoreDiminishingReturnsCheat(Message):
	opcode = 0x405

class CMSGKeepAlive(Message):
	opcode = 0x406

class SMSGRaidReadyCheckError(Message):
	opcode = 0x407

class CMSGOptOutOfLoot(Message):
	opcode = 0x408

class MSGQueryGuildBankText(Message):
	opcode = 0x409

class CMSGSetGuildBankText(Message):
	opcode = 0x40A

class CMSGSetGrantableLevels(Message):
	opcode = 0x40B

class CMSGGrantLevel(Message):
	opcode = 0x40C

class CMSGReferAFriend(Message):
	opcode = 0x40D

class MSGGMChangeArenaRating(Message):
	opcode = 0x40E

class CMSGDeclineChannelInvite(Message):
	opcode = 0x40F

class CMSGGroupactionThrottled(Message):
	opcode = 0x410

class SMSGOverrideLight(Message):
	opcode = 0x411

class SMSGTotemCreated(Message):
	opcode = 0x412

class CMSGTotemDestroyed(Message):
	opcode = 0x413

class CMSGExpireRaidInstance(Message):
	opcode = 0x414

class CMSGNoSpellVariance(Message):
	opcode = 0x415

class CMSGQuestgiverStatusMultipleQuery(Message):
	opcode = 0x416

class SMSGQuestgiverStatusMultiple(Message):
	opcode = 0x417

class CMSGSetPlayerDeclinedNames(Message):
	opcode = 0x418

class SMSGSetPlayerDeclinedNamesResult(Message):
	opcode = 0x419

class CMSGQueryServerBuckData(Message):
	opcode = 0x41A

class CMSGClearServerBuckData(Message):
	opcode = 0x41B

class SMSGServerBuckData(Message):
	opcode = 0x41C

class SMSGSendUnlearnSpells(Message):
	opcode = 0x41D

class SMSGProposeLevelGrant(Message):
	opcode = 0x41E

class CMSGAcceptLevelGrant(Message):
	opcode = 0x41F

class SMSGReferAFriendFailure(Message):
	opcode = 0x420

class SMSGSplineMoveSetFlying(Message):
	opcode = 0x421

class SMSGSplineMoveUnsetFlying(Message):
	opcode = 0x422

class SMSGSummonCancel(Message):
	opcode = 0x423

opcode_map = dict((c.opcode, c) for c in globals().itervalues() if type(c) == type and issubclass(c, Message) and hasattr(c, "opcode"))
