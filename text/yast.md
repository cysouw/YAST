## Preface {.unnumbered}

The motivation to develop yet another syntactic model for an already well-described language like German grew out of a large research project on German diathesis (Cysouw 2023). That book claims to provide a complete list of all monoclausal syntactic derivations for German. This list is long (currently more than 300 clause derivations, and counting), but clearly finite. Now, the impetus for the current syntactic model was the simple idea to investigate what remains to be done for the syntax once all these monoclausal derivations are put aside. In other words, how does a syntactic model look like when monoclausal derivations are reduced to just checkboxes to be ticked, alike to treating other finite morphosyntactic categories like tense or number. The current proposal is the result of following that premise through. In essence, the current approach is an experiment build on a single fundamental question, namely what a syntax would look like when monoclausal derivation (called 'stacking' in Cysouw 2023) is strictly separated from biclausal subordination.

Syntactic models need an acronym, so here I present to you YAST. This name started out in jest for 'Yet Another Syntax Theory', but I got enamoured by the name, so it stuck. There is a slightly deeper meaning to this name, however. The acronym YAST is an obvious nod to YAML, which started out as meaning 'Yet Another Markup Language'. But then, as YAML was developed further, it turned out to be much more powerful than anticipated, which lead to a recursive 'backronym' meaning 'YAML Ain't Markup Language'. In the same vein as YAML, the YAST approach turned out to be much more powerful than I had anticipated, so I now interpret the acronym YAST as a backronym meaning 'YAST Ain't (just) Syntax Theory'. But what's in a name? In the end it's just a sequence of letters to identify the approach to morphosyntactic analysis as outlined in this book.

The result is remarkable: with the hundreds of clause derivations out of the way, a reasonably fragment of a syntax for German can be formulated with just very few rules. I have implemented these rules in Python using XML-tree structures, and this part of the syntax takes just a few hundred lines of code. It can produce complete sentences with ordering, case marking, agreement and syntactic control for a wide range of complex syntactic structures. The remaining hundreds of clausal derivations (as described in Cysouw 2023) also can be easily implemented in just a dozen or so lines of code each. Currently only a small exemplary subset of those has been implemented. There is also a basic parser, which is not very good yet, but there is amply room for improvement.

The syntactic rules presented here describe (standard) German. However, the general architecture of YAST seems transferable to other languages. The analysis of sentence structures in YAST is fully compatible with typological insights about the worldwide linguistic diversity as, for example, summarised in Croft (2022). I have tried to adapt my terminology to Croft's to make the parallels even more obvious. Still, linguistic diversity is vast, and I do not dare to predict how much work is necessary to adapt the current framework to other languages.

# The YAST approach

## Basic principles

In its most basic sense, YAST is a generative model for sentence structures. It starts from a set of ~~instructions~~ that, when fed into the morphosyntactic ~~rules~~, result in an utterance, i.e. a sequence of pronounceable linguistic elements.

Pronunciation can often already start long before the instructions for even a single sentence are finished. So, YAST might also be a useful model for syntax processing, though note that the current model is based purely on syntactic analysis, without any actual research into real psychological processing. To produce utterances there is only minimal memory required, in that just very few parts of the instructions cannot be immediately uttered, but have to be retained for later. Most instructions simply lead to linguistic elements that can be uttered immediately.

The results of the instructions can be recorded, and this ~~receipt~~ looks like a familiar syntactic tree. Crucially, such syntactic trees are not necessary for the production of the utterance. The tree is just the combined effect of all instructions. So, the tree is really a receipt and not a recipe. 

The ephemeral role of the syntactic tree is also reflected in the workings of the ~~parser~~. The parser does not attempt to reconstruction the tree, but immediately (after observing each pronounced element) tries to reconstruct the underlying instructions. In the current implementation simply many different instructions are attempted within the range of possibilities as constrained by the utterance. Each attempt is fed into the rules until the actually observed utterance is replicated. In a sense, this parser is like an unexperienced learner of the language that knows the rules, but does not know any shortcuts to quickly arrive at the right interpretation.  The YAST-parser is thus actually a predictor that constantly tries to reconstruct the instructions (as intended by the generator) by performing generation in parallel and checking the results with the observed utterance.

![Basic workflow of YAST](figures/basis){#fig:basis}

## Instructions

Instructions consist of three different kinds of information, namely ~~linkage~~, ~~content~~ and ~~specification~~. All information in an instruction is of a functional/semantic nature. The formal linguistic structure is not something that should be of concern in the planning of the instructions. The syntactic structure is added to an utterance by the (automatic) rules. 

::: ex
Parts of an instruction in YAST

- ~~linkage~~: relation to earlier content (can be empty)
- ~~content~~: a single base lexeme
- ~~specification~~: language-specific grammatical marking (can be empty)
:::

As an example, consider the German sentence in [@next] as an appetizer. This German sentence is generated by the instructions in [@nnext] using the grammatical rules as will be laid out in the rest of this book. The instructions in [@nnext] can be seen as the intention of the speaker, with indentation marking modification. These instructions seem suitable for a semantic analysis, though this will not be pursued here. Note that the instructions are intentionally formulated with language-specific categories, so the semantic interpretation will have to be language-specific as well.

::: ex
- Die Männer, deren kleinen Kinder schlecht schlafen, habe ich gestern in deinem schönen Garten gesehen.
:::

::: {.ex noFormat=true}
```
sehen (Perfekt)
  Gesehene: Mann (Plural + Definit)
    schlafen
      Schlafende: Kind (Plural + Besitzer: Mann)
        klein
      schlecht
  Sehende: 1
  gestern
  in: Garten (Definit + Besitzer: 2)
    schön
```
:::

Each line in [@last] is a single instruction, possibly consisting of up to three different kinds of elements. Anything before any colon is the explicit ~~linkage~~, typically a lexical role, an adposition or a subjunction. When there is no colon than the linkage is of a default nature. 

After the linkage (or first in line when there is no explicit linkage) follows the main ~~content~~. This is typically a German lexeme, though there are a few codes used, like '1' for the speaker. The actual lexemes are included in the instructions because the language-specific lexemes are the best summary of their meaning.

Following the lexeme are explicit grammatical ~~specifications~~ between brackets. When there are no grammatical specifications the rules will infer a default ('unmarked') intention. Multiple grammatical specifications are separated with a plus-sign.

The ~~order of instructions~~ is to a large extend "free". The speaker is allowed to specify the intructions in any order (within certain limits to be worked out later in detail). As an result, the rules will sometimes have to work around the instructions to make this order work in accordance to the structure of the language. A proficient speaker with much experience will take the expected output into account in building the instructions.

## Syntactic model

The basic building blocks of human language are ~~lexemes~~. Lexemes induce a state-of-mind at the addressee, consisting of possible situations in accordance to the communally developed practice of using the lexeme (i.e. the lexeme's 'meaning'). The act of uttering a lexeme aims to conjure up some of those possible situations in the mind of the addressee.

Language extends the usefulness of these building blocks by combining multiple lexemes into utterances. The basic meaning of a combination of lexemes is the intersection of the two sets of possible situations. If the addressee is not able to find any intersection, the utterance of a lexeme combination forces the addressee to further search for possible situations that meet the desired combination.

However, a central tenet of human language is that combinations of linguistic elements is typicaly asymmetrical. Lexemes are not simply combined as equals, but there is always a ~~base~~ lexeme that is modified by another linguistic element.^[Explicitly symmetrical connections like coordination seem to be a much more recent add-on.] Such modifiers can become grammaticalised to a point at which they cannot be used themselves as a base anymore and become pure ~~operators~~. Base lexemes can be further differentiated in admodifiers and predicates.^[By using functional terms like 'base' and 'modifier' I explicitly refrain from using more structurally-oriented terms like 'head' and 'dependent', respectively, although those terms can largely be taken as synonymous. However, the discussion about the 'right' definition of the notion 'head' has become too contentious for it to be suitable in my opinion.]

I propose the following definitions for these three different kinds of syntactic elements: ~~operators~~, ~~admodifiers~~ and ~~predicates~~. Note that the statements below are definitions that might not always coincide with what one might otherwise conceive of as an operator, admodifier or predicate. However, the effect of these definitions seem close enough to most applications of these terms that it seemed worthwhile to retain these terms, notwithstanding possible confusion. To disambiguate the following definitions from other approaches using these terms one might think of them as 'YAST-operator', etc., but such clarification will here simply be omitted.

::: ex
Syntactic elements in YAST

- ~~operator~~: a modifier that itself cannot be modified.
- ~~admodifier~~: a base that can only be modified by operators.
- ~~predicate~~: a base that can be modified by operators, admodifiers and predicates.
:::

Prototypical operators are bound morphemes, but there are many other linguistic elements that are operators under the current definition (viz. they cannot themselves be modified), e.g. intensifiers, quantifiers, adpositions, subjunctions, etc. Prototypical admodifiers are adjectives and adverbs that allow for only limited modification like gradation and intensification. The syntactic function of a predicate is defined here in a very general sense. Predicates typically are verbs, but it also includes nouns as predicator of a referential entity. By definition, predicates can be modified by other predicates, so this is the moment where recursion becomes necessary.

## Hierarchical structure

The hallmark of human language is the possibility to productively combine many different linguistic elements into large utterances. One important aspect of morphosyntactic structure is that linguistic elements can in turn consist of multiple linguistic elements, leading to a hierarchical internal structure of the utterance. This hierarchical structure is commonly modelled by using the mechanisam of recursion. However, not all hierarchical structures are equally in need of a recursive treatment.

Coinciding with the three kinds of syntactic elements introduced in [@last], I propose to break down the hierarchical structure of human utterances into three different levels, which I will refer to as ~~stacking~~, ~~redoubling~~ and ~~embedding~~. These three levels of hierarchical structure are conceptually build on top of each other, i.e. redoubling is a special case of stacking, and embedding is a special case of iteration. In practice, I will use the term 'stacking' only when there is no redoubling nor embedding, and 'redoubling' is likewise only used for constructions that are not embedding. Crucially, only embedding will be modelled with recursion. Stacking and redoubling are much simpler and do not need recursion because they can easily be modelled by iteration.

::: ex
Hierarchical structures in YAST

- ~~stacking~~ is the modification of a base by operators.
- ~~redoubling~~ is the modification of a base by admodifiers.
- ~~embedding~~ is the modification of a base by predicates.
:::

These three levels suggest an evolutionary development in that human language first developed stacking, then redoubling and then embedding. However, that is purely speculation as all human languages currenty appear to employ all three kinds of hierarchical structure. Also note that contemporary language change does not follow the path from stacking to redoubling to embedding. In contrast, grammaticalisation typically develops in the reverse direction.

## Expressing the syntactic model

The syntactic model is turned into YAST-instructions as follows. Each base is a content lexeme that makes up a single instruction (i.e. a single line in the YAST-format as in the earlier example, repeated below). Redoubling and embedding are specified by indenting of the instructions. The difference between redoubling and embedding is not explicitly specified. However, embedding typically can have further modifications and their relation to the superordinate base can be specified with a linkage (before the colon). Syntactically, each linkage is an operator. All other operators are added in brackets after the base lexeme.

::: {.ex noFormat=true}
```
sehen (Perfekt)
  Gesehene: Mann (Plural + Definit)
    schlafen
      Schlafende: Kind (Plural + Besitzer: Mann)
        klein
      schlecht
  Sehende: 1
  gestern
  in: Garten (Definit + Besitzer: 2)
    schön
```
:::

- **level 0: morpheme combination**
  - a ~~morpheme~~ is a unanalyzable linguistic symbol, i.e a conventional and mostly arbitrary form-meaning pairing that cannot be meaningfully further subdivided.
  - two lexemes can be combined using simple set-intersection semantics
  - linear ordering of lexemes is not consistently used
  - combinations of more than two lexemes are difficult to interpret, but not impossible
  - this level of structure seems to be attested in other lifeforms as well
- **level 1: base-operator stacking**
  - lexemes are used in two different functions, i.e. there is an asymmetry between a ~~base~~-lexeme and an ~~operator~~-lexeme
  - in set-semantic terms, an operator restricts the reference of its base
  - multiple operators can hierarchically be added to a base
  - operators themselves cannot be further modified
  - ~~linear ordering~~ between base and operator is typically employed to indicate the asymmetry between base and operator
  - ordering base-operator seems more 'natural', typically leading to postposed operators
- **level 2: head-dependent iteration**
  - a base-lexeme is called a ~~head~~ when its operators can themselves have operators
  - an operator-lexeme is called a ~~dependent~~ when it can have operators for itself
  - dependents can have operators, but they cannot have dependents, i.e. there is only one level of embedding
  - multiple dependents per head are possible, but without further internal structure these are just lists of dependents added to a single head.
  - ~~bound morphology~~ is typically used to make operator scope explicit
- **level 3: subordination**
  - dependents can themselves have dependents, i.e. full recursion as a dependent can be a head
  - explicit relations to mark heads-as-dependents
  - complex internal ordering structure of constituents
  - specialisation of lexemes



Because of the spoken mode, language is necessarily ~~ordered~~. All utterances progress in time, necessitating the ordering of elements in a linear fashion. So, when combining two lexemes a decision has to be taken in which order to utter them. 

A typical correlate to a head-dependency asymmetry is to fix the ordering, in essence marking the asymmetry by the ordering.

Dependency:
- Unmarked
- Relation

Constituency:
- Binary
- Multiple

Hierarchical structure:
- Iteration (“tail-recursion”)
- Recursion

Order:
- External (before, after)
- Internal (first, second, pre-head, post-head, end)

Lexeme classes

Note the difference between "operated on" and "modified by". Modifier become operator through grammaticalisation, e.g. compounds leading to derivational morphology or auxiliaries becoming inflection.

Relationship-grammaticalisation: 
- junktor > relator > operator > contributor
- lexical relation > abstract relation > head specification > automatic rule ('double marking', probably rare)

## Syntactic rules

The basic syntactic principles are the following.

- YAST makes a strict separation between monoclausal ~~stacking~~ and multiclausal ~~subordination~~.
- A sentence is constructed by a hierarchical sequence of ~~instructions~~ that closely mimic descriptive approaches to linguistic structure. 
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

# An (almost) one-rule syntax for German

To be clear up-front: no, of course it is not possible to write a complete syntax for the German language with just a single rule. However, I will argue that it is (almost) possible to condense the basic recursive syntax of German into such a single rule, which basically amounts to the instruction ~~insert lexeme here~~. Clearly, this one rule alone is not sufficient to capture all the details of actual German sentences. In practice, dozends of additional rules are necessary to completely specify a sentence structure. However, these specifying rules are simple non-recursive instructions like 'make this lexeme plural' or 'put this lexeme in the past tense'. Also, while I think that this condensation into a single recursive rule is theoretically neat, in practice I prefer a slightly more verbose notation using six rules: ~~clause + predication~~, ~~phrase + reference~~, ~~addendum~~ and ~~coordination~~.

about the 'almost': lexemes have to be explicitly told to be either reference or predicate. So actually there are two rules 'insert lexeme as predicate' and 'insert lexeme as reference'. In practice: this is mostly done by marking the lexeme itself as 'verb' (non-capitalized) or 'noun' (capitalized). For some constructions an additional specification 'finite/infinite' is necessary to get the right syntactic structure. So this might be considered as an additional 'syntactic' rule

Crucially, these proposals are not purely theoretical. The necessary rules for the German language are implemented in a surprisingly small amount of just a few hundred lines of code. They can be applied to produce actual sentences of German, simultaneously constructing a detailed underlying syntactic structure. However, there are two important caveats. First, the current implementation captures very many actual German sentence structures, but it is clearly not complete. However, the claim I would like to stake here is that everything missing can be accomplished with a few additional specifying rules. The basic recursive architecture is claimed to be complete. The second caveat is that the current implementation can (still) result in sentences that are ungrammatical. However, there is a transparent framework in place to formulate restrictions on rule application. Many such restrictions are already implemented, but many more are needed to bar the generation of ungrammatical sentences. In most cases, though, the formulation of such restrictions needs much more research than I have been able to perform until now.
