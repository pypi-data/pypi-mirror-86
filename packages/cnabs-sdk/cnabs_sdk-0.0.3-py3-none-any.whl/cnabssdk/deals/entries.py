import cnabssdk.common.base_entry
import cnabssdk.common.utility

class deal_list_entry(cnabssdk.common.base_entry.baseEntry):
    def __init__(self, id = "", name = "", code = "", status = "", shortname = ""):
        super().__init__(id, code, name)
        self.status = status
        self.short_name = shortname

    def loadFromJson(self, jsonObj):
        super().loadFromJson(jsonObj)
        self.status = jsonObj["status"]
        self.short_name = jsonObj["short_name"]

class deal_info_entry(deal_list_entry):
    def __init__(self):
        super().__init__()
        self.total_offering = 0
        self.cut_off_date = ''
        