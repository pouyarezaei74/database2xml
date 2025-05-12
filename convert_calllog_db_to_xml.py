import sqlite3
import xml.etree.ElementTree as ET
import datetime
import os
import sys

def safe_value(value):
    return "null" if value is None or str(value).strip() == "" else str(value)

def convert_calllog_db_to_xml(db_path, output_path=None):
    if not os.path.exists(db_path):
        print(f"[!] Database file not found: {db_path}")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # تشخیص نام جدول درست (ممکن است "calls" یا "call_log" باشد)
    for table_name in ("calls", "call_log"):
        try:
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            total = cursor.fetchone()[0]
            break
        except:
            continue
    else:
        print("[!] Could not find a valid call log table (tried 'calls' and 'call_log').")
        return

    print(f"[*] Total call logs found: {total}")

    cursor.execute(f"""
        SELECT number, date, duration, type, name, numbertype, numberlabel
        FROM {table_name}
        ORDER BY date DESC
    """)

    calls = ET.Element("calls", attrib={"count": str(total)})

    for row in cursor.fetchall():
        number, date, duration, call_type, name, numbertype, numberlabel = row

        readable_date = datetime.datetime.fromtimestamp(date / 1000).strftime("%b %d, %Y %I:%M:%S %p")

        call = ET.Element("call", attrib={
            "number": safe_value(number),
            "date": safe_value(date),
            "duration": safe_value(duration),
            "type": safe_value(call_type),  # 1: incoming, 2: outgoing, 3: missed
            "name": safe_value(name),
            "numbertype": safe_value(numbertype),
            "numberlabel": safe_value(numberlabel),
            "readable_date": readable_date
        })

        calls.append(call)

    if not output_path:
        output_path = datetime.datetime.now().strftime("calllog-%Y%m%d%H%M%S.xml")

    tree = ET.ElementTree(calls)
    tree.write(output_path, encoding="utf-8", xml_declaration=True)

    print(f"[+] XML saved to: {output_path}")
    print("[✓] Done. You can now restore this using SMS Backup & Restore app (if it supports call logs).")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python convert_calllog_db_to_xml.py calllog.db [output.xml]")
        sys.exit(1)

    db_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) >= 3 else None

    convert_calllog_db_to_xml(db_file, output_file)
