
import glob, os, subprocess, tempfile, requests, time, sys

from planutils.package_installation import PACKAGES, check_installed
from planutils import settings

def run_server(port, host):

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

    app.run(port=port, host=host)


def package_remote_list():

    package_url = settings.PAAS_SERVER + "/package"
    r = requests.get(package_url)
    remote_packages = r.json()

    print("\nDeployed:")
    for p in remote_packages:
        arguments = " ".join(f'{{{a["name"]}}} ' for a in p['endpoint']['services']['solve']['args'])
        print("  %s: %s\n\tArguments: %s" % (p['package_name'], p['name'], arguments ))

def remote(target, options):

    # 1. check if the target is deployed

    package_url = settings.PAAS_SERVER + "/package"
    r = requests.get(package_url)
    remote_packages = r.json()

    remote_package = None
    for p in remote_packages:
        if p['package_name'] == target:
            remote_package = p
            break

    if (remote_package is None) or ('solve' not in remote_package['endpoint']['services']):
        sys.exit(f"Package {target} is not remotely deployed")


    # 2. unpack the options and target to the right json

    json_options = {}
    remote_call = remote_package['endpoint']['services']['solve']['call']
    call_parts = remote_call.split(' ')

    args = {arg['name']: arg for arg in remote_package['endpoint']['services']['solve']['args']}

    if len(options) != len(args):
        sys.exit(f"Call string does not match the remote call: {remote_package['endpoint']['services']['solve']['call']}")

    call_map = {}
    for i, step in enumerate(call_parts[1:]):
        if '{' == step[0] and '}' == step[-1]:
            option = step[1:-1]
            call_map[option] = options[i]
            if option not in args:
                sys.exit(f"Option {option} from call string is not defined in the remote call: {remote_call}")
            if args[option]['type'] == 'file':
                with open(options[i], 'r') as f:
                    json_options[option] = f.read()
            else:
                json_options[option] = options[i]

    rcall = remote_call
    for k, v in call_map.items():
        rcall = rcall.replace('{' + k + '}', v)
    print("\nMaking remote call: %s" % rcall)


    # 3. run the remote command

    solve_url = '/'.join([settings.PAAS_SERVER, 'package', target, 'solve'])
    r = requests.post(solve_url, json=json_options)
    if r.status_code != 200:
        sys.exit(f"Error running remote call: {r.text}")

    result_url = f"{settings.PAAS_SERVER}/{r.json()['result']}"

    # call every 0.5s until the result is ready
    result = None
    for _ in range(settings.PAAS_SERVER_LIMIT):
        r = requests.get(result_url)
        if (r.status_code == 200) and ('status' in r.json()) and (r.json()['status'] == 'ok'):
            result = r.json()['result']
            break
        time.sleep(0.5)

    if result is None:
        sys.exit(f"Error running remote call: {r.text}")


    # 4. unpack the results back to the client, including any new files

    result = r.json()['result']
    for fn in result['output']:
        with open(fn, 'w') as f:
            f.write(result['output'][fn])

    print("\n\t{stdout}\n")
    print(result['stdout'])
    print("\n\t{stderr}\n")
    print(result['stderr'])
