from dressphere import Dressphere
import pathlib
import time
import random
import binascii
from command import Command
from services import *
from abilty_tiers import tier1_abilities
# from abilty_tiers import tier2_abilities
# from abilty_tiers import tier3_abilities

#Menu


start_time = time.time()
#INPUT VARIABLES
job_bin_path = "Test Files/job.bin"
cmd_bin_path = "Test Files/command.bin"
auto_bin_path = "Test Files/a_ability.bin"
seed_path = "Test Files/seed.txt"
output_jobbin_path = "Output Files/job.bin"
output_cmdbin_path = "Output Files/command.bin"
output_aabin_path = "Output Files/a_ability.bin"
jobs_names = [
    "gunner", "gunmage", "alchemist", "warrior", "samurai", "darkknight", "berserker", "songstress", "blackmage",
    "whitemage", "thief", "trainer01", "gambler", "mascot01", "super_yuna1", "super-yuna2", "super-yuna3",
    "super-rikku1", "super-rikku2", "super-rikku3", "super_paine1", "super_paine2", "super_paine3", "trainer02", "trainer03", "mascot02",
    "mascot03", "psychic", "festivalist01", "festivalist02", "festilvalist03"
    ]
#previous seed: 111876967976853241
#659


def read_seed():
    seed = 0
    with open(seed_path, 'r') as seed_file:
        try:
            seed = int(seed_file.read())
        except:
            print("Error reading seed.txt file, please make sure it contains a valid integer.")
            exit()
    return seed
seed = read_seed()

def job_bin_to_hex():
    job_bin = pathlib.Path(job_bin_path)
    hex_data = read_hex(job_bin)
    return hex_data

def cmd_bin_to_hex():
    cmd_bin = pathlib.Path(cmd_bin_path)
    hex_data = read_hex(cmd_bin)
    return hex_data

def auto_bin_to_hex():
    auto_bin = pathlib.Path(auto_bin_path)
    hex_data = read_hex(auto_bin)
    return hex_data

#####RANDOMIZE STUFF####
def get_big_chunks(get_all_segments=False, segmentType="job"):
    chunks = []
    hex_file = ""
    if segmentType == "job":
        hex_file = job_bin_to_hex()
        initial_position = 520
        next_position = 976
    elif segmentType == "command":
        hex_file = cmd_bin_to_hex()
        initial_position = 64
        next_position = 64 + 280
    elif segmentType == "auto-ability":
        hex_file = auto_bin_to_hex()
        initial_position = 64
        next_position = 64 + 352
    start_chunk = hex_file[initial_position:next_position]
    chunks.append(start_chunk)
    ending_chunk = ""
    if segmentType == "command":
        for i in range(0, 553):
            initial_position = next_position
            next_position = next_position + 280
            chunks.append(hex_file[initial_position:next_position])
            if i == 552 and get_all_segments == True:
                ending_chunk = hex_file[next_position:len(hex_file)]
    elif segmentType == "job":
        for i in range (0,30):
            initial_position = next_position
            next_position = next_position + 456
            chunks.append(hex_file[initial_position:next_position])
            useless = ""
            if i == 29 and get_all_segments == True:
                ending_chunk = hex_file[next_position:len(hex_file)]
    elif segmentType == "auto-ability":
        for i in range(0, 161):
            initial_position = next_position
            next_position = next_position + 352
            chunks.append(hex_file[initial_position:next_position])
            if i == 160 and get_all_segments == True:
                ending_chunk = hex_file[next_position:len(hex_file)]
    if get_all_segments == True:
        beginning_chunk = hex_file[0:520]
        if segmentType=="command":
            beginning_chunk = hex_file[0:64]
            return [beginning_chunk, chunks, ending_chunk]
        if segmentType=="auto-ability":
            beginning_chunk = hex_file[0:64]
            return [beginning_chunk, chunks, ending_chunk]
        return [beginning_chunk,chunks,ending_chunk]
    else:
        return chunks


def test_randomize_big_chunks(seed: int):
    chunks = get_big_chunks(get_all_segments=True)
    random.Random(seed).shuffle(chunks[1])
    return chunks

#####RANDOMIZE STUFF ABOVE####
##############################

def cut_command_names(valid_abilities=False):
    command_ids = []
    filename = "Test Files/commands.txt"
    if valid_abilities == True:
        filename = "Test Files/valid_commands.txt"
    with open(filename, "r") as f:
        for line in f.readlines():
            id = line[32:36]
            name = line[46:len(line)]
            name = name[:name.find("\"")]
            tupl = (id,name)
            command_ids.append(tupl)
    return command_ids


def cut_autoability_names():
    autoability_ids = []
    with open("Test Files/auto_abilities.txt", "r") as f:
        for line in f.readlines():
            id = line[36:40]
            name = line[50:len(line)]
            name = name[:name.find("\"")]
            tupl = (id,name)
            autoability_ids.append(tupl)
    return autoability_ids

command_global_chunks = get_big_chunks(segmentType="command")
auto_global_chunks = get_big_chunks(segmentType="auto-ability")

#Initiates the list of abilities
#valid_ability_pooling is an argument for shuffle_abilities() that returns only abilities that are intended to be shuffled
def initiate_abilities(valid_ability_pooling=False):
    abilities = []
    if valid_ability_pooling == True:
        valid_ability_tuples = cut_command_names(valid_abilities=True)
    else:
        command_tuples = cut_command_names()
        autoability_tuples = cut_autoability_names()
    if valid_ability_pooling == True:
        for ability in valid_ability_tuples:
            if int(ability[0],16) <= 12841:
                cmd = Command(id_value=ability[0], name_value=ability[1], type_value="Command")
                # print(cmd)
                abilities.append(cmd)
            else:
                auto = Command(id_value=ability[0].upper(), name_value=ability[1], type_value="Auto-Ability")
                abilities.append(auto)
    else:
        for chunkindex, command in enumerate(command_tuples):
            cmd = Command(id_value=command[0],name_value=command[1],type_value="Command")
            cmd.og_hex_chunk = command_global_chunks[chunkindex]
            abilities.append(cmd)
        for autochunkindex, autoability in enumerate(autoability_tuples):
            auto = Command(id_value=autoability[0].upper(),name_value=autoability[1],type_value="Auto-Ability")
            auto.og_hex_chunk = auto_global_chunks[autochunkindex]
            abilities.append(auto)
    return abilities


global_abilities = initiate_abilities()
test = ""

def set_ability_ap_batch():
    for ability in global_abilities:
        if ability.type == "Command":
            hex_cut = ability.og_hex_chunk[268:268+4]
            hex_input = reverse_two_bytes(hex_cut)
            if len(hex_input) != 4:
                pass
            else:
                ability.ap = int(hex_input,16)
        elif ability.type == "Auto-Ability":
            hex_cut = ability.og_hex_chunk[348:348+4]
            hex_input = reverse_two_bytes(hex_cut)
            if len(hex_input) != 4:
                pass
            else:
                ability.ap = int(hex_input,16)

def set_dmg_info_batch():
    for ability in global_abilities:
        if ability.type == "Command":
            hex_cut = ability.og_hex_chunk[76:76+14]
            nth = 2
            hex_list = [hex_cut[i:i+nth] for i in range(0, len(hex_cut), nth)]
            #dmg_info_names = ["MP Cost", "Target", "Calc PS", "Crit", "Hit", "Power"]
            ability.dmg_info["MP Cost"] = int(hex_list[0], 16)
            ability.dmg_info["Target HP/MP"] = int(hex_list[1], 16)
            ability.dmg_info["Calc PS"] = int(hex_list[2], 16)
            ability.dmg_info["Crit"] = int(hex_list[3], 16)
            ability.dmg_info["Hit"] = int(hex_list[4], 16)
            ability.dmg_info["Power"] = int(hex_list[5], 16)
            ability.dmg_info["Number of Attacks"] = int(hex_list[6], 16)
            test = ""

def print_dmg_info(type=None):
    for ability in global_abilities:
        if ability.type == "Command":
            print(str(ability.id) + "; " + ability.name + "\t " + "TARGET: " + str(ability.dmg_info["Target HP/MP"]) + "\t   " +
                  "CALC_PS: " + str(ability.dmg_info["Calc PS"]) + "\t   " + "POWER: " +
                  str(ability.dmg_info["Power"]) + "\t    " + "CRIT: " + str(ability.dmg_info["Crit"]))



set_ability_ap_batch()
set_dmg_info_batch()
test = ""


delete_autoability_indexes = []
change_ap_indexes = []

def replace_ap_with_file_changes():

    with open("Test Files/ap_changes.txt", mode="r") as f:
        for line in f.readlines():
            line_edited = line.strip()
            if len(line_edited) <= 4:
                pass
            else:
                ap_check = line_edited.split(",")
                if ap_check[1] == "DELETE":
                    delete_autoability_indexes.append(ap_check[0])
                else:
                    change_ap_indexes.append(int(ap_check[0]))
                    global_abilities[int(ap_check[0])].ap = int(ap_check[1])

def batch_AP_multiply():

    for ability in global_abilities:
        if isinstance(ability.ap,int) and ability.ap > 0:
          ability.ap = round(ability.ap * 1.75)

replace_ap_with_file_changes()
batch_AP_multiply()

def translate_ability(hex_byte: str):
    hex_byte_reverse = hex_byte[2:4] + hex_byte[0:2]
    hex_byte_reverse = hex_byte_reverse.upper()
    for ability in global_abilities:
        if ability.search_by_id(hex_byte_reverse) != "Not found.":
            return ability.search_by_id(hex_byte_reverse)
        else:
            pass
    return "N/A"




def initiate_dresspheres_new():
    # Initiate dresspheres
    dresspheres = []
    hex_chunks = get_big_chunks()

    for index, job in enumerate(jobs_names):
        new_dressphere = Dressphere(job, index + 1)
        new_dressphere.hex_chunk = hex_chunks[index][16:16+232]
        new_dressphere.big_chunk = hex_chunks[index]
        dresspheres.append(new_dressphere)



    for dressphere in dresspheres:
        formulae = parse_chunk(dressphere.hex_chunk)
        stat_names = ["HP", "MP", "STR", "DEF", "MAG", "MDEF", "AGL", "EVA", "ACC", "LUCK"]
        ability_initial_position = 0
        stat_hex_og_string = ""
        for index, stat in enumerate(stat_names):
            stat_hex_og_string = stat_hex_og_string + formulae[index + 1]
            dressphere.stat_variables[stat] = formulae[index + 1]
            ability_initial_position = index + 1
        dressphere.stat_hex_og = stat_hex_og_string
        ability_initial_position = ability_initial_position + 1
        ability_list = formulae[ability_initial_position:len(formulae)]
        ability_hex_og_string = ""
        for i in range (1, len(ability_list)):
            if (i % 2) == 0 or (i==0):
                pass
            else:
                # ORDER = (Required Ability, Actual Ability)
                ability_hex_og_string = ability_hex_og_string + ability_list[i - 1]
                ability_hex_og_string = ability_hex_og_string + ability_list[i]
                ability_tuple = (ability_list[i - 1], ability_list[i])
                dressphere.abilities.append(ability_tuple)
        dressphere.ability_hex_og = ability_hex_og_string

    return dresspheres


#   RANDOMIZATION OF ABILITIES IN EVERY DRESSPHERE EXCEPT SPECIAL DRESSPHERES
#   "Mask" abilities have problematic hex so those will not be in the ability pool
def shuffle_abilities(dresspheres: list[Dressphere], percent_chance_of_branch=50):
    special_jobs = ["super_yuna1", "super-yuna2", "super-yuna3",
    "super-rikku1", "super-rikku3", "super_paine1", "super_paine2", "super_paine3"]
    dresspheres_edited = dresspheres

    no_ap_abilities =[]

    valid_abilities = initiate_abilities(valid_ability_pooling=True)
    commands_to_shuffle = valid_abilities[0:250]
    auto_abilities_to_shuffle = valid_abilities[250:len(valid_abilities)]
    random.Random(seed).shuffle(commands_to_shuffle)
    random.Random(seed).shuffle(auto_abilities_to_shuffle)
    seed_increment = 1
    # print("size before: ", len(commands_to_shuffle))
    commands_to_shuffle_repeat = commands_to_shuffle.copy()
    random.Random(seed+500).shuffle(commands_to_shuffle_repeat)
    delete_autoabilities = []
    for abilityindex in delete_autoability_indexes:
        delete_autoabilities.append(global_abilities[int(abilityindex)].name)


    #Ability tiers
    tier1_ability_repeats = tier1_abilities.copy()
    tier2_ability_repeats = tier1_abilities.copy()
    tier3_ability_repeats = tier1_abilities.copy()


    convert_to_mug = ["Pilfer Gil","Borrowed Time","Pilfer HP","Pilfer MP","Sticky Fingers","Master Thief","Soul Swipe","Steal Will","Bribe", "Tantalize","Bribe","Silence Mask","Darkness Mask",
                      "Poison Mask", "Sleep Mask", "Stop Mask", "Petrify Mask"]
    #ignored_abilities = []
    abilities_to_edit = []

    for dress in dresspheres_edited:
        if dress.dress_name in special_jobs:
            pass
        else:
            this_dress_abilities = []
            activated_abilities = [] #To make sure the ability branching always goes to the root
            output_abilities = [dress.abilities[0]]
            if dress.dress_name == "whitemage" or dress.dress_name == "blackmage":
                output_abilities = [dresspheres_edited[1].abilities[0]]
            #Attempt to make gunner Physical
            if dress.dress_name == "gunner":
                output_abilities = [dresspheres_edited[3].abilities[0]]

            root_abilities = []
            mug_flaggu = False
            repeat_flaggu = False
            for i in range(1,12):
                try:
                    new_command = commands_to_shuffle.pop()
                except IndexError:
                    new_command = commands_to_shuffle_repeat.pop()
                    repeat_flaggu = True
                if new_command.name in convert_to_mug:
                    mug_flaggu = True
                new_command.job = dress.dress_name
                this_dress_abilities.append(new_command)
                abilities_to_edit.append(new_command) #Might be useless

                #Edit global ability flags
                for f_index, flag_search in enumerate(global_abilities):
                    if flag_search.id == new_command.id:
                        global_abilities[f_index].mug_flag = mug_flaggu
                        if repeat_flaggu == True:
                            global_abilities[f_index].repeat_flag = True
                        else:
                            global_abilities[f_index].job = dress.dress_name
                mug_flaggu = False


            for i in range(1,5):
                new_auto_ability = auto_abilities_to_shuffle.pop()
                while (new_auto_ability.name in delete_autoabilities):
                    new_auto_ability = auto_abilities_to_shuffle.pop()
                this_dress_abilities.append(new_auto_ability)
            for i, ability in enumerate(dress.abilities[1:len(dress.abilities)]):
                ability_to_add = ""
                ability_required = "0001"
                if i <= 1:
                    if this_dress_abilities[i].id not in root_abilities:
                        root_abilities.append(this_dress_abilities[i].id)
                    ability_to_add = this_dress_abilities[i].id
                    seed_increment = seed_increment + 1
                    ability_required = "0000"
                elif i == 2:
                    activated_abilities.append(this_dress_abilities[i].id)
                    ability_to_add = this_dress_abilities[i].id
                    seed_increment = seed_increment + 1
                    ability_required = "0001"
                elif random.Random(seed+seed_increment).randint(1, 100) > percent_chance_of_branch:
                    if this_dress_abilities[i].id not in activated_abilities:
                        activated_abilities.append(this_dress_abilities[i].id)
                    ability_required = "0001"
                    ability_to_add = this_dress_abilities[i].id
                    seed_increment = seed_increment + 1
                else:
                    found = False
                    while(found == False):
                        index_check = random.Random(seed+seed_increment).randint(0, len(this_dress_abilities)-1)
                        if (this_dress_abilities[index_check].id in activated_abilities) and (this_dress_abilities[index_check].id not in root_abilities) :
                            ability_to_add = this_dress_abilities[i].id
                            ability_required = this_dress_abilities[index_check].id
                            activated_abilities.append(this_dress_abilities[i].id)
                            seed_increment = seed_increment + 1
                            found=True
                        else:
                            seed_increment = seed_increment + 1
                ability_required_reverse = ability_required.lower()[2:4] + ability_required.lower()[0:2]
                ability_to_add_reverse = ability_to_add.lower()[2:4] + ability_to_add.lower()[0:2]
                ability_tuple = (ability_required_reverse, ability_to_add_reverse)
                output_abilities.append(ability_tuple)
                seed_increment = seed_increment + 1
            dress.abilities = output_abilities
    # print("CHECKU CHECKU")
    # print("CHECKU CHECKU")

    # for i in dresspheres_edited:
    #     print(i)

    # print("CHECKU CHECKU")
    # print("CHECKU CHECKU")
    # print("size after: " , len(commands_to_shuffle))
    # print(len(auto_abilities_to_shuffle))
    return dresspheres_edited

def randomize_stat_pool(stat_pool_values = list):
    stat_pool = stat_pool_values.copy()
    seed_increment = 1
    for list in stat_pool:
        seed_increment = seed_increment + 1
        random.Random(seed+55000+seed_increment).shuffle(list)
    test = ""
    for index, stat_pool_sublist in enumerate(stat_pool):
        seed_increment = seed_increment + 1
        random.Random(seed+seed_increment).shuffle(stat_pool_sublist)
        if index == 0 or index == 1:    # HP / MP
            for jndex, stat_hex in enumerate(stat_pool_sublist):
                var_A = int(stat_hex[0:2], 16) + ( random.Random(seed+seed_increment).randint(-5, 5) )
                seed_increment = seed_increment + 1
                if var_A > 81:
                    var_A = 81
                if var_A <= 4:
                    var_A = 5

                var_B = int(stat_hex[2:4], 16) + (random.Random(seed+seed_increment).randint(-5, 5))
                seed_increment = seed_increment + 1
                if var_B < 67:
                    var_B = 67
                if var_B > 200:
                    var_B = 200


                var_C = int(stat_hex[4:6], 16) + (random.Random(seed+seed_increment).randint(-50, 50))
                seed_increment = seed_increment + 1
                if var_C > 200:
                    var_C = 200
                if var_C < 50:
                    var_C = 50

                concat_vars = [hex(var_A)[2:4], hex(var_B)[2:4], hex(var_C)[2:4]]
                for ccindex, hex_st in enumerate(concat_vars):
                    if len(hex_st) == 1:
                        concat_vars[ccindex] = "0" + hex_st
                hex_output = concat_vars[0] + concat_vars[1] + concat_vars[2]
                stat_pool[index][jndex] = hex_output
        else:   # All other stats
            for jndex, stat_hex in enumerate(stat_pool_sublist):
                var_A = int(stat_hex[0:2], 16)
                # if var_A < 4:
                #     pass
                # else:
                #     var_A = var_A + (random.Random(seed+seed_increment).randint(-1, 1))
                #     seed_increment = seed_increment + 1
                #     if var_A <= 0:
                #         var_A = 1
                #     if var_A > 24:
                #         var_A = 24
                var_A = round(var_A)

                var_B = int(stat_hex[2:4], 16)
                #var_B = round(var_B)

                var_C = int(stat_hex[4:6], 16)+ (random.Random(seed+seed_increment).randint(-30, 30))
                # + (random.Random(seed+seed_increment).randint(-2, 2))
                seed_increment = seed_increment + 1
                if var_C < 1:
                     var_C = 1
                if index == 6:
                    if var_C < 25:
                        var_C = 25
                    if var_C > 61:
                        var_C = 61
                if var_C > 129:
                    var_C = 129
                # if var_C > 30 and (index != 5 or index != 6):
                #      var_C = 55
                # var_C = round(var_C)


                var_D = int(stat_hex[6:8], 16)
                #var_D = round(var_D)

                var_E = int(stat_hex[8:10], 16) + (random.Random(seed+seed_increment).randint(-20, 255))
                seed_increment = seed_increment + 15
                if var_E <= 1:
                    var_E = 1
                if var_E > 254:
                    var_E = 254
                var_E = round(var_E)

                concat_vars = [hex(var_A)[2:4], hex(var_B)[2:4], hex(var_C)[2:4], hex(var_D)[2:4], hex(var_E)[2:4]]
                pass
                for ccindex, hex_st in enumerate(concat_vars):
                    if len(hex_st) == 1:
                        concat_vars[ccindex] = "0" + hex_st
                hex_output = concat_vars[0] + concat_vars[1] + concat_vars[2] + concat_vars[3] + concat_vars[4]
                stat_pool[index][jndex] = hex_output

    return stat_pool


def change_ability_jobs_to_shuffled(dresspheres: list[Dressphere],ability_list: list):
    effect_animation_start_index = 16
    effect_animation_stop_index = 16+8
    attack_motion_start_index = 24
    attack_motion_stop_index = 24+2

    sub_menu_action_start_index = 26     #01 for submenu
    sub_menu_action_stop_index = 26+2
    sub_menu_start_index = 28
    sub_menu_stop_index = 28+4

    sub_shared_start_index = sub_menu_start_index-2
    sub_shared_stop_index = sub_menu_stop_index

    belongs_to_job_start_index = 272
    belongs_to_job_stop_index = 272+4

    # "gunner", "gunmage", "alchemist", "warrior", "samurai", "darkknight", "berserker", "songstress", "blackmage",
    # "whitemage", "thief", "trainer01", "gambler", "mascot01", "super_yuna1", "super-yuna2", "super-yuna3",
    # "super-rikku1", "super-rikku3", "super_paine1", "super_paine2", "super_paine3", "trainer02", "trainer03", "mascot02",
    # "mascot03", "psychic", "festivalist01", "festivalist02", "festilvalist03"

    the_0b0b_jobs = ["gunner","alchemist","darkknight", "thief", "trainer01", "gambler", "mascot01", "psychic", "festivalist01",
                     "warrior", "samurai", "darkknight", "berserker","blackmage","whitemage"]
    the_0c0c_jobs = ["trainer02", "mascot02", "festivalist02", "gunmage","songstress"]
    the_0d0d_jobs = ["trainer03","mascot03", "festilvalist03"]
    shared_menu_abilities = ["Swordplay","Bushido","Arcana", "Instinct", "Black Magic", "White Magic","Festivities",
                             "Gunplay","Fiend Hunter","Blue Bullet","Dance",
                             "Sing","Kupo!","Wildcat","Cutlery","Flimflam","Gamble", "Kogoro" ,"Ghiki","Flurry", "Psionics"]
    dance_abilities = ["Darkness Dance", "Samba of Silence", "MP Mambo", "Magical Masque", "Sleepy Shuffle", "Carnival Cancan",
                       "Slowdance", "Brakedance", "Jitterbug", "Dirty Dancing"]
    edited_abilities = []



    for ability_index, ability in enumerate(ability_list):

        # hex_cut = ability.og_hex_chunk[268:268 + 4]
        # hex_cut = ability.og_hex_chunk[348:348 + 4]


        change_flag = False
        if ability_index in change_ap_indexes:
            change_flag = True
            if ability.type == "Command":
                edited_chunk = ability.og_hex_chunk[0:268] + str(convert_gamevariable_to_reversed_hex(ability.ap,bytecount=2)) + ability.og_hex_chunk[268+4:len(ability.og_hex_chunk)]
                if len(edited_chunk) != len(ability.og_hex_chunk):
                    raise ValueError
                ability.curr_hex_chunk = edited_chunk
            elif ability.type == "Auto-Ability":
                edited_chunk = ability.og_hex_chunk[0:348] + str(convert_gamevariable_to_reversed_hex(ability.ap,bytecount=2)) + ability.og_hex_chunk[348+4:len(ability.og_hex_chunk)]
                ability.curr_hex_chunk = edited_chunk

        if ability.job not in jobs_names or ability.job == "" or ability.type == "Auto-Ability" or ability.name in shared_menu_abilities:
            # 3 swordplay; 4 blm; 5 whm; 6 bushido; 7 arcana, 545 instinct
            if ability_index == 3:
                chunk_edited = ability.og_hex_chunk
                chunk_length = len(chunk_edited)
                chunk_edited = "1b4b3300" + chunk_edited[8:chunk_length]
                chunk_edited = chunk_edited[0:belongs_to_job_start_index] + "0450" + chunk_edited[
                                                                                                    belongs_to_job_stop_index:chunk_length]
                chunk_edited = chunk_edited[0:sub_shared_start_index] + "110B0B" + chunk_edited[
                                                                                   sub_menu_stop_index:chunk_length]
                ability.curr_hex_chunk = chunk_edited
            if ability_index == 4:
                chunk_edited = ability.og_hex_chunk
                chunk_length = len(chunk_edited)
                chunk_edited = "ce467100" + chunk_edited[8:chunk_length]
                chunk_edited = chunk_edited[0:belongs_to_job_start_index] + "0950" + chunk_edited[
                                                                                                    belongs_to_job_stop_index:chunk_length]
                chunk_edited = chunk_edited[0:sub_shared_start_index] + "110B0B" + chunk_edited[
                                                                                   sub_menu_stop_index:chunk_length]
                ability.curr_hex_chunk = chunk_edited
            if ability_index == 5:
                chunk_edited = ability.og_hex_chunk
                chunk_length = len(chunk_edited)
                chunk_edited = "63374f00" + chunk_edited[8:chunk_length]
                chunk_edited = chunk_edited[0:belongs_to_job_start_index] + "0a50" + chunk_edited[
                                                                                                    belongs_to_job_stop_index:chunk_length]
                chunk_edited = chunk_edited[0:sub_shared_start_index] + "110B0B" + chunk_edited[
                                                                                   sub_menu_stop_index:chunk_length]
                ability.curr_hex_chunk = chunk_edited
            if ability_index == 6:
                chunk_edited = ability.og_hex_chunk
                chunk_length = len(chunk_edited)
                chunk_edited = "48474c00" + chunk_edited[8:chunk_length]
                chunk_edited = chunk_edited[0:belongs_to_job_start_index] + "0550" + chunk_edited[
                                                                                                    belongs_to_job_stop_index:chunk_length]
                chunk_edited = chunk_edited[0:sub_shared_start_index] + "110B0B" + chunk_edited[
                                                                                   sub_menu_stop_index:chunk_length]
                ability.curr_hex_chunk = chunk_edited
            if ability_index == 7:
                chunk_edited = ability.og_hex_chunk
                chunk_length = len(chunk_edited)
                chunk_edited = "313f2b00" + chunk_edited[8:chunk_length]
                chunk_edited = chunk_edited[0:belongs_to_job_start_index] + "0650" + chunk_edited[
                                                                                                    belongs_to_job_stop_index:chunk_length]
                chunk_edited = chunk_edited[0:sub_shared_start_index] + "110B0B" + chunk_edited[
                                                                                   sub_menu_stop_index:chunk_length]
                ability.curr_hex_chunk = chunk_edited
            if ability_index == 545:
                chunk_edited = ability.og_hex_chunk
                chunk_length = len(chunk_edited)
                chunk_edited = "50412900" + chunk_edited[8:chunk_length]
                chunk_edited = chunk_edited[0:belongs_to_job_start_index] + "0750" + chunk_edited[
                                                                                                    belongs_to_job_stop_index:chunk_length]
                chunk_edited = chunk_edited[0:sub_shared_start_index] + "110B0B" + chunk_edited[
                                                                                   sub_menu_stop_index:chunk_length]
                ability.curr_hex_chunk = chunk_edited
            edited_abilities.append(ability)

        else:
            if change_flag == False:
                chunk_edited = ability.og_hex_chunk
            else:
                chunk_edited = ability.curr_hex_chunk
            chunk_length = len(chunk_edited)
            job_hex = ""
            for dress_search in dresspheres:
                a = ability.job
                b = dress_search.dress_name
                if a == b:
                    poppy = "yes"
                made_it="no"
                if dress_search.dress_name == ability.job:
                    job_hex = hex(dress_search.dress_id)
                    made_it="yas"
                    break
            job_hex_sliced = str(job_hex[2:len(job_hex)])
            useless = "breakpoint"
            if len(job_hex_sliced) == 1:
                job_hex_sliced = "0" + job_hex_sliced
                pass
            checku = ability.job
            if ability.mug_flag == True:
                chunk_edited = chunk_edited[0:attack_motion_start_index] + "03" + chunk_edited[attack_motion_stop_index:chunk_length]
                chunk_edited = chunk_edited[0:effect_animation_start_index] + "3903390322" + chunk_edited[effect_animation_stop_index+2:chunk_length]


            if ability.name == "Ultima" or ability.name == "Holy":
                chunk_edited = chunk_edited[0:40] + "56000120" + chunk_edited[40+8:chunk_length]
            if ability.name in dance_abilities:
                chunk_edited = chunk_edited[0:attack_motion_start_index] + "03" + chunk_edited[
                                                                                  attack_motion_stop_index:chunk_length]

            if ability.job in the_0b0b_jobs:
                chunk_edited = chunk_edited[0:sub_menu_start_index] + "0b0b" + chunk_edited[sub_menu_stop_index:chunk_length]
                chunk_edited = chunk_edited[0:belongs_to_job_start_index] + job_hex_sliced + "50" + chunk_edited[belongs_to_job_stop_index:chunk_length]
            if ability.job in the_0c0c_jobs:
                chunk_edited = chunk_edited[0:sub_menu_start_index] + "0c0c" + chunk_edited[sub_menu_stop_index:chunk_length]
                chunk_edited = chunk_edited[0:belongs_to_job_start_index] + job_hex_sliced + "50" + chunk_edited[
                                                                                                    belongs_to_job_stop_index:chunk_length]
            if ability.job in the_0d0d_jobs:
                chunk_edited = chunk_edited[0:sub_menu_start_index] + "0d0d" + chunk_edited[sub_menu_stop_index:chunk_length]
                chunk_edited = chunk_edited[0:belongs_to_job_start_index] + job_hex_sliced + "50" + chunk_edited[
                                                                                                    belongs_to_job_stop_index:chunk_length]
            # if ability.job == "blackmage":
            #     chunk_edited = chunk_edited[0:sub_shared_start_index] + "000101" + chunk_edited[
            #                                                                    sub_menu_stop_index:chunk_length]
            #     chunk_edited = chunk_edited[0:belongs_to_job_start_index] + job_hex_sliced + "50" + chunk_edited[
            #                                                                                         belongs_to_job_stop_index:chunk_length]
            # if ability.job == "whitemage":
            #     chunk_edited = chunk_edited[0:sub_shared_start_index] + "000202" + chunk_edited[
            #                                                                    sub_menu_stop_index:chunk_length]
            #     chunk_edited = chunk_edited[0:belongs_to_job_start_index] + job_hex_sliced + "50" + chunk_edited[
            #                                                                                         belongs_to_job_stop_index:chunk_length]
            # # if ability.job == "warrior":
            # #     chunk_edited = chunk_edited[0:sub_shared_start_index] + "000606" + chunk_edited[
            # #                                                                    sub_menu_stop_index:chunk_length]
            # #     chunk_edited = chunk_edited[0:belongs_to_job_start_index] + job_hex_sliced + "50" + chunk_edited[
            # #                                                                                         belongs_to_job_stop_index:chunk_length]
            #
            #
            # if ability.job == "warrior":
            #     chunk_edited = chunk_edited[0:sub_shared_start_index] + "000B0B" + chunk_edited[
            #                                                                    sub_menu_stop_index:chunk_length]
            #     chunk_edited = chunk_edited[0:belongs_to_job_start_index] + job_hex_sliced + "50" + chunk_edited[
            #                                                                                         belongs_to_job_stop_index:chunk_length]
            #
            #
            #
            # if ability.job == "samurai":
            #     chunk_edited = chunk_edited[0:sub_shared_start_index] + "000808" + chunk_edited[
            #                                                                    sub_menu_stop_index:chunk_length]
            #     chunk_edited = chunk_edited[0:belongs_to_job_start_index] + job_hex_sliced + "50" + chunk_edited[
            #                                                                                         belongs_to_job_stop_index:chunk_length]
            # if ability.job == "darkknight":
            #     chunk_edited = chunk_edited[0:sub_shared_start_index] + "000909" + chunk_edited[
            #                                                                    sub_menu_stop_index:chunk_length]
            #     chunk_edited = chunk_edited[0:belongs_to_job_start_index] + job_hex_sliced + "50" + chunk_edited[
            #                                                                                         belongs_to_job_stop_index:chunk_length]
            # if ability.job == "berserker":
            #     chunk_edited = chunk_edited[0:sub_shared_start_index] + "000A0A" + chunk_edited[
            #                                                                    sub_menu_stop_index:chunk_length]
            #     chunk_edited = chunk_edited[0:belongs_to_job_start_index] + job_hex_sliced + "50" + chunk_edited[
            #                                                                                         belongs_to_job_stop_index:chunk_length]
            if ability.name == "Mix":
                chunk_edited = chunk_edited[0:16] + "0000000000090505" + chunk_edited[16+16:chunk_length]


            #Swordplay
            if ability_index >= 101 and ability_index < 113:
                chunk_edited = chunk_edited[0:sub_shared_start_index] + "000606" + chunk_edited[
                                                                                   sub_menu_stop_index:chunk_length]
                chunk_edited = chunk_edited[0:belongs_to_job_start_index] + "0050" + chunk_edited[
                                                                                                    belongs_to_job_stop_index:chunk_length]

            # Black Magic
            if (ability_index >= 165 and ability_index < 177) or ability_index == 369 or ability_index == 368:
                chunk_edited = chunk_edited[0:sub_shared_start_index] + "000101" + chunk_edited[
                                                                                   sub_menu_stop_index:chunk_length]
                chunk_edited = chunk_edited[0:belongs_to_job_start_index] + "0050" + chunk_edited[
                                                                                     belongs_to_job_stop_index:chunk_length]

            # White Magic
            if (ability_index >= 179 and ability_index < 191) or ability_index == 370 or ability_index == 371:
                chunk_edited = chunk_edited[0:sub_shared_start_index] + "000202" + chunk_edited[
                                                                                   sub_menu_stop_index:chunk_length]
                chunk_edited = chunk_edited[0:belongs_to_job_start_index] + "0050" + chunk_edited[
                                                                                     belongs_to_job_stop_index:chunk_length]

            # Instinct
            if ability_index > 138 and ability_index <= 147:
                chunk_edited = chunk_edited[0:sub_shared_start_index] + "000A0A" + chunk_edited[
                                                                                   sub_menu_stop_index:chunk_length]
                chunk_edited = chunk_edited[0:belongs_to_job_start_index] + "0050" + chunk_edited[
                                                                                     belongs_to_job_stop_index:chunk_length]


            # Bushido
            if ability_index >= 113 and ability_index < 125:
                chunk_edited = chunk_edited[0:sub_shared_start_index] + "000808" + chunk_edited[
                                                                                   sub_menu_stop_index:chunk_length]
                chunk_edited = chunk_edited[0:belongs_to_job_start_index] + "0050" + chunk_edited[
                                                                                     belongs_to_job_stop_index:chunk_length]

            # Arcana
            if (ability_index >= 129 and ability_index < 137) or (ability_index >= 376 and ability_index <= 378):
                chunk_edited = chunk_edited[0:sub_shared_start_index] + "000909" + chunk_edited[
                                                                                   sub_menu_stop_index:chunk_length]
                chunk_edited = chunk_edited[0:belongs_to_job_start_index] + "0050" + chunk_edited[
                                                                                     belongs_to_job_stop_index:chunk_length]

            shared_abi_indexes = [101, 102, 103, 104, 105, 106, 107, 108, 109, 110,
                                  111, 112, 165, 166, 167, 168, 169, 170, 171, 172, 173,
                                  174, 175, 176, 369, 368, 179, 180, 181, 182, 183, 184, 185,
                                  186, 187, 188, 189, 190, 370, 371, 139, 140, 141, 142, 143, 144,
                                  145, 146, 147, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122,
                                  123, 124, 129, 130,131,132,133,134,135,136,376,377,378]

            if ability.name == "Spare Change":
                chunk_edited = ability.og_hex_chunk
            if ability_index in changed_hit_ids:
                chunk_edited = chunk_edited[0:40] + "4e002060" + chunk_edited[48:chunk_length]
            if (ability.repeat_flag == True) and (ability_index not in shared_abi_indexes):
                chunk_edited = chunk_edited[0:sub_menu_action_start_index] + "010000" + chunk_edited[sub_menu_action_stop_index+4:chunk_length]

            if len(chunk_edited) != len(ability.og_hex_chunk):
                raise ValueError
            ability.curr_hex_chunk = chunk_edited
            edited_abilities.append(ability)
    return edited_abilities









#Initialization
dresspheres = initiate_dresspheres_new()
# print(dresspheres[8])
# print(dresspheres[8].hex_chunk)
# print(dresspheres[9])
# print(dresspheres[9].hex_chunk)
# print(dresspheres[7])
# print(dresspheres[7].hex_chunk)
# print(dresspheres[1])
# print(dresspheres[1].hex_chunk)
# print(dresspheres[5])
# print(dresspheres[5].hex_chunk)
global_abilities[3].og_hex_chunk = global_abilities[31].og_hex_chunk
global_abilities[4].og_hex_chunk = global_abilities[31].og_hex_chunk
global_abilities[5].og_hex_chunk = global_abilities[31].og_hex_chunk
global_abilities[6].og_hex_chunk = global_abilities[31].og_hex_chunk
global_abilities[7].og_hex_chunk = global_abilities[31].og_hex_chunk
global_abilities[545].og_hex_chunk = global_abilities[31].og_hex_chunk


# print("_---------------------------")
# print(global_abilities[239].og_hex_chunk)
# print("_---------------------------")
# print("_---------------------------")
# #
# print(dresspheres[7])
# print(dresspheres[7].stat_variables["MAG"])
# #0e 0a 11 12 01
# variable_str = "0e 0a 11 12 01"
# variable_str = variable_str.replace(" ", "")
# dresspheres[7].stat_variables["MAG"] = variable_str
# stat_names = ["STR", "DEF", "MAG", "MDEF", "AGL", "EVA", "ACC", "LUCK"]
# print(dresspheres[0].hex_chunk)
# print(dresspheres[7].abilities)
# print(dresspheres[7].ability_hex)
# #Test change ability
# print(global_abilities[0].id)
# print(dresspheres[7].abilities)
# print(dresspheres[7].ability_hex)
# print(dresspheres[7].ability_hex_og)
# for ability_tuple in dresspheres[7].abilities:
#     print (translate_ability(ability_tuple[1]) + " requires " + translate_ability(ability_tuple[0]))
# print(dresspheres[7].ability_hex)
# print(dresspheres[7].ability_hex_og)
# print(dresspheres[7].stat_variables)

# print(global_abilities[107])
# print(global_abilities[107].og_hex_chunk)

valid_abilities_test = initiate_abilities(valid_ability_pooling=True)

# print(valid_abilities_test)
random_dresspheres_test = initiate_abilities(valid_ability_pooling=True)
# print(dresspheres[7].abilities)
#
# print("$$$$")
# print(randomize_stat_pool(pool_stats(dresspheres)))
#
# print("$$$$")

dresspheres = shuffle_abilities(dresspheres,percent_chance_of_branch=70)
# print("$$$$")
# print("$$$$")
# print("$$$$")
# for dress in dresspheres:
#     print(dress.dress_name)
# print("$$$$")
# print("$$$$")
# print("$$$$")

chunks_output = get_big_chunks(get_all_segments=True)
dress_chunks = []
county = 0
dresspheres = replace_stats(dresspheres,randomize_stat_pool(pool_stats(dresspheres)))


for dress in dresspheres:

    dress.big_chunk = dress.big_chunk.replace(dress.ability_hex_og, dress.ability_hex)
    dress.big_chunk = dress.big_chunk.replace(dress.stat_hex_og, dress.stat_hex)
    dress_chunks.append(dress.big_chunk)

dress_number = len(dress_chunks)

job_bin_string = chunks_output[0]
for chunk in dress_chunks:
    job_bin_string = job_bin_string + chunk
job_bin_string = job_bin_string + chunks_output[2]


    #                     with filepath.open(mode="wb") as f:
    #                         f.write(binary_converted)
#TEST JOBBIN REPLACE

#
#

changed_ids = []
changed_hit_ids = []

def change_potencies(ability_list: list[Command]):
    #Change Attack potency from 16 to 10
    for i in range(44,50):
        ability_list[i].dmg_info["Power"] = 10
        changed_ids.append(i)
    #Make sure thief attacks are less
    ability_list[46].dmg_info["Power"] = 5
    #Trigger Happy Nerf
    ability_list[50].dmg_info["Hit"] = 90
    ability_list[50].dmg_info["Power"] = 1
    changed_hit_ids.append(50)
    changed_ids.append(50)
    #Nerfs to Cait abilities
    for i in range(251,255):
        ability_list[i].dmg_info["Hit"] = 45
        ability_list[i].dmg_info["Power"] = 15
        ability_list[i].dmg_info["Crit"] = 25
        changed_ids.append(i)
        changed_hit_ids.append(i)
    #Nerfs to knife abilities
    for i in range(267,269):
        ability_list[i].dmg_info["Hit"] = 45
        changed_ids.append(i)
        changed_hit_ids.append(i)
    #Nerf to Stop Knife
    ability_list[266].dmg_info["Hit"] = 65
    changed_ids.append(266)
    changed_hit_ids.append(266)
    #Nerf to Quartet Knife
    ability_list[269].dmg_info["MP Cost"] = 35
    changed_ids.append(269)
    #Multiple Hit Cactling Gun
    ability_list[270].dmg_info["Power"] = 23
    ability_list[270].dmg_info["Number of Attacks"] = 4
    changed_ids.append(270)
    #Increase to MP cost of Yuna Mascot skills
    for i in range(241,249):
        if ability_list[270].dmg_info["MP Cost"] > 0:
            ability_list[i].dmg_info["MP Cost"] = ability_list[i].dmg_info["MP Cost"] * 2
            changed_ids.append(i)


    #Nerf magic attack potency. This would be good if not using randomizer
    # ability_list[44].dmg_info["MP Cost"] = 1
    # ability_list[44].dmg_info["Power"] = 5
    #Mug and Nab gil
    for i in range(372,374):
        ability_list[i].dmg_info["Power"] = 10
        changed_ids.append(i)
    #Burst Shot
    ability_list[57].dmg_info["Power"] = 12
    changed_ids.append(57)
    #Scattershot/Burst
    ability_list[59].dmg_info["Power"] = 12
    changed_ids.append(59)
    ability_list[60].dmg_info["Power"] = 12
    changed_ids.append(60)
    #Cheapshot
    ability_list[52].dmg_info["Power"] = 8
    changed_ids.append(52)
    #Sparkler
    ability_list[117].dmg_info["Power"] = 12
    changed_ids.append(117)
    #Fireworks
    ability_list[118].dmg_info["Power"] = 12
    changed_ids.append(118)
    #Change ranged attack to Magic-Based
    ability_list[44].dmg_info["Calc PS"] = 9
    #Attempt to make Bio do damage
    ability_list[133].dmg_info["Calc PS"] = 9
    ability_list[133].dmg_info["Power"] = 11
    ability_list[133].dmg_info["Target HP/MP"] = 1
    changed_ids.append(133)
    #Blind/Silence/Sleep Do Damage
    for i in range(376, 379):
        ability_list[i].dmg_info["Power"] = 11
        ability_list[i].dmg_info["Calc PS"] = 9
        ability_list[i].dmg_info["Target HP/MP"] = 1
        changed_ids.append(i)
    #Darkness nerf
    ability_list[127].dmg_info["Power"] = 15
    changed_ids.append(127)

    tier1magic_ids = [165,166,167,168]
    tier2magic_ids = [169,170,171,172]
    tier3magic_ids = [173,174,175,176]
    #Change Black Magic Potencies AND to "Special Magic" (based on Physical formula but affected by Magic Defence)
    for i in tier1magic_ids:
        ability_list[i].dmg_info["Calc PS"] = 9
        ability_list[i].dmg_info["Power"] = 15
        changed_ids.append(i)
    for i in tier2magic_ids:
        ability_list[i].dmg_info["Calc PS"] = 9
        ability_list[i].dmg_info["Power"] = 24
        changed_ids.append(i)
    for i in tier3magic_ids:
        ability_list[i].dmg_info["Calc PS"] = 9
        ability_list[i].dmg_info["Power"] = 32
        changed_ids.append(i)

change_potencies(global_abilities)





# for i in range (0,9):
#     if i % 2 != 0:
#         pass
#     else:
#         num = (dresspheres[0].stat_variables["STR"][i] + dresspheres[0].stat_variables["STR"][i+1]).replace(" ","")
#         num = int(num, 16)
#         print(num)

# print(pool_stats(dresspheres))
# print(len(pool_stats(dresspheres)))
# for pool in pool_stats(dresspheres):
#     print(len(pool))




# for dress in replace_stats(dresspheres,randomize_stat_pool(pool_stats(dresspheres))):
#     dress.stat_formula("MAG", tableprint=True)



# for command in global_abilities:
#     print("************************")
#     print("ability id: " + command.id)
#     print("ability name: " + command.name)
#     print("************************")
#     print("------------------------")


# print(job_bin_string)

# print_jobs_edit = [8,9,11,12,13,14,15,16,17,18,19,20,21,496,497,498,499]
# print("****")
# for i in print_jobs_edit:
#     print(get_big_chunks(segmentType="command")[i])
# print("****")
# print("****")

# for dress in dresspheres:
#     print(dress.dress_name)
#     print(dress.abilities)

# for cmd_search in global_abilities:
#     print(cmd_search.name + " length: " + str(len(cmd_search.curr_hex_chunk)))
# print("****")
# print("****")
# print(get_big_chunks(segmentType="command")[235])
# print("****")
# print("****")
# print("Length of og abilities: "+str(len(global_abilities)))


global_abilities = change_ability_jobs_to_shuffled(dresspheres,global_abilities)


#
# FOR POTENCY HEX CHUNK CHANGER
#
#
#

    # hex_cut = ability.og_hex_chunk[76:76 + 12]
    # nth = 2
    # hex_list = [hex_cut[i:i + nth] for i in range(0, len(hex_cut), nth)]
    # # dmg_info_names = ["MP Cost", "Target", "Calc PS", "Crit", "Hit", "Power"]
    # ability.dmg_info["MP Cost"] = int(hex_list[0], 16)
    # ability.dmg_info["Target HP/MP"] = int(hex_list[1], 16)
    # ability.dmg_info["Calc PS"] = int(hex_list[2], 16)
    # ability.dmg_info["Crit"] = int(hex_list[3], 16)
    # ability.dmg_info["Hit"] = int(hex_list[4], 16)
    # ability.dmg_info["Power"] = int(hex_list[5], 16)
def write_potencies():
    for i in changed_ids:
        edited_chunk = global_abilities[i].curr_hex_chunk
        if len(edited_chunk) < 1:
            edited_chunk = global_abilities[i].og_hex_chunk
        chunk_length = int(len(edited_chunk))
        initial_pos = 76
        edited_chunk = (edited_chunk[0:initial_pos] + convert_gamevariable_to_reversed_hex(global_abilities[i].dmg_info["MP Cost"],bytecount=1)
        + convert_gamevariable_to_reversed_hex(global_abilities[i].dmg_info["Target HP/MP"], bytecount=1)
        + convert_gamevariable_to_reversed_hex(global_abilities[i].dmg_info["Calc PS"],bytecount=1)
        + convert_gamevariable_to_reversed_hex(global_abilities[i].dmg_info["Crit"],bytecount=1)
        + convert_gamevariable_to_reversed_hex(global_abilities[i].dmg_info["Hit"],bytecount=1)
        + convert_gamevariable_to_reversed_hex(global_abilities[i].dmg_info["Power"],bytecount=1)
        + convert_gamevariable_to_reversed_hex(global_abilities[i].dmg_info["Number of Attacks"],bytecount=1)
                        + edited_chunk[initial_pos+14:chunk_length])
        if len(edited_chunk) != chunk_length:
            og = chunk_length
            nw = len(edited_chunk)
            raise ValueError
        else:
            global_abilities[i].curr_hex_chunk = edited_chunk

write_potencies()
print_dmg_info()

    #MAKE STRING FOR COMMAND.BIN
commands_shuffle_chunks = get_big_chunks(get_all_segments=True,segmentType="command")
command_string_to_output = commands_shuffle_chunks[0]
for cmd_search in global_abilities:
    # print(cmd_search.name + " length: " + str(len(cmd_search.curr_hex_chunk)))
    if cmd_search.type == "Auto-Ability":
        pass
    else:
        if len(cmd_search.curr_hex_chunk) != 280 and len(cmd_search.curr_hex_chunk) != 0:
            # print("AB NOT FOUND:"+ cmd_search.name)
            command_string_to_output = command_string_to_output + cmd_search.og_hex_chunk
        else:
            if len(cmd_search.curr_hex_chunk) == 0 and cmd_search.type != "Auto-Ability":
                # print("NOT IN THE POOL: " + cmd_search.name)
                command_string_to_output = command_string_to_output + cmd_search.og_hex_chunk
            command_string_to_output = command_string_to_output + cmd_search.curr_hex_chunk



# print("middle chunk: "+str(len(command_string_to_output)-64))
command_string_to_output = command_string_to_output + commands_shuffle_chunks[2]


#MAKE STRING FOR A_ABILITY.BIN
aa_shuffle_chunks = get_big_chunks(get_all_segments=True,segmentType="auto-ability")
aa_string_to_output = aa_shuffle_chunks[0]
for cmd_search in global_abilities:
    # print(cmd_search.name + " length: " + str(len(cmd_search.curr_hex_chunk)))
    if cmd_search.type == "Command":
        pass
    else:
        if len(cmd_search.curr_hex_chunk) != 352 and len(cmd_search.curr_hex_chunk) != 0:
            # print("AB NOT FOUND:"+ cmd_search.name)
            aa_string_to_output = aa_string_to_output + cmd_search.og_hex_chunk
        else:
            if len(cmd_search.curr_hex_chunk) == 0 and cmd_search.type != "Command":
                # print("NOT IN THE POOL: " + cmd_search.name)
                aa_string_to_output = aa_string_to_output + cmd_search.og_hex_chunk
            aa_string_to_output = aa_string_to_output + cmd_search.curr_hex_chunk
aa_string_to_output = aa_string_to_output + aa_shuffle_chunks[2]



# print("ending chunk: " + str(len(commands_shuffle_chunks[2])))
# print("all chunk: "+str(len(command_string_to_output)))
#
# print(command_string_to_output)
# print(global_abilities[88].og_hex_chunk)
# print(global_abilities[88].og_hex_chunk)

# for command in global_abilities:
#     print("************************")
#     print("ability id: " + command.id)
#     print("ability name: " + command.name)
#     print("************************")
#     print("------------------------")
# print(dresspheres[0].stat_formula(type="STR",tableprint=True))
# print(dresspheres[26].stat_formula(type="ACC",tableprint=True))
# print("****")

test = ""

def execute_randomizer():
    binary_converted_jobbin = binascii.unhexlify(job_bin_string)
    binary_converted_cmdbin = binascii.unhexlify(command_string_to_output)
    binary_converted_aabin = binascii.unhexlify(aa_string_to_output)
    with open(output_jobbin_path, 'wb') as f:
        f.write(binary_converted_jobbin)
    with open(output_cmdbin_path, 'wb') as f:
        f.write(binary_converted_cmdbin)
    with open(output_aabin_path, 'wb') as f:
        f.write(binary_converted_aabin)
    print("Files written successfully!")



# for index, ability in enumerate(global_abilities):
#     print(str(index) + ".\t ID: " + str(ability.id) + "\t\t" + str(ability.name) + "\t\t" + "AP: " + str(ability.ap))

# print("--- Completed in %s seconds ---" % (time.time() - start_time))


# for dress in dresspheres:
#     print(dress.dress_name)
#     print(dress.big_chunk)

# big_chunky = test_randomize_big_chunks(4)
# print_str=big_chunky[0]
# for i, x in enumerate(big_chunky[1]):
#     print(i)
#     print_str = print_str + x
# print_str= print_str + big_chunky[2]
# print(print_str)
# print(len(print_str))

# total = 248
# job_number = len(jobs_names) - 9
# job_ability_each = 11
# print("Job number: " + str(job_number))
# print("Job ability each: " + str(job_ability_each))
# print("tier1: " + str(len(tier1_abilities)) + "   %: " + str(len(tier1_abilities)/248) + "   No.: "
#       + str((len(tier1_abilities)/248)*job_ability_each))
# print("tier2: " + str(len(tier2_abilities)) + "   %: " + str(len(tier2_abilities)/248) + "   No.: "
#       + str((len(tier2_abilities)/248)*job_ability_each))
# print("tier3: " + str(len(tier3_abilities)) + "   %: " + str(len(tier3_abilities)/248) + "   No.: "
#       + str((len(tier3_abilities)/248)*job_ability_each))