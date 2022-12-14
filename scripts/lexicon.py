# TODO: double conjuncts: entweder/oder, sowohl/als-wie-auch, wenn/dann, weder/noch, nichtnur/sondernauch
# TODO: difference between nominal and clausal conjunction
Konjunktionen = ['und', 'oder', 'aber', 'doch', 'sondern', 'denn', 'vorausgesetzt', 'jedoch', 'sowie', 'noch']
# NOTE: 'wie/wo' here in the meaning of 'als'
Subjunktionen = ['als', 'als ob', 'bevor', 'bis', 'da', 'damit', 'ehe', 'falls', 'indem', 'insofern', 'insoweit', 'nachdem', 'obgleich', 'obschon', 'obwohl', 'obzwar', 'seit', 'seitdem', 'sobald', 'sofern', 'solange', 'sooft', 'sosehr', 'soviel', 'soweit', 'sowie', 'trotzdem', 'während', 'weil', 'wenn', 'wenngleich', 'wie', 'wo']
# Begründung (um), Alternative (statt, anstatt, anstelle), Außnahme (ohne: A-aber-nicht-B, außer: nicht-A-aber-B)
# NOTE: there is an old-fashioned usage of 'bis dass' not included here
Satzpräpositionen = ['um', 'ohne', 'außer', 'ausser', 'statt', 'anstatt', 'anstelle', 'im Falle', 'für den Fall']
Satzpartizipien = ['angenommen', 'ausgenommen', 'gegeben', 'gesetzt', 'ungeachtet', 'unterstellt', 'vorausgesetzt']
# the following can be combined with adverbials, even adverbs
# bis morgen, seit gestern, ab heute, von gestern
# nach links, von hier, nach oben, für gleich  
# bis in den frühen Morgen, seit unser letztes Treffen
Grenzpräpositionen = ['von', 'seit', 'ab', 'bis', 'nach']

# note 'werden' in both classes!
Modalverben = ['dürfen', 'können', 'mögen', 'möchten', 'müssen', 'sollen', 'werden', 'brauchen']
Kopulas = ['sein', 'werden', 'bleiben', 'geben', 'haben']

# NOTE: it looks like adjectives cannot be used productively!
# new ones are mainly added through derivation or complete new innovation
# can we list all basic adjectives in German?
Adjektive = ['albern', 'alt', 'arg', 'arm', 'barsch', 'bieder', 'bitter', 'blank', 'blass', 'blau', 'bleich', 'blind', 'blöd', 'blond', 'bös', 'braun', 'brav', 'breit', 'brüsk', 'bunt', 'derb', 'deutsch', 'dicht', 'dick', 'doof', 'dreist', 'dumm', 'dumpf', 'dunkel', 'dünn', 'dürr', 'düster', 'echt', 'edel', 'eigen', 'einzig', 'eitel', 'elend', 'eng', 'ernst', 'fad', 'falsch', 'faul', 'feig', 'fein', 'feist', 'fern', 'fesch', 'fest', 'fett', 'feucht', 'fies', 'finster', 'firn', 'flach', 'flau', 'flink', 'flott', 'forsch', 'frech', 'frei', 'fremd', 'froh', 'fromm', 'früh', 'gar', 'geil', 'gelb', 'gemein', 'genau', 'gerade', 'gering', 'geschwind', 'gesund', 'glatt', 'gleich', 'grau', 'greis', 'grell', 'grob', 'groß', 'grün', 'gut', 'hager', 'harsch', 'hart', 'heikel', 'heil', 'heiser', 'heiß', 'heiter', 'hell', 'herb', 'hoch', 'hohl', 'hübsch', 'irr', 'jäh', 'jung', 'kahl', 'kalt', 'kaputt', 'karg', 'keck', 'kess', 'keusch', 'kirre', 'klamm', 'klar', 'klein', 'klug', 'knapp', 'krank', 'krass', 'kraus', 'krud', 'krumm', 'kühl', 'kühn', 'kurz', 'lahm', 'lang', 'lasch', 'lau', 'laut', 'lauter', 'lecker', 'leer', 'leicht', 'leise', 'licht', 'lieb', 'lila', 'locker', 'los', 'mager', 'matt', 'mies', 'mild', 'morsch', 'müde', 'munter', 'mürb', 'nackt', 'nah', 'nass', 'nett', 'neu', 'nieder', 'öd', 'offen', 'orange', 'platt', 'plump', 'prall', 'prüde', 'rank', 'rar', 'rasch', 'rau', 'rauch', 'recht', 'rege', 'reich', 'reif', 'rein', 'roh', 'rosa', 'rot', 'rüd', 'rund', 'sacht', 'sanft', 'satt', 'sauber', 'sauer', 'schal', 'scharf', 'scheu', 'schick', 'schief', 'schlaff', 'schlank', 'schlapp', 'schlau', 'schlecht', 'schlicht', 'schlimm', 'schmal', 'schmuck', 'schnell', 'schnöd', 'schön', 'schräg', 'schrill', 'schroff', 'schwach', 'schwarz', 'schwer', 'schwul', 'schwül', 'seicht', 'selten', 'sicher', 'sonstig', 'spät', 'spitz', 'spröd', 'stark', 'starr', 'steif', 'steil', 'stier', 'still', 'stolz', 'straff', 'stramm', 'streng', 'stumm', 'stumpf', 'stur', 'süß', 'tapfer', 'taub', 'teuer', 'tief', 'toll', 'tot', 'träg', 'treu', 'trocken', 'trüb', 'übel', 'vag', 'viel', 'voll', 'wach', 'wacker', 'wahr', 'warm', 'weh', 'weich', 'weise', 'weiß', 'weit', 'wild', 'wirr', 'wirsch', 'wund', 'wüst', 'zäh', 'zähe', 'zahm', 'zart']

Adverbien = ['abends', 'anfangs', 'bald', 'bisher', 'da', 'dauernd', 'dort', 'draußen', 'drinnen', 'drüben', 'ebenfalls', 'endlich', 'fast', 'früh', 'ganz', 'geradewegs', 'gerne', 'gestern', 'gewiss', 'halbwegs', 'heute', 'hier', 'hinten', 'hoch', 'immer', 'jetzt', 'keinesfalls', 'keineswegs', 'links', 'mittags', 'morgen', 'morgens', 'nachmittags', 'nachts', 'natürlich', 'neulich', 'noch', 'nun', 'oben', 'oft', 'rechts', 'schon', 'selbst', 'sofort', 'unten', 'unterwegs', 'überall', 'übermorgen', 'unbedingt', 'von vornherein', 'vorgestern', 'vorn', 'wieder']

Konjunktionaladverbien = ['abermals', 'allein', 'allemal', 'allenfalls', 'allerdings', 'alsbald', 'alsdann', 'also', 'anderenfalls', 'andererseits', 'andernteils', 'anschließend', 'ansonsten', 'anstatt dessen', 'auch', 'aufgrund dessen', 'ausschließlich', 'außerdem', 'beispielsweise', 'beziehungsweise', 'bestenfalls', 'bloß', 'da', 'dabei', 'dadurch', 'dafür', 'daher', 'dahingegen', 'damit', 'danach', 'daneben', 'dann', 'darauf', 'darauhfin', 'darüber hinaus', 'darum', 'davor', 'dazu', 'dazwischen', 'dementgegen', 'dementsprechend', 'demgegenüber', 'demgemäß', 'demnach', 'demzufolge', 'dennoch', 'derweilen', 'desgleichen', 'deshalb', 'deswegen', 'ferner', 'folglich', 'freilich', 'gegebenenfalls', 'genauso', 'gleichwohl', 'gleichfalls', 'gleichzeitig', 'hernach', 'hierbei', 'hierdurch', 'hiermit', 'hingegen', 'hinterher', 'hinwiederum', 'immerhin', 'im Übrigen', 'indes', 'indessen', 'infolgedessen', 'insbesondere', 'insofern', 'insoweit', 'inzwischen', 'jedoch', 'kaum', 'mal', 'mithin', 'meinerseits', 'mittlerweile', 'nachher', 'nämlich', 'nebenbei', 'nebenher', 'nichtsdestominder', 'nichtsdestoweniger', 'nichtsdestotrotz', 'nunmehr', 'nur', 'obendrein', 'ohnedies', 'ohnehin', 'schließlich', 'schon', 'seitdem', 'seither', 'selbst', 'so', 'sodann', 'somit', 'sonst', 'soviel', 'soweit', 'sowieso', 'stattdessen', 'trotzdem', 'überdies', 'überhaupt', 'unterdessen', 'vielmehr', 'vor allem', 'vorher', 'währenddessen', 'weiter', 'weiterhin', 'weiters', 'wieder', 'wiederum', 'wohlgemerkt', 'zudem', 'zuguterletzt', 'zumal', 'zusätzlich', 'zuvor', 'zwar', 'zwischendurch', 'zwischenzeitlich']

Frageadverbien = ['warum', 'weshalb', 'weswegen', 'wieso', 'wofür', 'wo', 'wohin', 'woher', 'wann', 'wie']

Negationen = ['nicht', 'nie', 'niemals', 'nicht mehr']

Modalpartikel = ['aber', 'auch', 'bloß', 'denn', 'doch', 'eben', 'eh', 'etwa', 'gar', 'halt', 'ja', 'nur', 'rein', 'ruhig', 'schon', 'wohl']

Genera = {
  'm': 'Maskulin',
  'n': 'Neutrum',
  'f': 'Feminin', 
  'p': 'Plural',
  'q': 'Queer',
  'r': 'Runde',
}

Kasus = ['Nominativ', 'Akkusativ', 'Dativ', 'Genitiv']

Präpositionen = {
  # temporary solution for comparison: treat them as prepositions
  'wie': 'Nominativ',
  'als': 'Nominativ',
  # Akkusativ
  'bis': 'Akkusativ',
  'durch': 'Akkusativ',
  'entlang': 'Akkusativ',
  'für': 'Akkusativ',
  'gegen': 'Akkusativ',
  'ohne': 'Akkusativ',
  'um': 'Akkusativ',
  # Dativ
  'ab': 'Dativ',
  'aus': 'Dativ',
  'außer': 'Dativ',
  'bei': 'Dativ',
  'entgegen': 'Dativ',
  'entsprechend': 'Dativ',
  'gegenüber': 'Dativ',
  'gemäß': 'Dativ',
  'mit': 'Dativ',
  'nach': 'Dativ',
  'nahe': 'Dativ',
  'seit': 'Dativ',
  'von': 'Dativ',
  'zu': 'Dativ',
  # Wechselpräpositionen: dative default for stative location, use 'Bewegung' to make accusative
  # governed roles are variable, but: auf/über/in/vor take accusative when governed
  # an is variable (denken an Dativ, Dativ alternation with accusative)
  'an': 'Dativ',
  'auf': 'Dativ',
  'hinter': 'Dativ',
  'in': 'Dativ',
  'neben': 'Dativ',
  'über': 'Dativ',
  'unter': 'Dativ',
  'vor': 'Dativ',
  'zwischen': 'Dativ',
  # Genitiv
  'abseits': 'Genitiv',
  'abzüglich': 'Genitiv',
  'angesichts': 'Genitiv',
  'anfangs': 'Genitiv',
  'anhand': 'Genitiv',
  'anstatt': 'Genitiv',
  'außerhalb': 'Genitiv',
  'aufgrund': 'Genitiv',
  'bar': 'Genitiv',
  'bezüglich': 'Genitiv',
  'dank': 'Genitiv',
  'diesseits': 'Genitiv',
  'einschließlich': 'Genitiv',
  'entlang': 'Genitiv',
  'infolge': 'Genitiv',
  'innerhalb': 'Genitiv',
  'inmitten': 'Genitiv',
  'jenseits': 'Genitiv',
  'kraft': 'Genitiv',
  'längs': 'Genitiv',
  'laut': 'Genitiv',
  'mittels': 'Genitiv',
  'ob': 'Genitiv',
  'oberhalb': 'Genitiv',
  'seitens': 'Genitiv',
  'statt': 'Genitiv',
  'trotz': 'Genitiv',
  'ungeachtet': 'Genitiv',
  'unterhalb': 'Genitiv',
  'unweit': 'Genitiv',
  'während': 'Genitiv',
  'wegen': 'Genitiv',
  'zugunsten': 'Genitiv',
}

KomparativUmlaut = ['alt', 'arm', 'dumm', 'fromm', 'gesund', 'grob', 'groß', 'hart', 'hoh', 'kalt', 'klug', 'kurz', 'lang', 'nah', 'scharf', 'stark', 'warm']

KomparativSuppletion = {
  'gut':{
    'Komparativ': 'besser',
    'Superlativ': 'best',
  },
  'viel':{
    'Komparativ': 'mehr',
    'Superlativ': 'meist',
  },
}

Personalpronomina = {
  'Singular':{
    '1':{
      'Nominativ': 'ich',
      'Akkusativ': 'mich',
      'Dativ': 'mir',
      'Genitiv': 'meiner',
      'Attributiv': 'mein'
    },
    '2':{
      'Nominativ': 'du',
      'Akkusativ': 'dich',
      'Dativ': 'dir',
      'Genitiv': 'deiner',
      'Attributiv': 'dein'
    },
  },
  'Plural':{
    '1':{
      'Nominativ': 'wir',
      'Akkusativ': 'uns',
      'Dativ': 'uns',
      'Genitiv': 'unser',
      'Attributiv': 'unser'
    },
    '2':{
      'Nominativ': 'ihr',
      'Akkusativ': 'euch',
      'Dativ': 'euch',
      'Genitiv': 'euer',
      'Attributiv': 'euer'
    }
  }
}

Fragepronomina = {
  'Belebt':{
    'Nominativ': 'wer',
    'Akkusativ': 'wen',
    'Dativ': 'wem',
    'Genitiv': 'wessen',
  },
  'Unbelebt':{
    'Nominativ': 'was',
    'Akkusativ': 'was',
    'Dativ': 'was',
    'Genitiv': 'wessen',
  }
}

Anaphora = {
  'Maskulin':{
    'Nominativ': 'er',
    'Akkusativ': 'ihn',
    'Dativ': 'ihm',
    'Genitiv': 'seiner',
    'Attributiv': 'sein'
  },
  'Neutrum':{
    'Nominativ': 'es',
    'Akkusativ': 'es',
    'Dativ': 'ihm',
    'Genitiv': 'seiner',
    'Attributiv': 'sein'
  },
  'Feminin':{
    'Nominativ': 'sie',
    'Akkusativ': 'sie',
    'Dativ': 'ihr',
    'Genitiv': 'ihrer',
    'Attributiv': 'ihr'
  },
  'Plural':{
    'Nominativ': 'sie',
    'Akkusativ': 'sie',
    'Dativ': 'ihnen',
    'Genitiv': 'ihrer',
    'Attributiv': 'ihr'
  }
}

Demonstrativpronomina = { # also relative pronoun!
  'Nominativ':{
    'Maskulin': 'der',
    'Neutrum': 'das',
    'Feminin': 'die',
    'Plural': 'die'
    },
  'Akkusativ':{
    'Maskulin': 'den',
    'Neutrum': 'das',
    'Feminin': 'die',
    'Plural': 'die'
  },
  'Dativ':{
    'Maskulin': 'dem',
    'Neutrum': 'dem',
    'Feminin': 'der',
    'Plural': 'denen'
  },
  'Genitiv':{
    'Maskulin': 'dessen',
    'Neutrum': 'dessen',
    'Feminin': 'deren',
    'Plural': 'deren'
  }
}

Definitartikel = {
  'Nominativ':{
    'Maskulin': 'der',
    'Neutrum': 'das',
    'Feminin': 'die',
    'Plural': 'die'
    },
  'Akkusativ':{
    'Maskulin': 'den',
    'Neutrum': 'das',
    'Feminin': 'die',
    'Plural': 'die'
  },
  'Dativ':{
    'Maskulin': 'dem',
    'Neutrum': 'dem',
    'Feminin': 'der',
    'Plural': 'den'
  },
  'Genitiv':{
    'Maskulin': 'des',
    'Neutrum': 'des',
    'Feminin': 'der',
    'Plural': 'der'
  }
}

Quantoren = {
  'dies':{
    'Flexion': 'dies',
    'Deklination': 'schwach',
  },
  'jen':{
    'Flexion': 'dies',
    'Deklination': 'schwach',
  },
  'all':{
    'Flexion': 'all',
    'Deklination': 'schwach',
  },
  'jed':{
    'Flexion': 'all',
    'Deklination': 'schwach',
  },
  'beid':{
    'Flexion': 'all',
    'Deklination': 'schwach',
  },
  'solch':{
    'Flexion': 'all',
    'Deklination': 'schwach',
  },
  'manch':{
    'Flexion': 'all',
    'Deklination': 'schwach',
  },
  'kein':{
    'Flexion': 'ein',
    'Deklination': 'gemischt',
  },
}

# n-Deklination:
# Architekt, Bär, Bauer, Fotograf, Herr, Held, Katholik, Mensch, Monarch, Philosoph, Satellit, Prinz, Rebell, Soldat, Fürst, Graf, Prinz, Zar, Welf, Schenk, Hirt, Spatz, Fink, Pfau, Greif, Leu, Narr, Tor, Depp, Geck, Mohr, Oberst, Untertan, Vorfahr, Ahn, Typ, Graph, Tyrann, Kamerad

Substantive = {
  'Bäcker':{
    'Geschlecht': 'Maskulin',
    'Plural': 'Bäcker',
    'Belebt': True,
  },
  'Leistungserbringung':{
    'Geschlecht': 'Feminin',
    'Plural': None,
  },
  'Kostenvorteil':{
    'Geschlecht': 'Maskulin',
    'Plural': 'Kostenvorteile',
  },
  'Wahl':{
    'Geschlecht': 'Feminin',
    'Plural': 'Wahlen',
  },
  'Erfüllung':{
    'Geschlecht': 'Feminin',
    'Plural': None,
  },
  'Entscheidung':{
    'Geschlecht': 'Feminin',
    'Plural': 'Entscheidungen',
  },
  'Grund':{
    'Geschlecht': 'Maskulin',
    'Plural': 'Gründe',
  },
  'Schadenersatz':{
    'Geschlecht': 'Maskulin',
    'Plural': None,
  },
  'Zahlung':{
    'Geschlecht': 'Feminin',
    'Plural': 'Zahlungen',
  },
  'Schuldner':{
    'Geschlecht': 'Maskulin',
    'Plural': 'Schuldner',
    'Belebt': True,
  },
  'Leistung':{
    'Geschlecht': 'Feminin',
    'Plural': 'Leistungen',
  },
  'Lage':{
    'Geschlecht': 'Feminin',
    'Plural': 'Lagen',
  },
  'Verzögerungsschaden':{
    'Geschlecht': 'Feminin',
    'Plural': 'Verzögerungsschäden',
  },
  'Schaden':{
    'Geschlecht': 'Maskulin',
    'Plural': 'Schäden',
  },
  'Ersatz':{
    'Geschlecht': 'Maskulin',
    'Plural': None,
  },
  'Natur':{
    'Geschlecht': 'Feminin',
    'Plural': 'Naturen',
  },
  'Leistung':{
    'Geschlecht': 'Feminin',
    'Plural': 'Leistungen',
  },
  'Gläubiger':{
    'Geschlecht': 'Maskulin',
    'Plural': 'Gläubiger',
    'Belebt': True,
  },
  'Grund':{
    'Geschlecht': 'Maskulin',
    'Plural': 'Gründe',
  },
  'Lächeln':{
    'Geschlecht': 'Neutrum',
    'Plural': 'Lächeln',
  },
  'Grund':{
    'Geschlecht': 'Maskulin',
    'Plural': 'Gründe',
  },
  'Schuh':{
    'Geschlecht': 'Maskulin',
    'Plural': 'Schuhe',
  },
  'Auto':{
    'Geschlecht': 'Neutrum',
    'Plural': 'Autos',
  },
  'Tag':{
    'Geschlecht': 'Maskulin',
    'Plural': 'Tage',
  }, 
  'Mann':{
    'Geschlecht': 'Maskulin',
    'Belebt': True,
    'Plural': 'Männer',
  }, 
  'Karl':{
    'Geschlecht': 'Maskulin',
    'Belebt': True,
  },
  'Maria':{
    'Geschlecht': 'Feminin',
    'Belebt': True,
  },
  'Frau':{
    'Geschlecht': 'Feminin',
    'Belebt': True,
    'Plural': 'Frauen',
  },  
  'Schrank':{
    'Geschlecht': 'Maskulin',
    'Plural': 'Schränke'
  },  
  'Rat':{
    'Geschlecht': 'Maskulin',
    'Plural': 'Räte'
  },
  'Beschluss':{
    'Geschlecht': 'Maskulin',
    'Plural': 'Beschlüsse'
  },
  'Grundlage':{
    'Geschlecht': 'Feminin',
    'Plural': 'Grundlagen'
  },
  'Dokument':{
    'Geschlecht': 'Neutrum',
    'Plural': 'Dokumente'
  },
  'Angst':{
    'Geschlecht': 'Feminin',
    'Plural': 'Ängste'
  },
  'Mutter':{
    'Geschlecht': 'Feminin',
    'Belebt': True,
    'Plural': 'Mütter',
  },
  'Vater':{
    'Geschlecht': 'Maskulin',
    'Belebt': True,
    'Plural': 'Väter',
  },
  'Zuschauer':{
    'Geschlecht': 'Maskulin',
    'Belebt': True,
    'Plural': 'Zuschauer',
  },
  'Buch':{
    'Geschlecht': 'Neutrum',
    'Plural': 'Bücher',
  },
  'Kind':{
    'Geschlecht': 'Neutrum',
    'Belebt': True,
    'Plural': 'Kinder',
  },
  'Plan':{
    'Geschlecht': 'Maskulin',
    'Plural': 'Pläne',
  },
  'Frage':{
    'Geschlecht': 'Feminin',
    'Plural': 'Fragen',
  },
  'Haus':{
    'Geschlecht': 'Neutrum',
    'Plural': 'Häuser'
  },
  'Fenster':{
    'Geschlecht': 'Neutrum',
    'Plural': 'Fenster',
  },
  'Ursache':{
    'Geschlecht': 'Feminin',
    'Plural': 'Ursachen',
  },
  'Tanz':{
    'Geschlecht': 'Maskulin',
    'Plural': 'Tänze',
  },
  'Mensch':{
    'Geschlecht': 'Maskulin',
    'Belebt': True,
    'Plural': 'Menschen',
    'n-Deklination': True,
  },
}

# ==========
# Inflection
# ==========

Verbflexion = {
  'Präsens':{
    'Singular':{
       '1': 'e',
       '2': 'st',
       '3': 't',
     },
     'Plural':{
       '1': 'en',
       '2': 't',
       '3': 'en',
    }
  },
  'Präteritum':{
    'Singular':{
       '1': '',
       '2': 'st',
       '3': '',
     },
     'Plural':{
       '1': 'n',
       '2': 't',
       '3': 'n',
    }
  },
}

Adjektivflexion = {
  'schwach':{
    'Nominativ':{
      'Maskulin': 'e',
      'Neutrum': 'e',
      'Feminin': 'e',
      'Plural': 'en'
    },
    'Akkusativ':{
      'Maskulin': 'en',
      'Neutrum': 'e',
      'Feminin': 'e',
      'Plural': 'en'
    },
    'Dativ':{
      'Maskulin': 'en',
      'Neutrum': 'en',
      'Feminin': 'en',
      'Plural': 'en'
    },
    'Genitiv':{
      'Maskulin': 'en',
      'Neutrum': 'en',
      'Feminin': 'en',
      'Plural': 'en'
    }
  },
  'gemischt':{
    'Nominativ':{
      'Maskulin': 'er',
      'Neutrum': 'es',
      'Feminin': 'e',
      'Plural': 'en'
    },
    'Akkusativ':{
      'Maskulin': 'en',
      'Neutrum': 'es',
      'Feminin': 'e',
      'Plural': 'en'
    },
    'Dativ':{
      'Maskulin': 'en',
      'Neutrum': 'en',
      'Feminin': 'en',
      'Plural': 'en'
    },
    'Genitiv':{
      'Maskulin': 'en',
      'Neutrum': 'en',
      'Feminin': 'en',
      'Plural': 'en'
    }
  },
  'stark':{
    'Nominativ':{
      'Maskulin': 'er',
      'Neutrum': 'es',
      'Feminin': 'e',
      'Plural': 'e'
    },
    'Akkusativ':{
      'Maskulin': 'en',
      'Neutrum': 'es',
      'Feminin': 'e',
      'Plural': 'e'
    },
    'Dativ':{
      'Maskulin': 'em',
      'Neutrum': 'em',
      'Feminin': 'er',
      'Plural': 'en'
    },
    'Genitiv':{
      'Maskulin': 'en',
      'Neutrum': 'en',
      'Feminin': 'er',
      'Plural': 'er'
    }
  }
}

Quantorflexion = {
  'ein':{
    'Nominativ':{
      'Maskulin': '',
      'Neutrum': '',
      'Feminin': 'e',
      'Plural': 'e'
      },
    'Akkusativ':{
      'Maskulin': 'en',
      'Neutrum': '',
      'Feminin': 'e',
      'Plural': 'e'
    },
    'Dativ':{
      'Maskulin': 'em',
      'Neutrum': 'em',
      'Feminin': 'er',
      'Plural': 'en'
    },
    'Genitiv':{
      'Maskulin': 'es',
      'Neutrum': 'es',
      'Feminin': 'er',
      'Plural': 'er'
    }
  },
  'dies':{
    'Nominativ':{
      'Maskulin': 'er',
      'Neutrum': 'es',
      'Feminin': 'e',
      'Plural': 'e'
      },
    'Akkusativ':{
      'Maskulin': 'en',
      'Neutrum': 'es',
      'Feminin': 'e',
      'Plural': 'e'
    },
    'Dativ':{
      'Maskulin': 'em',
      'Neutrum': 'em',
      'Feminin': 'er',
      'Plural': 'en'
    },
    'Genitiv':{
      'Maskulin': 'es',
      'Neutrum': 'es',
      'Feminin': 'er',
      'Plural': 'er'
    }
  },
  'all':{
    'Nominativ':{
      'Maskulin': 'er',
      'Neutrum': 'es',
      'Feminin': 'e',
      'Plural': 'e'
      },
    'Akkusativ':{
      'Maskulin': 'en',
      'Neutrum': 'es',
      'Feminin': 'e',
      'Plural': 'e'
    },
    'Dativ':{
      'Maskulin': 'em',
      'Neutrum': 'em',
      'Feminin': 'er',
      'Plural': 'en'
    },
    'Genitiv':{
      'Maskulin': 'en',
      'Neutrum': 'en',
      'Feminin': 'er',
      'Plural': 'er'
    }
  },
}
