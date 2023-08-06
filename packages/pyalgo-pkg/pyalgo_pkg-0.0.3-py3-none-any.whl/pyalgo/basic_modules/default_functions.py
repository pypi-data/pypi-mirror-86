from . import default_values
import copy



def to_single_list(List):  # // needs to be optimized \\
                           # // may use a regression \\

    """
    This function takes a list and moving out the
    sub lists until there is no sublists
    """

    List = copy.deepcopy(List)  # deep copy the list to not make a reference

    dumbList = []
    ListType = type(dumbList)

    if not isinstance(List, ListType): raise TypeError("You need to enter a list")

    is_single_list = True

    while is_single_list:
        for i in range(len(List)):
            if isinstance(List[i], ListType):

                is_single_list = False

                length = len(List[i])
                transferList = List[i]

                del List[i]

                for j in range(length):
                    List.insert(i, transferList[-1-j])

        is_single_list = not is_single_list

    return List


def print_list_arguments(List, Tag="-->", print_the_msg=True, return_msg=True):

    """
    This function takes a list and prints its arguments separated with the Tag first

    example:

    option number {the number of the argument}:  {Tag} {The arguments}

    :param List: this should be a list
    :param Tag: This should be a string
    :return: this function doesn't returns anything
    """

    msg = ""

    # // check that the type of the inputs are valid to this function \\
    if not isinstance(List, default_values.ListType):
        raise TypeError("'List' should be a list type")
    if not isinstance(Tag, default_values.StringType):
        raise TypeError("'Tag' should be a String type")


    for i in range(len(List)):
        if print_the_msg:
            print("option number {0}:  {1} {2}".format(i+1, Tag, List[i]))

        msg += "option number {0}:  {1} {2}".format(i+1, Tag, List[i])
        msg += "\n"

    if return_msg: return msg