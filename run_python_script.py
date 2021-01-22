import cProfile
import sys
from time import time
script_names = ["simulate", "solution_1", "solution_2", "solution_3", "validate",
                "plots", "all"]


def run_python_script(script_name, *args, **kwargs):
    if 'profiler' in kwargs:
        use_profiler = True
    else:
        use_profiler = False

    if script_name == "simulate":
        from scripts import simulate as executable_script
    elif script_name == "solution_1":
        from scripts import solution_1 as executable_script
    elif script_name == "solution_2":
        from scripts import solution_2 as executable_script
    elif script_name == "solution_3":
        from scripts import solution_3 as executable_script
    elif script_name == "solution_4":
        from scripts import solution_4 as executable_script
    elif script_name == "validate":
        from scripts import validate as executable_script
    elif script_name == "plots":
        from scripts import plots as executable_script
    elif script_name == "all":
        from scripts import all as executable_script
    else:
        message = "Error, script_name ({}) must be one of {}".format(script_name, script_names)
        raise ValueError(message)

    if profiler:
        print("Running with profiler")
        command = "executable_script.main(*args)"
        filename = "%s.prof" % script_name
        start_time = time()
        cProfile.runctx(command, None, locals(), filename=filename)
        runtime = time() - start_time
        print('Runtime: %0.7f seconds' % runtime)
        print("To see profiler result, run:\nsnakeviz %s" % filename)
    else:
        executable_script.main(*args)


if __name__ == "__main__":
    profiler = ' -p' in ' '.join(sys.argv)
    script = sys.argv[1]
    arguments = sys.argv[2:]

    # remove the profile flag now that profiler is on
    arguments = [i for i in arguments if i != '-p']
    run_python_script(script, *arguments, profiler=profiler)
