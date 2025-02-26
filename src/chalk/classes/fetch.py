import re

import httpx

from chalk.classes.models import VirtualClassInfo


def get_csv(virtual_class: VirtualClassInfo, client: httpx.Client) -> None:
    resp = client.get(virtual_class.drupal_link).raise_for_status()
    match = re.search(r"/node/(\d+)/registrations", resp.text)

    virtual_class.csv_link = f"https://www.nypl.org{match[0]}/export/registrations.csv "
    print(virtual_class.csv_link)

    resp = client.get(virtual_class.csv_link).raise_for_status()
    virtual_class.csv_data = resp.text


def get_registration_emails(virtual_class: VirtualClassInfo) -> None:
    csv = virtual_class.csv_data
    rows = csv.replace('"', "").split("\r\n")
    email_list = []
    for r in rows[1:]:
        r = r.split(",")
        if len(r) > 2:
            email_list.append(r[1])
    virtual_class.registration_emails = email_list

