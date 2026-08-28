#!/usr/bin/env python3
"""Generate Class 8 English question paper PDF from source text (verbatim)."""

from fpdf import FPDF

# Verbatim content from the user's source (Set 1 only; Sets 2+ skipped).
COMP_10 = {
    "intro": "Read the text and answer questions 1, 2, and 3. (Unit–5, Lesson–04)",
    "passage": (
        "At the farthest corner of Bangladesh, there is a village called Tarapur. In this village, "
        "there lives a man named Kartik Poramanik. He is a hairdresser by profession, but a nature lover at heart.\n\n"
        "His passion is to plant saplings, which grow into gigantic trees. He started planting trees when he was only "
        "10 years old. He remembers what his father once told him, “My son, you can earn the blessings of God by planting trees.” "
        "He has never forgotten what his father told him. At present, he is 63 years old.\n\n"
        "He has planted hundreds of trees in his village. Many of the trees are now 35-40 years old. Once there were hardly "
        "any trees in this village. Kartik used to go to different houses for his job. At times he would get tired in the "
        "scorching sun, but there were no trees under which he could sit and rest for a while. Thinking about how people "
        "suffer in the heat, Kartik began his tree-planting mission.\n\n"
        "Occasionally Kartik would wake up early in the morning, take one or two laborers with him and set out to plant trees. "
        "He would walk long distances to plant trees, carrying with him some dry food and water. He would pay all the expenses "
        "from his own pocket. Kartik has planted trees beside the roads, in and around the Bazar, schools and colleges, open "
        "fields and many other places. At times it so happened that Kartik would go to water his plants at 10 or 11 pm. "
        "People asked him, “Kartik, are you mad? What are you doing so late at night?” Kartik would smile and say, "
        "“What to do, sir. I have to work hard the whole day to earn money for my family. I don’t get time during the day. "
        "But my trees would die if I don’t water them. So I come late at night to look after them.”\n\n"
        "Even today this old man continues planting trees as many as he can. A man, who can hardly sign his name, is leaving "
        "his signature all around in nature."
    ),
    "mcq": [
        "(a) Kartik was a ¾¾ by profession:",
        "1. tree planter ii. barbar iii. barber iv. barberer",
        "(b) The similar meaning of the phrase ‘set out’ is ¾¾.",
        "1. awarded ii. went iii. set trees outside iv. wanted",
        "(c) In the passage ‘water’ is used as a/an ¾¾.",
        "1. i) noun ii) adjective iii) verb",
        "which option/options is/are correct?",
        "1. A & B ii. B & C iii. A & C iv. C",
        "(d) “I come late at night to look after them,” Here ‘them’ refers to ¾¾.",
        "1. the people of Tarapur ii. the customers iii. the saplings iv. Kartik’s frind",
        "(e) The word ‘passion’ in the passage means ¾¾.",
        "1. obsession ii. outburst iii. apathy iv. hobby",
    ],
    "short": [
        "a) Who is Kartik Poramanik and how old is he now?",
        "b) How do you understand that he is a nature lover?",
        "c) Why did he plant trees?",
        "d) What do you understand by the saying, “A man who can hardly sign his name, is leaving his signature all around in nature?”",
        "e) Why did people call Kartik mad?",
    ],
    "summary": "Summarize the above text in around 85 words.",
}

COMP_11 = {
    "intro": "Read the text and answer questions 1, 2, and 3. (Unit–5, Lesson–05)",
    "passage": (
        "Once upon a time, a dove and a bat were very good friends. One day the two friends decided to set out on a journey. "
        "They flew over the rivers and hills and came to a big jungle. Both the friends were very tired, they needed to sit down "
        "and take a rest. Soon night fell and it was dark all around.\n\n"
        "A storm arose. It started to rain heavily. The dove and the bat started to look for shelter.\n\n"
        "They came upon a century-old rain tree. An owl had his nest in that tree. The dove and the bat knocked at the owl’s door. "
        "The old grumpy owl opened the door. The dove and the bat requested him to give them shelter. The owl unwillingly let them in. "
        "The two birds were hungry too. They begged for some food. The selfish owl was not happy. However, he shared his dinner with them.\n\n"
        "The dove was so tired that she could hardly eat. But the bat was sly. He ate greedily. He began to praise the owl with the "
        "thought of getting more food. The bat said, “O wise and brave owl, you are the most generous person I have ever seen. You are "
        "powerful and mighty.” The owl was very pleased at the bat’s flattery. He puffed and ruffled himself, trying to look as wise and "
        "brave as possible. Then he turned to the dove and asked, “Now little dove, what do you think about me?”"
    ),
    "mcq": [
        "a) After flying over the hills and rivers they came to a ¾¾.",
        "i. tree ii. jungle iii. river iv. hill",
        "b) Both the friends became very ¾¾.",
        "i. fresh ii. joyful iii. exhausted iv. delighted",
        "c) They took shelter ¾¾.",
        "i. on a rain tree ii. in the owl’s nest iii. in a hole iv. on a mango tree",
        "d) The word ‘generous’ means ¾¾.",
        "i. cruel ii. fine iii. wise iv. kind",
        "e) The owl was ¾¾ with the flattery of the bat.",
        "i. satisfied ii. tired iii. displeased iv. angry",
    ],
    "short": [
        "a) What did the two friends decide to do?",
        "b) Why did they look for a shelter?",
        "c) Why couldn’t the dove eat?",
        "d) Why did the bat praise the owl?",
        "e) What action of the owl tells you that he (the owl) wanted to hear more good things about him?",
    ],
    "summary": "Summarize the above text in around 85 words.",
}


class QuestionPaperPDF(FPDF):
    FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

    def __init__(self):
        super().__init__(format="A4", unit="mm")
        self.set_auto_page_break(auto=False)
        self.set_margins(12, 10, 12)
        self.add_font("DejaVu", "", self.FONT)
        self.add_font("DejaVu", "B", self.FONT_BOLD)

    def footer(self):
        self.set_y(-8)
        self.set_font("DejaVu", "", 9)
        self.cell(0, 5, f"Page {self.page_no()}/2", align="C")

    def write_block(self, text, size=11.5, bold=False, line_h=5.4):
        style = "B" if bold else ""
        self.set_font("DejaVu", style, size)
        self.multi_cell(0, line_h, text)
        self.ln(0.3)


def build_pdf(path: str):
    pdf = QuestionPaperPDF()

    # Page 1 — Seen Comprehension 10 (Set 1)
    pdf.add_page()
    pdf.write_block("Class 8 English 1st Paper seen passage", 12, bold=True)
    pdf.ln(1)
    pdf.write_block(COMP_10["intro"], 11.5, bold=True)
    pdf.ln(0.5)
    pdf.write_block(COMP_10["passage"], 11)
    pdf.ln(1)
    pdf.write_block("Set 1", 11.5, bold=True)
    pdf.ln(0.5)
    pdf.write_block("1. Choose the best answer from the alternatives :", 11.5, bold=True)
    for line in COMP_10["mcq"]:
        pdf.write_block(line, 11)
    pdf.ln(0.5)
    pdf.write_block("2. Give short answers to the following questions :", 11.5, bold=True)
    for line in COMP_10["short"]:
        pdf.write_block(line, 11)
    pdf.ln(0.5)
    pdf.write_block(f"3. {COMP_10['summary']}", 11.5, bold=True)

    # Page 2 — Seen Comprehension 11 (Set 1)
    pdf.add_page()
    pdf.write_block("11", 12, bold=True)
    pdf.write_block("Class 8 English Seen Passages", 12, bold=True)
    pdf.ln(1)
    pdf.write_block(COMP_11["intro"], 11.5, bold=True)
    pdf.ln(0.5)
    pdf.write_block(COMP_11["passage"], 11)
    pdf.ln(1)
    pdf.write_block("Set 1", 11.5, bold=True)
    pdf.ln(0.5)
    pdf.write_block("1. Choose the best answer from the alternatives :", 11.5, bold=True)
    for line in COMP_11["mcq"]:
        pdf.write_block(line, 11)
    pdf.ln(0.5)
    pdf.write_block("2. Give short answers to the following questions :", 11.5, bold=True)
    for line in COMP_11["short"]:
        pdf.write_block(line, 11)
    pdf.ln(0.5)
    pdf.write_block(f"3. {COMP_11['summary']}", 11.5, bold=True)

    pdf.output(path)


if __name__ == "__main__":
    out = "/workspace/Class_8_English_Question_Paper.pdf"
    build_pdf(out)
    print(f"Created: {out}")
