import base64
import gzip

objects = []
obj_string = ""
lvlname = ""



class Dashcode:
    def __init__(self):
        global objects
        self.params = {
            "NoTouch": 13,
            "Hide": 11,
            "Group": 57,
            "TGroup": 51,
            "Duration": 10,
            "Alpha": 11,
            "TouchTrigger": 11,  # Твой ID из GMD
            "ActivateGroup": 56,
            "ScaleX": 128,
            "ScaleY": 129,
            "Zoom": 107,
            "RotateDegrees": 68,
            "Times360": 69,
            "LockRot": 70,
        }
        self.objects = {
            "block": 1, "spike": 8, "yorb": 36, "coin": 1329,
            "monster": 918, "bush": 128, "cloud": 129,
            "alpha": 1007, "toggle": 1049, "rotate": 1346,
            "zoom": 1913, "reverse": 1912,
            "checkpoint": 2063,
            "end": 3600,
            "p_blue": 10, "p_yellow": 11, "p_green": 2926,
            "p_cube": 12, "p_ship": 13, "p_ball": 47, "p_ufo": 111,
            "p_wave": 660, "p_robot": 745, "p_spider": 1331, "p_swing": 1933
        }

    def setobjects(self, objs:dict):
        self.objects = objs

    def setparams(self, params:dict):
        self.params = params

    def addobject(self, obj: str, params: dict):
        extraparams = ""
        for param, value in params.items():
            if self.params.get(param) is not None:
                pid = self.params[param]
                extraparams += f",{str(pid)},{value}"
            else:
                extraparams += f",{str(param)},{value}"

        oid = self.objects.get(obj, 1)
        if oid:
            objects.append(
                f"1,{str(oid)},2,{str(params.get('X') * 30 + 15)},3,{str(params.get('Y') * 30 + 15)}{extraparams}")
        else:
            objects.append(
                f"1,{str(obj)},2,{str(params.get('X') * 30 + 15)},3,{str(params.get('Y') * 30 + 15)}{extraparams}")

    def create_gmd_file(self, level_name, author_name, objects_string):
        global lvlname
        lvlname = level_name
        final_string_to_pack = objects_string
        gzipped = gzip.compress(final_string_to_pack.encode('utf-8'))
        b64_objects = base64.b64encode(gzipped).decode('utf-8').replace('/', '_').replace('+', '-')
        return f'''<?xml version="1.0"?><plist version="1.0" gjver="2.0"><dict><k>kCEK</k><i>4</i><k>k2</k><s>{level_name}</s><k>k4</k><s>{b64_objects}</s><k>k5</k><s>{author_name}</s><k>k11</k><i>1091</i><k>k16</k><i>1</i><k>k80</k><i>56</i></dict></plist>'''

    def decode_objects(self):
        global obj_string
        obj_string = ";".join(objects) + ";"
        return obj_string
