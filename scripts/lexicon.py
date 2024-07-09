# TODO: double conjuncts: mal/mal, entweder/oder, sowohl/als-wie-auch, wenn/dann, weder/noch, nichtnur/sondernauch
# TODO: difference between nominal and clausal conjunction
Konjunktionen = ['und', 'und zwar', 'oder', 'aber', 'doch', 'sondern', 'denn', 'vorausgesetzt', 'jedoch', 'sowie', 'noch']
# NOTE: 'wie/wo' here in the meaning of 'als'
Subjunktionen = ['als', 'als ob', 'bevor', 'bis', 'da', 'damit', 'ehe', 'falls', 'indem', 'insofern', 'insoweit', 'nachdem', 'obgleich', 'obschon', 'obwohl', 'obzwar', 'seit', 'seitdem', 'sobald', 'sofern', 'solange', 'sooft', 'sosehr', 'soviel', 'soweit', 'sowie', 'trotzdem', 'während', 'weil', 'wenn', 'wenngleich', 'wie', 'wo']
# Temporale Subjunktionen mit modifikation: bis ganz kurz nachdem, kurz bevor, genau als, genau seit, ungefähr bis, ungefähr seitdem, 

# Begründung (um), Alternative (statt, anstatt, anstelle), Außnahme (ohne: A-aber-nicht-B, außer: nicht-A-aber-B)
# NOTE: there is an old-fashioned usage of 'bis dass' not included here
Satzpräpositionen = ['um', 'ohne', 'außer', 'ausser', 'statt', 'anstatt', 'anstelle', 'im Falle', 'für den Fall']

# abgesehen davon, dass
Satzpartizipien = ['angenommen', 'ausgenommen', 'gegeben', 'gesetzt', 'ungeachtet', 'unterstellt', 'vorausgesetzt']

# the following can be combined with adverbials, even adverbs
# bis morgen, seit gestern, ab heute, von gestern
# nach links, von hier, nach oben  
# von ... an
# für unterwegs/immer/umsonst/zwischendurch
Grenzpartikel = ['von', 'nach', 'seit', 'ab', 'bis', 'für']

# bis in den frühen Morgen, bis zu den Ferien, bis zum See
# bis fast bei der Ladentür
# bis an die Gartentür, bis unter das Dach, bis auf die Grundmauern, bis hinter den Wald, bis neben der Tür
# bis weit über die Knie, bis gegen Mitternacht, bis vor kurzem, bis auf weiteres
# seit/bis kurz vor/nach dem Essen
# von hinter der Torlinie, bis zwischen die Schulterblätter
# bis um Mitternacht, bis um das Zehnfache: this seems to be a different construction with 'um' meaning 'circa' (but still governing accusative!)
# rund um den Kehlkopf, weit um den Bahnhof
# schräg gegenüber
# nach nahe der Stadt: 'nahe' mostly in constructions in which it is almost still adjectival
# Ein Foul an Lászlo Kleinheisler verlegte Schiedsrichter Christian Dingert zu unrecht nach (weit) außerhalb des Strafraums
Lokalpräpositionen = ['an', 'auf', 'bei', 'gegenüber', 'hinter', 'in', 'neben', 'unter', 'um', 'über', 'vor', 'zwischen', 'zu', 'nach', 'außerhalb']
# = Wechselpräpositionen including 'bei, zu, nach, außerhalb, um, gegenüber'

# almost the same as predicative prepositions. But note:
# für, gegen, aus also predicative
# zu not predicative

# adverbiale adjektive nicht trennbar von präposition (nicht vorfeldfähig):
# kurz vor, seitlich vor, direkt vor, unmittelbar vor, dicht vor, knapp vor, schräg vor, weit vor, leicht hinter, östlich hinter, gerade über, hoch über, tief unter, gleich gegenüber
Präpositionsspezifikation = ['dicht', 'direkt', 'eng', 'genau', 'gerade', 'gleich', 'hoch', 'knapp', 'kurz', 'lang', 'leicht', 'nah', 'schräg', 'tief', 'weit', 'östlich', 'seitlich', 'ungefähr', 'unmittelbar']

# note 'werden' in both classes!
Modalverben = ['dürfen', 'können', 'mögen', 'möchten', 'müssen', 'sollen', 'werden', 'brauchen']
Kopulas = ['sein', 'werden', 'bleiben', 'geben', 'haben']

# NOTE: it looks like adjectives cannot be used productively!
# new ones are mainly added through derivation or complete new innovation
# can we list all basic adjectives in German?
Adjektive = ['absolut', 'albern', 'alt', 'andere', 'arg', 'arm', 'äußer', 'barsch', 'besonder', 'bieder', 'billig', 'bitter', 'blank', 'blass', 'blau', 'bleich', 'blind', 'blöd', 'blond', 'bloß', 'böse', 'braun', 'brav', 'breit', 'brüsk', 'bunt', 'derb', 'deutsch', 'dicht', 'dick', 'direkt', 'doof', 'doppelt', 'dreist', 'dumm', 'dumpf', 'dunkel', 'dünn', 'dürr', 'düster', 'echt', 'edel', 'egal', 'eigen', 'einzig', 'eitel', 'eklatant', 'elend', 'eng', 'enorm', 'ernst', 'erst', 'extrem', 'fad', 'falsch', 'faul', 'feig', 'fein', 'feist', 'fern', 'fesch', 'fest', 'fett', 'feucht', 'fies', 'finster', 'firn', 'flach', 'flau', 'flink', 'flott', 'forsch', 'frech', 'frei', 'fremd', 'froh', 'fromm', 'früh', 'ganz', 'gar', 'geil', 'gelb', 'gemein', 'genau', 'gerade', 'gering', 'geschwind', 'gesund', 'gewiss', 'glatt', 'gleich', 'grau', 'greis', 'grell', 'grob', 'groß', 'grün', 'gut', 'hager', 'harsch', 'hart', 'heikel', 'heil', 'heiser', 'heiß', 'heiter', 'hell', 'herb', 'hinter', 'hohe', 'hohl', 'hübsch', 'inner', 'irre', 'jäh', 'jung', 'kahl', 'kalt', 'kaputt', 'karg', 'keck', 'kess', 'keusch', 'kirre', 'klamm', 'klar', 'klein', 'klug', 'knapp', 'komplett', 'krank', 'krass', 'kraus', 'krude', 'krumm', 'kühl', 'kühn', 'kurz', 'lahm', 'lang', 'lasch', 'lau', 'laut', 'lauter', 'lecker', 'leer', 'leicht', 'leise', 'letzt', 'licht', 'lieb', 'lila', 'linke', 'locker', 'los', 'mager', 'matt', 'mies', 'mild', 'morsch', 'müde', 'munter', 'mürb', 'nächste', 'nackt', 'nah', 'nass', 'nett', 'neu', 'niedere', 'obere', 'öd', 'offen', 'orange', 'platt', 'plump', 'prall', 'prüde', 'rank', 'rar', 'rasch', 'rau', 'rechte', 'rege', 'reich', 'reif', 'rein', 'relativ', 'roh', 'rosa', 'rot', 'rüde', 'rund', 'sacht', 'sanft', 'satt', 'sauber', 'sauer', 'schal', 'scharf', 'scheu', 'schick', 'schief', 'schlaff', 'schlank', 'schlapp', 'schlau', 'schlecht', 'schlicht', 'schlimm', 'schmal', 'schmuck', 'schnell', 'schnöde', 'schön', 'schräg', 'schrill', 'schroff', 'schwach', 'schwarz', 'schwer', 'schwul', 'schwül', 'seicht', 'selten', 'sicher', 'spät', 'spitz', 'spröde', 'stark', 'starr', 'steif', 'steil', 'stier', 'still', 'stolz', 'straff', 'stramm', 'streng', 'stumm', 'stumpf', 'stur', 'süß', 'tapfer', 'taub', 'teuer', 'tief', 'toll', 'tot', 'total', 'träge', 'treu', 'trocken', 'trüb', 'ungefähr', 'unter', 'übel', 'vage', 'viel', 'voll', 'vollkommen', 'vorder', 'wach', 'wacker', 'wahr', 'warm', 'weh', 'weich', 'weise', 'weiß', 'weit', 'wild', 'wirr', 'wirsch', 'wund', 'wüst', 'zäh', 'zahm', 'zart']
# special adverbs n/r: außen, innen, oben, unten, vorne, hinten
# special adverbs s: linke, rechte, andere, besondere
# special adverbs: hoch/hoh, nieder/niedrig
# special predication: letzte(r)

# Note regular adjectival suffixes: ig/bar/end/los/sam/fach/lich/haft/isch/gemäß/mäßig/artig 
# sometimes root does not exist (anymore): häufig, ständig, wichtig, abwesend, anwesend, fortwährend, gewöhnlich, natürlich, wahrscheinlich, unmittelbar, demenstsprechend, gleichzeitig, anschließend, ausschließlich
# der dem Festessen anschließender Tanz
# note exceptions: folglich/freilich/nämlich/schließlich/lediglich only adverbial!
# Adjektive? Often listed as adverbs, because different meaning: anschließend, ausgerechnet, ausschließlich, demenstsprechend, neulich, gleichzeitig, zwischenzeitlich

# no predication: ziemlich, sonstig, zusätzlich, ehemalig, zwischenzeitlich, hochgradig, sogenannt, regelrecht, völlig, nämlich
# no referent: zwischenzeitlich, völlig
# also no Gradparitkel possible with these? but: fast völlig

Steigerungspräfixe = ['bitter', 'erz', 'hoch', 'hyper', 'mega', 'quietsch', 'schwer', 'super', 'tief', 'ultra', 'un', 'ur']
# hochpeinlich, schwerkrank, fieftraurig, bitterkalt, hypernervös, erzfaul, megaschnell, superfein, ultramodern, uralt
# many composita, e.g handgroß, schwarzgrün, kerngesund, quietschbund, usw.

# Ursprung teilweise adjektival, teilweise adverbial, aber das scheint keine Rolle zu spielen in der Benutzung
Gradadjektiv = ['absolut', 'annähernd', 'arg', 'ausgesprochen', 'außergewöhnlich', 'außerordentlich', 'äußerst', 'echt', 'eklatant', 'enorm', 'entsetzlich', 'erbärmlich', 'extrem', 'furchtbar', 'ganz', 'hochgradig', 'höchst', 'irre', 'komplett', 'recht', 'regelrecht', 'relativ', 'restlos', 'richtig', 'schrecklich', 'schön', 'tierisch', 'total', 'traumhaft', 'ungemein', 'ungeheuerlich', 'ungewöhnlich', 'unglaublich', 'unheimlich', 'unwahrscheinlich', 'übermäßig', 'verhältnismäßig', 'verschwindend', 'vollkommen', 'völlig', 'weit', 'weitgehend', 'wahnsinnig', 'ziemlich']
Gradadverb = ['beinahe', 'besonders', 'dermaßen', 'derart', 'durchaus', 'eher', 'einigermaßen', 'etwas', 'fast', 'kaum', 'nur', 'so', 'vergleichsweise', 'zumindest']
Gradpartikel = ['nahezu', 'schier', 'sehr', 'sogar', 'spätestens', 'überaus', 'weitaus', 'zu']

# Abkürzung??? er hat sehr geschwitzt

# mit NP
Fokuspartikel = ['allein', 'allenfalls', 'auch', 'ausgerechnet', 'bereits', 'besonders', 'bestenfalls', 'bloß', 'einzig', 'erst', 'gerade', 'mindestens', 'lediglich', 'nur', 'schon', 'selbst', 'sogar', 'spätestens', 'vor allem', 'wenigstens', 'zumindestens']

# also Post-NP: selbst, allein

# post-first fokus? 
# allerdings, also, andererseits, andernteils, auch, beispielsweise, freilich, hingegen, hinwiederum, immerhin, indes, indessen, insbesondere, jedoch, mittlerweile, nämlich, nur, schließlich, schon, sonst, stattdessen, überhaupt, unterdessen, währenddessen, wiederum, zumindest, zwar


# nur [fast alle] [maximal drei] Kinder
# die erste/nächste/letzte/gleiche drei freie Tage : reguläre adjektive mit Kongruenz!
# mit den erwähnten drei Schichten
Numeralpartikel = ['maximal', 'minimal', 'mindestens', 'ungefähr', 'zumindestens']

Adverbien = ['abends', 'anders', 'anfangs', 'bald', 'besonders', 'bisher', 'da', 'dauernd', 'dort', 'draußen', 'drinnen', 'drüben', 'ebenfalls', 'eingangs', 'einmal', 'endlich', 'fast', 'geradewegs', 'gerne', 'gestern', 'gewiss', 'gleich', 'halbwegs', 'heute', 'hier', 'hinten', 'hoch', 'immer', 'jetzt', 'keinesfalls', 'keineswegs', 'links', 'manchmal', 'mittags', 'mittendrin', 'morgen', 'morgens', 'nachmittags', 'nachts', 'natürlich', 'nebenan', 'neulich', 'nie', 'nirgends', 'nun', 'oben', 'oft', 'rechts', 'schon', 'selbst', 'so', 'sofort', 'umsonst', 'unten', 'unterwegs', 'überall', 'übermorgen', 'unbedingt', 'von vornherein', 'vorgestern', 'vormittags', 'vorn', 'vorne', 'wieder', 'zunächst', 'knack']

Konjunktionaladverbien = ['abermals', 'allein', 'allemal', 'allenfalls', 'allerdings', 'alsbald', 'alsdann', 'also', 'anderenfalls', 'andererseits', 'andernteils', 'anschließend', 'ansonsten', 'auch', 'ausschließlich', 'außerdem', 'beispielsweise', 'beziehungsweise', 'bestenfalls', 'bloß', 'dabei', 'dadurch', 'dafür', 'daher', 'dahingegen', 'damit', 'danach', 'daneben', 'dann', 'darauf', 'darauhfin', 'darüber hinaus', 'darum', 'davor', 'dazu', 'dazwischen', 'dementgegen', 'demgegenüber', 'demgemäß', 'demnach', 'demzufolge', 'dennoch', 'derweilen', 'desgleichen', 'deshalb', 'deswegen', 'ebenfalls', 'ferner', 'folglich', 'freilich', 'gegebenenfalls', 'genauso', 'gleichwohl', 'gleichfalls', 'gleichzeitig', 'hernach', 'hierbei', 'hierdurch', 'hiermit', 'hingegen', 'hinterher', 'hinwiederum', 'immerhin', 'im Übrigen', 'indes', 'indessen', 'infolgedessen', 'insbesondere', 'insofern', 'insoweit', 'inzwischen', 'jedoch', 'kaum', 'mal', 'mithin', 'meinerseits', 'mittlerweile', 'nachher', 'nämlich', 'nebenbei', 'nebenher', 'nichtsdestoweniger', 'nichtsdestotrotz', 'nunmehr', 'nur', 'obendrein', 'ohnedies', 'ohnehin', 'schließlich', 'schon', 'seitdem', 'seither', 'sodann', 'somit', 'sonst', 'soviel', 'soweit', 'sowieso', 'stattdessen', 'trotzdem', 'überdies', 'überhaupt', 'unterdessen', 'vielmehr', 'vor allem', 'vorher', 'währenddessen', 'weiterhin', 'weiters', 'wieder', 'wiederum', 'wohlgemerkt', 'zudem', 'zuguterletzt', 'zumal', 'zumindest', 'zuvor', 'zwar', 'zwischendurch', 'zwischenzeitlich']

Frageadverbien = ['warum', 'weshalb', 'weswegen', 'wieso', 'wofür', 'wo', 'wohin', 'woher', 'wann', 'wie']

Negationen = ['nicht', 'nie', 'niemals', 'nirgends', 'nirgendwo', 'nichts', 'nie mehr', 'nicht mehr']

Abtönungspartikel = ['aber', 'auch', 'bloß', 'denn', 'doch', 'eben', 'eh', 'etwa', 'gar', 'halt', 'ja', 'mal', 'nämlich', 'noch', 'nur', 'rein', 'ruhig', 'schon', 'wohl']

Genera = {
  'm': 'Maskulin',
  'n': 'Neutrum',
  'f': 'Feminin', 
  'p': 'Plural',
  'q': 'Queer',
  'r': 'Runde',
}

Kasus = ['Nominativ', 'Akkusativ', 'Dativ', 'Genitiv']

# Postpositionen:
# Akkusativ: hoch, entlang, über, durch (den Berg hoch, den Fluss entlang, den Tag über, die Nacht durch)
# Dativ: nach, zufolge, gegenüber, voran. hinterher (?) (dem Buch voran, meiner Meinung nach, dem Regen zufolge, mir gegenüber, dem Hund hinterher)
# Genitiv: halber, wegen (der Einfachheit halber, des Geldes wegen)

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
  'samt': 'Dativ',
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
  'eingangs': 'Genitiv', # eingangs des zweiten Drittel
  'einschließlich': 'Genitiv',
  'entlang': 'Genitiv',
  'infolge': 'Genitiv',
  'innerhalb': 'Genitiv',
  'inmitten': 'Genitiv',
  'jenseits': 'Genitiv',
  'kraft': 'Genitiv',
  'längs': 'Genitiv',
  'laut': 'Genitiv',
  'links': 'Genitiv',
  'mittels': 'Genitiv',
  'ob': 'Genitiv',
  'oberhalb': 'Genitiv',
  'rechts': 'Genitiv',
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

# mit all/kein/jed: gar, fast, nahezu, beinahe, keineswegs
# Note: die Menschen laufen alle weg / Alle Menschen laufen weg
# Quantoren als Kopf: Alle, die rennen, werden zu spät kommen

# etwas? z.B. 'etwas Großes', 'etwas Zucker'

Quantoren = {
  'dies':{
    'Flexion': 'dies',
    'Deklination': 'schwach',
  },
  'jen':{
    'Flexion': 'dies',
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
  'all':{
    'Flexion': 'all',
    'Deklination': 'schwach',
  },
  'jed':{
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
  'Woche':{
    'Geschlecht': 'Feminin',
    'Plural': 'Wochen'
  },
  'Montag':{
    'Geschlecht': 'Maskulin'
  },
  'Apfel':{
    'Geschlecht': 'Maskulin'
  },
  'Theke':{
    'Geschlecht': 'Feminin'
  },
  'Weg':{
    'Geschlecht': 'Maskulin'
  },
  'Sonne':{
    'Geschlecht': 'Feminin',
    'Plural': 'Sonnen'
  },
  'Raupe':{
    'Geschlecht': 'Feminin',
    'Plural': 'Raupen',
    'Belebt': True
  },
  'Ei':{
    'Geschlecht': 'Neutrum',
    'Plural': 'Eier'
  },
  'Blatt':{
    'Geschlecht': 'Neutrum',
    'Plural': 'Blätter'
  },
  'Mondschein':{
    'Geschlecht': 'Maskulin',
    'Plural': None
  },
  'Straße':{
    'Geschlecht': 'Feminin',
    'Plural': 'Straßen'
  },
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
