from Scope import Scope

#Script files have to be UTF-8-BOM and utf-8-sig is compatible with that and LF new line to be interpreted in the game
script = open("../eg _scrip_files/no_scope_change_no_comments.txt","r",encoding="utf-8-sig",newline="\n")
this_scope = Scope(script.read())
print(this_scope)