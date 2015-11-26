#!/usr/bin/env python

import wx
import wx.gizmos
import sys

if sys.platform == "win32":
	# Workaround for an annoying issue on x64 wxPython
	from ctypes import windll
	windll.comctl32

import messages
from weave import Dump

app = wx.PySimpleApp()

if len(sys.argv) > 1:
	dump_filename = sys.argv[1]
else:
	open_dialog = wx.FileDialog(None, style=wx.OPEN, wildcard="Weave Packet Dumps (*.wdmp)|*.wdmp|All files|*.*")

	if open_dialog.ShowModal() == wx.ID_OK:
		dump_filename = open_dialog.GetPath()
	else:
		raise SystemExit

	open_dialog.Destroy()

try:
	dump_filehandle = open(dump_filename, "rb")
	dump_object = Dump(dump_filehandle)
except IOError as e:
	print("""Could not open "%s" for input: %s""" % (dump_filename, str(e)))

frame = wx.Frame(None, wx.ID_ANY, "wxWarDis - %s" % dump_filename, None, (1024, 600))

tree = wx.gizmos.TreeListCtrl(frame, style=wx.TR_FULL_ROW_HIGHLIGHT | wx.TR_HIDE_ROOT | wx.TR_TWIST_BUTTONS | wx.TR_NO_LINES)
tree.AddColumn("Message", 200)
tree.AddColumn("Data", 225)
tree.AddColumn("Source", 70)
tree.AddColumn("Description", 500)

tree.root = tree.AddRoot("Root")

frame.CreateStatusBar()
frame.Show(True)


def get_docstrings(obj, fallback=""):
	"""Try really hard to obtain a reasonable pair of strings to represent the
	type of obj (short and long description)"""

	candidates = [obj.__doc__, type(obj).__doc__]
	try:
		candidates.append(obj.__name__)
	except:
		pass
	try:
		candidates.append(type(obj).__name__)
	except:
		pass

	candidates.append(fallback)

	for candidate in candidates:
		if candidate and not candidate.startswith("property") and not candidate.startswith("attrgetter"):
			part = [chunk.strip() for chunk in candidate.split("\n", 1)]

			if part[0].islower():
				part[0] = part[0].capitalize()

			if len(part) == 1:
				return (part[0], "")
			else:
				return part

	return ("", "")


def create_items_for(tv, parent, obj):
	"""Recursively create all sub-listitems for obj"""

	# Iterate over the objects properties
	for pname, prop in type(obj).__dict__.iteritems():
		if type(prop) == property and not prop in (messages.Message.data, messages.Message.name):
			name, descr = get_docstrings(prop, pname)

			subitem = tv.AppendItem(parent, name)
			try:
				value = getattr(obj, pname)
			except Exception as e:
				value = "<%s: %s>" % (type(e).__name__, str(e))

			try:
				tv.SetItemText(subitem, unicode(value), 1)
			except:
				# Something wrent wrong converting this value to unicode. Just
				# repr() it.
				tv.SetItemText(subitem, repr(value), 1)

			tv.SetItemText(subitem, descr, 3)

			# This value itself might be iterable (dicts, lists, etc.)
			create_items_for(tv, subitem, value)

	enumerations = tuple()

	if type(obj) == dict:
		# If it's a dict, make sure we're getting a tuple of both key and value
		enumerations = tuple(obj.iteritems())
	elif not type(obj) in (str, unicode): # we don't want to iterate each char
		try:
			try:
				enumerations = (("Item #%d" % index, item) for index, item in enumerate(obj))
			except TypeError:
				# TypeErrors are not fatal. The object might just not be
				# iterable. Is there a better way to check by now?
				pass
		except Exception as e:
			# This indicates that something else went wrong, most likely while
			# parsing a packet.
			enumerations = (("<Error during enumeration>", repr(e)),)

	for key, value in enumerations:
		subitem = tv.AppendItem(parent, key)

		try:
			tv.SetItemText(subitem, unicode(value), 1)
		except Exception:
			tv.SetItemText(subitem, repr(value), 1)

		create_items_for(tv, subitem, value)

for msg in dump_object:
	name, descr = get_docstrings(msg)
	new_item = tree.AppendItem(tree.root, msg.name)

	try:
		tree.SetItemText(new_item, unicode(msg), 1)
	except Exception as e:
		tree.SetItemText(new_item, "<%s: %s>" % (type(e).__name__, str(e)), 1)

	tree.SetItemText(new_item, ("Client", "Server")[msg.__type], 2)
	tree.SetItemText(new_item, descr, 3)

	create_items_for(tree, new_item, msg)

app.MainLoop()
