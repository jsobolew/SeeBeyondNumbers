import functions
import pandas as pd
import os


kiid_dir = "../KIIDs/"
kiids = os.listdir(kiid_dir)

kiid_paths = []
for kiid in kiids:
    kiid_paths.append(kiid_dir + kiid)

text_path = "kiid_text/"

all_text = []
files = []

for k in kiid_paths[155:]:
    text = functions.fitz_scan(k)
    text_corrected = functions.correct_grammar(text)
    text_sentences = functions.split_into_sentences(text_corrected)

    #translate workaround
    i = 0
    text_new = []
    while i < len(text_sentences):
        x = 1 #how many sentences into google translate at once
        if i + x < len(text):
            text_new.append(''.join(text_sentences[i:i + x]))
        else:
            text_new.append(''.join(text_sentences[i:len(text)]))
        i = i + x

    # stitch back together
    text = ''
    for i in range(0, len(text_new)):
        text = text + functions.tanslate(text_new[i])

    with open(kiid_dir + "../kiid_text/" + k[len(kiid_dir):-4] + '.txt', 'w', encoding="UTF-8") as f:
        f.write(text)

    #back into sentences
    text = functions.split_into_sentences(text)

    all_text = all_text + text
    files = files + [k[len(kiid_dir):-4]] * len(text)

    dict = {"sentences": text, "file_names": [k[6:-4]] * len(text)}
    df = pd.DataFrame(dict)

    df['stem'] = df.apply(lambda row: functions.stem(row["sentences"]), axis=1)
    df.to_pickle(kiid_dir + "../kiid_pcl/" + k[len(kiid_dir):-4] + ".pcl")

    print(k + " done")

dict = {"sentences": all_text, "file_names": files}
df = pd.DataFrame(dict)

df['stem'] = df.apply(lambda row:  functions.stem(row["sentences"]), axis = 1)

df.to_pickle("sentences.pcl")
