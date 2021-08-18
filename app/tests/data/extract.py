import json

with open("./residents.json") as f:
    content = f.readlines()

    for resident_line in content:
        resident = json.loads(resident_line.strip())
        profile = resident["person"]["profile"]
        address = resident["person"]["address"]
        contact = resident["person"]["contact"]
        print(
            '{},{},"{}",{},{}'.format(
                profile["first_name"],
                profile["last_name"],
                address["address_line_1"],
                address["city"],
                contact["email"],
            )
        )
