import inspect, json, re, sys


def pobj(obj):
    # print('---type---', type(obj).__name__ )
    t_obj = str(type(obj).__name__)
    size_obj = sys.getsizeof(obj)
    frame = inspect.currentframe().f_back
    s = inspect.getframeinfo(frame).code_context[0]
    r = re.search(r"\((.*)\)", s).group(1)
    if t_obj in ['dict', 'ReturnDict']:
        p_obj = json.dumps(obj, indent=2, sort_keys=True)
    elif t_obj in ['Request', 'WSGIRequest', 'SessionStore']:
        p_obj = vars(obj)
    else:
        p_obj = obj
    print('\n\n---{}---type:{}---size:{}-bytes---\n{}'.format(r, t_obj, size_obj, p_obj))
