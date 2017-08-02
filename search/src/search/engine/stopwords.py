'''Stopwords for QUA query processing engine.
'''


RUSSIAN = set([
    'а', 'без', 'более', 'больше', 'будет', 'будто', 'бы', 'был', 'была',
    'были', 'было', 'быть', 'в', 'вам', 'вас', 'вдруг', 'ведь', 'во', 'вот',
    'впрочем', 'все', 'всегда', 'всего', 'всех', 'всю', 'вы', 'где', 'говорил',
    'да', 'даже', 'два', 'для', 'до', 'другой', 'его', 'ее', 'ей', 'ему',
    'если', 'есть', 'еще', 'ж', 'же', 'жизнь', 'за', 'зачем', 'здесь', 'и',
    'из', 'или', 'им', 'иногда', 'их', 'к', 'кажется', 'как', 'какая', 'какой',
    'когда', 'конечно', 'кто', 'куда', 'ли', 'лучше', 'между', 'меня', 'мне',
    'много', 'может', 'можно', 'мой', 'моя', 'мы', 'на', 'над', 'надо',
    'наконец', 'нас', 'не', 'него', 'нее', 'ней', 'нельзя', 'нет', 'ни',
    'нибудь', 'никогда', 'ним', 'них', 'ничего', 'но', 'ну', 'о', 'об', 'один',
    'он', 'она', 'они', 'опять', 'от', 'перед', 'по', 'под', 'после', 'потом',
    'потому', 'почти', 'при', 'про', 'раз', 'разве', 'с', 'сам', 'свою',
    'себе', 'себя', 'сегодня', 'сейчас', 'сказал', 'сказала', 'сказать', 'со',
    'совсем', 'так', 'такой', 'там', 'тебя', 'тем', 'теперь', 'то', 'тогда',
    'того', 'тоже', 'только', 'том', 'тот', 'три', 'тут', 'ты', 'у', 'уж',
    'уже', 'хорошо', 'хоть', 'чего', 'человек', 'чем', 'через', 'что', 'чтоб',
    'чтобы', 'чуть', 'эти', 'этого', 'этой', 'этом', 'этот', 'эту', 'я'])


ENGLISH = set([
    'a', 'about', 'above', 'after', 'again', 'against', 'all', 'am', 'an',
    'and', 'any', 'are', 'aren\'t', 'as', 'at', 'be', 'because', 'been',
    'before', 'being', 'below', 'between', 'both', 'but', 'by', 'can\'t',
    'cannot', 'could', 'couldn\'t', 'did', 'didn\'t', 'do', 'does', 'doesn\'t',
    'doing', 'don\'t', 'down', 'during', 'each', 'few', 'for', 'from',
    'further', 'had', 'hadn\'t', 'has', 'hasn\'t', 'have', 'haven\'t',
    'having', 'he', 'he\'d', 'he\'ll', 'he\'s', 'her', 'here', 'here\'s',
    'hers', 'herself', 'him', 'himself', 'his', 'how', 'how\'s', 'i', 'i\'d',
    'i\'ll', 'i\'m', 'i\'ve', 'if', 'in', 'into', 'is', 'isn\'t', 'it',
    'it\'s', 'its', 'itself', 'let\'s', 'me', 'more', 'most', 'mustn\'t', 'my',
    'myself', 'no', 'nor', 'not', 'of', 'off', 'on', 'once', 'only', 'or',
    'other', 'ought', 'our', 'ours', 'ourselves', 'out', 'over', 'own', 'same',
    'shan\'t', 'she', 'she\'d', 'she\'ll', 'she\'s', 'should', 'shouldn\'t',
    'so', 'some', 'such', 'than', 'that', 'that\'s', 'the', 'their', 'theirs',
    'them', 'themselves', 'then', 'there', 'there\'s', 'these', 'they',
    'they\'d', 'they\'ll', 'they\'re', 'they\'ve', 'this', 'those', 'through',
    'to', 'too', 'under', 'until', 'up', 'very', 'was', 'wasn\'t', 'we',
    'we\'d', 'we\'ll', 'we\'re', 'we\'ve', 'were', 'weren\'t', 'what',
    'what\'s', 'when', 'when\'s', 'where', 'where\'s', 'which', 'while', 'who',
    'who\'s', 'whom', 'why', 'why\'s', 'with', 'won\'t', 'would', 'wouldn\'t',
    'you', 'you\'d', 'you\'ll', 'you\'re', 'you\'ve', 'your', 'yours',
    'yourself', 'yourselves'])


STOPWORDS = RUSSIAN | ENGLISH
