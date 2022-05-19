import json
from collections import OrderedDict
import glob
import os
import copy
import shutil


def load_json(f_name):
    with open(f_name, 'r') as f:
        json_body = json.load(f,object_pairs_hook=OrderedDict)
    return json_body

def save_json(f_name,f_content):
    with open(f_name, 'w') as f:
        f.write(json.dumps(f_content,indent=4, sort_keys=False, separators=(',', ': ')))

def load_template(template_dir):
    service_templates={}
    templates_name_list=glob.glob(os.path.join(template_dir,'*.json'))
    for template_file_address in templates_name_list:
        template_name=os.path.basename(template_file_address).split(".")[0]
        service_template_body=load_json(template_file_address)
        service_templates[template_name]=service_template_body
    return service_templates


def generate_full_manifest(service_templates,manifest,package_name):
    manifest_full=copy.deepcopy(manifest)
    for service in manifest["endpoint"]["services"]:
        service_body=manifest["endpoint"]["services"][service]
        if "template" in service_body:
            template_name=service_body["template"]
            template=service_templates.get(template_name,{})
            new_service_body=copy.deepcopy(template)
            # update addtional args
            for key in template:
                if key in service_body:
                    if key=="args":
                        for arg in service_body["args"]:
                            new_service_body["args"].append(arg)
                    else:
                        #update call, return
                        new_service_body[key]=service_body[key]
            new_service_body["call"]=new_service_body["call"].replace("{package_name}",package_name)
            manifest_full["endpoint"]["services"][service]=new_service_body
    return manifest_full

def generate_manifest():
    CUR_DIR=os.path.dirname(os.path.abspath(__file__))
    TEMPLATE_DIR=os.path.join(CUR_DIR, "packages", "TEMPLATE","SERVICE_TEMPLATE")
    PACKAGE_DIR = os.path.join(CUR_DIR, "packages")
    service_templates=load_template(TEMPLATE_DIR)
    # generate full manifest if manifest_compact.json is provided
    for conf_file in glob.glob(os.path.join(PACKAGE_DIR, '*')):
        base = os.path.basename(conf_file)
        if base not in ['README.md', 'TEMPLATE']:
            manifest_loc=os.path.join(conf_file, 'manifest.json')
            # Check if "template" is in manifest.json
            with open(manifest_loc, 'r') as f:
                contents = f.read()
            if "template" in contents:
                manifest_loc_bak=os.path.join(conf_file, 'manifest.json.bak')
                if os.path.exists(manifest_loc_bak):
                    os.remove(manifest_loc_bak)
                shutil.copy(manifest_loc, manifest_loc_bak)
                manifest_compact=load_json(manifest_loc)
                manifest_full=generate_full_manifest(service_templates,manifest_compact,base)
                save_json(manifest_loc,manifest_full)

