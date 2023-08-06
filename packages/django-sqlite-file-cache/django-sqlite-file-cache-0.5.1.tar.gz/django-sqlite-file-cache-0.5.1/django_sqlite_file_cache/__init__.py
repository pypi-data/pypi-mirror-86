import pickle
import time
import zlib
import sqlite3

from django.core.cache.backends.base import DEFAULT_TIMEOUT, BaseCache


class SQLiteFileCache(BaseCache):
    pickle_protocol = pickle.HIGHEST_PROTOCOL

    def __init__(self, location, params):
        if location == ':memory:':
            raise ValueError('\':memory:\' is not supported')

        super().__init__(params)
        self._location = location
        conn = self._connect()
        try:
            with conn:
                self._createfile(conn)
        finally:
            conn.close()

    def add(self, key, value, timeout=DEFAULT_TIMEOUT, version=None):
        if self.has_key(key, version):
            return False

        self.set(key, value, timeout, version)
        return True

    def get(self, key, default=None, version=None):
        key = self.make_key(key, version=version)
        self.validate_key(key)

        conn = self._connect()
        try:
            with conn:
                row = conn.execute(
                    '''SELECT value, expires_at FROM cache_entries WHERE key = ? LIMIT 1''', (key,)).fetchone()

                if row is not None:
                    value, expires_at = row
                    if self._is_expired(expires_at):
                        self._delete(conn, key)
                        return default
                    else:
                        return pickle.loads(zlib.decompress(value))
                else:
                    return default
        except sqlite3.OperationalError:
            return default
        finally:
            conn.close()

    def get_many(self, keys, version=None):
        if len(keys) == 0:
            return {}

        new_keys = []
        for key in frozenset(keys):
            new_key = self.make_key(key, version=version)
            self.validate_key(new_key)
            new_keys.append(new_key)

        conn = self._connect()
        try:
            with conn:
                key_values = {}

                for key in new_keys:
                    row = conn.execute('''SELECT value, expires_at FROM cache_entries WHERE key = ?''', (key,)).fetchone()
                    if row is not None:
                        value, expires_at = row
                        if self._is_expired(expires_at):
                            self._delete(conn, key)
                        else:
                            key_values[key] = pickle.loads(zlib.decompress(value))

                return key_values
        except sqlite3.OperationalError:
            return {}
        finally:
            conn.close()

    def set(self, key, value, timeout=DEFAULT_TIMEOUT, version=None):
        key = self.make_key(key, version=version)
        self.validate_key(key)

        expiry = self.get_backend_timeout(timeout)

        pickled_value = zlib.compress(
            pickle.dumps(value, self.pickle_protocol))

        conn = self._connect()
        try:
            with conn:
                self._createfile(conn)
                self._cull(conn)
                conn.execute(
                    '''INSERT INTO cache_entries (key, value, expires_at) VALUES (?, ?, ?)''', (key, pickled_value, expiry))
        finally:
            conn.close()

    def _set_many_tuple_generator(self, rekeyed_data, expiry):
        for key, value in rekeyed_data.items():
            pickled_value = zlib.compress(pickle.dumps(value, self.pickle_protocol))

            yield key, pickled_value, expiry

    def set_many(self, data, timeout=DEFAULT_TIMEOUT, version=None):
        rekeyed_data = {}
        for key, value in data.items():
            key = self.make_key(key, version=version)
            self.validate_key(key)

            rekeyed_data[key] = value

        expiry = self.get_backend_timeout(timeout)

        conn = self._connect()
        with conn:
            self._createfile(conn)
            self._cull(conn)

            conn.executemany('''INSERT INTO cache_entries (key, value, expires_at) VALUES (?, ?, ?)''', self._set_many_tuple_generator(rekeyed_data, expiry))

    def touch(self, key, timeout=DEFAULT_TIMEOUT, version=None):
        key = self.make_key(key, version=version)
        self.validate_key(key)

        conn = self._connect()
        try:
            with conn:
                row = conn.execute(
                    '''SELECT expires_at FROM cache_entries WHERE key = ?''', (key,)).fetchone()

                if row is not None:
                    expires_at, = row
                    if self._is_expired(expires_at):
                        self._delete(conn, key)
                        return False
                    else:
                        expiry = self.get_backend_timeout(timeout)
                        conn.execute(
                            '''UPDATE cache_entries SET expires_at = ? WHERE key = ?''', (expiry, key,))
                        return True
                else:
                    return False
        finally:
            conn.close()

    def delete(self, key, version=None):
        key = self.make_key(key, version=version)
        self.validate_key(key)

        conn = self._connect()
        try:
            with conn:
                row = conn.execute(
                    '''SELECT expires_at FROM cache_entries WHERE key = ? LIMIT 1''', (key,)).fetchone()

                if row is not None:
                    expires_at, = row
                    self._delete(conn, key)

                    if self._is_expired(expires_at):
                        return False
                    else:
                        return True
                else:
                    return False
        finally:
            conn.close()

    def delete_many(self, keys, version=None):
        rekeyed_key_tuples = []
        for key in keys:
            key = self.make_key(key, version=version)
            self.validate_key(key)

            rekeyed_key_tuples.append((key,))

        conn = self._connect()
        try:
            with conn:
                conn.executemany('''DELETE FROM cache_entries WHERE key = ?''', rekeyed_key_tuples)
        finally:
            conn.close()

    def has_key(self, key, version=None):
        key = self.make_key(key, version=version)
        self.validate_key(key)

        conn = self._connect()
        try:
            with conn:
                row = conn.execute(
                    '''SELECT expires_at FROM cache_entries WHERE key = ? LIMIT 1''', (key,)).fetchone()

                if row is not None:
                    expires_at, = row
                    if self._is_expired(expires_at):
                        self._delete(conn, key)
                        return False
                    else:
                        return True
                else:
                    return False
        except sqlite3.OperationalError:
            return False
        finally:
            conn.close()

    def clear(self):
        conn = self._connect()
        try:
            with conn:
                conn.execute('''DELETE FROM cache_entries''')
        finally:
            conn.close()

    def _connect(self):
        return sqlite3.connect(self._location, isolation_level='EXCLUSIVE')

    def _createfile(self, conn):
        conn.execute('''
            CREATE TABLE IF NOT EXISTS cache_entries
            (
                key TEXT NOT NULL,
                value BLOB NOT NULL,
                expires_at REAL NOT NULL,
                PRIMARY KEY (key) ON CONFLICT REPLACE
            )
        ''')

    def _cull(self, conn):
        count = conn.execute(
            '''SELECT COUNT(key) FROM cache_entries''').fetchone()[0]
        if count < self._max_entries:
            return

        if self._cull_frequency == 0:
            conn.execute('''DELETE FROM cache_entries''')
        else:
            limit = int(count / self._cull_frequency)
            cur = conn.execute(
                '''SELECT key FROM cache_entries ORDER BY RANDOM() LIMIT ?''', (limit,))
            key_tuples = cur.fetchall()
            conn.executemany('''DELETE FROM cache_entries WHERE key = ?''', key_tuples)

    def _is_expired(self, expires_at):
        return expires_at < time.time()

    def _delete(self, conn, key):
        conn.execute(
            '''DELETE FROM cache_entries WHERE key = ?''', (key,))
