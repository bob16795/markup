def prop_to_dict(prop):
    """
    converts a prop string to a dict object

    prop: the prop string
    """

    if prop.strip(" \n") != "":
        while "\n\n" in prop:
            prop = prop.replace("\n\n", "\n")
        prop_cached = prop.split("\n")
        prop_d = {"slave": "False"}
        for prop_line in prop_cached:
            if "|" in prop_line:
                req = prop_line.split("|")[0].strip("! ")
                cmd = prop_line.split("|")[1]
                property = cmd.split(":")[0].strip(" ")
                value = cmd.split(":")[1].strip(" ")
                req_value = "True"
                if "=" in req:
                    req_value = req.split("=")[1].strip(" ")
                    req = req.split("=")[0].strip(" ")
                req_bool = True
                if "!" in prop_line:
                    req_bool = False
                if req in prop_d:
                    if req_bool == ( req_value == prop_d[req]):
                        for key in prop_d:
                            value = value.replace("()"+key+"()", prop_d[key])
                        prop_d[property] = value
            else:
                cmd = prop_line
                property = cmd.split(":")[0].strip(" ")
                value = cmd.split(":")[1].strip(" ")
                for key in prop_d:
                    value = value.replace("()"+key+"()", prop_d[key])
                prop_d[property] = value
        return prop_d
    else:
        return {}
