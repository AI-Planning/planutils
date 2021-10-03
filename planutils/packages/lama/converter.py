import json

planner_template={
  "args": [
        {
          "name": "domain",
          "type": "file",
          "description": "domain file"
        },
        {
          "name": "problem",
          "type": "file",
          "description": "problem file"
        }
  ],
  "call": "{package_name} {domain} {problem}",
  "return": {
    "type": "json",
    "file": "plans.json"
  }
}

def get_template(template_name):
    if template_name=="planner":
        return planner_template
    return planner_template

def generate_full_manifest(manifest):
    with open(manifest, 'r') as f:
        manifest = json.load(f)
    new_manifest=manifest.copy()

    for service in manifest["endpoint"]["services"]:
        service_body=manifest["endpoint"]["services"][service]
        if "template" in service_body:
            template_name=service_body["template"]
            template=get_template(template_name)
            new_service_body=template.copy()
            # update addtional args

            for key in template:
                if key in service_body:
                    if key=="args":
                        for arg in service_body["args"]:
                            new_service_body["args"].append(arg)
                    else:
                        #update call, return
                        new_service_body[key]=service_body[key]
            new_service_body["call"]=new_service_body["call"].replace("{package_name}",manifest["name"].lower())
            new_manifest["endpoint"]["services"][service]=new_service_body

    with open("manifest_full.json", 'w') as f:
        f.write(json.dumps(new_manifest))

generate_full_manifest("manifest.json")  



            
