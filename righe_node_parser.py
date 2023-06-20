class Node:
    def __init__(self, id, fn, args, string_node):  # int, ccpar: int):
        self.id = id
        self.fn = fn
        self.args = args
        self.find = ''
        self.ccpar = ''
        self.string_node = string_node

    def __hash__(self):
        return hash((self.fn, self.args, self.find, self.ccpar, self.string_node))

    def __eq__(self, other):
        return isinstance(other, Node) and self.fn == other.fn and self.args == other.args and \
            self.find == other.find and self.ccpar == other.ccpar and self.string_node == other.string_node


# need a try catch
def is_integer(s):
    # TODO isinstance(variable, int)
    try:
        int(s)
        return True
    except ValueError:
        return False


def get_node(node_list, id_node):
    return next((node for node in node_list if node.id == id_node), None)


def find(node_list, id_node):
    n = get_node(node_list, id_node)
    if n.find == id_node:
        return id_node
    else:
        return find(node_list, n.find)


def union(node_list, id_node_1, id_node_2):
    n1 = get_node(node_list, find(node_list, id_node_1))
    n2 = get_node(node_list, find(node_list, id_node_2))
    n1.find = n2.find
    n2.ccpar = n1.ccpar + ',' + n2.ccpar
    n1.ccpar = ''


def ccpar(node_list, id_node):
    return (get_node(node_list, find(node_list, id_node))).ccpar


def congruent(node_list, id_node_1, id_node_2):
    n1 = get_node(node_list, id_node_1)
    n2 = get_node(node_list, id_node_2)

    if n1.fn != n2.fn or len(n1.args) != len(n2.args):
        return False

    n1_args = n1.args.split(',')
    n2_args = n2.args.split(',')

    for i in range(n1_args):
        if find(node_list, n1_args[i]) != find(node_list, n2_args[i]):
            return False

    return True


def merge(node_list, id_node_1, id_node_2):
    if find(node_list, id_node_1) != find(node_list, id_node_2):
        par_1 = ccpar(node_list, id_node_1).split(',')
        par_2 = ccpar(node_list, id_node_2).split(',')
        union(node_list, id_node_1, id_node_2)

        if par_1[0] != '' and par_2[0] != '':

            for p1 in par_1:
                for p2 in par_2:
                    if find(node_list, p1) != find(node_list, p2) and congruent(node_list, p1, p2):
                        merge(node_list, p1, p2)


def recursive_parser(expression: str, node_list):
    """
    1. find innermost parenthesis
    2. solve block
    """
    # find innermost parenthesis
    open_index, close_index = -1, -1
    innermost_block = ''
    for i, char in enumerate(expression):

        if char == '(':
            open_index = i
        elif char == ')':

            innermost_block = expression[open_index - 1:i + 1]
            close_index = i + 1
            break

    id_node_constant = len(node_list) + 1

    if innermost_block == '':

        if is_integer(expression):
            # if is an integer means node. I do not have to add it
            return (expression, node_list)

        # remains one literal
        fn = expression

        # create node
        args = ''
        string_node = fn
        node = Node(id_node_constant, fn, args, string_node)
        if node not in node_list:
            # if node was added
            node_list.append(node)
            id_node_constant += 1

        return (expression, node_list)

    # innermost block is f(a,b)
    innermost_block = innermost_block.replace(' ', '')
    func = innermost_block[0]
    literals = innermost_block[2:-1].split(',')

    #  id: int, fn: (int), args: [int], find: int, ccpar: int):
    args_fun = ''  # all id
    literals_strings = ''
    for fn in literals:

        # fn is string (a, b, c, x, y, z) or (0, 1, 2) indicating id of node (already created)
        if is_integer(fn):
            # do something when you have already initialize this node
            args_fun += f'{fn},'
            literals_strings += f'{get_node(node_list, int(fn)).string_node},'
        else:
            # create node
            args = ''
            string_node = fn
            node = Node(id_node_constant, fn, args, string_node)
            literals_strings += f'{string_node},'
            if node not in node_list:
                node_list.append(node)

            # if node was added
            if id_node_constant == len(node_list):
                args_fun += f'{id_node_constant},'
                id_node_constant += 1
            else:
                # node already exists
                for n in node_list:
                    if n.fn == fn:
                        args_fun += f'{n.id},'

    # create function
    fn = func
    args = args_fun[:-1]  # remove last comma

    string_node = fn + '(' + literals_strings[:-1] + ')'

    node = Node(id_node_constant, fn, args, string_node)
    if node not in node_list:
        node_list.append(node)

    # if was added
    if id_node_constant == len(node_list):
        innermost_block = f'{id_node_constant}'
    else:
        # node already exists
        for n in node_list:
            if n.fn == fn and n.args == args:
                innermost_block = f'{n.id}'

    expression = expression[:open_index - 1] + innermost_block + expression[close_index:]
    return recursive_parser(expression, node_list)


def set_ccpar(node_list):
    for n in node_list:
        if n.args != '':
            # node is a function
            fun_args = n.args.split(',')

            while len(fun_args) > 0:
                arg = fun_args[0]
                fun_args = fun_args[1:]

                this_node = get_node(node_list, int(arg))
                if this_node.args != '':
                    # this_node is a function
                    fun_args += this_node.args.split(',')
                else:
                    # this_node is a literal
                    if this_node.ccpar == '':
                        this_node.ccpar = f'{n.id}'
                    else:
                        ccpar_list = this_node.ccpar.split(',')
                        if str(n.id) not in ccpar_list:
                            this_node.ccpar += f',{n.id}'


def set_find(node_list):
    for n in node_list:
        n.find = n.id


def get_node_by_string(node_list, string_node):
    return next((node for node in node_list if node.string_node == string_node), None)
