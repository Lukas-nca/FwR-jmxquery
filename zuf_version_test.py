from collections import defaultdict
from typing import Dict
import re
from tqdm import trange
from file_utils import *
from call_jmx_method import *


def tsleep(seconds: int):
    if seconds > 0:
        for _ in trange(seconds):
            time.sleep(1)


def print_non_increasing_versions(zufId, versions, baseseed):
    text = f"{time.ctime()} - Found non increasing versions (seed: {baseseed}): {zufId}, {versions}\n"
    print(text)
    # save_to_file(text, os.path.join("C:\\", "devsbb", "tmp", "version-test", "result.txt"), mode='a')


def print_not_ok(dic):
    text = f"{time.ctime()} - ERROR Versions NOT ok: {print_dict('', dic)}\n"
    print(text)
    save_to_file(text, os.path.join("C:\\", "devsbb", "tmp", "version-test", "result.txt"), mode='a')


def print_dict(text: str, d: Dict):
    s = ""
    if text:
        s = text+NEWLINE
    for k, v in d.items():
        s += f"{k}: {v}{NEWLINE}"
    print(s)
    return s


def handle_line(line, verbose=False):
    REGEX = re.compile(r"Zugfahrt (\d*) .* hat version: (\d*)")
    match = REGEX.findall(line)
    if verbose:
        print(line, '->', match)
    zufId = int(match[0][0])
    version = int(match[0][1])

    return zufId, version


def check_version_dict(zufId_to_version: Dict, baseseed):
    ok = True
    for zufId, versions in zufId_to_version.items():
        # ignore seed version
        adj_versions = [v for v in versions if v != baseseed+1]
        if sorted(adj_versions) != adj_versions:
            print_non_increasing_versions(zufId, versions, baseseed)
            ok = False
    return ok


def call(processname, save_filepath):
    call_methods_and_save(
        [
            method_fwr_on_nodeId(processname, "getAllZugfahrtenVersionen", [])
        ],
        save_filepath, savemode='w')


def kill(processname):
    call_single_method(method_fwr_on_nodeId(processname, "kill", []))


def get_version_seed(processname, verbose=True):
    res = call_single_method(method_fwr_on_nodeId(processname, "getAllZugfahrtenVersionen", []))
    REGEX = re.compile(r"version seed: (\d*)(\s+)")
    match = REGEX.findall(res)
    seed = int(match[0][0])

    if verbose:
        print("version seed for ", processname, "is", seed)

    return seed


def print_test_paramns(max_calls, period, test_failover, activ_process, failover_process):
    print("active process: ", activ_process, "failover_process: ", failover_process)

    if max_calls == float('inf'):
        print("Running until interrupted (CTRL+C) every", period, "seconds")
    else:
        print("Doing", max_calls, "calls every", period, "seconds")

    if 0 < test_failover < float('inf'):
        print("And testing a failover at call", test_failover)


def zuf_version_test(max_calls=20, period=5, test_failover=10):
    """
    Vorgehensweise:
    Starte 2 prozesse
    trage den aktiven als aktiv und der andere als passiv ein (unten)
    """
    activ_process: str = 'K57077.16300'
    failover_process: str = 'K57077.4132'

    print_test_paramns(max_calls, period, test_failover, activ_process, failover_process)

    activ_seed = get_version_seed(activ_process)
    failover_seed = get_version_seed(failover_process)

    currprocname = activ_process
    currseed = activ_seed

    zuf_id_to_versions = defaultdict(list)
    count = 1
    while count <= max_calls:
        try:
            print("\nRun", count, flush=True)
            if count == test_failover:
                kill(currprocname)
                print("\n killed ", currprocname)
                currprocname = failover_process
                currseed = failover_seed
                tsleep(30)

            save_filepath = os.path.join("C:\\", "devsbb", "tmp", "version-test", f"{currprocname}_{count}.txt")

            call(currprocname, save_filepath)

            lines = file_to_lines(save_filepath, strip_=True)
            print(lines[0])
            for line in lines[1:]:
                zufId, version = handle_line(line)
                if len(zuf_id_to_versions[zufId]) == 0 or zuf_id_to_versions[zufId][-1] != version:
                    zuf_id_to_versions[zufId].append(version)

            if not check_version_dict(zuf_id_to_versions, baseseed=currseed):
                print_not_ok(zuf_id_to_versions)

            count += 1
            print("\nNext call in:")
            tsleep(period)
        except KeyboardInterrupt as ki:
            print("keyboard interrupt. exiting...")
            print_dict("zuf_id_to_versions:", zuf_id_to_versions)
            exit(0)

    print_dict("zuf_id_to_versions:", zuf_id_to_versions)


if __name__ == '__main__':
    zuf_version_test()
