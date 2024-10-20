import re, traceback

age_patterns = {
    "English1": r"(im|i'm|i\W*am)\W*(\d+|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve)",
    "English2": r"(\d+|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve)\W*(years\W*old|yrs|y\W*o)",
    "English3": r"old\W*(\d+|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve)\W*y",
    "Spanish": r'(\d+|uno|dos|tres|cuatro|cinco|seis|siete|ocho|nueve|diez|once|doce)\W*(años|añitos)',
    "Mandarin Chinese": r'(\d+|一|二|三|四|五|六|七|八|九|十|十一|十二)\W*(岁|歲)',
    "Hindi": r'(\d+|एक|दो|तीन|चार|पाँच|छह|सात|आठ|नौ|दस|ग्यारह|बारह)\W*(साल|साला)',
    "Arabic": r'(\d+|واحدة|اثنان|ثلاثة|أربعة|خمسة|ستة|سبعة|ثمانية|تسعة|عشرة|إحدى عشرة|اثنتا عشرة)\W*سنة',
    "Portuguese": r'(\d+|um|dois|três|quatro|cinco|seis|sete|oito|nove|dez|onze|doze)\W*(anos|aninhos)',
    "Bengali": r'(\d+|এক|দুই|তিন|চার|পাঁচ|ছয়|সাত|আট|নয়|দশ)\W*(বছর|বছরে)',
    "Russian": r'(\d+|один|два|три|четыре|пять|шесть|семь|восемь|девять|десять|одиннадцать|двенадцать)\W*(лет|годиков)',
    "Japanese": r'(\d+|一|二|三|四|五|六|七|八|九|十|十一|十二)\W*(歳|才|さい|サイ|ｻｲ)',
    "German": r'(\d+|eins|zwei|drei|vier|fünf|sechs|sieben|acht|neun|zehn|elf|zwölf)\W*(Jahre|Jährchen)',
    "French": r'(\d+|un|deux|trois|quatre|cinq|six|sept|huit|neuf|dix|onze|douze)\W*(ans|ansounets)',
    "Urdu": r'(\d+|ایک|دو|تین|چار|پانچ|چھ|سات|آٹھ|نو|دس| گیارہ| بارہ)\W*سال',
    "Indonesian": r'(\d+|satu|dua|tiga|empat|lima|enam|tujuh|delapan|sembilan|sepuluh|sebelas|duabelas)\W*tahun',
    "Italian": r'(\d+|uno|due|tre|quattro|cinque|sei|sette|otto|nove|dieci|undici|dodici)\W*(anni|annetti)',
    "Tagalog": r'(\d+|isa|dalawa|tatlo|apat|lima|anim|pito|walo|nwebe|diyes|onse|dose)\W*taon',
    "Farsi": r'(\d+|یک|دو|سه|چهار|پنج|شش|هفت|هشت|نه|ده|یازده|دوازده)\W*سال',
    "Polish": r'(\d+|jeden|dwa|trzy|cztery|pięć|sześć|siedem|osiem|dziewięć|dziesięć|jedenaście|dwanaście)\W*lat',
    "Thai": r'(\d+|หนึ่ง|สอง|สาม|สี่|ห้า|หก|เจ็ด|แปด|เก้า|สิบ|สิบเอ็ด|สิบสอง)\W*ปี',
    "Dutch": r'(\d+|een|twee|drie|vier|vijf|zes|zeven|acht|negen|tien|elf|twaalf)\W*jaar',
    "Tamil": r'(\d+|ஒன்று|இரண்டு|மூன்று|நான்கு|ஐந்து|ஆறு|ஏழு|எட்குளா|ஒன்பது|பத்து|பதினொன்று)\W*வயது',
    "Greek": r'(\d+|ένα|δύο|τρία|τέσσερα|πέντε|έξι|επτά|οκτώ|εννέα|δέκα|έντεκα|δώδεκα)\W*χρόνων',
    "Kurdish": r'(\d+|یەک|دوو|سێ|چوار|پێنج|شەش|حەوت|هەشت|نۆ|دەە|یازدە|دوازدە)\W*sal',
    "Ukrainian": r'(\d+|один|два|три|чотири|п\'ять|шість|сім|вісім|дев\'ять|десять|одинадцять|дванадцять)\W*років',
    "Czech": r'(\d+|jedna|dva|tři|čtyři|pět|šest|sedm|osm|devět|deset|jedenáct|dvanáct)\W*let',
    "Swedish": r'(\d+|en|två|tre|fyra|fem|sex|sju|åtta|nio|tio|elva|tolv)\W*år',
    "Finnish": r'(\d+|yksi|kaksi|kolme|neljä|viisi|kuusi|seitsemän|kahdeksan|yhdeksän|kymmenen|yksitoista|kaksitoista)\W*vuotta',
    "Norwegian": r'(\d+|en|to|tre|fire|fem|seks|syv|åtte|ni|ti|elleve|tolv)\W*år',
    "Hungarian": r'(\d+|egy|kettő|három|négy|öt|hat|hét|nyolc|kilenc|tíz|tizenegy|tizenkettő)\W*év',
    "Danish": r'(\d+|en|to|tre|fire|fem|seks|syv|otte|ni|ti|elleve|tolv)\W*år',
    "Malay": r'(\d+|satu|dua|tiga|empat|lima|enam|tujuh|lapan|sembilan|sepuluh|sebelas|duabelas)\W*tahun',
    "Croatian": r'(\d+|jedan|dva|tri|četiri|pet|šest|sedam|osam|devet|deset|jedanaest|dvanaest)\W*godina',
    "Serbian": r'(\d+|jedan|dva|tri|četiri|pet|šest|sedam|osam|devet|deset|jedanaest|dvanaest)\W*година',
    "Bulgarian": r'(\d+|един|два|три|четири|пет|шест|седем|осем|девет|десет|единадесет|дванадесет)\W*години',
    "Slovak": r'(\d+|jeden|dva|tri|štyri|päť|šesť|sedem|osem|deväť|desať|jedenásť|dvanásť)\W*rokov',
    "Lithuanian": r'(\d+|vienas|du|trys|keturi|penki|šeši|septyni|aštuoni|devyni|dešimt|vienuolika|dvylika)\W*metai',
    "Slovenian": r'(\d+|ena|dva|tri|štiri|pet|šest|sedem|osem|devet|deset|enajst|dvanajst)\W*let',
    "Latvian": r'(\d+|viens|divi|trīs|četri|pieci|seši|septiņi|astoņi|deviņi|desmit|vienpadsmit|divpadsmit)\W*gadi',
    "Estonian": r'(\d+|üks|kaks|kolm|neli|viis|kuus|seitse|kaheksa|üheksa|kümme|üksteist|kaksteist)\W*aastat',
    "Vietnamese": r'(\d+|một|hai|ba|bốn|năm|sáu|bảy|tám|chín|mười|mười một|mười hai)\W*tuổi',
    "Mongolian": r'(\d+|нэг|хоёр|гурав|дөрөв|тав|зургаа|долоо|найм|ес|арав|арван нэг|арван хоёр)\W*нас',
    "Romani": r'(\d+|ek|duj|trin|štar|pandž|šeš|ifta|oxto|inija|deš|jekh|diklisi)\W*vojb',
}

translation_table = str.maketrans(
    "ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ０１２３４５６７８９！”＃＄％＆’（）＊＋，－．／：；＜＝＞？＠［￥］＾＿｀｛｜｝～　",
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~ "
)


def _content_checker(_content):
    if not _content:
        return None
    content = str(_content).translate(translation_table)
    check_content = str(content)
    check_content = check_content.translate(translation_table)
    check_contents = []
    contents = check_content.split("https://")
    check_contents.append(contents.pop(0))
    for check_content in contents:
        check_contents.append(" ".join(check_content.split(" ")[1:]))
    check_content =  " ".join(check_contents)
    detected_lang = []
    for lang,age_pattern in age_patterns.items():
        check = True
        for n in range(5):
            check = re.search(age_pattern, check_content)
            if not check:
                break
            try:
                intr = int(check.group(1))
            except:
                try:
                    intr = int(check.group(2))
                except:
                    intr = None
            if not intr:
                detected = check.group()
                content = content.replace(detected, "[Masked]")
                check_content = check_content.replace(detected, "")
                detected_lang.append(lang)
                continue
            if intr < 13:
                detected = check.group()
                content = content.replace(detected, "[Masked]")
                check_content = check_content.replace(detected, "")
                detected_lang.append(lang)
                continue
    return content

def check_age_content(content):
    content = _content_checker(content)
    return content #if not age_check else f"```ansi\n\x1b[1;31m[error]\x1b[1;0m Filtered Age words ({lang})\n```"

if __name__ == "__main__":
    # test patterns
    print(check_age_content("私は10歳です"))
    print(check_age_content("i'm １２ years old"))