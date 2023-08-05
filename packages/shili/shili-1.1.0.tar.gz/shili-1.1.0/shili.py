def print_lol(the_list,indent=False,level=0):
    for each_iterm in the_list:
        if isinstance(each_iterm,list):
            print_lol(each_iterm,indent,level+1)
        else:
            if indent:
               for tab_stop in range(level):
                print("\t",end='')
            print(each_iterm)
