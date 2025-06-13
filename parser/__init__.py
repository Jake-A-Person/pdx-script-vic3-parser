from Scope import Scope

#Script files have to be UTF-8 and LF new line to be interpreted in the game
script = open("../eg _scrip_files/no_comments_50_sick_us_dtnw.txt","r",encoding="UTF-8",newline="\n")
this_scope = Scope(script.read())
print(this_scope)