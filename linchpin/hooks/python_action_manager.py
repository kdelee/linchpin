from action_manager import ActionManager
import sys
import subprocess
from cerberus import Validator


class PythonActionManager(ActionManager):
    def __init__(self, name, action_data, target_data, **kwargs):
        self.name = name
        self.action_data = action_data
        self.target_data = target_data
        self.context = kwargs.get('context', True)
        self.kwargs = kwargs

    def validate(self):
        schema= {
        'name': {'type': 'string', 'required': True },
        'type': { 'type': 'string', 'allowed': ['python']},
        'path': {'type': 'string', 'required': False},
        'context': {'type': 'boolean', 'required': False},
        'actions': { 
                     'type': 'list',
                     'schema': {'type':'string'},
                     'required': True
                   }
        }
        v = Validator(schema)
        status = v.validate(self.action_data)
        if not status:
            raise Exception("Invalid syntax: LinchpinHook:"+str((v.errors)))
        else:
            return status 

    def add_ctx_params(self, file_path, context=True):
        if not context:
            return "{0} {1}".format(sys.executable, 
                                    file_path)
        params = ""
        for key in self.target_data:
            params += " %s=%s " %(key, self.target_data[key])
        return "{0} {1} {2}".format(sys.executable,
                                    file_path,
                                    params)

    def execute(self):
        print("Execute module of PythonActionManager")
        for action in self.action_data["actions"]:
            context = self.action_data.get("context", True)
            path = self.action_data["path"]
            file_path = "{0}/{1}".format(
                        path,
                        action
                        )
            command = self.add_ctx_params(file_path, context)
            proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
            proc.wait()
            for line in proc.stdout:
                print(line)
