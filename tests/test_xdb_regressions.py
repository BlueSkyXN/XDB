import sqlite3
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
XDB_SCRIPT = REPO_ROOT / "XDB.py"


def import_xdb():
    sys.path.insert(0, str(REPO_ROOT))
    try:
        import XDB
    finally:
        sys.path.pop(0)
    return XDB


def run_xdb(*args):
    return subprocess.run(
        [sys.executable, str(XDB_SCRIPT), *args],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=True,
    )


class XDBRegressionTests(unittest.TestCase):
    def test_sqlite_mapping_preserves_all_rows_across_chunks(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            csv_path = tmp_path / "sample.csv"
            db_path = tmp_path / "mapped.db"
            csv_path.write_text("A,B\n1,x\n2,y\n3,z\n", encoding="utf-8")

            run_xdb(
                str(csv_path),
                "--db-type",
                "sqlite",
                "--sqlite-path",
                str(db_path),
                "--target-table",
                "mapped",
                "--mode",
                "overwrite",
                "--workers",
                "1",
                "--chunk-size",
                "2",
                "--mapping",
                "Sheet1:A=aa,B=bb",
                "--quiet",
            )

            with sqlite3.connect(db_path) as conn:
                rows = conn.execute("SELECT aa, bb FROM mapped ORDER BY aa").fetchall()

            self.assertEqual(rows, [(1, "x"), (2, "y"), (3, "z")])

    def test_mapping_order_does_not_swap_column_types(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            csv_path = tmp_path / "sample.csv"
            db_path = tmp_path / "mapped.db"
            csv_path.write_text("A,B\n1,x\n2,y\n3,z\n", encoding="utf-8")

            run_xdb(
                str(csv_path),
                "--db-type",
                "sqlite",
                "--sqlite-path",
                str(db_path),
                "--target-table",
                "mapped",
                "--mode",
                "overwrite",
                "--workers",
                "1",
                "--chunk-size",
                "10",
                "--mapping",
                "Sheet1:B=bb,A=aa",
                "--quiet",
            )

            with sqlite3.connect(db_path) as conn:
                table_info = conn.execute("PRAGMA table_info(mapped)").fetchall()
                rows = conn.execute("SELECT aa, bb FROM mapped ORDER BY aa").fetchall()

            types_by_name = {row[1]: row[2] for row in table_info}
            self.assertEqual(types_by_name["aa"], "INTEGER")
            self.assertEqual(types_by_name["bb"], "TEXT")
            self.assertEqual(rows, [(1, "x"), (2, "y"), (3, "z")])

    def test_identifier_sanitizer_keeps_common_audit_columns(self):
        XDB = import_xdb()

        self.assertEqual(XDB.sanitize_column_name("created_at"), "created_at")
        self.assertEqual(XDB.sanitize_column_name("updated_at"), "updated_at")
        self.assertEqual(XDB.sanitize_column_name("delete_flag"), "delete_flag")
        self.assertEqual(XDB.sanitize_column_name("select_code"), "select_code")

    def test_mysql_mapping_write_uses_source_column_order(self):
        XDB = import_xdb()

        class FakeCursor:
            def __init__(self):
                self.executemany_calls = []

            def __enter__(self):
                return self

            def __exit__(self, exc_type, exc, tb):
                return False

            def executemany(self, sql, rows):
                self.executemany_calls.append((sql, list(rows)))

            def execute(self, *args, **kwargs):
                return None

        class FakeConnection:
            def __init__(self):
                self.cursor_obj = FakeCursor()
                self.commits = 0

            def cursor(self):
                return self.cursor_obj

            def commit(self):
                self.commits += 1

            def rollback(self):
                pass

            def close(self):
                pass

        fake_conn = FakeConnection()
        db = XDB.MySQLDatabase("localhost", 3306, "root", "pass", "testdb")
        db.conn = fake_conn

        inserted = db.write_data(
            "mapped",
            ["A", "B"],
            [[(1, "x"), (2, "y"), (3, "z")]],
            {"B": "bb", "A": "aa"},
        )

        self.assertEqual(inserted, 3)
        self.assertEqual(fake_conn.commits, 1)
        sql, rows = fake_conn.cursor_obj.executemany_calls[0]
        self.assertIn("`aa`, `bb`", " ".join(sql.split()))
        self.assertEqual(rows, [(1, "x"), (2, "y"), (3, "z")])


if __name__ == "__main__":
    unittest.main()
