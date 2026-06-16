"""
Enhanced CRUD module for the CS-340 Grazioso Salvare dashboard.

Enhancements for CS-499 Milestone Two:
- Centralized connection configuration and safer credential handling.
- Added input validation for CRUD operations.
- Added clearer return values and defensive exception handling.
- Added read limit support to reduce accidental large result sets.
- Added a close() method so database resources can be released cleanly.
"""

import os
from typing import Any, Dict, List, Optional

from pymongo import MongoClient
from pymongo.errors import PyMongoError


class AnimalShelter:
    """CRUD operations for the AAC animals collection in MongoDB."""

    def __init__(
        self,
        username: Optional[str] = None,
        password: Optional[str] = None,
        host: str = "localhost",
        port: int = 27017,
        db: str = "aac",
        col: str = "animals",
        auth_source: str = "admin",
    ) -> None:
        """
        Initialize the MongoDB connection.

        Credentials may be passed directly for classroom/Codio use, or supplied
        through environment variables AAC_USERNAME and AAC_PASSWORD. This avoids
        forcing credentials to be hard-coded in the dashboard.
        """
        self.username = username or os.getenv("AAC_USERNAME")
        self.password = password or os.getenv("AAC_PASSWORD")
        self.host = host
        self.port = int(port)
        self.db_name = db
        self.collection_name = col
        self.auth_source = auth_source

        if not self.username or not self.password:
            raise ValueError(
                "MongoDB username and password are required. Pass them to "
                "AnimalShelter() or set AAC_USERNAME and AAC_PASSWORD."
            )

        uri = (
            f"mongodb://{self.username}:{self.password}@"
            f"{self.host}:{self.port}/{self.db_name}?authSource={self.auth_source}"
        )

        try:
            self.client = MongoClient(uri, serverSelectionTimeoutMS=5000)
            self.client.admin.command("ping")
            self.database = self.client[self.db_name]
            self.collection = self.database[self.collection_name]
        except PyMongoError as error:
            raise ConnectionError(f"Could not connect to MongoDB: {error}") from error

    @staticmethod
    def _is_valid_document(data: Any) -> bool:
        """Return True when data is a non-empty MongoDB document dictionary."""
        return isinstance(data, dict) and bool(data)

    def create(self, data: Dict[str, Any]) -> bool:
        """Insert one animal document. Return True when MongoDB acknowledges it."""
        if not self._is_valid_document(data):
            raise ValueError("create() requires a non-empty dictionary.")

        try:
            result = self.collection.insert_one(data)
            return bool(result.acknowledged)
        except PyMongoError as error:
            raise RuntimeError(f"Create operation failed: {error}") from error

    def read(self, query: Optional[Dict[str, Any]] = None, limit: int = 0) -> List[Dict[str, Any]]:
        """
        Return documents matching query.

        query defaults to an empty dictionary so the dashboard can load all
        records intentionally. limit=0 keeps PyMongo's default of no limit.
        """
        if query is None:
            query = {}
        if not isinstance(query, dict):
            raise ValueError("read() query must be a dictionary.")
        if limit < 0:
            raise ValueError("read() limit cannot be negative.")

        try:
            cursor = self.collection.find(query)
            if limit:
                cursor = cursor.limit(limit)
            return list(cursor)
        except PyMongoError as error:
            raise RuntimeError(f"Read operation failed: {error}") from error

    def update(self, query: Dict[str, Any], new_values: Dict[str, Any]) -> int:
        """Update all documents matching query. Return the modified document count."""
        if not self._is_valid_document(query):
            raise ValueError("update() requires a non-empty query dictionary.")
        if not self._is_valid_document(new_values):
            raise ValueError("update() requires a non-empty values dictionary.")

        try:
            result = self.collection.update_many(query, {"$set": new_values})
            return int(result.modified_count)
        except PyMongoError as error:
            raise RuntimeError(f"Update operation failed: {error}") from error

    def delete(self, query: Dict[str, Any]) -> int:
        """Delete all documents matching query. Return the deleted document count."""
        if not self._is_valid_document(query):
            raise ValueError("delete() requires a non-empty query dictionary.")

        try:
            result = self.collection.delete_many(query)
            return int(result.deleted_count)
        except PyMongoError as error:
            raise RuntimeError(f"Delete operation failed: {error}") from error

    def close(self) -> None:
        """Close the MongoDB client connection."""
        self.client.close()
