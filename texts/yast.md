# The YAST approach

## Why YAST

Do we really need yet another syntax theory? Time will have to tell. In essence, the current approach is an experiment build on a single fundamental question, namely what a syntax would look like when monoclausal derivation ('stacking') is strictly separated from biclausal subordination.

The motivation to develop this approach for an already well-described language like German grew out of a large research project on German diathesis (Cysouw 2022). That book claims to present a complete list of all monoclausal syntactic derivations for German. That list is long (currently more than 300 clause derivations, and counting), but clearly finite. Now, the impetus for a new syntactic approach was the simple idea to investigate what remains to be done for the syntax once all these monoclausal derivations are put aside. In other words, how does a syntactic theory look like when monoclausal derivations are reduced to just checkboxes to be ticked, alike to treating other finite morphosyntactic categories like tense or number. The current proposald is the result of following that premise through.

Syntactic theories need an acronym, so here I present to you YAST. This name started out in jest for 'Yet Another Syntax Theory', but I got enamoured by the name, so it stuck. There is a slightly deeper meaning to this name, however. The acronym YAST is an obvious nod to YAML, which started out as meaning 'Yet Another Markup Language'. But then, as YAML was developed further, it turned out to be much more powerful than anticipated, which lead to a recursive redefinition as meaning 'YAML Ain't Markup Language'. Such recursive 'backronyms' have a history in the computing community, a well-known example being GNU meaning 'GNU's Not Unix'. In the same vein as YAML, the YAST approach turned out to be much more powerful than I had anticipated, so I now interpret the acronym YAST now as a backronym meaning 'YAST Ain't Syntax Theory'. But what's in a name? In the end it's just a sequence of letters to refer to the approach to morphosyntactic analysis as outlined in this book.

The result is remarkable: with the hundreds of clause derivations out of the way, a reasonably complete syntax for German can be formulated with just about 20 rules. I have implemented these rules in Python using XML-tree structures, and this part of the syntax takes just a few hundred lines of code. It can produce complete sentences with correct ordering, case marking, agreement and syntactic control for a wide range of highly complex syntactic structures. The remaining hundreds of clausal derivations (as described in Cysouw 2022) also can be easily implemented in just a dozen or so lines of code each. Currently only a small exemplary subset of those has been implemented.

The syntactic rules presented here describe (standard) German. However, the general architecture of YAST seems transferable to other languages. The basic syntactic principles are the following.

- YAST makes a strict separation between monoclausal ~~stacking~~ and multiclausal ~~subordination~~.
- A sentence is constructed by a hierarchical sequence of ~~operations~~ that closely mimic descriptive approaches to linguistic structure. Many such operations have a variable to specify lexical elements to be inserted. As far as this distinction can be made, operations codify structural aspects of a sentence and the variables encode the lexical information.
- The operations and their lexical variables are supposed to be the minimal information needed to produce a sentence. All other syntactic details follow automatically from this information, with the help of a static dictionary.
- A YAST operation typically adds linguistic material to the sentence, i.e. ~~generation~~, but it can also change already available material, i.e. ~~transformation~~. Aspects of generation and transformation are thus intermixed in YAST.
- The nodes in the resulting hierarchical sentence structure record the operations applied, so the final YAST tree can be read as an archive of the building process.
- The leaves of the tree are the actual linguistic forms making up the sentence, making the YAST tree very similar to a ~~constituency tree~~.
- However, a YAST tree can easily be reformatted with the leaves (i.e. 'words') as nodes and the path to a leaf (i.e. 'sequence of operations') as the verteces. The result of that reformatting is very similar to a ~~dependency tree~~ because sequences of operations can be interpreted as relations between words.

## Restrictions

The YAST system of rules is proposed as a tool to describe attested sentences. It is not (yet) a fully restrictive model to exclude all impossible sentences. I consider it a research project to fine-tune the rules and their restrictions, inching ever so closer to this ideal. There are three different kinds of restrictions on possible syntactic trees:

- ~~rule restrictions~~: Some restrictions are inherent in the formulation of the rules, i.e. by choosing a particular rule there are some structural consquences. The number of such restrictions is conspicuously limited in YAST. Basically, there are event-structure rules that only can be applied to a predication and there are identification rules that can only be applied to a reference. Most other restrictions turn out to be lexically determined, as discussed below.
- ~~lexeme-insertion restrictions~~: Rules that insert lexical material are restricted by which lexical stems can be inserted. This basically amounts to a classification of lexical stems into word classes along familiar lines. However, note that a fair amount of lexical stems are amenably for insertion into different rules, e.g. the stem *tanz* can both be inserted in the ~~verb~~ rule and in the ~~nomen~~ rule. I do not consider this to be some kind of conversion or zero derivation. It is simply the same stem that can be used in different rules.
- ~~lexical restrictions~~: The most difficult, but also most interesting, kind of restrictions are lexical restrictions, i.e. the choice to insert a specific lexeme into the tree leads to restrictions later on in the syntactic tree. Such restrictions have to be documented in the extended lexicon, i.e. it has to be explicitly listed what are the consequences of each lexical entry.
- ~~semantic interpretation~~: Finally, there are sentences that might seem syntactically fine, but are semantically strange or nonsensical, like the infamous 'green ideas sleep furiously'. Such sentences are not necessarily wrong, they might just need some more (poetic) freedom to be amenable.

## YAST in a nutshell

A YAST-analysis of a sentence will form a syntactic tree, just like most modern syntax theories. However, different from most other proposals, the nodes of the tree will be ~~operations~~ and the leaves will be ~~linguistic forms~~. 

There are basically two different kinds of operations, namely ~~additions~~ and ~~changes~~. A tree with just additions would be completely comparable to any generative approach to syntactic trees. The role of changes is alike to the idea to allow transformations in the analysis of a sentence. In the YAST-tree additions ('generation') and changes ('transformations') are intermixed. They do not occur sequentially (i.e. first generation, then transformation), as in most classical transformational-generative aproaches. In contrast, the YAST-tree can have some generative steps, followed by transformational steps, returning to generative steps, and so on.

From a different perspective, the YAST-tree can also be interpreted as a dependency tree. To achieve this, the operations (i.e. the nodes in the YAST-tree) can be reinterpreted as relations. In practice, the nodes of the YAST-tree will become the vertices of a dependency tree and the labels of the YAST-nodes will become the names of the dependency relations. At every bifurcation of the YAST-tree there is a natural head, which will be the main node to be connected. All other branches from that same YAST-bifurcation are then dependent on that main node.

Finally, the idea of looking at the analysis of a sentence as a sequence of operations is very close to the common practice of grammatical analysis as used in schools and in the descriptive tradition, using concepts like 'adding' some part to a sentence, 'expanding' a particular section, or 'changing' a specific form to produce a coherent sentence.

## Infinity and recursion

The number of all possible sentences that can theoretically be produced in a specific language is infinite. This insight led to the development of syntax theories that can model this infinity. Above all, the notion of recursion received high prominence to explain the infinite possibilties of human languages. However, there are at least three different kinds of theoretical infinity in human languages that need to be distinguished, and only one of them needs recursion to be modelled.

First, some word classes are theoretically infinite, resulting in infinite different ways to form sentences. In practice, every language at a certain point in time of course has just a finite vocabulary, so this infinity is easy to handle. This kind of infinitiy led to a widespread practice to differentiate between the ~~lexicon~~ (possibly infinite) and the ~~grammar~~ (a finite set of specifications). Note that there are exist some very large semi-generative word classes like numerals.

Second, some phenomena in language are theoretically infinite by linear connection. For example, adjectives before nouns can be (theoretically) iterated infinitely. However, such infinite lists do not need recursion to be modelled. They could be modelled with recursion, but YAST proposes not to. Such infinity is typically attested with different kinds of modification and conjunction.

Third, infinity needing real recursion is reduced in YAST to only two different kinds of recursion, namely clausal (predication) and phrasal (reference) recursion.

Futher, there are various elements in the structure of German that are finite templatic in nature. This means that there are options to include additional elements, but there is a finite set of 'positions' to be filled. Such templates are always modelled as such, i.e. as finite templates with a fixed number of clearly delimited slots. For example, adjectives can be graded (e.g. *sehr klein*) or determiners can have quantification (e.g. *die drei*, *alle drei*, sometimes even *alle die drei*) but only in a clearly finite number of possible combinations.

## Elements of YAST

The two main recursive elements of a YAST-analysis are ~~predication~~ and ~~reference~~. Predication leads to a syntactic structure that will be called a ~~clause~~ (*Teilsatz*) and reference leads to a ~~noun phrase~~ (*Nominalphrase*). However, because there will be no other recursive elements, these two syntactic elements will simply be called ~~clause~~ (*Satz*) and ~~phrase~~ (*Phrase*).

Recursive operations in YAST:

- ~~predication~~ (*Prädikation*), resulting in a syntactic clause (*Satz*). This operation introduces a ~~predicate~~ (*Prädikat/Verb*) and one or more ~~lexical roles~~ (*Rollen*). In German, the predicate always includes some verbal element, either a full lexical verb or an auxiliary.
- ~~reference~~ (*Referenz*), resulting in a syntactic phrase (*Phrase*). This operation introduces a ~~referent~~ (*Referent/Nomen*) and typically a ~~determiner~~ (*Determinativ*). In German, the referent will in the end always be some kind of nominal element, either a noun or a nominalised element. Alternatively, some kind of pronominalisation (*Pronomen*) can be used for reference.

All other elements in the YAST-tree, besides clauses and phrases, will be either finite strings or linear lists of elements. So there is no hierachical recursion necessary to model these other elements.

Non-recursive operations in YAST:

- ~~modification~~ (*Modifikation*), either modification of a predication, resulting in an ~~adverbial~~ element (*Adverbiale*), or modification of an identifications, resulting in an ~~attributive~~ element (*Attribut*). Multiple modifications typically have scope over each other.
- ~~coordination~~ (*Koordination*), resulting in two (or more) identical elements introduced side-by-side in a tree, possibly linked by a special juncture (*Konjunktion*). This is possible at almost all nodes in the German YAST-tree. Coordinants typically have a sequential interpretation.

Recursion happens in the following combinations:

- a phrase as a lexical role: argument (*Argument*)
- a clause as a lexical role: complement clause (*Argumentsatz*)
- a phrase as an adverbial modifier: adjunkt (*Adverbiale*)
- a clause as an adverbial modifier: adverbial clause (*Adverbialsatz*)
- a phrase as an attributive modifier: attribute (*Attribut*)
- a clause as an attributive modifier: relative clause (*Attributsatz*)

Connecting tissue in YAST:

- ~~junction~~ (*Junktion*) sometimes an explicit juncture (*Junktor*) is inserted at recursion, describing the relation between the subordinate and the embedded element ('link downwards'). Although there is some overlap, I will use the name preposition (*Präposition*, also with *da-*) for junctures used with an embedded phrase and subordinator (*Subjunktion*) for junctures used with an embedded clause. also conjunctions (*Konjunktion*).
- ~~linkage~~ (*Verbindung*) is made with relators (*Relator*) inside clauses 'link upwards'. In German relative pronouns ('d'-*Relativpronomen*) and question words ('w'-*Fragewort*), with the default entries *dass* and *was*. Additionally the particle *ob* is used as relator. Relators always occur in the first position of a clause and there is a strong connection to the *Vorfeld* position in the German main clause (which can be interpreted as the linkage to the preceding context with a default entry *es*).

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