import pdx_script_vic3_parser.parser.commands.scope as scope
import pdx_script_vic3_parser.parser.commands.statement as stat
import pdx_script_vic3_parser.parser.util.util_statement as util_stat
import os

def gen_loc_for_sb(sb_name: str, law_group_str: str) -> str:
    law_group_space = law_group_str.replace("_"," ").title()
    return_val = sb_name + ': "1"'# + law_group_space + '"'
    return return_val
def gen_loc_desc_for_sb(sb_name: str, law_group_str: str) -> str:
    law_group_space = law_group_str.replace("_"," ").title()
    return_val = sb_name + '_desc : "Start a vote in if our current ' + law_group_space + ' law should be federation wide"'
    return return_val

input_dir = input("Path of directory with the files to make a modified copy of")
output_dir = input("Path of directory of the mod to place the modified copy")

pdx_law_new_files: dict[str,list[scope.Scope]] = dict()
pdx_scripted_button_file: list[scope.Scope] = []
pdx_sb_var_check: scope.Scope = scope.Scope()
pdx_sb_loc: str = "l_english:\n"

for filename in os.listdir(input_dir):
    #is a vick3 file and is not caste hegemony law as that is not applicable
    if filename.endswith('.txt') and filename != "00_caste_hegemony.txt":
        with (open(os.path.join(input_dir, filename), 'r',encoding="utf-8-sig", newline="\n") as file):
            this_files_laws:list[scope.Scope] = []
            #removes the 00_ and removes .txt from file name
            law_group = filename[3:-4]
            var_name = "ifp_federated_" + filename[3:-4] + "_var"
            parsed_law = scope.Scope(file.read())
            for law in parsed_law.get_scopes():
                eqv_scope = scope.Scope(name = "can_enact")
                can_enact_scope = law.find_eqv_scope(eqv_scope)
                if can_enact_scope is None:
                    can_enact_scope = eqv_scope
                    law.add_scope(eqv_scope)
                #check if valid subject type
                not_scope = scope.Scope(name = "not")
                can_enact_scope.add_scope(not_scope)
                not_scope.add_command(stat.Statement("is_subject","yes","="),0)
                not_scope.add_command(stat.Statement("is_subject_type","subject_type_ifp_fed_state","="),0)
                check_if_fed_law_scope = scope.Scope(name = "top_overlord")
                check_if_fed_law_scope.add_statement(stat.Statement("has_variable",var_name,"="))
                not_scope.add_scope(check_if_fed_law_scope)
                this_files_laws.append(law)

            pdx_law_new_files[filename] = this_files_laws
            #.append(this_files_laws)

            #create scripted button
            new_scripted_button_name = "je_ifp_federal_law_enact_" + law_group + "_sb"
            new_scripted_button = scope.Scope(name=new_scripted_button_name)
            new_scripted_button.add_command(stat.Statement("name",new_scripted_button_name,"="),0)
            new_scripted_button.add_command(stat.Statement("desc",new_scripted_button_name + "_desc","="),1)
            effect_scope = scope.Scope(name = "effect")
            active_law_scope = scope.Scope(name = "active_law:lawgroup_" + law_group)
            type_scope = scope.Scope(name = "type")
            type_scope.add_command(stat.Statement("save_scope_as","scope_ifj_new_fed_law","="),0)
            active_law_scope.add_command(type_scope,0)
            effect_scope.add_command(active_law_scope,0)
            set_var_scope = scope.Scope(name = "set_variable")
            set_var_scope.add_command(stat.Statement("name","ifp_selected_fed_law_var","="),0)
            set_var_scope.add_command(stat.Statement("value","scope:scope_ifj_new_fed_law","="),1)
            effect_scope.add_command(set_var_scope,1)
            je_scope = scope.Scope(name="add_journal_entry")
            je_scope.add_command(stat.Statement("type","je_federal_law_vote","="),0)
            effect_scope.add_command(je_scope,2)
            new_scripted_button.add_command(effect_scope,2)
            possible_scope = scope.Scope(name = "possible")
            not_scope = scope.Scope(name = "not")
            or_scope = scope.Scope(name="or")
            or_scope.add_command(stat.Statement("has_variable",var_name,"="),0)
            or_scope.add_command(stat.Statement("has_variable","ifp_selected_fed_law_var","="),1)
            not_scope.add_command(or_scope,0)
            possible_scope.add_command(not_scope,0)
            new_scripted_button.add_command(possible_scope,0)
            pdx_scripted_button_file.append(new_scripted_button)

            pdx_sb_loc += " " + gen_loc_for_sb(new_scripted_button_name,law_group) + "\n"
            pdx_sb_loc += " " + gen_loc_desc_for_sb(new_scripted_button_name,law_group) + "\n"


            #cheact an if sttament to check for sb
            if_scope = scope.Scope(name = "if")
            limit_Scope = scope.Scope(name = "limit")
            limit_Scope.add_command(stat.Statement("scope:scope_ifj_new_fed_law","active_law:lawgroup_" + law_group + ".type","="),0)
            if_scope.add_command(limit_Scope,0)
            if_scope.add_command(stat.Statement("set_variable",var_name,"="),1)
            pdx_sb_var_check.add_scope(if_scope)

def out_to_file_sb_loc():
    f = open(os.path.join(output_dir, "localization","english","ifp_scripted_buttons_enact_l_english.yml"), 'w',encoding="utf-8-sig", newline="\n")
    f.write(pdx_sb_loc)

out_to_file_sb_loc()


# # print(pdx_law_new_files[0][3])
# print(str(pdx_scripted_button_file[0]))
# f = open(os.path.join(output_dir, "common","scripted_buttons","test1.txt"), 'w',encoding="utf-8-sig", newline="\n")
# for sb in pdx_scripted_button_file:
#     f.write(str(sb))
#     f.write("\n")
# f.close()
# for file_name, law_file in pdx_law_new_files.items():
#     f = open(os.path.join(output_dir,"common","laws", file_name ), 'w', encoding="utf-8-sig",newline="\n")
#     for law in law_file:
#         f.write(str(law))
#         f.write("\n")
#     f.close()
# print(str(pdx_sb_var_check)[8:-1])