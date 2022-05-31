
import glob, os, subprocess, tempfile

from planutils.package_installation import PACKAGES, run
from planutils import settings

def run_server(port):

    # Check if flask is installed
    try:
        import flask
    except ImportError:
        print("Flask is not installed. Please install it with 'pip install flask'.")
        return

    from flask import Flask, jsonify, request
    app = Flask(__name__)

    @app.route('/package/<package>/<service>', methods=['GET', 'POST'])
    def runPackage(package, service):
        # Get request
        if request.method == 'GET':
            # This is where we will send the user to the API documentation
            if package in PACKAGES:
                return jsonify(PACKAGES[package])
            else:
                return jsonify({"Error":"That package does not exist"})

        # Post request
        elif request.method == 'POST':
            if package in PACKAGES:
                if service in PACKAGES[package]:

                    argmap = {}
                    for arg in PACKAGES[package][service]['args']:
                        argmap[arg['name']] = arg
                    callstring = PACKAGES[package][service]['call']
                    returnconfig = PACKAGES[package][service]['return']

                    temp_dir = tempfile.TemporaryDirectory()

                    # get the arguments and compare with the arguments in the package call string
                    args = request.get_json()
                    for arg in args:
                        if arg not in argmap:
                            return jsonify({"Error":f"argument {arg} does not exist in config"})
                        if "{"+arg+"}" not in callstring:
                            return jsonify({"Error":f"argument {arg} does not exist in call string"})

                        if argmap[arg]['type'] == 'file':
                            with open(os.path.join(temp_dir.name, arg), 'w') as f:
                                f.write(args[arg])
                            callstring.replace("{"+arg+"}", os.path.join(temp_dir.name, arg))
                        else:
                            callstring.replace("{"+arg+"}", args[arg])

                    if '{' in callstring:
                        return jsonify({"Error":"Not all arguments were provided - "+callstring})

                    executable = os.path.join(settings.PLANUTILS_PREFIX, "packages", callstring.split()[0], "run")
                    os.chdir(temp_dir.name)
                    subprocess.run([executable] + callstring.split()[1:])
                    # run(callstring.split()[0], callstring.split()[1:])

                    to_return = {}

                    generated_files = glob.glob(os.path.join(temp_dir.name, returnconfig['files']))
                    for fn in generated_files:
                        with open(fn, 'r') as f:
                            to_return[os.path.basename(fn)] = f.read()

                    # remove the temporary files
                    temp_dir.cleanup()

                    return jsonify(PACKAGES[package][service])
                else:
                    return jsonify({"Error":"That service does not exist"})
            else:
                return jsonify({"Error":"That package does not exist"})

    app.run(port=port)

"""
{
    "dependencies": [
        "downward"
    ],
    "description": "http://fast-downward.org/",
    "endpoint": {
        "services": {
            "solve": {
                "args": [
                    {
                        "description": "domain file",
                        "name": "domain",
                        "type": "file"
                    },
                    {
                        "description": "problem file",
                        "name": "problem",
                        "type": "file"
                    }
                ],
                "call": "lama {domain} {problem}",
                "return": {
                    "files": "*plan*",
                    "type": "generic"
                }
            }
        }
    },
    "install-size": "20K",
    "name": "LAMA",
    "runnable": true
}
"""

