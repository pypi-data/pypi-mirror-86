#!/usr/bin/python3
#
#  directory.py
"""
Class to represent directory of icons.
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
import configparser
import pathlib
from typing import List, Optional, Type, TypeVar

# 3rd party
from domdf_python_tools.bases import Dictable
from domdf_python_tools.doctools import prettify_docstrings
from domdf_python_tools.typing import PathLike
from memoized_property import memoized_property  # type: ignore

# this package
from .constants import IconTypes, mime
from .icon import Icon

__all__ = ["Directory"]

_D = TypeVar("_D", bound="Directory")


@prettify_docstrings
class Directory(Dictable):
	"""
	Represents a directory containing icons.

	:param path: The absolute path to the directory
	:param size: Nominal (unscaled) size of the icons in this directory.
	:param scale: Target scale of the icons in this directory.
		Any directory with a scale other than 1 should be listed in the ScaledDirectories list rather
		than Directories for backwards compatibility.
	:param context: The context the icon is normally used in. This is in detail discussed in the section called “Context”.
	:param type: The type of icon sizes for the icons in this directory.
		Valid types are ``'Fixed'``, ``'Scalable'`` and ``'Threshold'``.
		The type decides what other keys in the section are used.
	:param max_size: Specifies the maximum (unscaled) size that the icons in this directory can be scaled to.
		Defaults to the value of Size if not present.
	:no-default max_size:
	:param min_size: Specifies the minimum (unscaled) size that the icons in this directory can be scaled to.
		Defaults to the value of Size if not present.
	:no-default min_size:
	:param threshold: The icons in this directory can be used if the size differ at most this much from the desired (unscaled) size. Defaults to 2 if not present.
	:param theme: The name of the theme this directory is a part of
	"""

	max_size: int
	min_size: int

	def __init__(
			self,
			path: PathLike,
			size: int,
			scale: int = 1,
			context: str = '',
			type: IconTypes = "Threshold",  # noqa: A002
			max_size: Optional[int] = None,
			min_size: Optional[int] = None,
			threshold: int = 2,
			theme: str = '',
			):
		super().__init__()

		self.scale: int = int(scale)
		self.context: str = str(context)
		self.threshold: str = str(threshold)
		self.theme: str = str(theme)

		if not isinstance(path, pathlib.Path):
			path = pathlib.Path(path)
		self.path: pathlib.Path = path.resolve()

		if not isinstance(size, int):
			raise TypeError("'size' must be a integer.")
		self.size: int = int(size)

		if type not in {"Fixed", "Scalable", "Threshold"}:
			raise ValueError("'type' must be one of 'Fixed', 'Scalable' or 'Threshold'.")
		self.type = type

		if max_size:
			if not isinstance(max_size, int):
				raise TypeError("'max_size' must be a integer.")
			self.max_size = max_size
		else:
			self.max_size = size

		if min_size:
			if not isinstance(min_size, int):
				raise TypeError("'min_size' must be a integer.")
			self.min_size = min_size
		else:
			self.min_size = size

	@property
	def __dict__(self):
		return dict(
				path=self.path,
				size=self.size,
				scale=self.scale,
				context=self.context,
				type=self.type,
				max_size=self.max_size,
				min_size=self.min_size,
				threshold=self.threshold,
				theme=self.theme,
				)

	@classmethod
	def from_configparser(
			cls: Type[_D],
			config_section: configparser.SectionProxy,
			theme_content_root: pathlib.Path,
			) -> _D:
		"""
		Constructs a :class:`~.Directory` from a
		`configparser <https://docs.python.org/3/library/configparser.html>`_ section.

		:param config_section:
		:param theme_content_root:

		:rtype: :class:`~.Directory`
		"""  # noqa: D400

		if not isinstance(config_section, configparser.SectionProxy):
			raise TypeError("'config_section' must be a 'configparser.SectionProxy' object")

		path = theme_content_root / config_section.name
		size = int(config_section.get("Size"))
		scale = int(config_section.get("Scale", fallback='1'))
		context = config_section.get("Context", fallback='')
		type_ = config_section.get("Type", fallback="Threshold")

		max_size = config_section.get("MaxSize", fallback=None)
		max_size_: Optional[int]
		if max_size:
			max_size_ = int(max_size)
		else:
			max_size_ = None

		min_size = config_section.get("MinSize", fallback=None)
		min_size_: Optional[int]
		if min_size:
			min_size_ = int(min_size)
		else:
			min_size_ = None

		threshold = int(config_section.get("Threshold", fallback='2'))

		return cls(
				path,
				size,
				scale,
				context,
				type_,  # type: ignore
				max_size_,
				min_size_,
				threshold,
				)

	@memoized_property
	def icons(self) -> List[Icon]:
		"""
		Returns a list of icons in this :class:`~.Directory`.
		"""

		absolute_dir_path = self.path.resolve()
		# print(absolute_dir_path)

		icons = []

		for item in absolute_dir_path.iterdir():
			if item.is_file():
				if mime.from_file(str(item.resolve())) in {"image/svg+xml", "image/png"}:
					icon = Icon(item.stem, item, self.size, self.type, self.max_size, self.min_size, self.theme)
					icons.append(icon)

		return icons

	def __repr__(self) -> str:
		return f"Directory({self.path})"
