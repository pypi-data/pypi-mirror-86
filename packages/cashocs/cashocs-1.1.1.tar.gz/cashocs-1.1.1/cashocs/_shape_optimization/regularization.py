# Copyright (C) 2020 Sebastian Blauth
#
# This file is part of CASHOCS.
#
# CASHOCS is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# CASHOCS is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with CASHOCS.  If not, see <https://www.gnu.org/licenses/>.

r"""Regularization for shape optimization problems.

This includes a (target) volume, surface, and barycenter regularization,
which are the :math:`L^2` distances between current volume, surface,
and barycenter, and desired ones.
"""

import json

import fenics
from fenics import Constant, div, inner

from .._exceptions import ConfigError



def eps(u):
	"""Computes the symmetric gradient of u

	Parameters
	----------
	u : dolfin.function.function.Function

	Returns
	-------
	ufl.core.expr.Expr
		the symmetric gradient of u
	"""

	return fenics.Constant(0.5)*(fenics.grad(u) + fenics.grad(u).T)


def t_grad(u, n):
	"""Computes the tangential gradient of u

	Parameters
	----------
	u : dolfin.function.function.Function
		the argument
	n : ufl.geometry.FacetNormal
		the unit outer normal vector

	Returns
	-------
	ufl.core.expr.Expr
		the tangential gradient of u
	"""

	return fenics.grad(u) - fenics.outer(fenics.grad(u)*n, n)


def t_div(u, n):
	"""Computes the tangential divergence

	Parameters
	----------
	u : dolfin.function.function.Function
		the argument
	n : ufl.geometry.FacetNormal
		the outer unit normal vector

	Returns
	-------
	ufl.core.expr.Expr
		the tangential divergence of u
	"""

	return fenics.div(u) - fenics.inner(fenics.grad(u)*n, n)





class Regularization:
	"""Regularization terms for shape optimization problems

	"""

	def __init__(self, form_handler):
		"""Initializes the regularization

		Parameters
		----------
		form_handler : cashocs._forms.ShapeFormHandler
			the corresponding shape form handler object
		"""

		self.form_handler = form_handler
		self.config = self.form_handler.config

		self.dx = fenics.Measure('dx', self.form_handler.mesh)
		self.ds = fenics.Measure('ds', self.form_handler.mesh)

		self.spatial_coordinate = fenics.SpatialCoordinate(self.form_handler.mesh)

		self.measure_hole = self.config.getboolean('Regularization', 'measure_hole', fallback=False)
		if self.measure_hole:
			self.x_start = self.config.getfloat('Regularization', 'x_start', fallback=0.0)
			self.x_end = self.config.getfloat('Regularization', 'x_end', fallback=1.0)
			if not self.x_end >= self.x_start:
				raise ConfigError('Regularization', 'x_end', 'x_end must not be smaller than x_start.')
			self.delta_x = self.x_end - self.x_start

			self.y_start = self.config.getfloat('Regularization', 'y_start', fallback=0.0)
			self.y_end = self.config.getfloat('Regularization', 'y_end', fallback=1.0)
			if not self.y_end >= self.y_start:
				raise ConfigError('Regularization', 'y_end', 'y_end must not be smaller than y_start.')
			self.delta_y = self.y_end - self.y_start

			self.z_start = self.config.getfloat('Regularization', 'z_start', fallback=0.0)
			self.z_end = self.config.getfloat('Regularization', 'z_end', fallback=1.0)
			if not self.z_end >= self.z_start:
				raise ConfigError('Regularization', 'z_end', 'z_end must not be smaller than z_start.')
			self.delta_z = self.z_end - self.z_start
			if self.form_handler.mesh.geometric_dimension() == 2:
				self.delta_z = 1.0

		self.mu_volume = self.config.getfloat('Regularization', 'factor_volume', fallback=0.0)
		self.target_volume = self.config.getfloat('Regularization', 'target_volume', fallback=0.0)
		if self.config.getboolean('Regularization', 'use_initial_volume', fallback=False):
			if not self.measure_hole:
				self.target_volume = fenics.assemble(Constant(1)*self.dx)
			else:
				self.target_volume = self.delta_x*self.delta_y*self.delta_z - fenics.assemble(Constant(1.0)*self.dx)

		self.mu_surface = self.config.getfloat('Regularization', 'factor_surface', fallback=0.0)
		self.target_surface = self.config.getfloat('Regularization', 'target_surface', fallback=0.0)
		if self.config.getboolean('Regularization', 'use_initial_surface', fallback=False):
			self.target_surface = fenics.assemble(Constant(1)*self.ds)

		self.mu_barycenter = self.config.getfloat('Regularization', 'factor_barycenter', fallback=0.0)
		self.target_barycenter_list = json.loads(self.config.get('Regularization', 'target_barycenter', fallback='[0,0,0]'))
		
		if not type(self.target_barycenter_list) == list:
			raise ConfigError('Regularization', 'target_barycenter', 'This has to be a list.')
		
		if self.form_handler.mesh.geometric_dimension() == 2 and len(self.target_barycenter_list) == 2:
			self.target_barycenter_list.append(0.0)
		
		if self.config.getboolean('Regularization', 'use_initial_barycenter', fallback=False):
			self.target_barycenter_list = [0.0, 0.0, 0.0]
			if not self.measure_hole:
				volume = fenics.assemble(Constant(1)*self.dx)
				self.target_barycenter_list[0] = fenics.assemble(self.spatial_coordinate[0]*self.dx) / volume
				self.target_barycenter_list[1] = fenics.assemble(self.spatial_coordinate[1]*self.dx) / volume
				if self.form_handler.mesh.geometric_dimension() == 3:
					self.target_barycenter_list[2] = fenics.assemble(self.spatial_coordinate[2]*self.dx) / volume
				else:
					self.target_barycenter_list[2] = 0.0

			else:
				volume = self.delta_x*self.delta_y*self.delta_z - fenics.assemble(Constant(1)*self.dx)
				self.target_barycenter_list[0] = (0.5*(pow(self.x_end, 2) - pow(self.x_start, 2))*self.delta_y*self.delta_z - fenics.assemble(self.spatial_coordinate[0]*self.dx)) / volume
				self.target_barycenter_list[1] = (0.5*(pow(self.y_end, 2) - pow(self.y_start, 2))*self.delta_x*self.delta_z - fenics.assemble(self.spatial_coordinate[1]*self.dx)) / volume
				if self.form_handler.mesh.geometric_dimension() == 3:
					self.target_barycenter_list[2] = (0.5*(pow(self.z_end, 2) - pow(self.z_start, 2))*self.delta_x*self.delta_y - fenics.assemble(self.spatial_coordinate[2]*self.dx)) / volume
				else:
					self.target_barycenter_list[2] = 0.0

		if not (self.mu_volume >= 0.0 and self.mu_surface >= 0.0 and self.mu_barycenter >= 0.0):
			raise ConfigError('Regularization', 'mu_volume, mu_surface, or mu_barycenter', 'All regularization constants have to be nonnegative.')

		if self.mu_volume > 0.0 or self.mu_surface > 0.0 or self.mu_barycenter > 0.0:
			self.has_regularization = True
		else:
			self.has_regularization = False

		# self.relative_scaling = self.config.getboolean('Regularization', 'relative_scaling')
		# if self.relative_scaling and self.has_regularization:
		# 	self.scale_weights()

		self.current_volume = fenics.Expression('val', degree=0, val=1.0)
		self.current_surface = fenics.Expression('val', degree=0, val=1.0)
		self.current_barycenter_x = fenics.Expression('val', degree=0, val=0.0)
		self.current_barycenter_y = fenics.Expression('val', degree=0, val=0.0)
		self.current_barycenter_z = fenics.Expression('val', degree=0, val=0.0)



	def update_geometric_quantities(self):
		"""Updates the geometric quantities

		Updates the volume, surface area, and barycenters (after the
		mesh is updated)

		Returns
		-------
		None
		"""

		if not self.measure_hole:
			volume = fenics.assemble(Constant(1)*self.dx)
			barycenter_x = fenics.assemble(self.spatial_coordinate[0]*self.dx) / volume
			barycenter_y = fenics.assemble(self.spatial_coordinate[1]*self.dx) / volume
			if self.form_handler.mesh.geometric_dimension() == 3:
				barycenter_z = fenics.assemble(self.spatial_coordinate[2]*self.dx) / volume
			else:
				barycenter_z = 0.0

		else:
			volume = self.delta_x*self.delta_y*self.delta_z - fenics.assemble(Constant(1)*self.dx)
			barycenter_x = (0.5*(pow(self.x_end, 2) - pow(self.x_start, 2))*self.delta_y*self.delta_z - fenics.assemble(self.spatial_coordinate[0]*self.dx)) / volume
			barycenter_y = (0.5*(pow(self.y_end, 2) - pow(self.y_start, 2))*self.delta_x*self.delta_z - fenics.assemble(self.spatial_coordinate[1]*self.dx)) / volume
			if self.form_handler.mesh.geometric_dimension() == 3:
				barycenter_z = (0.5*(pow(self.z_end, 2) - pow(self.z_start, 2))*self.delta_x*self.delta_y - fenics.assemble(self.spatial_coordinate[2]*self.dx)) / volume
			else:
				barycenter_z = 0.0

		surface = fenics.assemble(Constant(1)*self.ds)

		self.current_volume.val = volume
		self.current_surface.val = surface
		self.current_barycenter_x.val = barycenter_x
		self.current_barycenter_y.val = barycenter_y
		self.current_barycenter_z.val = barycenter_z



	def compute_objective(self):
		"""Computes the part of the objective value that comes from the regularization

		Returns
		-------
		float
			Part of the objective value coming from the regularization

		"""

		if self.has_regularization:

			value = 0.0

			if self.mu_volume > 0.0:
				if not self.measure_hole:
					volume = fenics.assemble(Constant(1.0)*self.dx)
				else:
					volume = self.delta_x*self.delta_y*self.delta_z - fenics.assemble(Constant(1)*self.dx)

				value += 0.5*self.mu_volume*pow(volume - self.target_volume, 2)

			if self.mu_surface > 0.0:
				surface = fenics.assemble(Constant(1.0)*self.ds)
				# self.current_surface.val = surface
				value += 0.5*self.mu_surface*pow(surface - self.target_surface, 2)

			if self.mu_barycenter > 0.0:
				if not self.measure_hole:
					volume = fenics.assemble(Constant(1)*self.dx)

					barycenter_x = fenics.assemble(self.spatial_coordinate[0]*self.dx) / volume
					barycenter_y = fenics.assemble(self.spatial_coordinate[1]*self.dx) / volume
					if self.form_handler.mesh.geometric_dimension() == 3:
						barycenter_z = fenics.assemble(self.spatial_coordinate[2]*self.dx) / volume
					else:
						barycenter_z = 0.0

				else:
					volume = self.delta_x*self.delta_y*self.delta_z - fenics.assemble(Constant(1)*self.dx)

					barycenter_x = (0.5*(pow(self.x_end, 2) - pow(self.x_start, 2))*self.delta_y*self.delta_z - fenics.assemble(self.spatial_coordinate[0]*self.dx)) / volume
					barycenter_y = (0.5*(pow(self.y_end, 2) - pow(self.y_start, 2))*self.delta_x*self.delta_z - fenics.assemble(self.spatial_coordinate[1]*self.dx)) / volume
					if self.form_handler.mesh.geometric_dimension() == 3:
						barycenter_z = (0.5*(pow(self.z_end, 2) - pow(self.z_start, 2))*self.delta_x*self.delta_y - fenics.assemble(self.spatial_coordinate[2]*self.dx)) / volume
					else:
						barycenter_z = 0.0

				value += 0.5*self.mu_barycenter*(pow(barycenter_x - self.target_barycenter_list[0], 2) + pow(barycenter_y - self.target_barycenter_list[1], 2)
												 + pow(barycenter_z - self.target_barycenter_list[2], 2))

			return value

		else:
			return 0.0



	def compute_shape_derivative(self):
		"""Computes the part of the shape derivative that comes from the regularization

		Returns
		-------
		ufl.form.Form
			The weak form of the shape derivative coming from the regularization

		"""

		V = self.form_handler.test_vector_field
		if self.has_regularization:

			n = fenics.FacetNormal(self.form_handler.mesh)
			I = fenics.Identity(self.form_handler.mesh.geometric_dimension())

			self.shape_form = Constant(self.mu_surface)*(self.current_surface - Constant(self.target_surface))*t_div(V, n)*self.ds

			if not self.measure_hole:
				self.shape_form += Constant(self.mu_volume)*(self.current_volume - Constant(self.target_volume))*div(V)*self.dx
				self.shape_form += Constant(self.mu_barycenter)*(self.current_barycenter_x - Constant(self.target_barycenter_list[0]))\
								   		*(self.current_barycenter_x/self.current_volume*div(V) + 1/self.current_volume*(V[0] + self.spatial_coordinate[0]*div(V)))*self.dx \
								   + Constant(self.mu_barycenter)*(self.current_barycenter_y - Constant(self.target_barycenter_list[1]))\
								   		*(self.current_barycenter_y/self.current_volume*div(V) + 1/self.current_volume*(V[1] + self.spatial_coordinate[1]*div(V)))*self.dx

				if self.form_handler.mesh.geometric_dimension() == 3:
					self.shape_form += Constant(self.mu_barycenter)*(self.current_barycenter_z - Constant(self.target_barycenter_list[2]))\
									   *(self.current_barycenter_z/self.current_volume*div(V) + 1/self.current_volume*(V[2] + self.spatial_coordinate[2]*div(V)))*self.dx


			else:
				self.shape_form -= Constant(self.mu_volume)*(self.current_volume - Constant(self.target_volume))*div(V)*self.dx
				self.shape_form += Constant(self.mu_barycenter)*(self.current_barycenter_x - Constant(self.target_barycenter_list[0]))\
								   		*(self.current_barycenter_x/self.current_volume*div(V) - 1/self.current_volume*(V[0] + self.spatial_coordinate[0]*div(V)))*self.dx \
								   + Constant(self.mu_barycenter)*(self.current_barycenter_y - Constant(self.target_barycenter_list[1]))\
								   		*(self.current_barycenter_y/self.current_volume*div(V) - 1/self.current_volume*(V[1] + self.spatial_coordinate[1]*div(V)))*self.dx

				if self.form_handler.mesh.geometric_dimension() == 3:
					self.shape_form += Constant(self.mu_barycenter)*(self.current_barycenter_z - Constant(self.target_barycenter_list[2]))\
									   		*(self.current_barycenter_z/self.current_volume*div(V) - 1/self.current_volume*(V[2] + self.spatial_coordinate[2]*div(V)))*self.dx


			return self.shape_form

		else:
			dim = self.form_handler.mesh.geometric_dimension()
			return inner(fenics.Constant([0]*dim), V)*self.dx


	# TODO: Take a look at reimplementing this (scaling of the regularization terms)
	# def scale_weights(self):
	# 	"""
	# 	Scales the coefficients of the regularization, such that a factor of 1 corresponds to the term having the same weight as the initial cost function
	# 	"""
	#
	#
	#
	# 	if self.mu_volume > 0.0:
	# 		val = 0.5*pow(fenics.assemble(Constant(1.0)*self.dx) - self.target_volume, 2)
	# 		self.mu_volume /= np.abs(val)
	#
	# 	if self.mu_surface > 0.0:
	# 		val = 0.5*pow(fenics.assemble(Constant(1.0)*self.ds) - self.target_surface, 2)
	# 		self.mu_surface /= np.abs(val)
