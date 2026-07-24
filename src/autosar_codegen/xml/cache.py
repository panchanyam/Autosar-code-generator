"""
autosar_codegen.xml.cache
=========================

ARXML document cache.

Provides:

- Parsed XML caching
- File change detection
- Cache invalidation
- Multi-file support

"""

from __future__ import annotations

import hashlib

from dataclasses import dataclass
from pathlib import Path
from threading import RLock

from autosar_codegen.xml.loader import (
    XmlDocument,
    XmlLoader,
)



# ============================================================================
# Cache Entry
# ============================================================================


@dataclass(slots=True)
class XmlCacheEntry:
    """
    Cached XML document information.
    """

    document: XmlDocument

    file_hash: str

    timestamp: float



# ============================================================================
# XML Cache
# ============================================================================


class XmlCache:
    """
    XML document cache manager.

    """

    def __init__(
        self,
        loader: XmlLoader,
    ) -> None:

        self.loader = loader


        self._cache: dict[
            str,
            XmlCacheEntry
        ] = {}


        self._lock = RLock()



    # -------------------------------------------------------------------------
    # Load
    # -------------------------------------------------------------------------


    def load(
        self,
        path: str | Path,
    ) -> XmlDocument | None:
        """
        Load document using cache.
        """

        file_path = Path(path)


        key = str(
            file_path.resolve()
        )


        current_hash = self._hash_file(
            file_path
        )


        with self._lock:


            entry = self._cache.get(
                key
            )


            #
            # Cache hit
            #
            if (

                entry

                and

                entry.file_hash == current_hash

            ):

                return entry.document



        #
        # Cache miss
        #
        document = self.loader.load_file(
            file_path
        )


        if document is None:

            return None



        with self._lock:


            self._cache[key] = XmlCacheEntry(

                document=document,

                file_hash=current_hash,

                timestamp=file_path.stat().st_mtime,

            )



        return document



    # -------------------------------------------------------------------------
    # Hashing
    # -------------------------------------------------------------------------


    def _hash_file(
        self,
        path: Path,
    ) -> str:
        """
        Generate SHA256 file hash.
        """

        sha = hashlib.sha256()


        with path.open(
            "rb"
        ) as file:


            for block in iter(
                lambda:
                    file.read(1024 * 1024),
                b"",
            ):

                sha.update(
                    block
                )


        return sha.hexdigest()



    # -------------------------------------------------------------------------
    # Cache Management
    # -------------------------------------------------------------------------


    def invalidate(
        self,
        path: str | Path,
    ) -> None:
        """
        Remove cached document.
        """

        key = str(
            Path(path).resolve()
        )


        with self._lock:

            self._cache.pop(
                key,
                None,
            )



    def clear(
        self,
    ) -> None:
        """
        Clear all cache.
        """

        with self._lock:

            self._cache.clear()



    def contains(
        self,
        path: str | Path,
    ) -> bool:
        """
        Check cached file.
        """

        key = str(
            Path(path).resolve()
        )

        return key in self._cache



    def size(
        self,
    ) -> int:
        """
        Number of cached documents.
        """

        return len(
            self._cache
        )