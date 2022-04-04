from pathlib import Path
from botok import *
import re
from botok.third_party.has_skrt_syl import has_skrt_syl



def parse_text(text):
    words = []
    pages = re.split(r"\n\n", text)
    for num, page in enumerate(pages,0):
        page_lines = re.split(r"\s", page)
        for word in page_lines:
            if has_skrt_syl(word):
                if word in words:
                    pass
                else:
                    words.append(word)
    return words

def write_sanskrit(page_list, vol):
    final_sanskrit = ""
    for page in page_list:
        final_sanskrit += page + "\n"
        
    Path(f"./sanskrit_text/sanskrit_text_tengyur_v{vol:03}.txt").write_text(final_sanskrit, encoding='utf-8')
    
    
def get_syls(text):
    chunks = re.split('(་|།།|།)',text)
    syls = []
    cur_syl = ''
    for chunk in chunks:
        if re.search('་|།།|།',chunk):
            cur_syl += chunk
            syls.append(cur_syl)
            cur_syl = ''
        else:
            cur_syl += chunk
    if cur_syl:
        syls.append(cur_syl)
    return syls


def get_text_for_multiple_sanskrit_in_line(tokens, pos):
    text = ""
    tok_len = len(tokens)
    first_pos = pos[0]
    last_pos = pos[len(pos)-1]
    if first_pos != 0 and last_pos != tok_len:
        for num, token in enumerate(tokens, 0):
            if num >= first_pos and num <= last_pos:
                text += token.text
            return tokens[first_pos-1].text+text+tokens[last_pos+1].text
    elif first_pos == 0 and last_pos != tok_len:
        for num, token in enumerate(tokens, 0):
            if num >= first_pos and num <= last_pos:
                text += token.text
            return text+tokens[last_pos+1].text
    elif first_pos != 0 and last_pos == tok_len:
        for num, token in enumerate(tokens, 0):
            if num >= first_pos and num <= last_pos:
                text += token.text
            return tokens[first_pos-1].text+text



def check_syls(line):
    line = line.replace('།', "")
    total_sans = 0
    pos = []
    wt = WordTokenizer()
    tokens = wt.tokenize(line)
    for token in tokens:
        if token.skrt:
            total_sans += 1
    if total_sans >= (len(tokens))/2:
        return True, line
    else:
        for num, token in enumerate(tokens,0):
            if token.skrt:
                pos.append(num)
        if len(pos) == 1:
            if pos[0] != 0:
                tok_num = pos[0]
                text = tokens[tok_num-1].text+tokens[tok_num].text+tokens[tok_num+1].text
                return True, text
            else:
                return True, tokens[0].text+tokens[1].text
        else:
            text = get_text_for_multiple_sanskrit_in_line(tokens, pos)
            return True, text

    
    
def filter_sanskrit_text(text):
    sanskrit_list = []
    lines = text.splitlines()
    for line in lines:
        check, sanskrit = check_syls(line)
        if check :
            sanskrit_list.append(sanskrit)
    
    return sanskrit_list


if __name__ == "__main__":
    for vol in range(2, 80):
        text = Path(f"./sanskrit_text/sanskrit_text_tengyur_v{vol:03}.txt").read_text(encoding='utf-8')
        sanskrit_list = filter_sanskrit_text(text)
        write_sanskrit(sanskrit_list, vol)
    