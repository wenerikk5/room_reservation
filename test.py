def permute1(seq):
    if not seq:
        # print('if not [seq]:', [seq])
        return [seq]
    else:
        res = []
        for i in range(len(seq)):
            rest = seq[:i] + seq[i+1:]
            for x in permute1(rest):
                res.append(seq[i:i+1] + x)
                # print("appended (seq[i:i+1] + x):", seq[i:i+1] + x)
        # print('returend res:', res)
        return res



print(len(permute1('achive')))
