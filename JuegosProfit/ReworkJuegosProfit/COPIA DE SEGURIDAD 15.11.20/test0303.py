# def Remove_unsoported_characters(string):
#     list_letters = []
#     chars = set('\',:;!"#&/$()=?¿.<>-_[]{}¡+\\@%')
#     for letter in string:
#         if letter.isalnum():
#             list_letters.append(letter)
#         elif letter.isspace():
#             list_letters.append(letter)
#         elif any((c in chars) for c in string):
#             list_letters.append(letter)
#         else:
#             pass
#     new_string = "".join(list_letters)
#     return new_string
#
# asd = "Once in Yaissor"
#
# asd2 = Remove_unsoported_characters(asd)
# print(asd2)

asd = 'https://store.steampowered.com/app/243800/Gas_Guzzlers_Extreme/?snr=1_7_7_2300_150_19'

def link_sanitizer(link):
    new_link = []
    link_separator = link.split('/')
    del link_separator[-1]
    for part in link_separator:
        if part == '':
            continue
        elif part.startswith('http'):
            new_link.append(part)
            new_link.append('/' * 2)
        else:
            new_link.append(part)
            new_link.append('/')
    new_link = "".join(new_link)
    return new_link


asd2 = link_sanitizer(asd)
print(asd2)