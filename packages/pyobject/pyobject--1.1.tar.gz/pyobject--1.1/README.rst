pyobject - һ��Python���������ģ�顣A python object browser with tkinter and command-lines.

������ģ�� Included modules: 
============================

pyobject.browser - ��ͼ�η�ʽ���Python����
pyobject.search - ����python����
pyobject.newtypes - ����һЩ�µ�����

�����ĺ��� Functions:
===========================
objectname(obj)

    objectname(obj) - ����һ�����������,����xxmodule.xxclass��
    ��:objectname(int) -> 'builtins.int'

bases(obj, level=0, tab=4)

    bases(obj) - ��ӡ���ö���Ļ���
    tab:�����Ŀո���,Ĭ��Ϊ4��

describe(obj, level=0, maxlevel=1, tab=4, verbose=False, file=sys.stdout, mode='w' encoding='utf-8')

    "����"һ������,����ӡ������ĸ������ԡ�
    ����˵��:
    maxlevel:��ӡ�������ԵĲ�����
    tab:�����Ŀո���,Ĭ��Ϊ4��
    verbose:һ������ֵ,�Ƿ��ӡ����������ⷽ��(��__init__)��
    file:һ�������ļ��Ķ���


browse(object, verbose=False, name='obj')

    ��ͼ�η�ʽ���һ��Python����
    verbose:��describe��ͬ,�Ƿ��ӡ����������ⷽ��(��__init__)

�������� New Functions:
=============================

make_list(start_obj, recursions=2, all=False)

    ����һ��������б�
    start:��ʼ�����Ķ���
    recursion:�ݹ����
    all:�Ƿ񽫶������������(��__init__)�����б�


search(obj, start, recursions=3)

    ��һ����㿪ʼ��������
    obj:�������Ķ���
    start:������
    recursion:�ݹ����

���� Author:
*�߷ֳ��� qq:3076711200 ����:3416445406@qq.com*