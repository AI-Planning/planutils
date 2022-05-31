
import glob, os, subprocess, tempfile

from planutils.package_installation import PACKAGES, check_installed
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
    app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

    def _confirm_available(package):
        if package not in PACKAGES:
            return {"error": "Package not found"}
        if "endpoint" not in PACKAGES[package] or not PACKAGES[package]["runnable"]:
            return {"error": "Package not runnable as a service"}
        if not check_installed(package):
            return {"error": "Package not installed"}
        return PACKAGES[package]

    @app.route('/package')
    def show_packages():
        available = {}
        for package in PACKAGES:
            if "endpoint" in PACKAGES[package] and PACKAGES[package]["runnable"] and check_installed(package):
                available[package] = PACKAGES[package]
        return jsonify(available)

    @app.route('/package/<package>')
    def show_package(package):
        return jsonify(_confirm_available(package))

    @app.route('/package/<package>/<service>', methods=['GET', 'POST'])
    def runPackage(package, service):
        # Get request
        if request.method == 'GET':
            return show_package(package)

        # Post request
        elif request.method == 'POST':
            pkg = _confirm_available(package)
            if 'error' in pkg:
                return jsonify(pkg)
            if service not in pkg["endpoint"]["services"]:
                return jsonify({"error": "Service not found"})
            service = pkg["endpoint"]["services"][service]

            argmap = {}
            for arg in service['args']:
                argmap[arg['name']] = arg
            callstring = service['call']
            returnconfig = service['return']

            temp_dir = tempfile.mkdtemp()

            # get the arguments and compare with the arguments in the package call string
            args = request.get_json()
            for arg in args:
                if arg not in argmap:
                    return jsonify({"error":f"argument {arg} does not exist in config"})
                if "{"+arg+"}" not in callstring:
                    return jsonify({"error":f"argument {arg} does not exist in call string"})

                if argmap[arg]['type'] == 'file':
                    with open(os.path.join(temp_dir, arg), 'w') as f:
                        f.write(args[arg])
                    callstring = callstring.replace("{"+arg+"}", os.path.join(temp_dir, arg))
                else:
                    callstring = callstring.replace("{"+arg+"}", args[arg])

            if '{' in callstring:
                return jsonify({"error":"Not all arguments were provided - "+callstring})

            executable = os.path.join(settings.PLANUTILS_PREFIX, "packages", callstring.split()[0], "run")
            call = ' '.join([executable] + callstring.split()[1:])

            res = subprocess.run(call, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                            executable='/bin/bash',  encoding='utf-8',
                            shell=True, cwd=temp_dir)

            to_return = {
                "stdout": res.stdout,
                "stderr": res.stderr,
            }

            generated_files = glob.glob(os.path.join(temp_dir, returnconfig['files']))
            for fn in generated_files:
                with open(fn, 'r') as f:
                    to_return[os.path.basename(fn)] = f.read()

            # remove the temporary files
            os.system(f"rm -rf {temp_dir}")

            return jsonify(to_return)

    app.run(port=port)

