"搜索python对象的模块"
import traceback

__all__=["make_list","search_obj"]

def _make_list(start_obj,level,recursions,_list,all=False):
    if level>=recursions:return

    for attr in dir(start_obj):
        if all or not attr.startswith("__"):
            try:
                obj=getattr(start_obj,attr)
                if obj not in _list:_list.append(obj)
                _make_list(obj,level+1,recursions,_list,all)
            except Exception:
                traceback.print_exc()
    if isinstance(start_obj,list):
        for item in start_obj:
            if item not in _list:_list.append(obj)
    if isinstance(start_obj,dict):
        for obj in start_obj.keys():
            if obj not in _list:_list.append(obj)
        for obj in start_obj.values():
            if obj not in _list:_list.append(obj)

def make_list(start_obj,recursions=2,all=False):
    """创建一个对象的列表。
start:开始搜索的对象
recursion:递归次数
all:是否将对象的特殊属性(如__init__)加入列表"""
    list=[]
    _make_list(start_obj,0,recursions,list,all)
    return list

def _search(obj,start_obj,level,_results,recursions=3,name="obj"):

    if level>=recursions:return
    for attrname in dir(start_obj):
        try:
            obj2=getattr(start_obj,attrname)
            _name="{}.{}".format(name,attrname)
            if obj == obj2:
                _results.append(_name)
            _search(obj,obj2,level+1,_results,recursions,_name)
        except Exception:
            #traceback.print_exc()
            pass

    if isinstance(start_obj,list):
        for i in range(len(start_obj)):
            _name="{}[{}]".format(name,i)
            if obj == start_obj[i]:
                _results.append(_name)
            _search(obj,obj2,level+1,_results,recursions,_name)

    if isinstance(start_obj,dict):
        for key in start_obj.keys():
            if key == obj:
                _results.append("字典 {} 的键".format(name))
            obj2=start_obj[key]
            _name="{}[{}]".format(name,key)
            if obj == obj2:
                _results.append(_name)
            _search(obj,obj2,level+1,_results,recursions,_name)


def search(obj,start,recursions=3):
    """从一个起点开始搜索对象
obj:待搜索的对象
start:起点对象
recursion:递归次数
"""

    results=[]
    _search(obj,start,0,results,recursions,
                name=getattr(obj,"__name__","obj"))
    return results

def test_make_list():
    import pprint
    import pyobject
    print(pprint.pformat(make_list(pyobject)))

def test_search():
    import pyobject
    print(search(pyobject.ObjectBrowser.load_image,pyobject))

if __name__=="__main__":
    #test_make_list()
    test_search()
