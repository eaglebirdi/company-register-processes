from typing import List


class Braced2DictConverter:
    def __init__(self):
        pass

    def convert(self, text: str):
        objs_stack: List[dict] = [{}]
        curr_str = ""

        i = 0
        previous_nonempty: str = ''

        while i < len(text):
            char = text[i]
            curr_obj = objs_stack[-1]

            if char.isspace():
                i += 1
                continue

            is_left_par = char == '('
            is_right_par = char == ')'
            is_comma = char == ','

            harvest = is_left_par or ((is_right_par or is_comma) and previous_nonempty != ')')
            pop = is_right_par or is_comma
            newarg = is_left_par or is_comma
            seed = not is_left_par and not is_right_par and not is_comma
            empty_args = is_right_par and previous_nonempty == '('

            if harvest:
                curr_obj['_name'] = curr_str
                curr_str = ""
            if pop:
                objs_stack.pop()
                curr_obj = objs_stack[-1]
            if newarg:
                new_obj = {}
                args = curr_obj.get('args')
                if args is None:
                    args = curr_obj['args'] = []
                args.append(new_obj)
                objs_stack.append(new_obj)
            if empty_args:
                curr_obj['args'].pop()
            if seed:
                curr_str += char

            previous_nonempty = char
            i += 1

        return objs_stack.pop()
