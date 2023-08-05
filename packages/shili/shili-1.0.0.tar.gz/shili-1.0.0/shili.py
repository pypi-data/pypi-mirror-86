def print_lol(the_list,level):
    for each_iterm in the _list:
        if isinstance(each_iterm,list):
            print_lol(each_iterm,level+1)
        else:
            for tab_stop in range(level):
                print("\t",end='')
            print(each_iterm)
