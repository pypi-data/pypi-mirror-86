from padaos import IntentContainer
from little_questions.utils import normalize
from little_questions.settings import RESOURCES_PATH
from little_questions.parsers import BasicQuestionParser
from os import listdir
from os.path import join, isdir


class RegexQuestionParser(BasicQuestionParser):
    """
    Dead Simple Regex intent parser

    """

    def __init__(self, lang="en-us"):
        super().__init__(lang)
        self.container = IntentContainer()
        self._intents = []
        self.lang = lang
        self.register_default_intents()

    def normalize(self, text):
        # pos parsing normalization
        text = text.replace(" 's", "'s").replace("''", "").replace("``", "")
        text = normalize(text)
        text = text.lower()
        words = text.split(" ")
        questions = ['what', 'when', 'where', 'why', 'how', 'which',
                     'whose', 'who']
        removes = ["a", "an", "of", "that", "this", "to", "with", "as", "by",
                   "for", "me", "do", "have", "does", "is", "your", "in", "i"
                   ] + questions
        replaces = {"are": "is", "was": "is", "were": "is"}
        for idx, word in enumerate(words):
            if word in replaces:
                words[idx] = replaces[word]
            if word in removes:
                words[idx] = ""

        return " ".join([w for w in words if w])

    @property
    def intents(self):
        return self._intents

    def register_intent(self, name, rules):
        self._intents.append(name)
        self.container.add_intent(name, rules)

    def register_default_intents(self):
        self.container.add_entity('question',
                                  ['what', 'when', 'where', 'why', 'how',
                                   'which', 'whose', 'who'])

        self.from_folder(join(RESOURCES_PATH, self.lang))

    def from_folder(self, folder_path, reset=False):
        assert isdir(folder_path)
        if reset:
            self.container = IntentContainer()
            self._intents = []
        for f in listdir(folder_path):
            if f.endswith(".intent"):
                intent = f.replace(".intent", "")
                with open(join(folder_path, f)) as fi:
                    rules = fi.readlines()
                rules = [r.strip() for r in rules if r and not r.startswith("#")]
                self.register_intent(intent, rules)

    def parse(self, utterance):
        # normalization pre-parsing
        data = super().parse(utterance)
        utterance = normalize(str(utterance)).lower()

        COMMON_STARTERS = ["on average", "about", "tell me", "approximately"]
        for c in COMMON_STARTERS:
            if utterance.startswith(c):
                utterance = utterance.replace(c, "").strip()
        utterance = " ".join(utterance.split(" "))

        match = self.container.calc_intent(utterance)
        if match.get("name"):
            data["QuestionIntent"] = match["name"] or "unknown"
            entities = match["entities"]
            data.update(entities)
            if "query" in data:
                data["query"] = self.normalize(data["query"])
        return data


if __name__ == "__main__":
    from pprint import pprint
    from little_questions.data import SAMPLE_QUESTIONS
    import random

    parser = RegexQuestionParser()
    print(parser.intents)
    questions = [
        "Who was the first English circumnavigator of the globe ?",
        "When was Rosa Parks born ?",
        "Where is the Kalahari desert ?",
        "What country has the highest arson rate ?",
        "What city in Florida is Sea World in ?",
        "What is Portugal most famous for ?"
    ]
    for q in questions:
        data = parser.parse(q)
        print("Q:", q)
        print("Intent:", data['QuestionIntent'])
        pprint(data)
        print("___")

    questions = SAMPLE_QUESTIONS
    random.shuffle(questions)

    for q in questions[:10]:
        data = parser.parse(q)
        print("Q:", q)
        print("Intent:", data['QuestionIntent'])
        pprint(data)
        print("___")
