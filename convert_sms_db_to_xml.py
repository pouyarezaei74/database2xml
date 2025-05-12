import sqlite3
import xml.etree.ElementTree as ET
import datetime
import os
import sys

def safe_value(value):
    if value is None or str(value).strip() == "":
        return "null"
    return str(value)

def convert_mmssms_db_to_xml(db_path, output_path=None):
    if not os.path.exists(db_path):
        print(f"[!] Database file not found: {db_path}")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM sms")
    total = cursor.fetchone()[0]

    print(f"[*] Total SMS messages found: {total}")

    cursor.execute("""
        SELECT _id, thread_id, address, person, date, protocol, read, 
               status, type, subject, body, service_center, locked
        FROM sms ORDER BY date DESC
    """)

    smses = ET.Element("smses", attrib={"count": str(total)})

    for row in cursor.fetchall():
        (_id, thread_id, address, person, date, protocol, read,
         status, sms_type, subject, body, service_center, locked) = row

        readable_date = datetime.datetime.fromtimestamp(date / 1000).strftime("%b %d, %Y %I:%M:%S %p")

        sms = ET.Element("sms", attrib={
            "protocol": safe_value(protocol),
            "address": safe_value(address),
            "date": safe_value(date),
            "type": safe_value(sms_type),
            "subject": safe_value(subject),
            "body": safe_value(body),
            "service_center": safe_value(service_center),
            "read": safe_value(read),
            "status": safe_value(status),
            "locked": safe_value(locked),
            "readable_date": readable_date
        })

        smses.append(sms)

    if not output_path:
        output_path = datetime.datetime.now().strftime("sms-%Y%m%d%H%M%S.xml")

    tree = ET.ElementTree(smses)
    tree.write(output_path, encoding="utf-8", xml_declaration=True)

    print(f"[+] XML saved to: {output_path}")
    print("[✓] Done. You can now restore this using SMS Backup & Restore app.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python convert_sms_db_to_xml.py mmssms.db [output.xml]")
        sys.exit(1)

    db_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) >= 3 else None

    convert_mmssms_db_to_xml(db_file, output_file)
