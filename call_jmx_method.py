from typing import Union
import sys

from jmxquery import *
import logging

from file_utils import *

logging.getLogger().setLevel(logging.DEBUG)
NEWLINE = os.linesep

# Read the passwords file
passwordlines = file_to_lines("./passwords", strip_=True)
JMX_CONNECTION_URI = passwordlines[0]
JMX_USER = passwordlines[1]
JMX_PASSWORD = passwordlines[2]
#print(XAVER_JMX_CONNECTION_URI, JMX_USER, JMX_PASSWORD)
JMX_CONNECTION = JMXConnection(connection_uri=JMX_CONNECTION_URI, jmx_username=JMX_USER, jmx_password=JMX_PASSWORD)


def query_all_fwr_with_nodeId(nodeId: str):
    """
    :param nodeId: example: K57077.2028
    :return:
    """
    return JMXQuery(f"*:*,name=FahrwegRechner*,type=*,process=*,nodeId={nodeId}*")


def method_fwr_on_nodeId(nodeId: str, methodName: str, params: List[JMXParam] = None):
    """
    :param nodeId: example: K57077.2028
    :param methodName: example: getStoredPotenziellRelevanteZugfahrtenIds
    :param params:
    :return:
    """
    try:
        return JMXMethod(
            f"Processes:name=FahrwegRechner,type=ServerProcess,process=FahrwegRechner,nodeId={nodeId}",
            methodName, params=params if params else list())
    except Exception as e:
        print(f"exception wile calling JMXmethod. Does the nodeId {nodeId} exist?")
        raise e


def call_single_query(query: JMXQuery, print_result=False):
    jmx_query = [query]
    metrics = JMX_CONNECTION.query(jmx_query)
    result_string = f"received {len(metrics)} metrics:"
    for metric in metrics:
        result_string += f"\n{metric.to_query_string()} ({metric.value_type}) = {metric.value}"
    if print_result:
        print(result_string)
    return result_string


def call_single_method(method: JMXMethod, print_result=False):
    result = JMX_CONNECTION.call(method)
    if print_result:
        print(f"received result: {result}")
    return result


def test_connection():
    print("testing connection to ", JMX_CONNECTION.connection_uri, "...")
    jmx_query = [JMXQuery("*:*/HeapMemoryUsage")]
    metrics = JMX_CONNECTION.query(jmx_query)
    if len(metrics):
        print(f"received {len(metrics)} metrics. Connection OK :)")
    else:
        print("got response but no metrics:", metrics, "Probably NOT ok")


def call_methods_and_save(methods: Union[JMXMethod, List[JMXMethod]], filepath: str,
                          print_results=False, savemode='w'):
    if not hasattr(methods, "__iter__"):
        methods = [methods]
    result_str = NEWLINE
    for method in methods:
        try:
            answer = call_single_method(method, print_result=print_results)
            result_str += answer + NEWLINE
        except Exception as e:
            print(f"Error during method call {str(method)}. -> ignored \n{str(e)}", file=sys.stderr)

    save_to_file(result_str, filepath, mode=savemode)


if __name__ == '__main__':
    test_connection()
    """
    # call_single_query(query_all_fwr_with_nodeId(XAVER_NODE_ID))
    print(f"====================== {MY_NODE_ID} ===========================")
    call_single_method(method_fwr_on_nodeId(MY_NODE_ID, "getAllAlternativeFahrwegeZugfahrten", [JMXParam("OL")]))
    call_single_method(method_fwr_on_nodeId(MY_NODE_ID, "getStoredPotenziellRelevanteZugfahrtenIds"))

    print(f"====================== {XAVER_NODE_ID} ===========================")
    call_single_method(method_fwr_on_nodeId(XAVER_NODE_ID, "getAllAlternativeFahrwegeZugfahrten", [JMXParam("OL")]))
    """
