from binascii import hexlify
import string
__all__ = ["hexdump"]


def hexdump(data, bytes_per_row=16, bytes_per_block=8):
	outp = ""
	for index in range(0, len(data), bytes_per_row):
		row = data[index:index + bytes_per_row]
		row_hex = tuple(hexlify(b) for b in row)

		outp += "%05d " % index

		outp_hexd = ""
		outp_str = ""
		for bindex in range(0, bytes_per_row, bytes_per_block):
			outp_hexd += "  " + " ".join(row_hex[bindex:bindex + bytes_per_block]).ljust(bytes_per_block * 3 - 1)
			for b in row[bindex:bindex + bytes_per_block]:
				if b in string.printable and (b == " " or b not in string.whitespace):
					outp_str += b
				else:
					outp_str += "."
			outp_str += "  "

		outp += outp_hexd + "   " + outp_str
		outp += "\n"
	return outp
