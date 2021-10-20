data = {
    "person": {
        "address": {
            "zip": "92651",
            "city": "East Natashashire",
            "zip4": "9265",
            "state": "Rhode Island",
            "address_line_1": "1646 Christopher Square Apt. 537",
        },
        "contact": {
            "email_1": "karen.ellison@gmail.com",
            "email_2": "karen.ellison@yahoo.com",
            "email_3": "karen.ellison@hotmail.com",
            "email_4": "",
            "email_5": "",
        },
        "profile": {"last_name": "Ellison", "first_name": "Karen"},
        "identifiers": {
            "email_id_1": "6572216693205773159",
            "email_id_2": "60952639465106395422",
            "email_id_3": "24469066085878709054",
            "email_id_4": "59383233823521157569",
            "email_id_5": "69054093361240516383",
            "speedeon_id": "4c9cdec93069416183a4160711dbfec2",
        },
    }
}

# print(eval(''data["person"]["contact"]["email_1"]'))


# map_source = {
#    "contact": {
#        "email": '"{},{},{},{},{}".format(data["person"]["contact"]["email_1"], data["person"]["contact"]["email_2"], data["person"]["contact"]["email_3"], data["person"]["contact"]["email_4"], data["person"]["contact"]["email_5"])',
#    }
# }

# map = { k: ", ".join(filter(None, eval(v).split(","))) for k, v in map_source.items()}

# print(map)


def concat(*args):
    return ",".join(filter(None, args))


email = eval(
    "concat(data['person']['contact']['email_1'], data['person']['contact']['email_2'], data['person']['contact']['email_3'], data['person']['contact']['email_4'], data['person']['contact']['email_5'])"
)

import json
from functools import reduce

path = "person.contact.email".split(".")
target = reduce(lambda d, k: d.setdefault(k, {}), path[:-1], data)
target[path[-1]] = email
print(json.dumps(data))

"person.contact.email=concat(data[''person''][''contact''][''email_1''], data[''person''][''contact''][''email_2''], data[''person''][''contact''][''email_3''], data[''person''][''contact''][''email_4''], data[''person''][''contact''][''email_5''])"
