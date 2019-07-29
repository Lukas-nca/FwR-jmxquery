from typing import Union
import sys

from jmxquery import *
import logging

from file_utils import *

logging.getLogger().setLevel(logging.DEBUG)

XAVER_JMX_CONNECTION_URI = "service:jmx:rmi:///jndi/rmi://rcsxaver1:2099/rcs"

JMX_USER = file_to_lines("./passwords")[0].strip()
JMX_PASSWORD = file_to_lines("./passwords")[1].strip()

print(JMX_USER, JMX_PASSWORD)

NEWLINE = "\n"

CON_JMX_XAVER = JMXConnection(connection_uri=XAVER_JMX_CONNECTION_URI, jmx_username=JMX_USER, jmx_password=JMX_PASSWORD)


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
    return JMXMethod(
        f"Processes:name=FahrwegRechner,type=ServerProcess,process=FahrwegRechner,nodeId={nodeId}",
        methodName, params=params if params else list())


def call_single_query(query: JMXQuery, print_result=False):
    jmx_query = [query]
    metrics = CON_JMX_XAVER.query(jmx_query)
    result_string = f"received {len(metrics)} metrics:"
    for metric in metrics:
        result_string += f"\n{metric.to_query_string()} ({metric.value_type}) = {metric.value}"
    if print_result:
        print(result_string)
    return result_string


def call_single_method(method: JMXMethod, print_result=False):
    result = CON_JMX_XAVER.call(method)
    if print_result:
        print(f"received result: {result}")
    return result


def test_connection():
    jmx_query = [JMXQuery("*:*/HeapMemoryUsage")]
    metrics = CON_JMX_XAVER.query(jmx_query)
    if len(metrics):
        print(f"received {len(metrics)} metrics. Connection OK :)")


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

    """
    # call_single_query(query_all_fwr_with_nodeId(XAVER_NODE_ID))
    print(f"====================== {MY_NODE_ID} ===========================")
    call_single_method(method_fwr_on_nodeId(MY_NODE_ID, "getAllAlternativeFahrwegeZugfahrten", [JMXParam("OL")]))
    call_single_method(method_fwr_on_nodeId(MY_NODE_ID, "getStoredPotenziellRelevanteZugfahrtenIds"))

    print(f"====================== {XAVER_NODE_ID} ===========================")
    call_single_method(method_fwr_on_nodeId(XAVER_NODE_ID, "getAllAlternativeFahrwegeZugfahrten", [JMXParam("OL")]))
    """
