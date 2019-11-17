class doc_properties():
    def __init__(self, props = ""):
        """
        setup for doc props

        props: starting propeties
        """
        props = ("slave: False\n%s" % props).strip("\n")
        self.prop_d = {}
        for i in props.split("\n"):
            self.set(i)

    def get(self, prop, default = ""):
        """
        gets a doc prop

        prop: the prop to get
        default: the value to return if prop is undefined
        """
        if prop in self.prop_d:
            return self.prop_d[prop]
        return default

    def set(self, command):
        """
        sets a property from a string

        string: the command to parse
        """
        property, value, req, req_bool, req_value = self.parse(command)
        self.add(property, value, req, req_bool, req_value)

    def parse(self, command):
        """
        splits a command for set

        command: the command to split
        """
        if "|" in command:
            req = command.split("|")[0].strip("! ")
            cmd = command.split("|")[1]
            property = cmd.split(":")[0].strip(" ")
            value = cmd.split(":")[1].strip(" ")
            req_value = "True"
            if "=" in req:
                req_value = req.split("=")[1].strip(" ")
                req = req.split("=")[0].strip(" ")
            req_bool = True
            if "!" in command:
                req_bool = False
        else:
            req = ""
            req_bool = False
            req_value = ""
            cmd = command
            property = cmd.split(":")[0].strip(" ")
            value = cmd.split(":")[1].strip(" ")
        return property, value, req, req_bool, req_value

    def add(self, prop, value, req = "", req_bool = False, req_value = "True"):
        """
        adds a prop if it should

        prop: the prop to set
        value: the value to set the prop to
        req: the required prop name
        req_bool: if true the value of req should be equal to req_value
        req_value: the required value of req
        """
        if req != "":
            if req_bool == ( req_value == self.prop_d[req]):
                self.prop_d[prop] = value
        else:
            self.prop_d[prop] = value
    
    def tag_rep(self, string):
        for key in self.prop_d:
            string = string.replace("()"+key+"()", self.prop_d[key])
        return string
