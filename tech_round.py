
# Input: {'a': {'x': 1, 'y': 2}, 'b': 3}
# Output: {'a_x': 1, 'a_y': 2, b: 3}


def flatten_dict(input, parent, res):
    for i in input:
        if type(input[i]) == dict:
            parent = parent+"_"+i
            flatten_dict(input[i], parent, res)
        elif type(input[i]) == list:
            for item in input[i]:
                if parent:
                    p = parent+"_"+i
                else:
                    p = i
                flatten_dict(item, p, res)
        else:
            res.update({
                parent+"_"+i: input[i]
            })

# input = {"a": [{"e": [{"h": "9"}, {"h": 10}], "f": "7"}, {"g": "8"}, [1, 8]], "d": 5}

# res = {}
# flatten_dict(input, "", res)
# print(res)








