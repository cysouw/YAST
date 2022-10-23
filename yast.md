# The YAST approach

## Why YAST

Do we really need Yet Another Syntax Theory™ (YAST)? Time will have to tell. In essence, YAST is an experiment build on a single fundamental question, namely what a syntax theory would look like when monoclausal derivation ('stacking') is strictly separated from biclausal subordination.

The motivation to propose such a syntax theory for an already well-described language like German grew out of a large research project on German diathesis (Cysouw 2022). That book proposes a long list of all monoclausal syntactic derivations for German. That list is long (currently more than 300 clause derivations, and counting), but clearly finite. Now, the impetus for YAST was the simple idea to investigate what remains to be done for a syntactic theory once all these clause derivations are put aside. In other words, how does a syntactic theory look like when monoclausal derivations are reduced to just check boxes to be ticked, alike to treating other finite categories like tense or number somewhere in the syntax tree. YAST is the result of following that premise through.

The result is remarkable: with the hundreds of clause derivations out of the way, a reasonably complete syntax for German can be formulated with just about 20 rules. I have implemented these rules in Python using XML-tree structures, and this part of the syntax takes just a few hundred lines of code. It can produce complete sentences with correct ordering, case marking, agreement and syntactic control for a wide range of highly complex syntactic structures. The remaining hundreds of clausal derivations (as described in Cysouw 2022) also can be easily implemented in just a dozen or so lines of code each. Currently only a small exemplary subset of those has been implemented.

The syntactic rules presented here describe (standard) German. However, the general architecture of YAST seems transferable to other languages. The basic principles are the following.

- YAST makes a strict separation between monoclausal ~~stacking~~ and multiclausal ~~subordination~~.
- A sentence is constructed by a hierarchical sequence of ~~operations~~ that closely mimic descriptive approaches. Many such operations include variables to specify lexical elements to be inserted.
-  The operations and their variables are supposed to be the minimal information needed to produce a sentence. All other syntactic details follow automatically from this information.
- A YAST operation typically adds linguistic material to the sentence, i.e. ~~generation~~, but it can also change already available material, i.e. ~~transformation~~. Aspects of generation and transformation are thus intermixed in YAST.
- The nodes in the resulting hierarchical sentence structure record the operations applied, so the final YAST tree can be read as an archive of the building process.
- The leaves of the tree are the actual linguistic forms making up the sentence, making the YAST tree very similar to a ~~constituency tree~~.
- However, a YAST tree can easily be reformatted with the leaves (i.e. 'words') as nodes and the path to a leaf (i.e. 'sequence of operations') as the verteces. The result of that reformatting is very similar to a ~~dependency tree~~ because sequences of operations can be interpreted as relations between words.

## Currently excluded

- dislocated structures, e.g. "Aussenfeld"
- long-range anaphors, including
- comparative *wie/als* constructions
- 'Mittelfeld' ordering variations

## Restrictions

The YAST system of rules is proposed as a tool to describe attested sentences. It is not (yet) a fully restrictive model to exclude all impossible sentences. I consider it a research project to fine-tune the rules, inching ever so closer to this ideal. The priniciple is that rules come with restrictions. There are different kinds of restrictions on possible syntactic trees:

- ~~rule restrictions~~: Some restrictions are inherent in the formulation of the rules, i.e. by choosing a particular rule opion there are all kind of structural consquences. This actually amounts to a analytic decision to treat certain decisions as crucial, implicating ofther effects. Note that there is nothing inherently demanding such analytic decisions. The current decisions to formulate rules are a hypothesis about the interaction between to-be-decided options and structural consequences from these options
- ~~lexical restrictions~~: Restrictions can be lexically determined, i.e. the choice for a particular lexeme forces certain structural consquences. Again, such lexical determination is open for debate.
- ~~rule interactions~~: Some rules can block or enhance the application of other rules. Note that such restrictions are supposed to be different from the ~~rule restrictions~~. Interactions are more probibalistic in nature.
- ~~lexical interaction~~: Such lexical choices do not go together with other lexical choices in the construction of a tree. This is the most 'vague' kind of restrictions, bordering on pragmatics. It relates to the 'grammatical but nonsensical' restrictions like 'green ideas sleep furiously'.

## YAST in a nutshell

A YAST-analysis of a sentence will form a syntactic tree, just like most modern syntax theories. However, different from most other proposals, the nodes of the tree will be ~~operations~~ and the leaves will be ~~linguistic form~~. 

There are basically two different kinds of operations, namely ~~additions~~ and ~~changes~~. A tree with just additions would be completely comparable to any generative approach to syntactic trees. The role of changes is alike to the idea to allow transformations in the analysis of a sentence. In the YAST-tree additions ('generation') and changes ('transformations') are intermixed. They do not occur sequentially (i.e. first generation, then transformation), as in most transformational-generative aproaches. In contrast, the YAST-tree can have some generative steps, followed by transformational steps, returning to generative steps, and so on.

From a different perspective, the YAST-tree can also be interpreted as a dependency tree. To achieve this the operations (i.e. the nodes in the YAST-tree) can be reinterpreted as relations. In practice, the nodes of the YAST-tree will become the vertices of a dependency tree and the labels of the YAST-nodes will become the names of the dependency relations. At every bifurcation of the YAST-tree there is a natural head, which will be the main node to be connected. All other branches from that same YAST-bifurcation are then dependent on that main node.

Finally, the idea of looking at the analysis of a sentence as a sequence of operations is very close to the common practice of grammatical analysis as used in schools and in the descriptive tradition, using concepts like 'adding' some part to a sentence, 'expanding' a particular section, or 'changing' a specific form to produce a coherent sentence.

## Infinity and recursion

The number of all possible sentences that can theoretically be produced in a specific language is infinite. This insight led to the development of syntax theories that can model this infinity. Above all, the notion of recursion 

However, there are at least three different kinds of theoretical infinity in human languages that need to be distinguished, and only one of them needs recursion to be modelled.

First, some word classes are theoretically infinite, resulting in infinite different ways to form sentences. In practice, every language at a certain point in time has a finite vocabulary, so this infinity is easy to handle. This led to a widespread practice to differentiate between the ~~lexicon~~ (possible infinite) and the ~~grammar~~ (a finite set of specifications). Note that there are also some very large semi-transparent word classes like numerals.

Second, some phenomena in language are theoretically infinite by linear connection. For example adjectives before nouns can be (theoretically) iterated infinitely. However, such infinite lists do not need recursion to be modelled. They can be modelled with recursion, but YAST proposes not to. Such infinity is typically attested with different kinds of modification and conjunction.

Third, infinity needing real recursion can be reduced to only two different kinds, namely clausal and phrasal recursion.

Futher, there are various elements in the structure of German that are finite templatic in nature. This means that there are options to include additional elements, but there is a finite set of 'positions' to be filled. Such templates are always modelled as such, i.e. as finite templates with a fixed number of clearly delimited slots. For example, adjectives can be graded (e.g. *sehr klein*) or determiners can have quantification (e.g. *die drei*, *alle drei*, sometimes even *alle die drei*) but only in a clearly finite number of possible combinations.

## Elements of YAST

The two main recursive elements of a YAST-analysis are ~~predication~~ and ~~reference~~. Predication leads to a syntactic structure that will be called a ~~clause~~ (*Teilsatz*) and reference leads to a ~~noun phrase~~ (*Nominalphrase*). However, because there will be no other recursive elements, these two will simply be called ~~clause~~ (*Satz*) and ~~phrase~~ (*Phrase*).

Recursive operations in YAST:

- ~~predication~~ (*Prädikation*), resulting in a syntactic clause (*Satz*). This operation introduces a ~~predicate~~ (*Prädikat/Verb*) and one or more ~~lexical roles~~ (*Rollen*). In German, the predicate will in the end always by some kind of verbal element, either a full lexical verb or an auxiliary.
- ~~reference~~ (*Referenz*), resulting in a syntactic phrase (*Phrase*). This operation introduces a ~~referent~~ (*Referent/Substantiv*) and typically a ~~determiner~~ (*Determinativ*). In German, the referent will in the end always be some kind of nominal element, either a noun or a nominalised element. Alternatively, some kind of pronominalisation (*Pronomen*) can be used for reference.

All other elements in the YAST-tree, besides clauses and phrases, will be either finite strings or linear lists of elements. So there is no hierachical recursion necessary to model these other elements.

Non-recursive operations in YAST:

- ~~modification~~ (*Modifikation*), either modification of a predication, resulting in an ~~adverbial~~ element (*Adverbiale*), or modification of an identifications, resulting in an ~~attributive~~ element (*Attribut*).
- ~~coordination~~ (*Koordination*), resulting in two (or more) identical elements introduced side-by-side in a tree, possibly linked by a special juncture (*Konjunktion*). This is possible at almost all nodes in the German YAST-tree.

Multiple modifications typically have scope over each other. Coordinants typically have a sequential interpretation.

Recursion happens in the following combinations:

- a phrase as a lexical role: argument (*Komplementphrase*)
- a clause as a lexical role: complement clause (*Komplementsatz*)
- a phrase as an adverbial modifier: adjunkt (*Adverbialphrase*)
- a clause as an adverbial modifier: adverbial clause (*Adverbialsatz*)
- a phrase as an attributive modifier: attribute (*Attributphrase*)
- a clause as an attributive modifier: relative clause (*Attributsatz* ~ *Relativsatz*)

String insertion in YAST:

- ~~junction~~  (*Junktion*) sometimes an explicit juncture (*Junktor*) is inserted at recursion, describing the relation between the subordinate and the embedded element. Although there is some overlap, I will use the name preposition (*Präposition*) for junctures used with an embedded phrase and subordinator (*Subjunktion*) for junctures used with an embedded clause.
- ~~expression~~ (*Ausdruck*) the lexical elements inserted at the leaves of the tree, sometimes in the form of templatic constructs that allow for various different kinds of words.
  

Conjunction is strictly syntactically defined!

# Rules for predication

## Clause (*Satz*)

## Predication setup (*Prädikation*)

Basically a verb with lexical arguments. A PHRASE leads to *Prädikatives Substantiv*
Lexical arguments can be filled with either PHRASE or SATZ (*Komplementsatz*)

- verbal predication
- nominal predication (SUBJ + role 'noun predicate' + auxiliary)
- adjectival predication (SUBJ + attribute 'adjectival predicate' + auxiliary)
- possession (possessor(SUBJ) + possessee + auxiliary)
- comparison (comparee(SUBJ) + 'comparison adjectival predicate' + auxiliary + role 'standard of comparison': both SATZ and PHRASE possible, additional Junktion *als, wie*)

## Predication derivation (*Ableitung*)

Epitheses and diatheses

## Predication modification (*Adverbial*)

Either a PHRASE or SATZ (*Adverbialsatz*)
also: adverbs, negation, particles, adjectives+gradation

## Predication format (*Satzart*)

*Hauptsatz*, *nicht-finite Nebensätze*, *Nominalisation*, usw.
also: add characteristic *Finit* to the verb

d/w-Sentences: important first position in embedded clauses, alike to Vorfeld (e.g. questionwords) and Determinative (e.g. relative pronouns).

# Rules for reference

## Phrase (*Phrase*)

## Reference setup (*Referenz*)

Determination (quantification+article+numeral) and phrasal head
If SATZ then *Nominalisation*

## Reference modification (*Attribut*)

either PHRASE (*Präpositionalphrase*) or SATZ (*Relativsatz*)
also: adjectives+gradation

# Finishing up

## Lexical insertion

## Government and agreement

mostly inside phrase, except

- verbagreement between subject and finite verb
- reflexive pronoun agreement
- anaphoric reference inside sentence ('checking')

## Flexible word order & fusion

only changes here that are really optional, e.g. preposition+article that can also be spelled out. Or reordering that are synchronically flexible

# Reducing YAST

## YAST to constituent structure

## YAST to dependency structure

## YAST to basic school grammar

## YAST to advanced school grammar

