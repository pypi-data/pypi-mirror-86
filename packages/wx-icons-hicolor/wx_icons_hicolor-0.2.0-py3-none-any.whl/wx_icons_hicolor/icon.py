#!/usr/bin/python3
#
#  icon.py
"""
Class to represent icons.
"""
#
#  Copyright (C) 2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#

# stdlib
import base64
import pathlib
import warnings
from io import BytesIO
from typing import Optional

# 3rd party
import cairosvg  # type: ignore
import wx  # type: ignore
from domdf_python_tools.bases import Dictable
from domdf_python_tools.doctools import prettify_docstrings
from domdf_python_tools.typing import PathLike

# this package
from .constants import IconTypes, mime

__all__ = ["Icon"]


@prettify_docstrings
class Icon(Dictable):
	"""
	Represents an icon.

	:param name: The name of the icon.
	:param path: The path to the icon.
	:param size: Nominal (unscaled) size of the icon.
	:param type: The type of icon sizes for the icon.
		Valid types are ``'Fixed'``, ``'Scalable'`` and ``'Threshold'``.
		The type decides what other keys in the section are used.
	:param max_size: Specifies the maximum (unscaled) size that the icon can be scaled to.
		Defaults to the value of ``Size`` if not present.
	:no-default max_size:
	:param min_size: Specifies the minimum (unscaled) size that the icon can be scaled to.
		Defaults to the value of ``Size`` if not present.
	:no-default min_size:
	:param theme: The name of the theme this icon came from.
	"""

	max_size: int
	min_size: int

	def __init__(
			self,
			name: str,
			path: PathLike,
			size: int,
			type: IconTypes = "Threshold",  # noqa: A002
			max_size: Optional[int] = None,
			min_size: Optional[int] = None,
			theme: str = ''
			):

		super().__init__()

		if not isinstance(path, pathlib.Path):
			path = pathlib.Path(path)
		self.path: pathlib.Path = path.resolve()

		if self.mime_type not in {"image/svg+xml", "image/png"}:
			raise TypeError("The specified file is not a valid icon")

		self.name: str = str(name)
		self.theme: str = str(theme)

		if not isinstance(size, int):
			raise TypeError("'size' must be a integer.")
		self.size: int = int(size)

		if type not in {"Fixed", "Scalable", "Threshold"}:
			raise ValueError("'type' must be one of 'Fixed', 'Scalable' or 'Threshold'.")
		self.type = str(type)

		if max_size:
			if not isinstance(max_size, int):
				raise TypeError("'max_size' must be a integer.")
			self.max_size = int(max_size)
		else:
			self.max_size = int(size)

		if min_size:
			if not isinstance(min_size, int):
				raise TypeError("'min_size' must be a integer.")
			self.min_size = int(min_size)
		else:
			self.min_size = int(size)

	@property
	def __dict__(self):
		return dict(
				name=self.name,
				path=self.path,
				size=self.size,
				type=self.type,
				max_size=self.max_size,
				min_size=self.min_size,
				theme=self.theme,
				)

	@property
	def mime_type(self) -> str:
		"""
		The mime type of the icon.
		"""

		return str(mime.from_file(str(self.path)))

	@property
	def scalable(self) -> bool:
		"""
		Whether the icon is scalable.
		"""

		if self.type == "Fixed" and self.mime_type == "image/png":
			return False
		return True

	def as_png(self, size: Optional[int] = None) -> BytesIO:
		"""
		Returns the icon as a :class:`~io.BytesIO` object containing PNG image data.

		:return: :class:`io.BytesIO` object representing the PNG image.
		"""

		if not size:
			size = self.size

		if self.mime_type == "image/png":
			with self.path.open("rb") as fin:
				data = BytesIO(fin.read())
			return data

		elif self.mime_type == "image/svg+xml":
			svg_img = cairosvg.svg2png(url=str(self.path), output_width=size, output_height=size)
			return BytesIO(svg_img)

		else:
			raise ValueError(f"Unknown mime type '{self.mime_type}'")

	def as_base64_png(self, size: Optional[int] = None) -> str:
		"""
		Returns the icon as a base64-encoded object containing PNG image data.

		:return: Base64-encoded string representing the PNG image.
		"""

		return str(base64.b64encode(self.as_png(size).getvalue()).decode("utf-8"))

	def as_bitmap(self, size: Optional[int] = None) -> wx.Bitmap:
		"""
		Returns the icon as a wxPython bitmap.

		:param size:
		"""

		if not size:
			size = self.size

		if not self.scalable:
			if size != self.size:
				raise ValueError("This icon cannot be scaled")

		if size > self.max_size:
			print(size, self.size, self.max_size)
			warnings.warn(f"This icon should not be scaled larger than {self.max_size} px")

		elif size < self.min_size:
			warnings.warn(f"This icon should not be scaled smaller than {self.min_size} px")

		if self.mime_type == "image/png":
			# TODO Scaling
			return wx.Bitmap(wx.Image(str(self.path), wx.BITMAP_TYPE_PNG))

		elif self.mime_type == "image/svg+xml":
			svg_img = cairosvg.svg2png(url=str(self.path), output_width=size, output_height=size)
			return wx.Bitmap(wx.Image(BytesIO(svg_img), wx.BITMAP_TYPE_PNG))

	def __repr__(self) -> str:
		return f"Icon({self.name})"

	def __eq__(self, other) -> bool:
		if isinstance(other, str):
			return self.name == other

		return NotImplemented
