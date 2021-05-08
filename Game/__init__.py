from Core import Event, Render
from Game import Object
import Instance

#TODO: clean up this file, it's ugly

c_movement_speed = 1

#movement acceleration and deceleration factor
#min:0, max:1
#vel = vel * mv_accel + vel_desired * (1-mv_accel)
#high values = more slippery, low values = more friction
#default: 0.85
mv_accel = 0.85


def game_launch():
	EntityPly(0)
	Event.keybind_press("ESCAPE", Event.self.close)
	x = Instance.InstVector().assign(Instance.VEC_3D)
	print("T: ",x.convert(Instance.VEC_3D))
	print("C: ", x)
	pass


class EntityPly:
	def __init__(self, uid):
		self.id = str(uid)

		self.ang = Object.Angle()

		#entity position
		self.pos = Object.Vector()

		self.pos.y -= 6

		#entity velocity
		self.vel = Object.Vector()

		#aim direction vector
		self.aim = Object.VectorNormed()

		#aim direction vector 90 with degree turn
		self.aim_right = Object.VectorNormed()

		#aim direction vector sans vertical axis
		self.heading = Object.VectorNormed()

		#aim direction vector sans vertical axis with 90 degree turn
		self.heading_right = Object.VectorNormed()

		#direction to apply gravity and where to reference camera
		self.down = Object.VectorNormed()

		#vector for smooth velocity changes with movement
		self.move_vel = Object.Vector()

		self.forces = {
				"Gravity": Object.VectorNormed(),
				"Drag":    Object.VectorNormed(),
				"Jump":    Object.VectorNormed(),
		}
		self.forces_wasd = {

				"Forward": Object.VectorNormed(),
				"Back":    Object.VectorNormed(),
				"Left":    Object.VectorNormed(),
				"Right":   Object.VectorNormed(),

		}

		self.force_sum = Object.Vector()

		def bg(f_type, val):
			def subprocess():
				self.forces_wasd[f_type].set(val)

			return subprocess

		"""
		runs the keybind initialisation and stores the keybind IDs
		used for modification and unbinding
		
		make sure to keep the keybind id stored somewhere if you ever plan to have the control unbound
		there is no easy way to identify a keybind event without it's id
		"""
		self.events = {
				"EventLoop":         Event.add_evl([self.update], 1),
				#the "mv key" is mouse movement, values can be referenced with Event.self.mouse.dx/dy
				"Mouse":             Event.keybind_press("mv", self.camera),
				"Direction Forward": Event.keybind_press_and_release(
						"W",
						bg("Forward", [1, 1, 1]),
						bg("Forward", [0, 0, 0])
				),
				"Direction Left":    Event.keybind_press_and_release(
						"A",
						bg("Left", [1, 1, 1]),
						bg("Left", [0, 0, 0])
				),
				"Direction Back":    Event.keybind_press_and_release(
						"S",
						bg("Back", [-1, -1, -1]),
						bg("Back", [0, 0, 0])
				),
				"Direction Right":   Event.keybind_press_and_release(
						"D",
						bg("Right", [-1, -1, -1]),
						bg("Right", [0, 0, 0])
				),
		}

		self.heading.set((0, 0, 1))
		self.heading_right.set((1, 0, 0))
		self.mouse_settings = {

				#v_lim: limits how much you can look up or down
				#values must obey {-90 < v_lim < 90} and {v_lim[0] < v_lim[1]}, otherwise this will cause divide by 0 errors
				"v_lim":         [-89, 89],
				"sensitivity_x": 1,
				"sensitivity_y": 1,
				"invert":        False
		}

	def sum_forces(self):
		self.force_sum.reset()
		desired_vel = (
				self.forces_wasd["Forward"] * self.heading +
				self.forces_wasd["Back"] * self.heading +
				self.forces_wasd["Left"] * self.heading_right +
				self.forces_wasd["Right"] * self.heading_right
		).norm()
		self.move_vel *= [mv_accel, mv_accel, mv_accel]
		self.move_vel += desired_vel * [1 - mv_accel, 1 - mv_accel, 1 - mv_accel]
		self.force_sum += self.move_vel * [c_movement_speed, c_movement_speed, c_movement_speed]
		for x in self.forces:
			self.force_sum += self.forces[x]
		self.vel = self.force_sum

	def update(self):
		self.aim = self.ang.vector() + [0, 0, 0]

		#this is a very dirty way to get the 'right' from the forward vector
		#but its more efficient than trying to normalise it again,
		#so it works for the update() routine
		self.ang.y -= 90
		self.aim_right = self.ang.vector() + [0, 0, 0]
		self.ang.y += 90

		self.heading = (self.aim * [-1, 0, 1]).norm()
		self.heading_right = (self.aim_right * [-1, 0, 1]).norm()
		self.sum_forces()
		self.pos += self.vel
		Render.cam_ang(*self.ang())
		Render.cam_pos(*self.pos())

	def camera(self):
		#add a flag here to toggle camera movement
		#have this influenced by self.mouse_settings
		self.ang.y += Event.self.mouse.dx / 10
		self.ang.x -= Event.self.mouse.dy / 10
