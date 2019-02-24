def format_card_string_for_database(string):
    string = string.split('\\')[1]
    string = string.split('.')[0]

    new_string = ""

    for c in string:
        is_num = False
        for n in range(0, 10):
            if (c == str(n)):
                is_num = True
        if (not is_num):
            new_string += c if (c != '-') else ' '

    # strip first 3 chars of new string
    new_string = new_string[3:string.__len__()]
    final_string = ""
    final_string = str(new_string[0]).capitalize()
    for n in range(0, new_string.__len__() - 1):
        final_string += new_string[n + 1].capitalize() if (new_string[n] == ' ') else new_string[n + 1]
    return final_string

print(format_card_string_for_database("img/creature\\m19-166-viashino-pyromancer.jpg"))