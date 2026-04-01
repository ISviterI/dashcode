import base64
import gzip
obj_string = ""
lvlname = ""

class Dashcode:
    def __init__(self):
        self.objects = []
        self.params = {
            "NoTouch": 13,
            "Hide": 12,
            "Group": 57,
            "TGroup": 51,
            "Duration": 10,
            "Alpha": 11,
            "TouchTrigger": 11,
            "ActivateGroup": 56,
            "ScaleX": 128,
            "ScaleY": 129,
            "Zoom": 107,
            "RotateDegrees": 68,
            "Times360": 69,
            "LockRot": 70,
            "Red":7,
            "Green":8,
            "Blue":9,
            "Fade":10,
            "TargetColor":23,
            "Delay": 63,
            "SpawnTrigger":62,
            "MultiTrigger":87
        }
        self.objectids = {
            "block": 1, "spike": 8, "yorb": 36, "coin": 1329,
            "monster": 918, "bush": 128, "cloud": 129,
            "alpha": 1007, "toggle": 1049, "rotate": 1346,
            "zoom": 1913, "reverse": 1912,
            "checkpoint": 2063,
            "spawn":1268,
            "end": 3600,
            "p_blue": 10, "p_yellow": 11, "p_green": 2926,
            "p_cube": 12, "p_ship": 13, "p_ball": 47, "p_ufo": 111,
            "p_wave": 660, "p_robot": 745, "p_spider": 1331, "p_swing": 1933
        }
        self.prefabs = {
            "wall": {"Y":0},
            "platform": {"X":0},
            "square": {"SQ":0},
            "corridor": {"X":1},
        }
        self.timeline = {}
    def setobjects(self, objs:dict):
        self.objectids = objs
    def export_gmd(self, filedata, filename:str="Level"):
        with open(f"{filename}.gmd", "w", encoding="utf-8") as f:
            f.write(filedata)
    def setparams(self, params:dict):
        self.params = params

    def get_free_group(self):
        used_groups = set()
        for obj in self.objects:
            if "57" in obj:
                parsed = Dashcode().parse_object_string(obj)
                for i,v in parsed.items():
                    #print(i,v,type(i))
                    if i == "57":
                        used_groups.add(int(v))
        current_id = 1
        while current_id in used_groups:
            current_id += 1
        return str(current_id)
    def addobject(self, obj: str, params: dict):
        objects = self.objects
        if len(objects) <= 0:
            objects.append(
                f"1,1,2,{str(-10 * 30)},3,{str(-10 * 30)},12,1,13,1")
        extraparams = ""
        for param, value in params.items():
            for i in self.params:
                if param.startswith(i):
                    pid = self.params[param]
                    extraparams += f",{str(pid)},{value}"
                else:
                    extraparams += f",{str(param)},{value}"

        oid = self.objectids.get(obj, 1)
        if oid:
            objects.append(
                f"1,{str(oid)},2,{str(params.get('X') * 30 + 15)},3,{str(params.get('Y') * 30 + 15)}{extraparams}")
        else:
            objects.append(
                f"1,{str(obj)},2,{str(params.get('X') * 30 + 15)},3,{str(params.get('Y') * 30 + 15)}{extraparams}")
    def parse_object_string(self,objstr):
        data = objstr.split(',')

        obj_dict = {}
        for i in range(0, len(data) - 1, 2):
            key = data[i]
            value = data[i + 1]
            obj_dict[key] = value

        return obj_dict
    def addprefab(self, obj:str, params:dict, prefab:str):
        objects = self.objects
        extraparams = ""
        for param, value in params.items():
            if self.params.get(param) is not None:
                pid = self.params[param]
                extraparams += f",{str(pid)},{value}"
            else:
                extraparams += f",{str(param)},{value}"

        oid = self.objectids.get(obj, 1)
        if prefab:
            #print("1")
            fab = self.prefabs.get(prefab)
            if fab:
                #print(fab)
                #print("2")
                newobjs = []
                if fab.get("X") == 0:
                    #print("3")
                    for i in range(params.get('EX')):
                        newobjs.append(
                            f"1,{str(oid)},2,{str(params.get('X') * 30 + 15 + (i * 30))},3,{str(params.get('Y') * 30 + 15)}{extraparams}")
                if fab.get("Y") == 0:
                    #print("3")
                    for i in range(params.get('EY')):
                        newobjs.append(
                            f"1,{str(oid)},2,{str(params.get('X') * 30 + 15)},3,{str(params.get('Y') * 30 + 15 + (i * 30))}{extraparams}")
                if fab.get("SQ") == 0:
                    for i in range(params.get('EX')):
                        newobjs.append(
                            f"1,{str(oid)},2,{str(params.get('X') * 30 + 15 + (i * 30))},3,{str(params.get('Y') * 30 + 15)}{extraparams}")
                        for v in range(params.get('EY') - 1):
                            newobjs.append(
                                f"1,{str(oid)},2,{str(params.get('X') * 30 + 15 + (i * 30))},3,{str(params.get('Y') * 30 + 15 + (v * 30) + 30)}{extraparams}")
                if fab.get("X") == 1:
                    for i in range(params.get('EX')):
                        newobjs.append(
                            f"1,{str(oid)},2,{str(params.get('X') * 30 + 15 + (i * 30))},3,{str(params.get('Y') * 30 + 15)}{extraparams}")
                    for i in range(params.get('EX')):
                        newobjs.append(
                            f"1,{str(oid)},2,{str(params.get('X') * 30 + 15 + (i * 30))},3,{str(params.get('Y') * 30 + 15 + params.get("EY") * 30)}{extraparams}")
                if fab.get("Y") == 1:
                    for i in range(params.get('EY')):
                        newobjs.append(
                            f"1,{str(oid)},2,{str(params.get('X') * 30 + 15)},3,{str(params.get('Y') * 30 + 15 + (i * 30))}{extraparams}")
                    for i in range(params.get('EY')):
                        newobjs.append(
                            f"1,{str(oid)},2,{str(params.get('X') * 30 + 15 + params.get("EX") * 30)},3,{str(params.get('Y') * 30 + 15 + (i * 30))}{extraparams}")
                objects += newobjs
    def build_timeline(self, timeline:list):
        cdelay = 0
        for tlobj in timeline:
            i = tlobj.get("Index")
            v = tlobj.get("Value")
            if i == "wait":
                cdelay += v
            elif i == "spawn":
                self.addobject("spawn", {"X":-1, "Y":6, "Delay":str(cdelay),"TGroup":str(v)})
            else:
                params = {"X":-1,"Y":5}
                for i2,v2 in v.items():
                    params[i2] = v2
                self.addobject(i,params)
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
