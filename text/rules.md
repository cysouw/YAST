
# Rules for predication

## Clause (*Satz*)

## Predication (*Prädikation*)

Basically a verb with lexical arguments. A PHRASE leads to *Prädikatives Substantiv*
Lexical arguments can be filled with either PHRASE or SATZ (*Komplementsatz*)

- verbal predication

Nonverbal predication in German is 'overloaded': the same auxiliary/copula(!) constructions are used fro various different kinds of predication. In YAST they are treated as the same structures, but the interpretation is of course different. They all have roles 'Subjekt' and 'Prädikativ'

- possession (possessor(SUBJ) + possessee + auxiliary)
- nominal predication (SUBJ + role 'noun predicate' + auxiliary)
- identification (noun predicate with definite marking)
- adjectival predication (SUBJ + attribute 'adjectival predicate' + auxiliary)
- adverbial predications (local/temporal)
- location predication with prepositions.

To be done:

- comparison (comparee(SUBJ) + 'comparison adjectival predicate' + auxiliary + role 'standard of comparison': both SATZ and PHRASE possible, additional Junktion *als, wie*)

## Event structure (*Ereignisstruktur*)

Epitheses, diatheses, tense

## Adverbial modification of predication (*Adverbiale*)

Either a PHRASE or SATZ (*Adverbialsatz*)
also: adverbs, negation, particles, adjectives+gradation

# Rules for reference

## Phrase (*Phrase*)

## Reference (*Referenz*)

Determination (quantification+article+numeral) and phrasal head
If SATZ then *Nominalisation*

## Identification (*Identifikation*)

## Attributive modification of reference (*Attribut*)

either PHRASE (*Präpositionalphrase*) or SATZ (*Relativsatz*)
also: adjectives+gradation

# Subordination

Clauses can be inserted at various places, leading to different kinds of *Subordination*. 

- *Koordination*
- *Subordination*
  - *Vollsatz*
    - *Subjunktionssatz* (adverbial + juncture)
    - *Präpositionssatz* (adverbial + juncture)
  - *Relatorsatz*
    - *Komplementsatz* (argument ± juncture)
    - *Weiterführungssatz* (= *weiterführender Relativsatz*) (adverbial)
    - *Adverbialrelativsatz* (adverbial + juncture)
    - *Relativsatz* (attributive)
  - *Kontrollsatz* (= *infiniter Nebensatz*)
    - *Kontrollkomplementsatz* (argument ± juncture)
    - *Kontrollpräpositionssatz* (adverbial + juncture)
    - *Partizipsatz* (= *Kontrollrelativsatz*) (attributive)

nonfinite:

Komplementsatz -> Kontrollkomplementsatz
präpositionssatz -> Kontrollpräpositionssatz (delete 'dass')
Relativsatz -> Partizipsatz

NOTE: *freier Relativsatz* is transparent combination of 'free' relative pronoun as head with a relative clause referring to it. This construction can grammaticalise, e.g. *Adverbialrelativsatz* is an example of this.

Three dimensions, 10 of 18 theoretical possiblities attested (Vollsatz always adverbial, Attributsatz never juncture. missing: Adverbialsatz+Kontrollsatz without juncture)

- Place of attachment (*Argumentsatz, Adverbialsatz, Attributsatz*)
- Structure of subordinate clause (*Vollsatz, Relatorsatz, Kontrollsatz*)
- Presence of juncture (*ja, nein*)

Lexical interpretation important


Sie wartet darauf, dass ihr Kind tanzt
Sie wartet auf den Tanz ihres Kindes

# Finishing up

## Lexical insertion

## Government and agreement

mostly inside phrase, except

- verbagreement between subject and finite verb
- reflexive pronoun agreement
- anaphoric reference inside sentence

## Flexible word order & fusion

only changes here that are really optional, e.g. preposition+article that can also be spelled out. Or reordering that are synchronically flexible

# Reducing YAST

## YAST to constituent structure

## YAST to dependency structure

## YAST to basic school grammar

## YAST to advanced school grammar

# Currently excluded

- dislocated structures, e.g. "Aussenfeld"
- comparative *wie/als* constructions
- 'Mittelfeld' ordering variations based on size
- secondary predication (dislocation of attributes)
- Details of Negation scope

- Quantoren are strange, e.g.: 'alle meine Bücher', 'jedes meiner Bücher', 'Die Bücher habe ich alle/beide gelesen', 'alle die Bücher in der Schublade'



NOTE: the following is a combination of two adverbials
"vorne/hinten im Garten"
they have to be inserted separately
semantics are inferred from regular scoping of multiple modifiers
also for 'noch nicht' ???

TODO: what about 'nur heute' ? cf. Fokuspartikel!?

# An (almost) one-rule syntax for German

To be clear up-front: no, of course it is not possible to write a complete syntax for the German language with just a single rule. However, I will argue that it is (almost) possible to condense the basic recursive syntax of German into such a single rule, which basically amounts to the instruction ~~insert lexeme here~~. Clearly, this one rule alone is not sufficient to capture all the details of actual German sentences. In practice, dozends of additional rules are necessary to completely specify a sentence structure. However, these specifying rules are simple non-recursive instructions like 'make this lexeme plural' or 'put this lexeme in the past tense'. Also, while I think that this condensation into a single recursive rule is theoretically neat, in practice I prefer a slightly more verbose notation using six rules: ~~clause + predication~~, ~~phrase + reference~~, ~~addendum~~ and ~~coordination~~.

about the 'almost': lexemes have to be explicitly told to be either reference or predicate. So actually there are two rules 'insert lexeme as predicate' and 'insert lexeme as reference'. In practice: this is mostly done by marking the lexeme itself as 'verb' (non-capitalized) or 'noun' (capitalized). For some constructions an additional specification 'finite/infinite' is necessary to get the right syntactic structure. So this might be considered as an additional 'syntactic' rule

Crucially, these proposals are not purely theoretical. The necessary rules for the German language are implemented in a surprisingly small amount of just a few hundred lines of code. They can be applied to produce actual sentences of German, simultaneously constructing a detailed underlying syntactic structure. However, there are two important caveats. First, the current implementation captures very many actual German sentence structures, but it is clearly not complete. However, the claim I would like to stake here is that everything missing can be accomplished with a few additional specifying rules. The basic recursive architecture is claimed to be complete. The second caveat is that the current implementation can (still) result in sentences that are ungrammatical. However, there is a transparent framework in place to formulate restrictions on rule application. Many such restrictions are already implemented, but many more are needed to bar the generation of ungrammatical sentences. In most cases, though, the formulation of such restrictions needs much more research than I have been able to perform until now.
