import base64
import gzip
from operator import index

timelineY = 3
itemeditx = -1
obj_string = ""
lvlname = ""

print("Dashcode loaded! Have fun and also join our discord server please: https://discord.gg/MXv3KTFmPE")


class Dashcode:
    def __init__(self):
        self.objects = []
        self.params = {
            "NoTouch": 13,
            "Hide": 12,
            "Group": 57,
            "TGroup": 51,
            "MoveX": 28,
            "MoveY": 29,
            "LockToPX": 34,
            "LockToPY": 35,
            "UseTarget": 36,
            "TMoveGroup": 39,
            "Duration": 10,
            "Alpha": 11,
            "TouchTrigger": 11,
            "ActivateGroup": 56,
            "ScaleX": 128,
            "ScaleY": 129,
            "Zoom": 107,
            "Rotation":6,
            "RotateDegrees": 68,
            "Times360": 69,
            "LockRot": 70,
            "Red": 7,
            "Green": 8,
            "Blue": 9,
            "Fade": 10,
            "TargetColor": 23,
            "SpawnTrigger": 62,
            "MultiTrigger": 87,
            "X": 2,
            "Y": 3,
            "ItemA": 80,
            "ItemB": 95,
            "TItemId": 51,
            "ItemValue": 77,
            "ItemModType": 476,
            "ItemMod": 479,
            "Comparison": 88,
            "2ItemMod":483,
            "2TGroup":71,
            "Delay":292,
            "FollowGid":71,
            "MaxSpeed":298,
            "MaxRange":308,
            "UseP1":138,
            "UseP2":200,
            "UseCenter":201,
            "Static_TGroup":71,
            "ExitStatic":110,
            "ExitInstant":465
        }
        self.objectids = {
            "block": 1, "spike": 8, "yorb": 36, "coin": 1329,
            "monster": 918, "bush": 128, "cloud": 129,
            "alpha": 1007, "toggle": 1049, "rotate": 1346,
            "zoom": 1913, "reverse": 1912, "move": 901, "adv_follow":3016,
            "checkpoint": 2063,
            "spawn": 1268,
            "end": 3600,
            "p_blue": 10, "p_yellow": 11, "p_green": 2926,
            "p_cube": 12, "p_ship": 13, "p_ball": 47, "p_ufo": 111,
            "p_wave": 660, "p_robot": 745, "p_spider": 1331, "p_swing": 1933,
            "h_block": 1859, "d_block": 1755, "f_block": 2866,
            "item_edit": 3619, "item_compare": 3620, "item_display": 1615,
        }
        self.prefabs = {
            "wall": {"Y": 0},
            "platform": {"X": 0},
            "square": {"SQ": 0},
            "corridor": {"X": 1},
        }
        self.variables = {}

    def setobjects(self, objs: dict):
        self.objectids = objs

    def export_gmd(self, filedata, filename: str = "Level"):
        with open(f"{filename}.gmd", "w", encoding="utf-8") as f:
            f.write(filedata)

    def setparams(self, params: dict):
        self.params = params

    def format_groups(self, group_list):
        if not group_list:
            return ""
        return ".".join(map(str, group_list))

    def get_free_group(self):
        used_groups = set()
        for obj in self.objects:
            if "57" in obj:
                parsed = Dashcode().parse_object_string(obj)
                for i2, v2 in parsed.items():
                    #print(i,v,type(i))
                    if i2 == "57":
                        for v in v2.split("."):
                            used_groups.add(int(v))
        current_id = 1
        while current_id in used_groups:
            current_id += 1
        return str(current_id)

    def addobject(self, obj, params: dict):
        if len(self.objects) <= 0:
            self.objects.append(f"1,1,2,{-10 * 30},3,{-10 * 30},12,1,13,1")
        extraparams = ""
        for param, value in params.items():
            if param in ["X", "Y", "EX", "EY"]:
                continue
            target_id = None
            for i, v in self.params.items():
                if str(param).startswith(str(i)):
                    target_id = v
                    break
            if target_id is not None:
                if target_id == 57 and isinstance(value, list):
                    extraparams += f",57,{self.format_groups(value)}"
                else:
                    extraparams += f",{target_id},{value}"
            else:
                extraparams += f",{param},{value}"
        oid = self.objectids.get(obj, obj)
        pos_x = params.get('X', 0) * 30 + 15
        pos_y = params.get('Y', 0) * 30 + 15
        full_obj_string = f"1,{oid},2,{pos_x},3,{pos_y}{extraparams}"
        self.objects.append(full_obj_string)
        return full_obj_string

    def parse_object_string(self, objstr):
        data = objstr.split(',')
        obj_dict = {}
        for i in range(0, len(data) - 1, 2):
            key = data[i]
            value = data[i + 1]
            obj_dict[key] = value
        return obj_dict

    def removeobject(self, obj: str):
        self.objects.remove(obj)

    def editobject(self, obj: str, params: dict):
        parsed = self.parse_object_string(obj)
        #print(parsed)
        newparams = {}
        for i, v in parsed.items():
            if not newparams.get(i):
                newparams[i] = v
        for i, v in params.items():
            #print(i,v)
            if self.params.get(i) and not i in ["X", "Y"]:
                if not parsed.get(self.params.get(i)) and self.params.get(i):
                    newparams[str(self.params.get(i))] = str(v)
            elif i in ["X", "Y"]:
                #print(i,v)
                newparams[str(self.params.get(i))] = str(v * 30)
            else:
                newparams[str(i)] = str(v)
        new_obj = ""
        for i, v in newparams.items():
            new_obj += f"{i},{v},"
        #print(newparams)
        #print(new_obj)
        self.removeobject(obj)
        self.objects.append(new_obj)
        return new_obj

    def addprefab(self, obj: str, params: dict, prefab: str):
        fab = self.prefabs.get(prefab)
        if not fab:
            return
        ex = params.get('EX', 0)
        ey = params.get('EY', 0)
        base_x = params.get('X', 0)
        base_y = params.get('Y', 0)
        placed = []

        def place(x_val, y_val):
            current_params = dict(params)
            current_params["X"] = x_val
            current_params["Y"] = y_val
            preobj_str = self.addobject(obj, current_params)
            placed.append(preobj_str)

        if fab.get("X") == 0:
            for i in range(ex):
                place(base_x + i, base_y)
        elif fab.get("Y") == 0:
            for i in range(ey):
                place(base_x, base_y + i)
        elif fab.get("SQ") == 0:
            for i in range(ex):
                for v in range(ey):
                    place(base_x + i, base_y + v)
        elif fab.get("X") == 1:
            for i in range(ex):
                place(base_x + i, base_y)
                place(base_x + i, base_y + ey)
        elif fab.get("Y") == 1:
            for i in range(ey):
                place(base_x, base_y + i)
                place(base_x + ex, base_y + i)
        return placed

    def build_timeline(dcself):
        class Timeline:
            def __init__(self):
                self.timeline = []
                self.delay = 0
                self.spawn_trigger_enabled = False
                self.spawn_group = dcself.get_free_group()
                self.x_position = -1
                self.x2_position = -1
                self.spawn_trigger_on_objects = False

            def spawn(self, group: int):
                if self.spawn_trigger_enabled:
                    dcself.addobject("spawn",
                                     {"X": self.x_position, "Y": 6, "Delay": str(self.delay), "TGroup": str(group),
                                      "Group": self.spawn_group, "SpawnTrigger": 1, "MultiTrigger": 1})
                else:
                    dcself.addobject("spawn",
                                     {"X": self.x_position, "Y": 6, "Delay": str(self.delay), "TGroup": str(group),
                                      "Group": self.spawn_group})
                self.timeline.append(["spawn", str(group)])
                self.x_position += -1

            def wait(self, seconds: float):
                self.delay += seconds
                self.timeline.append(["wait", str(seconds)])

            def create_object(self, obj: str, params: dict):
                if params.get("X") is None and params.get("Y") is None:
                    params["X"] = self.x2_position
                    params["Y"] = 5
                    self.x2_position += -1
                if self.spawn_trigger_on_objects:
                    params["SpawnTrigger"] = 1
                    params["MultiTrigger"] = 1
                self.timeline.append([obj, params])
                dcself.addobject(obj, params)

        return Timeline()

    def add_variable(self, variable: int, value: int):
        global itemeditx
        params = {
            "X": itemeditx,
            "Y": 4,
            "TGroup": variable,
            "ItemMod": value,
        }
        itemeditx -= 1
        raw = self.addobject("item_edit", params)
        self.variables[variable] = value
        return raw
    def set_variable(self, variable:int, value:int, x:float, y:float, touchtrigger:bool):
        params = {
            "X": x,
            "Y": y,
            "TGroup": variable,
            "ItemMod": value,
        }
        if touchtrigger:
            params["TouchTrigger"] = 1
        raw = self.addobject("item_edit", params)
        self.variables[variable] = value
        return raw
    def if_variable(self, variable:int, value:int, x:float, y:float, touchtrigger:bool=False, truegid:int=0,falsegid:int=0, modtype:str="=="):
        params = {
            "X": x,
            "Y": y,
            "ItemA": variable,
            "ItemMod": 1,
            "2ItemMod": value,
            "TGroup": truegid,
            "2TGroup": falsegid,
        }
        if touchtrigger:
            params["TouchTrigger"] = 1
        modtypes = {
            "==":0,
            ">":1,
            "<":2,
            ">=":3,
            "<=":4,
            "!=":5
        }
        params["ItemModType"] = modtypes[modtype]
        raw = self.addobject("item_compare", params)
        return raw
    def get_variable(self, variable:int):
        return self.variables[variable]

    def create_gmd_file(self, level_name, objects_string):
        global lvlname
        lvlname = level_name
        final_string_to_pack = objects_string
        gzipped = gzip.compress(final_string_to_pack.encode('utf-8'))
        b64_objects = base64.b64encode(gzipped).decode('utf-8').replace('/', '_').replace('+', '-')
        return f'''<?xml version="1.0"?><plist version="1.0" gjver="2.0"><dict><k>kCEK</k><i>4</i><k>k2</k><s>{level_name}</s><k>k4</k><s>{b64_objects}</s><k>k5</k><s>Doesn't matter</s><k>k11</k><i>1091</i><k>k16</k><i>1</i><k>k80</k><i>56</i></dict></plist>'''

    def decode_objects(self):
        objects = self.objects
        global obj_string
        obj_string = ";".join(objects) + ";"
        return obj_string
