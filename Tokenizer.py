import re
class Tokenizer:
    def __init__(self):
        # smiles vocab
        self.pad_index = 0
        self.mask_index = 1
        self.unk_index = 2
        self.start_index = 3
        self.end_index = 4
        self.vocab =  ['<pad>', '<mask>', '<unk>', '<start>', '<end>']  + \
            ["(", ")", "[", "]"] + \
            [".", "=", "-", "#", "+", "$", ":", "/", "\\", "%"] + \
            ["B", "C", "N", "O", "P", "S", "F", "I", "H"] + \
            ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"] + \
            ["c", "o", "M", "R", "L", "X", "A", ]
        #B, C, N, O, P, S, F, Cl, Br, I is basic SMILES skeleton creating atoms
        self.vocab_theoretical_size = 118 + 30 + 50 # 118 for all the elements, 30 for SMILES special symbols, 50 for the rest
        
        self.replace_pairs = [
            ("Br", "R"),
            ("Cl", "L"),
            ("Sn", "X"),
            ("Na", "A"),
            ("Ca", "M"),
        ]

    def add_vocab(self, new_vocab, replace_pairs=None):
        self.vocab.extend(new_vocab)
        if replace_pairs is not None:
            self.replace_pairs.extend(replace_pairs)

    def replace(self, string):
        # """Regex to replace Br,Cl,Sn,Na with single letters"""
        for rex, replace in self.replace_pairs:
            regx = re.compile(rex)
            string = regx.sub(replace, string)
        return string
    def __len__(self):
        return len(self.vocab)
    def __getitem__(self, idx):
        return self.vocab[idx]
    def find(self, string):
        for x in self.vocab:
            if x == string:
                return self.vocab.index(x)
        return self.unk_index
    def get_vocab(self):
        return self.vocab
    def encode(self, string, max_length=None, padding=False,):
        string = self.replace(string)
        out = [self.start_index]
        for x in string:
            if x in self.vocab:
                out.append(x)
            else:
                out.append(self.unk_index)
        out.append(self.end_index)
        if max_length is not None:
            out = out[:max_length]
            if padding:
                out = out + [self.pad_index] * (max_length - len(out))
        return out
    def decode(self, input, drop_start_end=True):
        out = []
        for x in input:
            if x == self.pad_index:
                continue
            elif x == self.unk_index:
                out.append("<unk>")
            elif x == self.start_index:
                if not drop_start_end:
                    out.append("<start>")
            elif x == self.end_index:
                if not drop_start_end:
                    out.append("<end>")
                break
            else:
                out.append(self.vocab[x])
        return "".join(out)
    def __call__(self, input: str | list | None = None):
        if isinstance(input, str):
            return self.encode(input)
        elif isinstance(input, list):
            return self.decode(input, drop_start_end=True)
        return None
        