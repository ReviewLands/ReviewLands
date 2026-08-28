#!/usr/bin/env python3
"""Generate Class 8 English question paper from user's scanned PDF (verbatim)."""

from fpdf import FPDF

SOURCE = "/home/ubuntu/.cursor/projects/workspace/uploads/CamScanner_08-28-2026_19.07_compressed_3229.pdf"


def build_pdf(path: str):
    pdf = QuestionPaperPDF()

    # Page 1 — Seen Comprehension 10
    pdf.add_page()
    pdf.write_block("Practice Items : English First Paper ■ 35", 10.5, bold=True)
    pdf.ln(0.5)
    pdf.write_block("Seen Comprehension 10", 11.5, bold=True)
    pdf.write_block(
        "Read the text and answer the following questions. [Unit-6 : Lesson-6(C)]",
        10.5,
        bold=True,
    )
    pdf.ln(0.3)
    pdf.write_block(COMP_10_PASSAGE, 10)
    pdf.ln(0.5)
    pdf.write_block("● Seen Passage – 1 (First Seen) :", 10.5, bold=True)
    pdf.write_block("1. Choose the best answer from the alternatives:", 10.5, bold=True)
    for line in COMP_10_MCQ:
        pdf.write_block(line, 10)
    pdf.ln(0.2)
    pdf.write_block("2. Write short answers to the following questions:", 10.5, bold=True)
    for line in COMP_10_SHORT:
        pdf.write_block(line, 10)
    pdf.ln(0.2)
    pdf.write_block("● Seen Passage – 2 (Second Seen) :", 10.5, bold=True)
    pdf.write_block("3. Complete the passage with suitable words:", 10.5, bold=True)
    pdf.write_block(COMP_10_GAP, 10)
    pdf.ln(0.2)
    pdf.write_block(
        "4. Read the passage carefully and replace the following words with their suitable synonyms or antonyms:",
        10.5,
        bold=True,
    )
    pdf.write_block(COMP_10_SYNONYM, 10)

    # Page 2 — Seen Comprehension 11 + grammar
    pdf.add_page()
    pdf.write_block("Seen Comprehension 11", 11, bold=True)
    pdf.write_block(
        "Read the text and answer the following questions. [Unit-6 : Lesson-7(B)]",
        10,
        bold=True,
    )
    pdf.ln(0.2)
    pdf.write_block(COMP_11_PASSAGE, 9.5, line_h=4.3)
    pdf.ln(0.3)
    pdf.write_block("● Seen Passage – 1 (First Seen) :", 10, bold=True)
    pdf.write_block("1. Choose the best answer from the alternatives:", 10, bold=True)
    for line in COMP_11_MCQ:
        pdf.write_block(line, 9.5, line_h=4.2)
    pdf.ln(0.1)
    pdf.write_block("2. Write short answers to the following questions:", 10, bold=True)
    for line in COMP_11_SHORT:
        pdf.write_block(line, 9.5, line_h=4.2)
    pdf.ln(0.1)
    pdf.write_block("● Seen Passage – 2 (Second Seen) :", 10, bold=True)
    pdf.write_block("3. Complete the passage with suitable words:", 10, bold=True)
    pdf.write_block(COMP_11_GAP, 9.5, line_h=4.2)
    pdf.ln(0.1)
    pdf.write_block(
        "4. Read the passage carefully and replace the following words with their suitable synonyms or antonyms:",
        10,
        bold=True,
        line_h=4.3,
    )
    pdf.write_block(COMP_11_SYNONYM, 9.5, line_h=4.2)
    pdf.ln(0.3)
    pdf.write_block("Practice Items : English Second Paper", 10, bold=True)
    pdf.ln(0.15)
    pdf.write_block(CHANGE_SENTENCE_HEADER, 9.5, bold=True, line_h=4.2)
    for line in CHANGE_SENTENCES:
        pdf.write_block(line, 9.5, line_h=4.2)
    pdf.ln(0.15)
    pdf.write_block(VERB_FILL, 9.5, line_h=4.2)

    pdf.output(path)


COMP_10_PASSAGE = (
    "Oxygen and the air pressure are always being monitored. In the event of a lack of oxygen, an oxygen mask will "
    "automatically appear in front of you. Pull the mask towards you and place it firmly over your nose and mouth. "
    "Secure the elastic band behind your head, and breathe normally. If you are travelling with a child or someone who "
    "requires assistance, secure your mask first, and then assist the other person. Keep your mask on until a uniformed "
    "crew member advises you to remove it. In the event of an emergency, please assume the bracing position. That is, "
    "lean forward with your hands on top of your head and your elbows against your thighs. Ensure your feet are flat on "
    "the floor. A life vest is located in a pouch under your seat or between the armrests. When instructed to do so, open "
    "the plastic pouch and remove the vest. Slip it over your head. Pass the straps around your waist and adjust at the "
    "front. To inflate the vest, pull firmly on the red cord, before you leave the aircraft. We remind you that this is a "
    "nonsmoking flight. You will find this and all the other safety information in the card located in the seat pocket in "
    "front of you. We strongly suggest you read it before takeoff. If you have any questions, please don't hesitate to ask "
    "one of our crew members. We wish you all an enjoyable flight."
)

COMP_10_MCQ = [
    "i. A passenger can't remove the oxygen mask without the permission of ---.",
    "(a) crew (b) captain (c) air hostess (d) doctor",
    "ii. A life vest is kept in a ---.",
    "(a) seat (b) plastic bag (c) wooden box (d) glass box",
    "iii. Safety information card is kept ---.",
    "(a) in the seat pocket (b) in the seat (c) in the plastic bag (d) in the cylinder",
    "iv. All the safety information --- written in the card.",
    "(a) is (b) are (c) has (d) have",
    "v. The captain is giving necessary --- to the passengers.",
    "(a) information (b) data (c) speech (d) instruments",
    "vi. The word 'hesitate' means ---.",
    "(a) frustrate (b) vacillate (c) thinking (d) motionless",
    "vii. The word 'enjoyable' means ---.",
    "(a) bitter (b) boring (c) disgust (d) pleasant",
]

COMP_10_SHORT = [
    "a. What are always monitored?",
    "b. What appears automatically for the lacking of oxygen?",
    "c. Where is the elastic band secured?",
    "d. How long are you to keep mask?",
    "e. What do you mean by bracing position?",
]

COMP_10_GAP = (
    "Oxygen and air pressure are (a) --- during the flight. If oxygen is low, an oxygen mask will (b) ---. Pull the mask "
    "towards you and (c) --- it over your nose and mouth. If traveling with a child, put your mask on first, then help the "
    "child. Keep the mask on (d) --- told to remove it. In an emergency, assume the bracing position: lean forward with "
    "hands on your head. A life vest is under your seat; (e) --- instructions to wear it and inflate it. This is a "
    "non-smoking flight, and safety instructions are available in the seat pocket."
)

COMP_10_SYNONYM = (
    "(a) event (synonym); (b) place (synonym); (c) remove (antonym); (d) safety (antonym); (e) enjoyable (synonym)."
)

COMP_11_PASSAGE = (
    "(The plane landed at Suvarnabhumi Airport at 4:55 p.m.) The name 'Suvarnabhumi' is pronounced as \"su-wan-na-poom\". "
    "The name is derived from Sanskrit, which means golden land. The name was chosen by the late king Bhumibol Adulyadej. "
    "The airport is located in Racha Thewa subdistrict in the Bang Phli district of Samut Prakan province, 30 kilometres "
    "east of Bangkok. The airport has two parallel runways. All of them are 60 metres wide. Two of the runways are 4000 "
    "metres long and the other is 3,700 metres. It can handle 94 flight operations per hour. It can handle 45 million "
    "passengers and 3 million tonnes of cargo per year. The airport has two terminals including the main terminal and a "
    "satelite terminal. The main terminal is 563,000 square metres that is, 6,060,000 square feet. It is the fourth "
    "largest passenger terminal building in the world. The airport is going through phase 2. It will raise its capacity to "
    "handle 65 million passengers per year. The airport has two 5-storey car park buildings. The buildings can house 5000 cars."
)

COMP_11_MCQ = [
    "i. Bhumibol Adulyadej was ---.",
    "(a) king (b) a minister (c) a landlord (d) a president",
    "ii. The airport has ---.",
    "(a) 2 equal runways (b) 2 parallel runways (c) 2 separate runways (d) 2 joined runways",
    "iii. The origin of the name of the airport is ---.",
    "(a) Thai (b) Malay (c) Sanskrit (d) Hindi",
    "iv. The name 'Suvarnabhumi' means a --- land.",
    "(a) dream (b) golden (c) treasure (d) ivory",
    "v. The plane landed at the airport in the ---.",
    "(a) morning (b) afternoon (c) evening (d) midnight",
    "vi. The word 'derived' of the text in the line 2 means ---.",
    "(a) got (b) profit (c) gained (d) achieved",
    "vii. The word 'pronounced' of the text in the line 1 means ---.",
    "(a) said (b) called (c) told (d) uttered",
]

COMP_11_SHORT = [
    "a. When did the plane land at the airport?",
    "b. What does the word 'Suvarnabhumi' mean?",
    "c. Who chose the name of the airport?",
    "d. What are the breadth and length of the runways?",
    "e. How many passengers can the airport handle per year?",
]

COMP_11_GAP = (
    "The plane landed at Suvarnabhumi Airport at 4:55 p.m. Its name, meaning \"golden land\" in Sanskrit, was (a) --- by "
    "King Bhumibol Adulyadej. Located east of Bangkok, the airport has two (b) --- runways (4000m and 3700m long, both 60m "
    "wide). The airport, the world's fourth (c) ---, can handle 45 million passengers annually. (d) --- renovations will "
    "raise its capacity to 65 million. The two 5-story parking (e) --- can house 5,000 cars."
)

COMP_11_SYNONYM = (
    "(a) landed (antonym); (b) wide (synonym); (c) long (antonym); (d) chosen (synonym); (e) raise (antonym)."
)

CHANGE_SENTENCE_HEADER = "20. Change the following sentences as directed in the brackets."

CHANGE_SENTENCES = [
    "(a) Bangladesh is a small country. (Make it a negative sentence without changing meaning)",
    "(b) It is one of the most beautiful countries in the world. (Make it positive)",
    "(c) The farmers work hard to support themselves. (Make it an interrogative sentence)",
    "(d) They should be taken care of by us. (Make it active)",
    "(e) It is the most populous country in the world. (Make it comparative)",
]

VERB_FILL = (
    "8. Fill in the blanks with the correct form of the verbs given in the brackets.\n"
    "A poor man was once (a) --- (put) in a jail, although he did no wrong. After a long time, the king of the state "
    "(b) --- (visit) the jail and the man told him that he was innocent but a case (c) --- (file) against him by some of "
    "his enemies. The king (d) --- (inquire) privately and found that it was true. He (e) --- (give) the man some money "
    "and set him free. He went straight to the market."
)


class QuestionPaperPDF(FPDF):
    FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

    def __init__(self):
        super().__init__(format="A4", unit="mm")
        self.set_auto_page_break(auto=False)
        self.set_margins(14, 12, 14)
        self.add_font("DejaVu", "", self.FONT)
        self.add_font("DejaVu", "B", self.FONT_BOLD)

    def footer(self):
        self.set_y(-8)
        self.set_font("DejaVu", "", 9)
        self.cell(0, 5, f"Page {self.page_no()}/2", align="C")

    def write_block(self, text, size=10.5, bold=False, line_h=4.8):
        style = "B" if bold else ""
        self.set_font("DejaVu", style, size)
        self.multi_cell(0, line_h, text)
        self.ln(0.15)


if __name__ == "__main__":
    out = "/workspace/Class_8_English_Question_Paper.pdf"
    build_pdf(out)
    print(f"Created: {out}")
