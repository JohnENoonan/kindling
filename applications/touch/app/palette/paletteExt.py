
class PaletteExt:

	def __init__(self, ownerComp):
		pass
		self.palette_table = op("palette")

	def ToGLSL(self):
		out = ""
		for i in range(1, self.palette_table.numRows):
			row = self.palette_table.row(i)
			out += '#define {} vec4({}, {}, {}, {})\n'.format(str(row[0]).upper(), row[1], row[2], row[3], row[4])
		op("/app/custom_glsl/palette_edit").text = out
		
	def Update(self):
		self.ToGLSL()