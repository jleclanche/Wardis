from struct import unpack, unpack_from
from subprocess import Popen, PIPE
import messages

__all__ = ["Dump", "launch"]


class Dump(object):
	"""Parses a packet dump from a file object.

	Instantiate this object by passing it an open file descriptor. You can also
	pass sys.stdin to read from standard input.

	If no errors have occurred, you can iterate over the Dump object to get the
	messages that are stored inside."""

	def __init__(self, stream):
		self.stream = stream
		self.ident, self.version = unpack_from("<8sH", self.stream.read(32))

		if self.ident != "WeaveDmp":
			raise ValueError("Unknown header")

		if self.version > 3:
			raise ValueError("Unsupported version")

	def __iter__(self):
		while True:
			size_raw = self.stream.read(4)
			if len(size_raw) < 4:
				break

			size = unpack("<L", size_raw)[0]

			field_names = (
				"_type",
				"reserved1",
				"client_build",
				"client_addr",
				"client_port",
				"server_addr",
				"server_port",
				"tv_sec",
				"tv_usec",
				"opcode",
				"reserved2"
			)

			field_values = unpack("<BBHLHLHLLL16s", self.stream.read(44))
			field_dict = dict(zip(field_names, field_values))

			packet_data = self.stream.read(size - 48)

			if not field_dict["_type"] in (0, 1):
				# Unknown type of packet. We better skip it.
				continue

			if field_dict["opcode"] in messages.opcode_map:
				# We know this opcode and can instantiate a specific class
				# from it.
				m = messages.opcode_map[field_dict["opcode"]]()
			else:
				# The opcode is not known - instantiate a generic Message and
				# set its opcode manually.
				m = messages.Message()
				m._opcode = field_dict["opcode"]

			# Apply the new attributes, prefixed with _
			for n, v in field_dict.iteritems():
				setattr(m, "_" + n, v)

			try:
				# Some messages parse their data upon receiving it, and if
				# something goes wrong then, we don't want the app to crash.
				m.data = packet_data
			except:
				pass

			yield m


def launch(binary=True, verbosity=0, log=False, stdout=PIPE, **popenargs):
	"""Launch Weave and setup a pipe for reading data from it.

	By default, it opens Weave for binary output with no status output (except
	errors, which go to stderr) and creates a new pipe, which can be accessed
	using the "stdout" attribute of the returned object.

	You can, for example, directly pass it to Dump():
		for packet in Dump(launch().stdin):
			# do stuff with packet

	This is a wrapper for subprocess.Popen and, as a such, accepts all keyword
	arguments that Popen accepts. To fulfill its purpose as a quick way of
	launching Weave, some useful parameters are pre-filled however."""

	args = ["weave"]
	if binary:
		args.append("-b")
	if log:
		args.append("-l")
	args.append("-v%d" % verbosity)
	return Popen(args, stdout=stdout, **popenargs)
