import os
import json
import uuid
import shared
import shutil

class ExtensionsManager:
    def __init__(self):
        pass
    
    def loads(self):
        print("loading extensions")
        for i in os.listdir('addons/extensions'):
            if not os.path.isdir(f'addons/extensions/{i}'):
                continue
            for j in os.listdir(f'addons/extensions/{i}'):
                if j.endswith('.json'):
                    with open(f'addons/extensions/{i}/{j}', 'r') as f:
                        data = json.load(f)
                        if not data['installed']:
                            data['uuid'] = str(uuid.uuid4())
                            data['installed'] = True
                            with open(f'addons/extensions/{i}/{j}', 'w') as f:
                                json.dump(data, f, indent=4)
                        new_dir = f'addons/extensions/{data["uuid"]}'
                    shared.EXTENSIONS_LISTS[data["uuid"]] = data
    def check_for_start_page_extension(self):
        for i in shared.EXTENSIONS_LISTS:
            try:
                if shared.EXTENSIONS_LISTS[i]['start_page']:
                    print("start page found!")
                    i = json.loads(json.dumps(shared.EXTENSIONS_LISTS[i]))
                    return i["start_page"]
                break
            except:
                pass
        return None
    def get_extension_conf(self, uuid):
        for i in shared.EXTENSIONS_LISTS:
            if i == uuid:
                return shared.EXTENSIONS_LISTS[i]
        return None
    def check_for_inject_code_js(self, url):
        INJECT_LIST = []
        for i in shared.EXTENSIONS_LISTS:
            if isinstance(shared.EXTENSIONS_LISTS[i], dict) and 'injects' in shared.EXTENSIONS_LISTS[i]:
                if "INJECT_CODE_JS" not in shared.EXTENSIONS_LISTS[i]["authorizations"]:
                    continue
                for inject in shared.EXTENSIONS_LISTS[i]['injects']:
                    if inject["domain"] == url.toString():
                        settings = self.get_extension_conf(i)
                        ipatch = {
                            "path": f"addons/extensions/{settings['name']}/{inject['code']}",
                            "type": inject["type"]
                        }
                        INJECT_LIST.append(ipatch)
        return INJECT_LIST if INJECT_LIST else None
