from collections import OrderedDict

N = "NOUN"
V = "VERB"
PP = "PREPOSITION"
Q = "QUERY"
NAME = "NAME"
PUNC = "PUNCTUATION"
YN = "YESNO"
ADV = "ADVERB"
P = "PRONOUN"
DET = "DETERMINER"
AUX = "AUXILIARY"

TOKEN_DICT = OrderedDict({
    "có thể": "có_thể",
    "tất cả": "tất_cả",
    "đà nẵng": "đà_nẵng",
    "hồ chí minh": "hồ_chí_minh",
    "nha trang": "nha_trang",
    "phú quốc": "phú_quốc",
    "phương tiện": "phương_tiện",
    "bao lâu": "bao_lâu",
    "bao nhiêu": "bao_nhiêu",
    "được không": "được_không",
})

ENG_WORD = {
    "train": "xe lửa",
    "airplane": "máy bay",
}

POS = {
    "em": N,
    "có_thể": ADV,
    "nhắc": V,
    "lại": ADV,
    "tất_cả": P,
    "các": DET,
    "tour": N,
    "được_không": Q, 
    "đi": V,
    "từ": PP,
    "tới": PP,
    "hết": V,
    "bao_lâu": Q,
    "có": V,
    "bao_nhiêu": Q, 
    "vậy": P, 
    "bạn": N,
    "bằng": PP,
    "phương_tiện": N,
    "gì": Q,
    "những": DET,
    "ngày": N,
    "nào": Q,   
    "nhỉ": AUX,

    "?": PUNC,

    "hồ_chí_minh": NAME,
    "nha_trang": NAME,
    "phú_quốc": NAME,
    "đà_nẵng": NAME,
}

PRONOUN = ["em", "anh"]