from typing import List, Tuple

from .types import TokenType, ObjectType


def find_declared(parsed: List[Tuple[str, TokenType, int]]) -> (List[Tuple[str, ObjectType]], List):
    """
    Find all classes, functions and variable declaration in a given parsed tokens
    Also inject new docstring tokens and find existring docstrings

    :param parsed: parsed tokens
    :return: found declarations as a pair of token in string form and object type and updated tokens with injected docstrings
    """
    prv_tokens = [None] + parsed[:-1]
    prv_tokens_white = [None] + parsed[:-1]
    nxt_tokens = parsed[1:] + [None]
    nxt_tokens_white = parsed[1:] + [None]
    for i in range(1, len(parsed)):
        if prv_tokens[i][1] == TokenType.WHITESPACE:
            prv_tokens[i] = prv_tokens[i - 1]
        if nxt_tokens[-i - 1][1] == TokenType.WHITESPACE:
            nxt_tokens[-i - 1] = nxt_tokens[-i]

    declared, new_parsed = [], []
    in_def, in_class, in_lambda, in_for, in_eq, in_import, in_return_hint, in_def_hint = \
        False, False, False, False, False, False, False, False
    convert_next, append_next = False, False
    def_args = []
    balance = 0
    for i, (cur, prv, nxt, prv_white, nxt_white) in \
            enumerate(zip(parsed, prv_tokens, nxt_tokens, prv_tokens_white, nxt_tokens_white)):
        new_parsed.append(cur)
        if append_next:
            indent = cur[0].split('\n')[-1]

            new_s = '"""'
            if len(def_args) != 0:
                new_s += '\n' + indent + '\n'
                for arg in def_args:
                    new_s += indent + f':param {arg}:\n'
                new_s += indent
            new_s += '"""' + '\n' + indent

            new_parsed.append((new_s, TokenType.DOCSTRING, None))
            append_next = False
            def_args = []

        if cur[1] == TokenType.WHITESPACE:
            if prv[0] != '\\' and '\n' in cur[0]:
                in_eq = False
                in_import = False
            continue

        if convert_next:
            end_trio = cur[0][-3:]
            s = cur[0][:-3]
            indent = nxt_white[0].split('\n')[-1]
            if len(def_args) > 0 and '\n' not in s:
                s = s[:3] + '\n' + indent + s[3:] + '\n' + indent + '\n' + indent
            for arg in def_args:
                if arg not in s:
                    s += f':param {arg}:\n' + indent
            s += end_trio

            new_parsed[-1] = s, TokenType.DOCSTRING, cur[2]
            convert_next = False
            def_args = []

        if cur[1] == TokenType.NOT_PARSED:
            if '->' in cur[0]:
                in_return_hint = True
            for c in cur[0]:
                if c in '[{(':
                    balance += 1
                if c in ']})':
                    balance -= 1

                if c == '=':
                    in_eq = True

        if (in_def or in_class) and ':' in cur[0] and balance == 0:  # TODO: consider dicts as default argument values
            if nxt[1] == TokenType.TRIPLE_STRING:
                convert_next = True
            else:
                append_next = True
        if in_def:
            if ':' in cur[0]:
                in_def_hint = True
            if ',' in cur[0]:
                in_def_hint = False

        if ':' in cur[0] and balance == 0:
            in_def = False
            in_class = False
            in_lambda = False
            in_return_hint = False
            in_def_hint = False
        if in_for and cur[0] == 'in':
            in_for = False

        if cur[1] == TokenType.OBJECT:
            if prv is not None and prv[0] == 'class':
                declared.append((cur[0], ObjectType.CLASS))
                # print('DECLARED 1', cur, ObjectType.CLASS)
            elif prv is not None and prv[0] == 'def':
                declared.append((cur[0], ObjectType.FUNCTION))
                # print('DECLARED 2', cur, ObjectType.FUNCTION)
            elif prv is not None and prv[0] == 'as':
                declared.append((cur[0], ObjectType.VARIABLE))
                # print('DECLARED 3', cur, ObjectType.VARIABLE)
            elif nxt is not None and not in_eq and balance == 0 and \
                    ((nxt[0][0] == '=' and (len(nxt[0]) == 1 or nxt[0][1] not in '=<>')) or
                     (nxt[0] == ',' and not in_import)):
                declared.append((cur[0], ObjectType.VARIABLE))
                # print('DECLARED 4', cur, ObjectType.VARIABLE)
            elif in_lambda or in_for:
                declared.append((cur[0], ObjectType.VARIABLE))
                # print('DECLARED 5', cur, ObjectType.VARIABLE)
            elif in_def and not in_return_hint and not in_def_hint:
                def_args.append(cur[0])
                declared.append((cur[0], ObjectType.VARIABLE))
                # print('DECLARED 6', cur, ObjectType.VARIABLE)

        if cur[0] == 'def':
            in_def = True
        if cur[0] == 'class':
            in_class = True
        if cur[0] == 'lambda':
            in_lambda = True
        if cur[0] == 'for':
            in_for = True
        if cur[0] == 'import':
            in_import = True

    # print('\n'.join(f'{d[0]}, {d[1]}' for d in declared), '\n\n\n')

    return declared, new_parsed
