import os
import sys

sys.path.insert(1, '../driver')
import utils

#TODO: move into builder
#with utils.chdir(os.path.join(utils.config.RepoPath, self.source)):
#    self.env['DYLD_FRAMEWORK_PATH'] = os.path.abspath('WebKitBuild/Release'))
#self.omit = False

class Default(object):
    def __init__(self, engine, shell):
        self.args_ = []
        self.env_ = {}
        self.profile_ = ""
        self.omit_ = False

        if engine == "firefox":
            self.env_["JSGC_DISABLE_POISONING"] = "1"
            self.profile_ += "user_pref(\"dom.max_script_run_time\", 0);\n"
        elif engine == "chrome":
            pass
        elif engine == "webkit":
            pass
        elif engine == "ie":
            pass
        elif engine == "edge":
            pass
        elif engine == "servo":
            pass
        else:
            self.omit_ = True

    def omit(self):
        return self.omit_
        
    def args(self):
        return self.args_

    def env(self):
        return self.env_

    def profile(self):
        # Currently only for firefox profile js file.
        return self.profile_

class UnboxedObjects(Default):
    def __init__(self, engine, shell):
        super(UnboxedObjects, self).__init__(engine, shell)
        if engine == "firefox":
            if shell:
                self.args_.append("--unboxed-arrays")
            self.env_["JS_OPTION_USE_UNBOXED_ARRAYS"] = '1'
        else:
            self.omit_ = True

class TestbedRegalloc(Default):
    def __init__(self, engine, shell):
        super(TestbedRegalloc, self).__init__(engine, shell)
        if engine == "firefox":
            self.args_.append("--ion-regalloc=testbed")
        else:
            self.omit_ = True

class TurboFan(Default):
    def __init__(self, engine, shell):
        super(TurboFan, self).__init__(engine, shell)
        if engine == "chrome"and shell:
            self.args_.append("--turbo");
        else:
            self.omit_ = True

class NoAsmjs(Default):
    def __init__(self, engine, shell):
        super(NoAsmjs, self).__init__(engine, shell)
        if engine == "firefox" and shell:
            self.args_.append("--no-asmjs");
        else:
            self.omit_ = True
            
class NonWritableJitcode(Default):
    def __init__(self, engine, shell):
        super(NonWritableJitcode, self).__init__(engine, shell)
        if engine == "firefox" and shell:
            self.args_.append("--non-writable-jitcode");
        else:
            self.omit_ = True

class NoE10S(Default):
    def __init__(self, engine, shell):
        super(NoE10S, self).__init__(engine, shell)
        if engine == "firefox" and not shell:
            self.profile_ += "user_pref(\"browser.tabs.remote.autostart\", false);\n"
            self.profile_ += "user_pref(\"browser.tabs.remote.autostart.1\", false);\n"
            self.profile_ += "user_pref(\"browser.tabs.remote.autostart.2\", false);\n"
            self.profile_ += "user_pref(\"browser.tabs.remote.autostart.3\", false);\n"
            self.profile_ += "user_pref(\"browser.tabs.remote.autostart.4\", false);\n"
        else:
            self.omit_ = True

class E10S(Default):
    def __init__(self, engine, shell):
        super(E10S, self).__init__(engine, shell)
        if engine == "firefox" and not shell:
            self.profile_ += "user_pref(\"browser.tabs.remote.autostart\", true);\n"
            self.profile_ += "user_pref(\"browser.tabs.remote.autostart.1\", true);\n"
            self.profile_ += "user_pref(\"browser.tabs.remote.autostart.2\", true);\n"
            self.profile_ += "user_pref(\"browser.tabs.remote.autostart.3\", true);\n"
            self.profile_ += "user_pref(\"browser.tabs.remote.autostart.4\", true);\n"
        else:
            self.omit_ = True

def getConfig(name, info):
    if name == "default":
        return Default(info["engine_type"], info["shell"])
    if name == "unboxedobjects":
        return UnboxedObjects(info["engine_type"], info["shell"])
    if name == "testbedregalloc":
        return TestbedRegalloc(info["engine_type"], info["shell"])
    if name == "turbofan":
        return TurboFan(info["engine_type"], info["shell"])
    if name == "noasmjs":
        return NoAsmjs(info["engine_type"], info["shell"])
    if name == "nonwritablejitcode":
        return NonWritableJitcode(info["engine_type"], info["shell"])
    if name == "noe10s":
        return NoE10S(info["engine_type"], info["shell"])
    if name == "e10s":
        return E10S(info["engine_type"], info["shell"])
    raise Exception("Unknown config")
