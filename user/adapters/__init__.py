from adapters.file_storage.minio import MinioFileStorageDep
from adapters.nsfw_checker.nsfwjs import NsfwJSCheckerDep
from adapters.nsfw_checker.base import NsfwCheckResult

FileStorageDep = MinioFileStorageDep
NsfwCheckerDep = NsfwJSCheckerDep

__all__ = ['FileStorageDep',
           'NsfwCheckerDep',
           'NsfwCheckResult']
