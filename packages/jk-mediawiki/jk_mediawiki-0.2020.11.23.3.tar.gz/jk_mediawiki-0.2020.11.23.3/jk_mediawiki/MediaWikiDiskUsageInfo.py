

import collections

import jk_typing




class MediaWikiDiskUsageInfo(object):

	@jk_typing.checkFunctionSignature()
	def __init__(self, sizeCore:int, sizeCache:int, sizeImages:int, sizeExtensions:int, sizeDatabase:int):
		self.core = sizeCore
		self.cache = sizeCache
		self.images = sizeImages
		self.extensions = sizeExtensions
		self.database = sizeDatabase
	#

	@property
	def ro(self) -> int:
		return self.core + self.extensions
	#

	@property
	def rw(self) -> int:
		return self.cache + self.images + self.database
	#

	@property
	def total(self) -> int:
		return self.core + self.cache + self.images + self.extensions + self.database
	#

#













