
class Settings:
	def __init__(self):
		self.blur_step = 2
		self.blur_filter = 23
		self.blur_shrink = 1

		self.bit_depth = 32

		self.particles_max = 100000
		self.particles_spawn = 10000


APP_SETTINGS = Settings()
APP_SETTINGS.blur_shrink = 3
APP_SETTINGS.blur_step = 1
APP_SETTINGS.blur_filter = 10
APP_SETTINGS.bit_depth = 16
APP_SETTINGS.particles_max = 50000
APP_SETTINGS.particles_spawn = 5000

RENDER_SETTINGS = Settings()