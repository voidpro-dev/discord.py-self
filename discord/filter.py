import re

age_patterns = {
    "English1": r"(im|i'm|iam)(\d{1,2}|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve)",
    "English2": r"(\d{1,2}|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve)(yearsold|yrs|yo)",
    "English3": r"old(\d{1,2}|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve)y",
    "Spanish": r'(\d{1,2}|uno|dos|tres|cuatro|cinco|seis|siete|ocho|nueve|diez|once|doce)(años|añitos)',
    "Mandarin Chinese": r'(\d{1,2}|一|二|三|四|五|六|七|八|九|十一|十二)(岁|歲)',
    "Hindi": r'(\d{1,2}|एक|दो|तीन|चार|पाँच|छह|सात|आठ|नौ|दस|ग्यारह|बारह)(साल|साला)',
    "Arabic": r'(\d{1,2}|واحدة|اثنان|ثلاثة|أربعة|خمسة|ستة|سبعة|ثمانية|تسعة|عشرة|إحدى عشرة|اثنتا عشرة)سنة',
    "Portuguese": r'(\d{1,2}|um|dois|três|quatro|cinco|seis|sete|oito|nove|dez|onze|doze)(anos|aninhos)',
    "Bengali": r'(\d{1,2}|এক|দুই|তিন|চার|পাঁচ|ছয়|সাত|আট|নয়|দশ)(বছর|বছরে)',
    "Russian": r'(\d{1,2}|один|два|три|четыре|пять|шесть|семь|восемь|девять|десять|одиннадцать|двенадцать)(лет|годиков)',
    "Japanese": r'(\d{1,2}|一|二|三|四|五|六|七|八|九|十一|十二)(歳|才|さい|サイ|ｻｲ)',
    "German": r'(\d{1,2}|eins|zwei|drei|vier|fünf|sechs|sieben|acht|neun|zehn|elf|zwölf)(Jahre|Jährchen)',
    "French": r'(\d{1,2}|un|deux|trois|quatre|cinq|six|sept|huit|neuf|dix|onze|douze)(ans|ansounets)',
    "Urdu": r'(\d{1,2}|ایک|دو|تین|چار|پانچ|چھ|سات|آٹھ|نو|دس| گیارہ| بارہ)سال',
    "Indonesian": r'(\d{1,2}|satu|dua|tiga|empat|lima|enam|tujuh|delapan|sembilan|sepuluh|sebelas|duabelas)tahun',
    "Italian": r'(\d{1,2}|uno|due|tre|quattro|cinque|sei|sette|otto|nove|dieci|undici|dodici)(anni|annetti)',
    "Tagalog": r'(\d{1,2}|isa|dalawa|tatlo|apat|lima|anim|pito|walo|nwebe|diyes|onse|dose)taon',
    "Farsi": r'(\d{1,2}|یک|دو|سه|چهار|پنج|شش|هفت|هشت|نه|ده|یازده|دوازده)سال',
    "Polish": r'(\d{1,2}|jeden|dwa|trzy|cztery|pięć|sześć|siedem|osiem|dziewięć|dziesięć|jedenaście|dwanaście)lat',
    "Thai": r'(\d{1,2}|หนึ่ง|สอง|สาม|สี่|ห้า|หก|เจ็ด|แปด|เก้า|สิบ|สิบเอ็ด|สิบสอง)ปี',
    "Dutch": r'(\d{1,2}|een|twee|drie|vier|vijf|zes|zeven|acht|negen|tien|elf|twaalf)jaar',
    "Tamil": r'(\d{1,2}|ஒன்று|இரண்டு|மூன்று|நான்கு|ஐந்து|ஆறு|ஏழு|எட்குளா|ஒன்பது|பத்து|பதினொன்று)வயது',
    "Greek": r'(\d{1,2}|ένα|δύο|τρία|τέσσερα|πέντε|έξι|επτά|οκτώ|εννέα|δέκα|έντεκα|δώδεκα)χρόνων',
    "Kurdish": r'(\d{1,2}|یەک|دوو|سێ|چوار|پێنج|شەش|حەوت|هەشت|نۆ|دەە|یازدە|دوازدە)sal',
    "Ukrainian": r'(\d{1,2}|один|два|три|чотири|п\'ять|шість|сім|вісім|дев\'ять|десять|одинадцять|дванадцять)років',
    "Czech": r'(\d{1,2}|jedna|dva|tři|čtyři|pět|šest|sedm|osm|devět|deset|jedenáct|dvanáct)let',
    "Swedish": r'(\d{1,2}|en|två|tre|fyra|fem|sex|sju|åtta|nio|tio|elva|tolv)år',
    "Finnish": r'(\d{1,2}|yksi|kaksi|kolme|neljä|viisi|kuusi|seitsemän|kahdeksan|yhdeksän|kymmenen|yksitoista|kaksitoista)vuotta',
    "Norwegian": r'(\d{1,2}|en|to|tre|fire|fem|seks|syv|åtte|ni|ti|elleve|tolv)år',
    "Hungarian": r'(\d{1,2}|egy|kettő|három|négy|öt|hat|hét|nyolc|kilenc|tíz|tizenegy|tizenkettő)év',
    "Danish": r'(\d{1,2}|en|to|tre|fire|fem|seks|syv|otte|ni|ti|elleve|tolv)år',
    "Malay": r'(\d{1,2}|satu|dua|tiga|empat|lima|enam|tujuh|lapan|sembilan|sepuluh|sebelas|duabelas)tahun',
    "Croatian": r'(\d{1,2}|jedan|dva|tri|četiri|pet|šest|sedam|osam|devet|deset|jedanaest|dvanaest)godina',
    "Serbian": r'(\d{1,2}|jedan|dva|tri|četiri|pet|šest|sedam|osam|devet|deset|jedanaest|dvanaest)година',
    "Bulgarian": r'(\d{1,2}|един|два|три|четири|пет|шест|седем|осем|девет|десет|единадесет|дванадесет)години',
    "Slovak": r'(\d{1,2}|jeden|dva|tri|štyri|päť|šesť|sedem|osem|deväť|desať|jedenásť|dvanásť)rokov',
    "Lithuanian": r'(\d{1,2}|vienas|du|trys|keturi|penki|šeši|septyni|aštuoni|devyni|dešimt|vienuolika| dvylika)metai',
    "Slovenian": r'(\d{1,2}|ena|dva|tri|štiri|pet|šest|sedem|osem|devet|deset|enajst|dvanajst)let',
    "Latvian": r'(\d{1,2}|viens|divi|trīs|četri|pieci|seši|septiņi|astoņi|deviņi|desmit|vienpadsmit|divpadsmit)gadi',
    "Estonian": r'(\d{1,2}|üks|kaks|kolm|neli|viis|kuus|seitse|kaheksa|üheksa|kümme|üksteist|kaksteist)aastat',
    "Vietnamese": r'(\d{1,2}|một|hai|ba|bốn|năm|sáu|bảy|tám|chín|mười|mười một|mười hai)tuổi',
    "Mongolian": r'(\d{1,2}|нэг|хоёр|гурав|дөрөв|тав|зургаа|долоо|найм|ес|арав|арван нэг|арван хоёр)нас',
    "Romani": r'(\d{1,2}|ek|duj|trin|štar|pandž|šeš|ifta|oxto|inija|deš|jekh|diklisi)vojb',
}

translation_table = str.maketrans(
    "ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ０１２３４５６７８９！”＃＄％＆’（）＊＋，－．／：；＜＝＞？＠［￥］＾＿｀｛｜｝～　",
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~ "
)

def _content_checker(content):
    if not content:
        return False, False
    check_content = str(content)
    check_content = check_content.replace("||", "").replace("~~", "").replace("*", "")
    check_contents = []
    contents = check_content.split("https://")
    check_contents.append(contents.pop(0))
    for check_content in contents:
        check_contents.append(" ".join(check_content.split(" ")[1:]))
    check_content =  " ".join(check_contents)
    for lang,age_pattern in age_patterns.items():
        check = re.findall(age_pattern, str(check_content).replace(" ", "").lower())
        if check:
            for a in check:
                try:
                    if int(a[0]) < 13:
                        return True, lang
                except:
                    try:
                        if int(a[1]) < 13:
                            return True, lang
                    except:
                        return True, lang
            return False, False

def check_age_content(content):
    age_check, lang = _content_checker(content)
    return content if not age_check else f"```ansi\n\x1b[1;31m[error]\x1b[1;0m Filtered Age words ({lang})\n```"
