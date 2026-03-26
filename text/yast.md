## Preface {.unnumbered}

The motivation to develop yet another syntactic model for an already well-described language like German grew out of a large research project on German diathesis (Cysouw 2023). That book claims to provide a complete list of all monoclausal syntactic derivations for German like passives, causatives, etc. This list is long (currently more than 300 clause derivations, and counting), but clearly limited. The impetus for the current syntactic model was the simple idea to investigate what remains to be done for the syntax once all these monoclausal derivations are put aside. In other words, what does a syntactic model look like when monoclausal derivations are reduced to just checkboxes to be ticked, alike to the treatment of other morphosyntactic categories like tense or number in a syntactic theory. The current proposal is the result of following that premise through. In essence, the current approach is an experiment build on a single fundamental question, namely what a syntax would look like when monoclausal derivation (called "stacking" in Cysouw 2023) is strictly separated from clausal subordination.

Syntactic models need an acronym, so here I present to you YAST. This name started out in jest for 'Yet Another Syntax Theory', but I got enamored by the name, so it stuck. There is a slightly deeper meaning to this name, however. The acronym YAST is an obvious nod to YAML, and the astute observer will discern some superficial similarities in notation. The abbreviation YAML started out as meaning "Yet Another Markup Language". But then, as YAML was developed further, it turned out to be much more useful than originally anticipated, which led to the instroduction of a recursive backronym "YAML Ain't Markup Language". In the same vein, the YAST approach turned out to be much more useful than I had anticipated, so I now interpret the acronym YAST as a backronym meaning "YAST Ain't (just) Syntax Theory". But what's in a name? In the end it's just a sequence of letters to identify the approach to morphosyntactic analysis as outlined in this book.

The result is remarkable: with the hundreds of clause derivations from Cysouw (2023) out of the way, a reasonably fragment of a syntax for German can be formulated with just very few rules. I have implemented these rules in Python using XML-tree structures, and this part of the syntax takes just a few hundred lines of code. It can produce complete sentences with ordering, case marking, agreement and syntactic control for a wide range of complex syntactic structures. The remaining hundreds of clausal derivations (as listed in Cysouw 2023) also can be easily implemented in just a dozen or so lines of code each. Currently only a small exemplary subset of those has been implemented. There is also a basic parser, which is not very good yet, but there is ample room for improvement.

The syntactic rules presented here describe (standard) German. However, the general architecture of YAST seems transferable to other languages. The analysis of sentence structures in YAST is fully compatible with typological insights about the worldwide linguistic diversity as discussed in the work of Croft, Dixon and Haspelmath, which have strongly influenced my views on morphysyntax. I have tried to adapt my terminology to theirs to make the parallels even more obvious. Still, linguistic diversity is vast, and I currently do not dare to predict how much work is necessary to adapt the current framework to other languages.

The first chapter lays out the principles of YAST in rather abstract terms. This is not how YAST originated in my own personal thinking. I started out with some simple lines of code to produce German sentences and found various ways to generalize and simplify this algorithm. Once things worked quite well in practice I started formulating in more detail what kind of theoretical assumptions I was making. In so doing I followed the real scientific procedure as proposed by the Dutch cartoonists John Reid, Bastiaan Geleijnse and Jean-Marc von Tol: "very impressive, dear colleague ... but does it also work in theory?"

![The real scientific procedure: "Fokke & Sukke know how science works: very impressive, dear colleague ... but does it also work in theory?"  
(© Reid, Geleijnse & van Tol)](figures/fokkesukke.png){#fig:fokkesukke}

# Introducing YAST

## Key characteristics

Given the abundance of existing structural models for morphosyntax, I introduce YAST here by highlighting several key characteristics that distinguish it from most other generative models of grammatical structure.

**Language-specific model.** The majority of the rules and structures in YAST are language-specific. There are only very few principles proposed that hold for human language in general.

**Proximity to traditional grammar.** By being language-specific, the current approach remains relatively close to traditional notions of grammatical description (although in this first chapter that might not look like that at all). Differently from traditional grammars, YAST includes a generative implementation (which traditional grammars typically lack). However, the "ingredients" that drive generation closely resemble the rules and regularities described in traditional grammars. Traditional grammatical descriptions require only minor adjustments to allow for this kind of computational implementation. This approach also ensures that the formalized model remains easily comprehensible to non-technically minded linguists.

**Content-then-structure generation.** The generative process employs concrete morphemes from a specific language rather than abstract categories. This contrasts with the predominant approach of first generating an abstract structure and only later inserting lexical elements. In YAST, generation begins by selecting language-specific morphemes for insertion. Each such choice triggers structural repercussions that collectively establish the abstract morphosyntactic structure. Rather than "structure-then-content," YAST follows a "content-then-structure" generative process.

**Two-way generative distinction.** The current approach distinguishes two types of generative operations, namely (i) predominantly "free" lexical insertion with some grammatical restrictions resulting from the inserted lexemes, and (ii) completely automatic formal rules of language structure. This twofold distinction is useful for linguistic comparison and may benefit didactic approaches to language structure. The grammatical restrictions from (i) and the rules of (ii) typically appear in descriptive grammars, while the lexical inseration from (i) is better handled by probabilistic models like large language models.

**Dual structural representation.** Morpheme choice and their repercussions (i.e. generation type (i) from above) generate a dependency-like "underlying" structure. Subsequently, mandatory rules (i.e. generation type (ii) from above) then transform this morphosyntactic structure into a linear utterance through an intermediate constituency-like representation. In grammatical analysis—that is, when working backwards from actual utterances—the constituency structure thus represents a level of abstraction closer to the surface structure than the dependency structure. The dependency structure constitutes an underlyingly more abstract analytical representation of utterances.

**Rule-defined word classes.** Classes of morphemes ("parts of speech") in YAST only exist as secondary phenomena based on their morphosyntactic characteristics. Each grammatical structure defines its own class of applicable morphemes. This approach has two key effects, namely (a) languages exhibit numerous overlapping word classes, with most morphemes belonging simultaneously to multiple classes, and (b) no singular atomic classification exists to which each morpheme can be uniquely assigned, that is, no set of mutually exclusive classes can serve as the basis for grammatical rules. Rather than "word classes determine the application of rules," YAST asserts that "rules define word classes."

**Minimal universal assumptions.** Because most grammatical structures arise from language-specific choices, YAST assumes only a very limited set of universal morphosyntactic principles. Observations of recurrent grammatical properties ("statistical universals") are better modeled through semantic-map approaches that describe cross-linguistic differences and similarities as language-specific discrete divisions of an underlying continuous semantic space, which itself is probably universal.

[--
A generative potentially-probabilistic traditional-like templatic (GP^2^T^2^) model for human language
--]::

## Synopsis of the model

### Recipe-rule-result-receipt

In its most basic sense, YAST is a generative model for sentence structures. It starts from a set of ~~instructions~~ that, when fed into the morphosyntactic ~~rules~~, lead to an ~~result~~, i.e. a sequence of pronounceable linguistic elements. The instructions are language-specific, i.e. the instructions to make a German sentence consist of German elements. The basic guideline determining what should appear in the instructions is the notion of predictability: all parts of an actual utterance that can be predicted are added by the rules, only the non-predictable elements remain for the instructions. So, the research that is needed to write morphosyntactic YAST-rules for a specific language is to decide which parts of the utterance are predictable and which are non-predictable.

Pronunciation can often already start long before the instructions for even a single sentence are finished. So, YAST might also be a useful model for language processing, though note that the current model is based purely on syntactic analysis without any actual research into real psychological processing. Still, to produce utterances in YAST there is only minimal memory required, in that just very few parts of the instructions cannot be immediately uttered, but have to be retained for later. Most instructions simply lead to linguistic elements that can be uttered immediately.

The complete process that leads to the utterance (i.e. the results of the evaluated instructions) can be recorded, and this ~~receipt~~ looks like a constituent tree. Crucially, the creation of such constituent trees are not necessary for the production of the utterance. The constituent tree is just the combined effect of all instructions. So, the constituent tree is really a receipt and not a recipe. In short, the syntactic approach of YAST can be summarized as a ~~recipe-rules-result-receipt~~ model. The (dependency-like) instructions are the recipe. The recipe is fed into the the rules to produce a resulting utterance. Additionally, a (constituent-like) receipt is a summary of all the procedures leading to the result.

This multi-step approach to syntactic analysis probably feels eerily similar to the familiar "deep structure being transformed to surface structure" approach developed by Harris and Chomsky starting in the late 1950s, and there are surely parallels to be found. However, in actual practice there is not much similarity in the inner working of the algorithms. The difference is most obvious in the rules of YAST, which do not transform the recipe, but start from scratch building a syntactic structure on the basis of the recipe.

### The recipe

The recipe consists of a collection of one-line instructions that use indentation to indicate hierarchical modifications. Instructions consist of five different kinds of information, namely ~~modification~~, ~~type~~, ~~junction~~, ~~nucleus~~ and ~~specification~~. 

::: ex
Parts of an instruction in YAST

- **Modification** \
  When an instruction modifies an earlier instruction this is indicated by indentation.
- **Type** \
  There are three different types of instructions distinguished, which will be called ~~phrase~~, ~~clause~~ and ~~admodifier~~. The type of an instruction is mostly inferred by default.
- **Junction** \
  Junctions express the relation of the instruction to earlier content. Such explicit relational ingredients are called ~~junctors~~. This part of the instruction can be empty for default ("unmarked") modification.
- **Nucleus** \
  The obligatory nucleaus of each instructions is a single base content lexeme. For phrases and clauses the nucleus is called a ~~head~~.
- **Specification** \
  Depending on the type of instruction, language-specific grammatical marking can be added. Such ingredients are called ~~specifiers~~. This part of the instruction can be empty for default ("unmarked") morphosyntax. 
:::

The information in an instruction mostly consists of language-specific forms. The idea is that the details of the morphosyntactic form is not something that should be of concern in the planning of the instructions. The morphosyntactic structure of the eventual utterance is produced by the (automatic) rules. The most precise and straightforward method to specify meaning in a recipe is to use language-specific elements. So, in YAST, a user of a specific language is juggling with the available language-specific elements to construct an utterance, instead of manipulating abstract linguistic concepts.

As an example, consider the German sentence in [@next] as an appetizer. This German sentence is generated by the instructions in [@nnext] and using the grammatical rules as will be laid out in the rest of this book. The instructions in [@nnext] can be seen as the intention of the speaker, with indentation marking modification. These instructions seem suitable for a semantic analysis, though this side of the model will have to be worked out another time in more detail. Note that the specifications (in brackets) are intentionally formulated with language-specific morphosyntactic terminology, so their semantic interpretation will have to be language-specific as well. Any comprehensive cross-linguistic generalization over such language-specific elements is a separate–though highly important–endeavor, which will not be pursued here.

::: ex
Die Männer, deren kleinen Kinder schlecht schlafen, habe ich gestern in deinem schönen Garten gesehen.
:::

::: {.ex noFormat=true}
```
sehen (perfekt)
  Gesehene: Mann (plural + definit)
    schlafen
      Schlafende: Kind (plural)
        Behälter: Mann
        klein
      schlecht
  Sehende: 1
  gestern
  in: Garten (definit)
    Behälter: 2
    schön
```
:::

Each line in [@last] is a single instruction with hierarchical indentation, possibly consisting of up to three different kinds of elements. Anything before the colon is an explicit ~~junctor~~ that marks the relation to the superordinate instruction. This is either a lexical role, an adposition or a subjunction/conjunction. When there is no colon, then the junction is assumed to be default modification. After the linkage follows the main lexical ~~nucleus~~. This is typically a German lexeme, though there are a few abstract abbreviations used, like '1' for the speaker. The actual lexemes are included in the instructions because the language-specific lexemes are the best summary of their meaning. 

After the content lexeme follows a list with explicit grammatical ~~specifications~~ (between brackets). When there are no grammatical specifications the rules will infer a default ("unmarked") grammatical structure. Multiple grammatical specifications are separated with a plus-sign, and their order is relevant in some situations. Specifications are often grammatical terms like *plural* because of the highly allomorphic formation of the German plural. However, these specifications are always abbreviations for language-specific forms and do not describe universal grammatical categories.

The ~~type~~ of the instruction is not explicitly shown in the example of a recipe in [@last]. Technically speaking, each line should be marked as being a phrase, clause or admodifier. However, it turns out that for German the type of the large majority of instructions can be inferred from the nucleus. To simplify the recipe I decided to leave out the explicit indication of the type and resort to default inference. Only in very special circumstances an explicit override of this default is necessary.

### The rules

The rules produce an actual utterance on the basis of the instructions. The rules specify how to put the elements from an instruction in their appropriate linear position and give them their proper grammatical form. The basic action induced by an instruction is the attachment of linguistic material onto the linguistic structure prepared by the preceding instructions. The attachment is typically followed by various automatic morphosyntactic edits to produce the right form, including allomorphy, agreement and government. More complex morphosyntactic structures will be modelled using ~~templates~~, i.e. fixed linear structures with "slots" that only allow for a restricted set of "filler" morphemes. The rules for German will be discussed in details in later chapters when the concrete implementation of YAST for German will be presented.

### The result

In the current implementation, the result of applying the rules to a recipe is an utterance in orthographic form. Each part of the utterance is prepared as soon as possible, i.e. the first words of an utterance can mostly already be uttered long before all instructions for a complete sentence are even finished. This is illustrated in [@tbl:example] for the recipe from [@last]. This intuitively seems similar to actual language production in that it is often possible to start speaking without even knowing what will be said in the rest of the sentence.

There are a few syntactic restrictions that result in a slight delay in the result. Basically, finite verbs have to wait for the subject to be planned, so the verb agreement can be added. Also, nouns have to be in a waiting queue for the production to be sure that there are no further pre-nominal attributes that have to placed before the noun. Still, the production of the resulting utterance stays really close to the generation of the instructions.

Recipe                                          | Result
:--------------                                 | :------
`sehen (Perfekt)`                               |
` Gesehene: Mann (Plural + Definit)`            | *Die*
`  schlafen`                                    | *Männer*
`   Schlafende: Kind (Plural + Besitzer: Mann)` | *deren*
`    klein`                                     | *kleinen*
`   schlecht`                                   | *Kinder schlecht*
` Sehende: 1`                                   | *schlafen*
` gestern`                                      | *habe ich gestern*
` in: Garten (Definit + Besitzer: 2)`           | *in deinem*
`  schön`                                       | *schönen Garten gesehen*

Table: Resulting production of the utterance (right), shown parallel to the instructions from the recipe (left). There is only a minimal delay between the generation of an instruction and the production of the utterance. {#tbl:example}

### The receipt

The receipt summarizes the process of building an output from the recipe. I use a constituent-like structure for the receipt, as shown in [@fig:receipt], but this is not necessarily the best or ideal approach. In general, the details of the receipt are rather ephemeral in that it is mostly a question of taste which aspects of the recipe+rules process is shown in the receipt. That is to say, most details of how the receipt currently looks are easily changed to other preferences. For example, in the current implementation, I have added a "cleanup" stage, in which various details are removed to present a simpler receipt. 

![Constituent structure in YAST](figures/receipt){#fig:receipt}

Still, I have retained various "traces" of the process leading to the end result, which might look somewhat like transformational movements from early proposals in transformational grammar. This happens because some elements of the instructions have to be temporarily kept "in memory" as they cannot immediately be cleared for pronunciation. This happens, for example, with verbs that are waiting for their subject specification to get subject agreement. Such ingredients "in waiting" are stored internally somewhere and are only uttered at the requisite moment/position. At the moment when such ingredients are being processed for pronunciation, they are taken from their internal storage and "moved" to their eventual position in the constituent structure. Crucially though, the location of the internal storage in the structure is really arbitrary, so the movement is actually more like a process of "preparing for pronunciation". I tend to temporarily store elements in such a position that it only needs minimal movement, but the internal storage could just as well be a unordered named list, separate from the receipt.

### The parser

The ephemeral role of the constituent-like receipt is also reflected in the workings of the ~~parser~~. The parser does not attempt to reconstruct the constituent tree, but immediately (after observing each pronounced element) tries to reconstruct the underlying dependency-like instructions of the recipe. In the current implementation, various different instructions are attempted within the range of possibilities as constrained by the actual utterance. Each attempt is fed into the rules until the actually observed utterance is replicated. The YAST-parser is thus actually a predictor that constantly tries to reconstruct the instructions (as intended by the generator) by performing generation of a recipe in parallel and checking the results of these mirrored generation with the observed utterance. The parser mostly does not have to wait until an utterance is finished, but can already start predicting while the utterance is still ongoing. This aspect of YAST seems to be a very fruitful approach for modeling language processing. 

![Basic workflow of YAST](figures/basis){#fig:basis}

### Formal complexity

Before delving into the details of this syntactic model, a few words on the algorithmic complexity of this model are in order. This topic needs more in-depth investigation, but my initial impressions are as follows:

- Each instruction in the recipe can be generated with a simple regular language, i.e. a type-3 grammar.
- The recipe consists of a set of hierarchically ordered instructions, which can be modeled with a context-free language, i.e. a type-2 grammar.
- The rules differ in their complexity. Most operators are simple insertions with some reformatting, which are regular, i.e. captured by a type-3 grammar.
- Each insertion of a templatic constituent structure, with possibly multiple slots to be filled, are context-free, i.e. they form a type-2 grammar.
- Finally, the rules that are defined as "diathesis/valency alternation" in Cysouw (2023) are exactly the rules that need multiple joint insertions, so these are mildly-context-sensitive, i.e. they fall in between a type-2 and a type-1 grammar. It seems to be the case that it is this part, and only this part, of the morphosyntax that is more complex than context-free.
- The parsing needs more work, but it consist of reconstructing a dependency-like structure from an utterance, which does not appear to be highly complex, possibly just regular, i.e. a type-3 grammar.

## Postulates for morphosyntax {#sec:postulates}

A small set of concepts are proposed here as universal postulates for the structural analysis of morphosyntax. These postulates are no requisite for the morphosyntactic model proposed in this book. Rather, they represent an attempt to explicitly articulate the basic assumptions underlying YAST and to propose principles that may prove useful for investigating the nature of human language and its evolution. Even if these postulates ultimately might prove unconvincing, this does not affect the subsequent practical operations of the YAST morphosyntactic model.

These notions are termed "postulates" because they exhibit three key properties: they are (i) axiomatic, (ii) presumed, and (iii) cancelable. First, they are axiomatic in that they establish a foundation for morphosyntax from which other characteristics can be derived. Second, they are presumed, that is, they constitute "obvious" components of human language structure and are assumed to exist without extensive argumentation. Third, they are cancelable, meaning they need not necessarily form part of any communicational system. Human languages could conceivably exist without any of these characteristics. Thus, none of these postulates claim strict universality, if only because they must have emerged at some point during the evolution of human language. Nevertheless, the following characteristics appear widespread among human languages and are arguably present universally in contemporary human languages.

- (P1) **Morphemic division** \
  Utterances are separable into morphemes.
- (P2) **Hierarchical modification** \
  Morphemes modify other morphemes, and modifiers in turn can be modified.
- (P3) **Differential modification** \
  Morphemes have constraints on the extent to which they can be modified.
- (P4) **Grammatical relations** \
  Different kinds of modification are distinguished.
- (P5) **Identification** \
  Morphemes can be used to identify entities (i.e. to make an assertion that something exists).
- (P6) **Assertion** \
  Morphemes can be used to make statements about referenced entities.
- (P7) **Semantic space** \
  The meaning of a morpheme is a distinctive subspace of a universal continuous multidimensional semantic space.
- (P8) **Grammaticalisation** \
  Over time morphemes can become increasingly specialized, structurally and/or functionally.
- (P9) **Innovation** \
  New morphemes can be introduced by grammaticalisation, but also by borrowing or by pure creative fabrication.

These postulates describe general principles that lead to very different grammatical structures in different languages. So, as general principles they appear to be universally present, but the concrete instantiation is widely variable. The capricious process of grammaticalisation (P8) is the root cause for the accumulation of differences in structure between languages.

The notion of differential modification (P3) has various immediate ramifications that all appear to be universally attested in human languages. This postulate thus might very well be further subdivided into more specific postulates describing special kinds of constraints on modification, including the following apparently universal phenomena.

- (P3a) **Non-modifiable operators** \
  Some morphemes cannot be further modified.
- (P3b) **Spawned roles** \
  Morphemes can induce morpheme-specific grammatical relations.
- (P3c) **Templatic structure** \
  Grammaticalisation can lead to a fixed linear structure with multiple "slots" that each only allow for a restricted set of "filler" morphemes.
- (P3d) **Probabilistic modifier choice** \
  Each morpheme has different preferences for what kind of modification typically follows. This kind of restrictions seems best modelled by large language models and will not be further pursued here.

As a basic H~0~ hypothesis, I assume that semantic space (P7) is a high-dimensional and continuous space, but also a compact, flat and simply connected space (borrowing terms from cosmology). However, this is just a wild guess. It basically means that the underlying semantic space has no structure. Each individual language imposes a structure on semantic space by the distribution of its linguistic elements over the space. It could very well be the case that recurrent semantic similarities across languages are the result of some kind of structure in the underlying semantic space, thereby refuting the H~0~ hypothesis. However, other explanations for semantic universals are also possible, like frequency-of-use and shared historical coincidences. Any argument refuting the hypothesis of an unstructured semantic space will need major cross-linguistic research, far beyond the scope of the current book.

## Elements of a recipe

### Generating a recipe: ingredients

In the syntactic model pursued here, the production of an utterance consists of two stages: first a ~~recipe~~ is created, followed by the application of ~~rules~~. Planning an utterance means to create a recipe for it, and this formation of a recipe is a generative process. This generative process also has some "rules"–that is, restrictions on which recipes can be constructed. However, these restrictions are relatively minor, even for a strongly flectional language like German. Other languages might exhibit even less constraints in this regard. The relative freedom to produce recipes reflects the wide leeway speakers have to produce a wide variety of utterances. In extremis, the automatic rules will sometimes have to "work around" the instructions in the recipe to mould the speaker's creative intention in accordance to the structure of the language.

The basic building blocks of a recipe will be called ~~ingredients~~ (in keeping with the cooking metaphor). The existance of ingredients follows from postulate P1 from [@sec:postulates]. Basically, ingredients are morphemes, but they also include fixed grammaticalized combinations of morphemes (like non-compositional idioms) and multi-part grammatical structures (like auxiliary constructions). Semantically, ingredients induce a state-of-mind at the addressee, probably consisting of a multitude of possible situations in accordance to the communally developed practice of using the ingredient (i.e. the ingredient's "meaning"). The act of using an ingredient intends to conjure up some of those possible situations in the mind of the addressee, narrowing down the interpretative possibilities with each further ingredient used.

Restrictions on building a recipe mainly consist of limits on which ingredients can be used in the generation. There will ultimately be two different kinds of restrictions, namely (i) restrictions on lexical insertion of ~~heads~~, which will be minimal, and (ii) restrictions on adding grammatical ~~operators~~, which are strongly determined by the chosen head. To fully describe these limits it will ultimately be necessary to specify individual possibilities separately for each ingredient of a language, because ultimately each ingredient has different distributional constraints and tendencies. In the end, something like a Large Language Model with millions of parameters is necessary to fully describe the distributional detail of a language. However, in this book I will only describe some general patterns with the understanding that these patterns are just a starting point for the subsequent specification of more detail. Ultimately, there is clearly a need for some kind of "grammatical lexicon" that includes the full syntactic detail for each ingredient in humanly readably form (as opposed to the unintelligible black box that is a Large Language Model).

### Combining ingredients: base & modifier

Language extends the usefulness of its ingredients by combining multiple of them into larger utterances. The underlying semantic effect of the combination of ingredients is probably something quite general like intersecting the two sets of possible situations. Uttering an ingredient-combination asks the addressee to search for possible situations that are in accordance with both ingredients. When, at first, the addressee might not be able to find any feasible intersection, this forces a reconsideration of possible interpretations of the ingredients, hopefully eventually leading to some kind of "understanding" on the part of the addressee.

Additionally, a central tenet of human language is that combinations of linguistic elements is in general asymmetrical. Ingredients are not simply combined as equals, but there is always a ~~base~~ that is modified by another linguistic element: the ~~modifier~~. Symmetrical connections with European-style *and*-coordination seem to be a relatively late addition to the grammatical spectrum. For the recipe, I will assume that all combinations of ingredients in human language are asymmetrical, including in coordination (i.e. in coordination there is always a primary and a secondary member with slight asymmetric properties).

Bases can have multiple modifiers and each modifier can itself be a base that again can be modified. The existence of such hierarchical modification in human language is proposed as postulate P2 in [@sec:postulates]. So, a recipe is in essence just a complex hierarchical dependency structure. When a base has multiple modifiers, then the ordering of these modifiers is often meaningful, so the ordering will have to be encoded in the recipe. However, in many situations the actual ordering of modifiers is strongly restricted in a language, for example in morphologically bound constructions. Such templatic ordering restrictions are encoded in the rules, not in the recipe. Yet, there are also situation in which the ordering is not completely fixed, but there nevertheless are strong tendencies, for example in the ordering of attributive adjectives in many languages. It is currently unclear how to best encode such tendencies. For now the recipe will simply allow all possible orders, even when there is only minimal possible variation.

### Syntactic elements: head & operator

To streamline the raw intricacy of pure modification, it is helpful to distinguish two different kinds of elements in the hierarchical structure depending on to which extend they can be modified (cf. postulate P3 from [@sec:postulates]). First, when an ingredient cannot itself be modified again, or when it only can have a single modifier from a small set of possible ingredients, then it will be called an ~~operator~~. Second, when an ingredient potentially allows for more than one modifier in parallel, then it will be called a ~~head~~. It is important to note that these terms describe syntactic functions and not specific ingredients. One and the same ingredient might be both a head and an operator, depending on the context in which it is used. 

Typical operators are bound morphemes, but there are many other non-bound linguistic elements that are operators under the current definition (namely, they cannot themselves be modified), for example intensifiers, quantifiers, adpositions, subjunctions and some ingredients traditionally called adverbs. Heads typically include nouns, verbs and adjectives, though there are also some heads among the disparate group of adverbs.

::: ex
Syntactic elements in YAST

- **Operator** \
  An ingredient that itself cannot be modified, or can only have a single modifier chosen from a small class of possibilities.
- **Head** \
  An ingredient that can be modified by multiple other ingredients in parallel.
:::

The distinction between operator and head is largely independent from the distinction between base and modifier from the previous section. Heads and operators alike can be both modifiers and bases. However, the modification of operators is quite restricted (by definition), so operators are less commonly used as the base of a modification. The special situation in which an operator modifies another operator is called a ~~stack~~. Stacks are typically found in bound morphology, but not all stacks are bound and not all bound morphology forms stacks. When heads modify heads this is called ~~embedding~~. Note that this term is used here referring to both nominal and verbal embedding. The more traditional usage of the term "embedding" for clausal recursion will be explicitly called "clausal embedding".

The hallmark of human language is the possibility to productively combine many different linguistic elements into large utterances. A central aspect of morphosyntactic structure is that linguistic elements can in turn consist of multiple linguistic elements, leading to a hierarchical internal structure of the utterance (cf. postulate P2 from [@sec:postulates]). This hierarchical structure is commonly modeled in syntactic theories by using the mechanism of recursion. However, not all hierarchical structures are equally in need of a recursive treatment. Crucially, only embedding will be modeled with recursion. Stacking is much simpler and does not need recursion. It can easily be modeled by iteration ("tail recursion"), i.e. stacked modifiers are simply applied one after the other without intricate branching.

### Heads: predicate & referendum {#sec:heads}

Heads, as defined in the previous section, are ingredients that can be modified freely, and they alone allow for embedding. For German (and possibly for all human languages), it only appears to be necessary to distinguish two different kinds of syntactic uses of heads, coinciding with two central functions of human language, namely ~~identification~~ and ~~assertion~~. 

First, speakers attempt to convey which entities they are talking about and these entities (the referents) then have to be identified by the addressee (cf. postulate P5 from [@sec:postulates]). The primary ingredient that is used to encode the identity of a referent in an utterance is called a ~~referendum~~. This referendum is the head of a referential expression that includes all its modifiers (which might themselves again be modified). The whole referential expression is called a ~~phrase~~. A referent is typically encoded by what is traditionally called a noun, but many other parts of speech can also be used as referent. Note that, differently from most syntactic theories, there is only one kind of phrase in YAST, roughly equivalent to what is called "noun phrase" in most other approaches. For convenience, any head modifying a phrase is called an ~~attribute~~ (or maybe better an ~~adnominal~~).

Second, in a typical utterance some kind of assertion is made about these referents (cf. postulate P6 from [@sec:postulates]). The primary ingredient that is used to encode the assertion is called a ~~predicate~~. The predicate is the head of an assertion that also includes all its modifiers (which might themselves again be modified). This whole assertive expression is called a ~~clause~~. A predicate is typically encoded by what is traditionally called a verb, but other parts of speech can also be used predicatively. For convenience, any head modifying a clause is called an ~~adverbial~~.

::: ex
Heads in YAST

- **Referendum** \
  The head of a ~~phrase~~, used for ~~identification~~. Its modifiers are called ~~attributes~~ (or ~~adnominals~~).
- **Predicate** \
  The head of a ~~clause~~, used for ~~assertion~~. Its modifiers are called ~~adverbials~~.
:::

It is by no means necessary for identification and assertion to be encoded by syntactic heads and their encompassing expressions. Personal pronouns, demonstratives and content interrogatives can be interpreted as identifying expression, but they are operators (i.e. they cannot be modified). Likewise, interjections and conversational particles can be seen as assertions without much internal structure. Still, it does not seem to be a coincidence that exactly the most elaborate syntactic structures (phrases and clauses) are precisely those structures that are used for two main communicative elements in a linguistic utterance.

[--
semi-clause, non-finite clause, restricted clause, deranked clause
--]::

### Operators: admodifiers, junctors & specifiers

Operators, as defined previously, are ingredients that cannot be modified, or can only have a single modifier out of a small set of possibilities. I will distinguish three different kinds of operators based on their morphosyntactic characteristics, called admodifiers, junctors and specifiers.

**Positionally-flexible admodifiers.** Most operators are positionally predictable–that is, when they are used to modify a base, their position relative to the base is morphosyntactically fixed. However, there is a group of operators that have more freedom in their positioning, so the speaker has to explicitly decide where to place them, mostly leading to slight differences in the intended meaning. Such positionally flexible operators will be called ~~admodifiers~~.^[This term is used differently here from Croft (2022:§2.2.2). Alternative terms for "admodifier" might be adorner, additor, adjustor or adaptor.] In German these admodifiers comprise various ingredients that are traditionally called adverbs. Also some adjectives might belong to this class, but in German this does not seem to be the case. Diachronically, admodifiers seem to be an intermediate phase in the grammaticalisation of heads into positionally-fixed operators.

**Relation-marking junctors.** Among the positionally-fixed operators there is a special class of ingredients that specify the kind of modification–that is, they spell out more precisely what is the relation between a base and its modifier (cf. postulate P4 from [@sec:postulates]). Heads can be modified by multiple other heads, each with their own relation to the superordinate head. These relations between base-heads and modifier-heads are often explicitly marked in the linguistic structure by operators that are called ~~junctors~~ here. In German, examples of phrasal junctors are prepositions and case marking ("flagging"), while examples of clausal junctors are subjunctions and conjunctions. Default ("unmarked") relations also exist in the form of constructions like appositive phrases, relative clauses and non-finite "restricted" clauses.

**Positionally-fixed specifiers.** For clarity of exposition, all other positionally-fixed operators (i.e. all operators except for the admodifiers and junctors) are called ~~specifiers~~ here. These specifiers contain many traditional grammatical categories like tense-aspect-mood marking for clauses, or number and definiteness for phrases. Which specifiers can be added depends on the base being modified. The two largest groups of specifiers are the phrasal and clausal specifiers, but specifiers for other operators also exist (possibly leading to stacks of operators).

### Spawned junctors: roles

Heads typically spawn junctors. These phenomenena are commonly known as lexically-determined arguments or roles, but it will be approaches from a slightly different angle here. The basic idea is that individual lexemes will have restrictions on how they can be modified (cf. postulate P3 from [@sec:postulates]). One such type of restriction is that a lexeme induces specific relations that are typically added to modify this lexeme. For example, the German verb *hoffen* 'to hope' has a relation *Hoffende* 'the hoping one', typically using the German *Nominativ* case as a junctor, and a relation *Hoffnung* 'the object of hope', typically using the German preposition *auf* as a junctor. 

Such lexically-determined junctors are called ~~roles~~. Although there are many widespread tendencies as to which roles exist and how they are expressed, for now I will simply specify the roles for each lexical ingredient seperately. German phrases and clauses almost always have a "principal" role, which for phrases will be called the ~~container~~ (German: *Behälter*, typically using a *Genitiv* junctor) and for clauses will be called the ~~protagonist~~ (German: *Protagonist*, typically using a *Nominativ* junctor).

These principal roles only very rarely appear to be absent, like the absence of a protagonist with weather verbs. In contrast, additional roles are spawned by many lexical items, like the well-known roles of (di)transitive verbs. However, adjectives and nouns can also spawn additional roles, in German typically using grammaticalised prepositions. For example, the adjective *froh* 'happy' uses the preposition *über* 'above, over' for the origin of the happiness, or the noun *Reaktion* 'reaction' using the preposition *auf* 'on top of' for the event causing the reaction.

### Building a recipe

Very simple utterances can consist of just an assertion (e.g. imperatives) or just an identification (i.e. answers to content questions). Recipes for such utterances consist of just a single predicate or just a single referendum. For more complex utterances various of the previously discussed ingredients are combined into larger recipes consisting of multiple instructions.

The generation of a recipe can be formalised as a very simple recursive procedure shown in [@next]. This procedure is completely context free as there are no restrictions on the generation at this level of abstraction. The notation used here is inspired by generative rewrite rules for constituency trees, but they work slightly differently to generate a dependency tree. The plus symbol stands for modification of the first element on the right side of the arrow. The arrow itself literally means replacement of the left side with the right side. Additionally, in the notation below the vertical bar stands for "or", the round brackets indicate optionality and the superscripted (Kleene) star indicates that the enclosed elements can occur zero or more times. 

::: ex
Formalisation of the generation of a recipe:

1: base → instruction + (base)\* \
2: instruction → (junctor) + nucleus + (specifier)\* \
3: nucleus → predicate | referendum | admodifier
:::

The central elements of a recipe are the instructions. Using the first rule, instructions are inserted recursively modifying other instructions. For readability of the recipe I propose to write each instruction as a single line, using indentation for modification. Each instruction has an obligatory nucleus with optionally a junctor in front, separated by a colon, and optionally specifiers in round brackets at the end of the line. These details of the formatting of a recipe are just cosmetic decisions.

Randomly applying the above rules might result in a recipe like in [@next]. However, when building a real recipe, each instruction will immediately be constructed with actual linguistic content before moving to the generation of a subsequent instruction. A "skeleton" recipe like in [@next] will thus never be generated and it is just shown here to illustrate the formalisation in [@last].

::: {.ex noFormat=true}
```
predicate (specifier)
  junctor: referendum (specifier)
    admodifier
  admodifier
  junctor: predicate (specifier)
    junctor: referendum
      junctor: referendum
```
:::

To illustrate the dependency nature of such a recipe, the first three instructions from [@last] are shown as a dependency tree in [@fig:dependency]. The difference between such a dependency tree and a constituency tree is not really substantial. When the procedure in [@llast] is interpretated as a set of classic generative rewrite rules, then the first three instructions from [@last] result in a constituency tree as shown in [@fig:constituency]. Added to this figure is a notion of headedness, as indicated by the arrows. When these arrows are "collapsed" by inserting the arrow-origin into the arrow-goal, then the same dependency structure as shown in [@fig:dependency] is obtained. This demonstrates that a constituency structure (with an additional notion of headedness) is equivalent to a dependency structure. The only difference is that the constituent tree explicitly includes the history of application of the rewrite rules.

![Example of a dependency tree generated by the formalisation in [@llast], illustrated here for the first three lines of the example in [@last].](figures/dependency){#fig:dependency width=63%}

![Consituent tree for the same example as in [@fig:dependency]. This structure is the result of interpreting the formalisation in [@last] as generative rewrite rules. The arrows indicate the headedness of each constituent.](figures/constituency){#fig:constituency}

How to choose an appropriate linguistic content is to a large extent a matter of speaker choice, which seems most profitably to be handled by the kind of large language models developed recently. However, grammatical restrictions start to appear as soon as individual ingredients are chosen, specifically after any chosen nucleus. There are basically three kinds of syntactic restrictions: any chosen nuclues typically will restrict (i) the choice of junctor in the instruction, (ii) the choice of specifiers in the instruction, and possibly (iii) the choice of junctors in subsequent modifying instructions. 

Each instruction has an obligatory ~~nucleus~~ with optionally a ~~junctor~~ in front (separated by a colon) and optionally ~~specifiers~~ following (in round brackets). For example, the first instruction of the recipe in [@nnext] has a nucleus *hören* 'to hear' with a specifier indicating that it should be put in the *Perfekt* form. There is no junctor here, although a conjunction like *und* 'and' or *aber* 'but' could have been added.

Each instruction has two further elements, which are less obviously present in the recipe. First, each instruction indicates which element it is modifying by indentation. In the example below, the first instruction is not indented, so there is no modification of an earlier instruction. Second, each instruction is either a clause, a phrase or an admodifier. In the example below, the first instruction is inferred to be a clause. This is the default inference for a verbal nucleus like *hören* 'to hear'. To simplify the recipes, such defaults are not explicitly written down.

::: ex
Das kleine Kind hat gestern gehört, dass sein Vater Bürgermeister wird.
:::

::: {.ex noFormat=true}
```
hören (perfekt)
  Hörende: Kind (definit)
    klein
  gestern
  Gehörte: Bürgermeister (werden)
    Werdende: Vater
      Behälter: Kind
```
:::

The second instruction in [@last] indicates by indentation that it modifies the first instruction. The relation *Hörende* is just a German name for the protagonist role spawned by the verb *hören* of the modified instruction. The nucleus noun *Kind* 'child' by default is inferred to be the head of a phrase. The third instruction *klein* 'small' only consist of a nucleus, modifying *Kind* from the second instruction with a default relationship (i.e. there is no junction).

The fourth instruction *gestern* 'yesterday' has only a single indentation, indicating that it modifies the clause *hören* of the first instruction. Crucially, this means that the possibility of the modification of the phrase *Kind* is now finished. This allows for the formulation of this phrase to be completed. In general, modification in the recipe is always immediate: it is not possible to resume modification later, once a hierarchically higher base is modified.

# Syntactic functions and ingredient classes

## Syntactic functions

in a specific utterance, each ingredient has a syntactic function. it is possible (and useful) to enumerate the ingredients that can be used in a syntactic function. Such a class of elements is alike to a part of speech. Ho

The main question is thus which syntactic functions should be distinguished. Each function then defines a class. 

function determines class! how to define a syntactic function? 

for heads: form of predicate and referendum
for operators: classified by the kind of modification:

- what kind of base is modified? Main options: modification of predicate or referendum. Additionally: some limited groups of modification of operators 
- what is the positional relation to the modified base? (e.g. bound, syntactically fixed, positionally variable, note that variable+bound also is possible). A class is simple a group of ingredients with the same positional relation, whatever it is.

## Parts of speech

Ingredients can be categorized into classes on the basis of their syntactic characteristics. However, such ingredient classes ("parts of speech") are not an atomic feature of the morphosyntax in YAST, but a secondary consequence of the possible syntactic functions of the ingredients. In the end, when considering all morphosyntactic phenomena, I expect that each ingredient will have its own individual syntactic characteristics, so ultimately each ingredient will be its own class. When scrutinizing all linguistic details, ingredient classes will dissolve into an ever expanding pile of subclasses. 

Still, a few large classes, somewhat reminiscent of traditional parts of speech, can profitably be identified. However, these classes should not be expected to be perfectly homogeneous (i.e. they will always be internally variable), nor will they be complementary (i.e. they will always overlap). 

Moreover, the group of ingredient that belong to a certain class is not fixed. In principle, all ingredients can occur in all classes because the creativity of language use allows ingenious speakers to employ any ingredient anyway they like. So, in principle each class includes the whole language. However, the probability for a specific ingredient to occur in a class is strongly skewed. I will pretend here that inclusion of an ingredient into a class is a yes/no question, but this is a strong simplification. In reality the question of the class-membership of an ingredient is a probabilistic decision.

The major elements of a recipe as defined in the previous section are the most extensive of these ingredient classes. The four major kinds of ingredients are recapped briefly in [@next] below. These classes are defined in such a way that they are probably universally applicable to all human languages. To get closer to the traditional parts of speech, these macro-classes will be subdivided in this chapter into smaller groups based on language-specific distributional characteristics.

::: ex
Macro-classes in YAST

- **Heads.** Heads are ingredients that can be freely modified by multiple other ingredients. In German, heads basically include what are traditionally called verbs, nouns, adjectives, but also some adverbs.
- **Admodifiers.** Admodifiers are operators (i.e. they cannot be modified, or only allow for very limited modification) that have some positional flexibility. In German, admodifiers are basically adverbs and numerals.
- **Specifiers.** Specifiers are operators that have no positional variability. In German this includes most morphology as attached to heads (e.g. affixes for nominal plural, verbal past or adjectival comparative), but also various kinds of syntactic "particles".
- **Junctors.** Junctors are operators that indicate the kind of modification. In German this includes prepositions, subjunctions and conjunctions, but also grammaticalised roles with their accompanying case marking.
:::

Sometimes rules that need to know classes (e.g. postpositions). Also: attribute genitives: pre-nominal with proper names, otherwise postnominal. Also: order of adjectives

Note: compounding is extremely frequent to make new bases

morpheme classes are language specific

Morphemes can be classified into classes based on the 'construction' in which they can appear. Such a class should clearly be implemented as a gradual class, e.g. by adding frequencies. Speaker's ingenuity can always add a specific morpheme into a class.

- templates and operators define classes
- morphemes can be (and typically are) multi-functional, i.e. they appear in multiple classes
- classes cross-sect each other ()

Adverbs are a non-coherent group:

- typically they are operators

Roots that are noun, verb and adjective: fett, harsch, laut (lauten/läuten), leck, schmuck (schmücken)

- dieser Laut wird unterschiedlich geschrieben
- die Glocken lauten seit gestern
- die seit gestern lautende Glocken sind nervig
- die Lautenden sind nervig
- die Glocken sind seit gestern sehr laut
- die seit gestern sehr laute Glocken sind nervig
- die Laute ist am nervigsten

## Heads

Heads are used either as predicate or as referendum (see [@sec:heads]).

Heads will be classified on the basis how they are used in the two main syntactic functions, namely as (i) predicate and as (ii) referendum. 

- predicate with person/number inflection ("indexing"!?) ("verb")
- predicate with auxiliary
  - *werden/sein/bleiben* ("adjectives" and participles and alienable anthroponyms)
  - only *sein*: (various "adverbs")
  - *haben* (various nouns, like Angst, Schmerz, Hoffnung, Vertrauen, Sehnsucht, Appetit, Durst, Hunger, Kopfschmerzen, Fieber, Schnupfen, Zeit, Geduld, Talent, Recht, Glück, Pech, Einfluss, Ferien, Urlaub, Dienst, Pause, Geld, Schulden, Besitz, Eigentum) Note: *Freude haben an etwas*

- referendum with fixed genus ("noun")
- referendum with agreement and free genus ("adjective", participles)
- referendum neutrum with -en ("verb")

Classes of heads can be established by the possibility of a base being the center of any of the four major syntactic functions, namely whether they can be used as (i) referential head, (ii) predicative head, (iii) attributive adjustor, or as (iv) adverbial adjustor. Five German base classes can then be defined by the distribution as shown in [@tbl:heads]. These classes largely correspond to the traditional categories as used in German grammar, except for adverbs, which turn out to be a rather incoherent hybrid class. The first three classes (*Nomen, Verb, Adjektiv*) are very large, while the latter two (*Adverb, Numerale*) are strongly restricted in size. Additionally, as indicated by the "plus-minus" symbol, the classes of adverbs and numerals actually consist of various syntactic subclasses.

--
               *Verb*      *Adjektiv*   *Anthroponym*   *Nomen*   *Adprädikat*
------------- ----------- ------------ --------------- --------- --------------
Predicate      +INFL       AUX+INFL     AUX+INFL        –         *sein*+INFL

Referendum     gender \    gender \     gender \        gender \   
               choice \    choice \     fixed \         fixed \    –
               *‑end*+AGR  +AGR                                    

--

Table: Syntactic expression of German heads. Five large German word classes can be defined by how heads are expressed when used as predicate and as referendum. (INFL=person/number inflection (*Verbflektion*), AGR=case/number/gender agreement (*Kongruenz*). AUX=*werden/sein/bleiben*) {#tbl:heads}

Referendum \
(inherent gender)

Predicate \
(inflection)



*Nomen*

Humannomen (better: alienable human noun!): Sohn/Freund geht nicht, Wirklichkeit event. wohl

The class of *Nomen* corresponds to the traditional concept of nouns as it is used in German grammar, and it is arguably the largest of the base classes. Nouns in German have a lexically determined inherent gender when used as a referential head [@next a] and they can all be used as predicative head with the help of a copula, either *werden* 'to become', *sein* 'to be', or *bleiben* 'to remain' [@next b]. Note that such a "real" predicative use of a noun does not have an article. Many nouns can only be used as "real" predicative head (i.e. without article) in the plural to indicate the generic meaning [@next c]. With an article the predicative use of a noun turns into an identificational construction to be discussed later (see ???).

::: ex
Syntactic uses of a *Nomen* in German

- Referential head: *Der **Vater** ist noch jung.*
- Predicative head: *Er wird bald **Vater**.*
- Predicative head (Generic plural): *Dryaden und Hamadryaden sind **Bäume**.*^[~~DWDS~~: Spengler, Oswald: Der Untergang des Abendlandes, München: Beck 1929 [1918], S. 516.]
- Identification: *Er ist der **Vater**.*
:::

German nouns can only be used as an attributive adjustor and as an adverbial adjustor using lexically-specific morphological derivations with suffixes like *‑haft, ‑ig, ‑isch, ‑lich, ‑gemäß, ‑mäßig* or *‑artig*. The availability of these derivations are strongly lexically dependent. Many nouns allow for multiple such derivations (e.g. *kindhaft, kindisch, kindlich, kindgemäß*), while others do not seem to allow any of these derivational suffixes (e.g. *Stuhl* or *Schuh*). Such uses of nouns as adjustors are not included here as syntactic possibilities because these suffixes are not productively available to all nouns.

*Verb*

The class of *Verb* also corresponds to the traditional concept as used in German grammar, illustrated here with the verb *lesen* 'to read' in [@next]. When used as a predicative head a German verb has person-number-tense inflection [@next a]. All German verbs can be used as a referential head in the *Infinitiv*, a form ending in *-en* and written with a capital in German orthography when used as a referential head [@next b]. As a referential head, the gender of a verb is always neuter.

All German verbs can also be used as an attributive adjustor in the form of a so-called *Partizip Präsens* (also called *Partizip I* the German grammatical tradition) ending in *-end* and taking adjectival agreement [@next c]. Other non-finite verbal forms (like the *Partizip Perfekt*) are also possible in this function, but not for all verbs, so they are not included here as a general syntactic option. 

The same non-finite participle can also be used as a "fake" adverbial adjustor [@next d]. Although this construction looks syntactically like an adverbial, the participle *lesend* in this sentence modifies the object *mich* of the sentence. In general, participles used syntactically like adverbials in German always modify an argument of the main verb (sometimes called "depictive secondary predication"). The main verb of the sentence is only modified indirectly by such depictively used non-finite verbforms, because the main verb is modified by the argument, which in turn is modified by the non-finite verbform.

::: ex
Syntactic uses of a *Verb* in German

- Predicative head: *Ich **lese** keine Romane mehr.*^[~~DWDS~~: Die Zeit, 06.11.2017, Nr. 45.]
- Referential head: *Meine Urgroßmutter machte das **Lesen** dieser Briefe sehr müde.*^[~~DWDS~~: Hermann, Judith: Sommerhaus, später, Frankfurt a. M.: Fischer-Taschenbuch-Verl. 2000 [1998], S. 13.]
- Attributive adjustor: *Überall traf man nun **lesende** Landarbeiter und Bauern an.*^[~~DWDS~~: Enzensberger, Hans Magnus: Der kurze Sommer der Anarchie, Frankfurt a. M.: Suhrkamp 1972, S. 31.]
- "Fake" adverbial adjustor (depictive): *Man hat mich in Apfelbäumen **lesend** erwischt.*^[~~DWDS~~: Zeit Magazin, 15.11.2012, Nr. 47.]
:::

*Adjektiv*

The class of *Adjektiv* consists of ingredients that can be used in all four syntactic functions from [@tbl:heads], as illustrated with the adjective *groß* 'large' in [@next]. Grammatically, there are few special characteristics of the different uses of adjectives. First, when used as a referential head [@next a] the gender can be freely assigned. Second, both as a referential head [@next a] and as an attributive adjustor [@next c], adjectives in German have case-number-gender agreement suffixes, so-called *KNG-Kongruenz* in the German grammatical tradition. Third, an adjective needs a copula when used as a predicative head [@next b], either *werden* 'to become', *sein* 'to be', or *bleiben* 'to remain'. When used as an adverbial adjustor it is used without any further morphological change [@next d]. Note that it is also possible to use adjectives as "fake" adverbials, i.e. to use them depictively [@next e], similar to the use of participles in [@last d]. This is treated as an attributive adjustor, though with a different syntactic appearance in the sentence.

::: ex
Syntactic uses of an *Adjektiv* in German

- Referential head: *Die **Große** zuckte mit keiner Wimper.*^[~~DWDS~~: Brussig, Thomas: Wasserfarben, Berlin: Aufbau-Taschenbuch-Verl. 2001 [1991], S. 93.]
- Predicative head: *Die Aufregung über diesen Fall war **groß**.*^[~~DWDS~~: Hars, Wolfgang: Nichts ist unmöglich! Lexikon der Werbesprüche, München: Piper 2001 [1999], S. 378.]
- Attributive adjustor: *Das **große** und mächtige Schiff hob und senkte sich noch einmal.*^[~~DWDS~~: Lebert, Benjamin: Crazy, Köln: Kiepenheuer & Witsch 1999 [1999], S. 150.]
- Adverbial adjustor: *»Kaffeekultur« wird in Österreich überall ganz **groß** geschrieben.*^[~~DWDS~~: Die grosse Welt der Getränke, Hamburg: Tschibo Frisch-Röst-Kaffee Max Herz 1977, S. 274.]
- "Fake" adverbial adjustor: *Ich habe meine Hose zu **groß** gekauft.*
:::

The following ingredient belong to this class of adjectives:

- There are about 300 monomorphemic adjectives as summarized in [@next].
- Additionally, there are many additional German adjectives that are clearly Latinate/Greek loans, like *ambivalent, ambulant, binär, brachial, eklatant*, etc. I have not yet attempted to list them all.
- Some non-adjectival ingredients can be turned into adjectives by using one of the following suffixes: *‑artig , ‑bar, ‑end, ‑fach, ‑gemäß, ‑haft, ‑ig, ‑isch, ‑lich, ‑los, ‑mäßig* and *‑sam*. Note that various lexemes with one of these suffixes cannot be transparently related to a root, so those are actually lexicalised adjectives, like *häufig, ständig, wichtig, gleichzeitig, abwesend, anwesend, fortwährend, dementsprechend, anschließend, gewöhnlich, natürlich, wahrscheinlich, ausschließlich, unmittelbar*, etc.
- Substance-adjective from nouns in *-en*: *eiben, seiden, golden, erden, Stoffen, hänfen, pechen, milchen, eschen, buchen, leinen, birken, opalen, metallen, wollen, tannen, zinnen, papieren, taften, basalten, graniten, samten, eichen, bronzen, erzen* [@eisenberg1992: 103]
- Intensifying prefixes can be added to many of these adjectives to form new adjectives: *bitter‑, erz‑, hoch‑, hyper‑, mega‑, schwer‑, super‑, tief‑, ultra‑, un‑, ur‑*.

There are a few exceptions to this list of adjectives, in the sense that some ingredients that correspond to the above criteria do not allow for all functions as illustrated in [@last]. These ingredients, as listed below, thus form separate syntactic subclasses.

- A small group of ingredients from [@next] end in *‑n* instead of *‑r* wenn used as a predicative head or adverbial adjustor, namely exactly the following ingredients: *äußere/außen, innere/innen, obere/oben, untere/unten, vordere/vorn(e)* and *hintere/hinten*.
- Similarly, a few adjectives have an extra *‑s* when used as adverbial adjustor, namely exactly the following ingredients: *andere/anders, besondere/besonders, linke/links, rechte/rechts*.
- Also *hohe/hoch* and *niedere/niedrig* have a different form depending on the syntactic function in which they are used.
- Some derived adjectives cannot be used as a predicative head (e.g. *ehemalig, hochgradig, regelrecht, sogenannt, zusätzlich*), some cannot be used as a referential head (e.g. *absolut, neulich, relativ*) and some cannot be used in both those functions (e.g. *schließlich, sonstig, völlig, ziemlich, zwischenzeitlich*).^[Adjectives with such restrictions are sometimes discussed under the heading of 'relational adjectives' [@zifonun2011: 105], but it remains to be seen whether the syntactic restrictions can be explained by morphology and/or semantics.]
- Some apparent adjectives can only be used as an adverbial adjustor (and not attributively), namely exactly the following ingredients: *folglich, freilich, lediglich* and *nämlich*. They are not classified as adjectives anymore, but categorized as adverbs below. The ingredient *nämlich* is completely idiosyncratic in its syntactic possibilities and will be discussed in Section ???. 

::: ex
German monomorphic adjectives 

*albern, alt, andere, arg, arm, äußere, bang, barsch, besondere, bequem, besser, bieder, billig, bitter, blank, blass, blau, bleich, blind, blöd, blond, bloß, böse, braun, brav, breit, brüsk, bunt, derb, deutsch, dicht, dick, direkt, doof, doppelt, dreist, dumm, dumpf, dunkel, dünn, dürr, düster, echt, edel, egal, eigen, einzig, eitel, elend, eng, enorm, ernst, erst, extrem, fad, falsch, faul, feig, fein, feist, fern, fesch, fest, fett, feucht, fies, finster, firm, firn, flach, flau, flink, flott, forsch, frech, frei, fremd, froh, fromm, früh, ganz, gar, geil, gelb, gemein, genau, gerade, gering, geschwind, gesund, gewiss, glatt, gleich, grau, greis, grell, grob, groß, grün, gut, hager, harsch, hart, heikel, heil, heilig, heiser, heiß, heiter, hell, herb, hintere, hohe, hohl, hübsch, innere, irre, jäh, jung, kahl, kalt, kaputt, karg, keck, kess, keusch, kirre, klamm, klar, klein, klug, knapp, komplett, krank, krass, kraus, krude, krumm, kühl, kühn, kurz, lahm, lang, lasch, lau, laut, lauter, lässig, leck, lecker, ledig, leer, leicht, leise, letzt, licht, lieb, lila, lind, linke, locker, los, mager, matt, mies, mild, minder, morsch, müde, muff, munter, mürbe, nächste, nackt, nah, nass, nett, neu, niedere, nüchtern, obere, öd, offen, orange, platt, plump, prall, prüde, quick, rank, rar, rasch, rau, rechte, rege, reich, reif, rein, richtig, roh, rosa, rot, rüde, rund, sacht, sanft, satt, sauber, sauer, schal, scharf, scheu, schick, schief, schlack, schlaff, schlank, schlapp, schlau, schlecht, schleunig, schlicht, schlimm, schmal, schmuck, schnell, schnöde, schön, schräg, schrill, schroff, schüchtern, schwach, schwanger, schwarz, schwer, schwul, schwül, seicht, selig, selten, sicher, simpel, sohr, spät, spitz, spröde, stark, starr, steif, steil, stetig, stier, still, stolz, straff, stramm, streng, stumm, stumpf, stur, süß, tapfer, taub, teuer, tief, toll, tot, total, träge, treu, trocken, trüb, ungefähr, untere, übel, übrig, vage, viel, voll, vollkommen, vordere, wach, wacker, wahr, warm, weh, weich, weise, weiß, weit, welk, wild, wirr, wirsch, wund, wüst, zäh, zag, zahm, zart*
:::

## *Admodifiers*

The class of *Adverb* is a rather disparate group of ingredients from a syntactic point of view. This class will consequently be further subdivided in at least five different syntactic subclasses. The number of ingredients in this class is small: there are a few affixes that can be used semi-productively to produce adverbs, but other than those there are just short of 200 monomorphemic adverbs in German (as listed at the end of this section). These monomorphemic adverbs are often semi-transparent to German speakers but completely grammaticalized in their adverbial use, e.g. *nebenbei* 'lit. besides+by' or *deswegen* 'lit. of the+because of'.

To define the class of adverbs, this lexical class has to be strictly separated from the syntactic function of being used as an adverbial adjustor. Most prominently, adjectives are also commonly used as adverbial modifier, cf. [@llast d] above, but that does not make them adverbs (even though they are often called as such).

Adjectives used in the syntactic function of "preverbial modifier" are also excluded from the class of adverbs (cf. Cysouw 2023: #sec9.2.4). Preverbial modifiers construct new compound verbs, like the adjectives *leer‑* and *voll‑* in verbs like *leerfischen* or *volltanken*. These are not included here as adverbs. There is also a small set of non-adjectival preverbials (cf. Cysouw 2023: #sec9.2.5), like *weg‑* and *hoch‑* in compound verbs like *wegfahren* and *hochspringen*. In such compound usage these are also not included here as adverbs. 

The ingredients to be included here as adverbs can be positively characterized by three criteria. First, they all can function as adverbial adjustors, i.e. they are ingredients in adverbial function that themselves can be modified, like *seit gestern* in [@next a]. Second, they either cannot be used attributively at all, like *bald* 'soon' in [@next c], or, when they can be used attributively, then they are placed post-nominally without agreement, like *gestern* 'yesterday' in [@next b]. Finally, all adverbs can occur rather freely in the sentence, including crucially in first position, i.e. as the complete content of the *Vorfeld* [@next d,e].

::: ex
- Adverbial adjustor: ***Seit gestern** suchen Polizei, Feuerwehr und weitere Helfer nach dem Jungen.*^[~~DWDS~~: Die Zeit, 08.11.2016 (online).]
- Attributive adjustor: *Die Befragung **gestern** begann mit einem großen Schweigen.*^[~~DWDS~~: Der Tagesspiegel, 20.11.2000.]
- ^* *Die Befragung **bald** wird mit einem Schweigen beginnen*.
- ***Gestern** suchte die Polizei nach dem Jungen.*
- ***Bald** wird die Befragung beginnen.*
:::

adverbs after genitiv!

- Am Erstlauf des BR715 gestern nahm auch der Vorsitzende der chinesischen Plankommission, Chen Jinhua, teil. (Berliner Zeitung, 29.04.1997)
- In der Entscheidung des Gerichts gestern hieß es, der italienische Anspruch, den mutmaßlichen Kriegsverbrecher anzuklagen, habe Vorrang […]. (Berliner Zeitung, 04.03.1997)
- […] sondern auch die Vorstellung des Regierungsprogramms gestern betrifft. (Deutscher Bundestag: Plenarprotokoll Nr. 18/73 vom 04.12.2014, S. 6932)
- […] wenn ich an die Rede des Bundeskanzlers gestern denke […] (Deutscher Bundestag: Plenarprotokoll Nr. 07/102 vom 21.05.1974, S. 6710.)
- Das ganze Verhalten des Mannes gestern zeigte mir evident, daß er mehr als nur ein Gerücht wußte, daß irgend etwas zwischen gemäßigter Arbeiterschaft, Bürgertum und Heer in Vorbereitung sein muß. (Klemperer, Victor: [Tagebuch] 1943. In: ders., Ich will Zeugnis ablegen bis zum letzten, Berlin: Aufbau-Taschenbuch-Verl. 1999 [1943], S. 32)

Now, investigating the class of adverbs in more detail, there turn out to be at least five different subclasses depending on their syntactic possibilities. All adverbs can be used adverbially, but they differ in whether they can be used as referential head, as predicative head and/or as attributive adjustor. Confusingly, the resulting syntactic classes do not show any obvious semantic differentiation, so they will simply be numbered here. There is a tendency for adverbs with a local meaning to allow for more different syntactic uses, while adverbs with a modal meaning have fewer syntactic uses. However, this is just a statistical tendency and it is completely unclear to me whether this observation has any ramifications for the understanding of the different syntactic possibilities of adverbs.

Also, there appears to be quite some dynamism in the syntactic possibilities of adverbs. Some options that are excluded by the categorizations below will be considered to be perfectly possible to more adventurous speakers of German. This flexibility is most obvious with the use of adverbs as a referential head (i.e. as "noun"). There are many occurrences of such uses in the philosophical literature (e.g. *^?^das Seither* 'the since' and *^?^das Niemals* 'the never') that I consider only borderline acceptable.

Adverbs of type 1, for example *gestern* 'yesterday' [@next a], can be used in all four syntactic functions. In the function of an attributive adjustor (i.e. as an "adjective") it is placed after the modified noun without any agreement [@next b]. In the function of a predicative head (i.e. as a "verb") the copula *sein* 'to be' is necessary [@next c]. No other copulas are possible. In the function of a referential head (i.e. as a "noun") adverbs always have the neuter gender [@next d]. All ± 40 adverbs that allow for all these four syntactic functions are listed in [@adverbstype1] below.

::: ex
Syntactic uses of Adverbs type 1

- Adverbial adjustor: ***Gestern** hatte ich eine Lesung in Neubrandenburg.*^[~~DWDS~~: Die Zeit, 11.12.2017, Nr. 51.]
- Attributive adjustor: *Das Feuer **gestern** entstand beim Überfahren von Weichen.*^[~~DWDS~~: Der Tagesspiegel, 12.07.2001.]
- Predicative head: *Holzkiste und Kinderwagenräder waren **gestern**.*^[~~DWDS~~: Die Zeit, 18.08.2016 (online).]
- Referential head: *Aber das **Gestern** kann das Heute nicht gänzlich erklären.*^[~~DWDS~~: Die Zeit, 01.07.2017, Nr. 27.]
:::

Adverbs of type 2, for example *immer* 'always' [@next a], can also be used as predicative head [@next b], but not as attributive adjustor. The ± 20 adverbs of this type are listed in [@adverbstype2] below. They can mostly not be used as a referential head. However, there are a few adverbs that seem to be quite naturally used in this function, so they might form a special subgroup, specifically *das Hoch* [@next c], *das Nichts* [@next d] and *im Nirgendwo* [@next e]. Other adverbs from this class are also attested as referential heads, but only attested very rarely in rather creative contexts.^[A few additional examples of adverbs type 2 used as referential head are the following: *Nach Spielschluss gab Lehmann ein Interview, das seinen Weg vom Hier und Jetzt **ins Immer** eindrücklich belegte.* (~~DWDS~~: Die Zeit, 06.07.2006, Nr. 28) *Sie kommen aus der Leere, der Abwesenheit, sie langen an **im Nirgends**.* (~~DWDS~~: Die Zeit, 02.10.1997, Nr. 41) *Die Grundbestimmungen Dauer, Einheit, Endzweck geben so dem prozessualen Leitbild nur seinen Gegensatz zum Flüchtigen, zur Vielheit des Chaos, **zum Umsonst** oder Nihilismus, aber sie geben noch keinerlei Entschiedenheit des positiven Inhalts.* (~~DWDS~~: Bloch, Ernst: Das Prinzip Hoffnung Bd. 3, Berlin: Aufbau-Verl. 1956, S. 433) *Bei Gerhard Schröder bezieht sich **das Überall** nicht auf den geographischen Globus.* (~~DWDS~~: Der Tagesspiegel, 22.12.2002) *Als ginge es nicht nur ums Lebenswerk und seine Vollendetheit, sondern um seine Vollendung, anders gesagt: **das Vorbei**.* (~~DWDS~~: Der Tagesspiegel, 03.05.2000).]

::: ex
Syntactic uses of Adverbs type 2

- Adverbial adjustor: *Es kann **immer** schnell vorbei sein.*^[~~DWDS~~: Die Zeit, 18.01.2018, Nr. 01.]
- Predicative head: *Irgendein Wetter ist **immer**.*^[~~DWDS~~: Ulrich Seidler: Frei Luft Theater Fest. Berliner Zeitung, 22.06.2000.]
- Referential head: *Weil **das Hoch** der SPD schon irgendwann einbrechen werde.*^[~~DWDS~~: Die Zeit, 16.03.2017, Nr. 10.]
- Referential head: ***Das Nichts** kennt kein Unglück.*^[~~DWDS~~: Busch, Werner: Das sentimentalische Bild, München: Beck 1993, S. 480.]
- Referential head: *Berlin im Frühjahr, ein Sportplatz **im Nirgendwo** zwischen Berlin und Spandau.*^[~~DWDS~~: Die Zeit, 26.04.2017 (online).]
:::

Adverbs of type 3, for example *bisher* 'up to now' [@next a], can also be used as attributive adjustor [@next b], but not as predicative head ("verbs"). There are about 10 monomorphemic adverbs of this type and some affixes can be used to construct more examples this type of adverbs, as summarized in [@adverbstype3] below. Some of these adverbs are attested as referential heads ("nouns"), but only in rather philosophical contexts [@next c].^[A few additional examples of adverbs type 3 used as referential head are the following: *Im Danach ist auch immer schon **das Demnächst** zu entdecken.* (~~DWDS~~: Die Zeit, 04.10.2007, Nr. 41) *Während er mechanisch nach rechts steuerte, […] sah er in sich das ganze Buch, die Vertiefungen, die Ausblicke, **das Zuvor** und **das Hernach**.* (~~DWDS~~: Feuchtwanger, Lion: Erfolg. Gesammelte Werke in Einzelbänden, Bd. 6, Berlin: Aufbau-Verl. 1930, S. 749) *Überhaupt lernt man hier alles wie **im Nebenbei**.* (~~DWDS~~: Die Zeit, 14.03.2013, Nr. 12) *Ganz **im Nebenher** regelten sich die technischen Dinge.* (~~DWDS~~: Die Zeit, 31.05.1956, Nr. 22) *Ihre Lebensgeschichte hat einen tiefen Einschnitt, der das Vorher **vom Seither** scheidet.* (~~DWDS~~: Die Zeit, 08.08.1997, Nr. 33) *Aber auch **das Zwischendurch** spielt natürlich eine Rolle.* (~~DWDS~~: Blinden-Ensemble probt Konzert im Grünen. Berliner Zeitung, 21.09.1996) *Derzeit führt die stark schwankende Finanzierungskurve für diesen Bereich **ins Abwärts**, während sich die Herzen der Bewilliger bei Anträgen von Ingenieur- und Naturwissenschaftlern weit öffnen.* (~~DWDS~~: Die Zeit, 17.05.1985, Nr. 21) *Peter-Klaus Schuster sucht das Neue gern im Alten, **das Vorwärts im Rückwärts**.* (~~DWDS~~: Die Zeit, 05.10.2000, Nr. 41).]

::: ex
Syntactic uses of Adverbs type 3

- Adverbial adjustor: ***Bisher** hatte er nicht den Eindruck, abgehängt zu sein.*^[~~DWDS~~: Die Zeit, 04.01.2018, Nr. 52.]
- Attributive adjustor: *Die Leistung **bisher** stimmt, das Ergebnis noch nicht.*^[~~DWDS~~: Die Zeit, 28.08.2015 (online).]
- Referential head: *Die meisten reizt schon der leere Unterschied **zum Bisher**, die Frische, gleichviel zunächst, was ihr Inhalt ist.*^[~~DWDS~~: Bloch, Ernst: Das Prinzip Hoffnung Bd. 1, Berlin: Aufbau-Verlag 1954, S. 52.]
:::

Adverbs of type 4, for example *anfangs* 'initially', can only be used adverbially [@next a]. The about 30 monomorphemic adverbs of this type are listed in [@adverbstype4] below. A referential use seems to be possible for *darum* [@next b], *warum* [@next c] and *wie* [@next d].^[A few additional examples of adverbs type 4 used as referential head are the following: *Es ist das Ungenossene, das diese große Kolportage von Musik füllt; das Noch-Nicht, ja selbst **das Niemals** hat ebenso sein eigentümlichstes Dasein aus den Luftwurzeln des Klangs.* (~~DWDS~~: Bloch, Ernst: Das Prinzip Hoffnung Bd. 3, Berlin: Aufbau-Verl. 1956, S. 152) ***Das Wobei** es die Bewandtnis hat, ist **das Wozu** der Dienlichkeit, **das Wofür** der Verwendbarkeit.* (~~DWDS~~: Heidegger, Martin: Sein und Zeit, Tübingen: Niemeyer 1927, S. 84) ***Das Nirgendwo** ist als postulativ gedacht für **das Wo**, in dem sich die Menschen wirklich befinden.* (~~DWDS~~: Bloch, Ernst: Das Prinzip Hoffnung Bd. 2, Berlin: Aufbau-Verl. 1955, S. 78) *In der ewigen Wiederkehr des Gleichen fällt **das Wohin** mit **dem Woher** zusammen.* (~~DWDS~~: Taubes, Jacob: Abendländische Eschatologie, München: Matthes und Seitz, 1947, S. 11) *Die Urfrage der Apokalyptik ist **das Wann**.* (Taubes, Jacob: Abendländische Eschatologie, München: Matthes und Seitz, 1947, S. 32) *Für Heidegger und Wittgenstein bildet der Normalfall, **das Zunächst und Zumeist**, kurzum, das Konventionelle den Ausgangspunkt ihrer Überlegungen.* (~~DWDS~~: Die Zeit, 31.01.2002, Nr. 06).]

::: ex
Syntactic uses of Adverbs type 4

- Adverbial adjustor: ***Anfangs** haben wir uns gestritten.*^[~~DWDS~~: Die Zeit, 15.12.2017, Nr. 52.]
- Referential head: *Die Antwort, **das Darum**, fällt ziemlich trocken aus.*^[~~DWDS~~: Ulrich Seidler: Pamphlete gegen Tatsachen. Berliner Zeitung, 06.09.2001.]
- Referential head: *[…], wobei er sich allerdings um **das Warum** keine Gedanken macht.*^[~~DWDS~~: Schmidt-Rogge, Carl H.: Dein Kind &#x96; Dein Partner, München: List 1973 [1969], S. 339.]
- Referential head: *Nicht das Ob, sondern **das Wie** ist hier das Entscheidende.*^[~~DWDS~~: Kurz, Robert: Schwarzbuch Kapitalismus, Frankfurt a. M.: Eichborn 1999, S. 270.]
:::

Finally, there is a large group of ingredients that can be used adverbially, but these ingredients themselves cannot be further modified at all. All the previously discussed adverbs (type 1 through 4) can themselves be further modified, for example *seit gestern* 'since yesterday', *fast immer* 'almost always', *schon bisher* 'already up to now' or *gleich anfangs* 'immediately at the start'. 

In contrast, adverbs like *außerdem* 'besides', *durchaus* 'quite' or *dauernd* 'constantly' and all others listed below in [@adverbstype5] do not allow for such modification. There is a strong correspondence between these non-modifiable adverbs and the class of adverbs traditionally called *Konjunktionaladverb*. Consequently, I will use this name for this class of adverbs. However, it is important to realize that the definition of this class is not based on the semantic notion of conjunction at all. It is based on the syntactic phenomenon that they are not modifiable. 

By the current definitions, ingredients that cannot be modified are called operators and not bases. So, strictly speaking this class of ingredients belongs to the operators that will be discussed later in this chapter. However, atypically for operators, the adverbs as listed in [@adverbstype5] are positionally flexible in that a speaker can position them in various places in a sentence, including at the start (i.e. in the *Vorfeld*). In this syntactic aspect they are similar to the previously discussed adverbs and different from adverbial operators like *nämlich* or *sehr* and modal particles like *bloß* or *doch* that cannot occur as the *Vorfeld* of a sentence (see ???).

Concluding, the five different classes of adverbs are summarized in [@adverbstype1] through [@adverbstype5].

::: {.ex #adverbstype1}
Adverbs type 1: **referential, predicative, attributive & adverbial** uses

- Local meaning: *hier, da, dort, drüben, außen, draußen, innen, drinnen, oben, unten, hinten, vorn(e), links, rechts, mittendrin, nebenan, unterwegs, zuhause, zurück*
- Temporal meaning: *vorgestern, gestern, heute, morgen, übermorgen, damals, jetzt, vorher, nachher*
- Modal meaning: *allein(e), zusammen*
- Prepositions with the prefix *da‑*, e.g. *davor, darunter, dahinter*, etc.
:::

::: {.ex #adverbstype2}
Adverbs type 2: **predicative & adverbial** uses

- Local meaning: *hoch, nirgends, nirgendwo, überall*
- Temporal meaning: *bald, demnächst, immer, nie*
- Modal meaning: *anders, barfuß, besonders, genauso, nichts, so, soweit, umsonst, vergebens*
:::

::: {.ex #adverbstype3}
Adverbs type 3: **attributive & adverbial** uses

- Local meaning: *dahin, dorthin*
- Temporal meaning: *bisher, hernach, hinterher, jüngst, nebenbei, nebenher, seitdem, seither, zuvor, zwischendurch*
- Prepositions with the prefix *hier‑*, e.g. *hiervor, hierunter, hierhinter*, etc.
- Prepositions and local nouns with the suffix *‑wärts*, e.g. *abwärts, aufwärts, auswärts, heimwärts, rückwärts, seitwärts, vorwärts*, etc.
- Temporal nouns with the suffix *‑s* (except *anfangs, eingangs*), e.g. *morgens, vormittags, mittags, nachmittags, abends, nachts, montags, dienstags, mittwochs, donnerstags, freitags, samstags, sonntags, vortags*, etc.
:::

::: {.ex #adverbstype4}
Adverbs type 4: **only adverbial** uses

- Local meaning: *halbwegs, nirgendwo, wo, woher, wohin*
- Temporal meaning: *anfangs, dann, eingangs, gleich, längst, manchmal, nie mehr, niemals, oft, von vornherein, vorab, wann, weiterhin, wieder, zuerst, zuletzt*
- Modal meaning: *darum, deshalb, deswegen, eher, gern(e), insofern, insoweit, mehrmals, sofort, soviel, warum, wie, wobei, wofür, wozu, zumeist, zunächst*
- Nouns with the modal suffix *‑weise* (except *beispielsweise, beziehungsweise*), e.g. *abschnittsweise, ausnahmsweise, monatsweise, schrittweise, tröpfchenweise*, etc.
- Numerals with the modal suffix *‑mal*, e.g. *einmal, zweimal, dreimal*, etc.
:::

::: {.ex #adverbstype5}
**Non-modifiable** adverbs with **only adverbial** uses (*Konjunktionaladverb*)

- Temporal meaning: *alsbald, alsdann, bislang, daraufhin, dauernd, derweilen, eben, einstweilen, fast, gerade, inzwischen, mittlerweile, nun, schließlich, schon*
- Modal meaning: *allemal, allerdings, also, andernteils, ansonsten, auch, außerdem, beinahe, beispielsweise, bereits, beziehungsweise, bloß, dahingegen, darüber hinaus, dementgegen, demgegenüber, demgemäß, demnach, demzufolge, dennoch, derart, dermaßen, desgleichen, durchaus, einigermaßen, ferner, folglich, freilich, geradewegs, gleichwohl, hingegen, hinwiederum, im Übrigen, immerhin, indes, insbesondere, jedoch, kaum, keineswegs, lediglich, maximal, minimal, mithin, nichtsdestotrotz, nichtsdestoweniger, nunmehr, obendrein, ohnedies, ohnehin, sodann, somit, sonst, sowieso, trotzdem, überdies, überhaupt, vielleicht, vielmehr, vor allem, wiederum, wohlgemerkt, zudem, zuguterletzt, zumal, zumindest, zwar*
- Prepositions with the suffix *‑dessen*, e.g. *indessen, infolgedessen, stattdessen, unterdessen, währenddessen*, etc.
- Superlatives and ordinals with the suffix *‑ns*, e.g. *bestens, frühestens, genauestens, höchstens, meistens, mindestens, schnellstens, spätestens, strengstens, wenigstens, erstens, zweitens, drittens*, etc.
- Stems with the suffix *‑falls*, e.g. *allenfalls, anderenfalls, bestenfalls, ebenfalls, gegebenenfalls, gleichfalls, keinesfalls*, etc.
- Stems with the suffix *‑mals* (except *damals, mehrmals*), e.g. *abermals, ehemals, nochmals, oftmals, vormals, vielmals*, etc.
- Stems with the suffix *‑lings*, e.g. *blindlings, seitlings, rücklings*, etc.
- Stems with the suffix *‑erseits*, e.g. *andererseits, deinerseits, einerseits, meinerseits, väterlicherseits, staatlicherseits*, etc.
:::

There are still a few ingredients that need special attention. First, the double prepositions *voran, voraus, vorbei, vorüber* are often listed as adverbs, but they cannot be used as adverbial adjustors at all and will thus not be classified as adverbs here. They can be used as preverbials in compound verbs, like in *voranlaufen, vorauslaufen, vorbeilaufen* and *vorüberlaufen*. Also, except for *voran*, they can be used as predicative heads, like in *es ist vorbei/vorüber* and *er ist den anderen voraus*. Finally, *voran* can be used (although somewhat old-fashioned) as a postposition governing a dative case, like *dem Festzug voran*. Yet, these four ingredients *voran, voraus, vorbei, vorüber* cannot be used as an adverbial modifier and are consequently not adverbs. This is notably different from *vorab*, which is an adverb type 4 as listed in [@adverbstype4].

Second, most dictionaries of German categorize the ingredients *nahezu, nämlich, schier, sehr, sogar, überaus* and *weitaus* as adverbs.^[No attempt is made to propose English translations for these ingredients, because a faithful translation for them is extremely context-dependent.] They can indeed be used adverbially without being modifiable themselves, like the adverbs listed in [@adverbstype4]. However, they are not very frequent in this adverbial usage. They occur much more frequently in narrow-scope modification, like *schier unmöglich* 'practically impossible' or *weitaus größer* 'much larger'. Crucially, they are syntactically special in that they cannot be used as the sole content of the first position of the sentence, i.e. as the *Vorfeld*. This makes them different from all adverbs discussed in this section. They are not classified as adverbs here, but as non-initial particles (see ???).

*Numerale*

The class of *Numerale* (numerals) is arguably a subclass of adjectives, but it has various different syntactic characteristics that warrant a separate class. First note that numerals are actually bases (and not operators), because they can be modified [@next a]. Also note that numerals are typically ordered at the start of a chain of attributive modifiers, but it is also possible for them to occur after other attributes in the noun phrase [@next b].

::: ex
- Modifiable: *Aber der Nobelpreis lässt eben nur **maximal drei** Preisträger zu.*^[~~DWDS~~: Die Zeit, 03.10.2017 (online).]
- Variable ordering: *Die **anderen drei Topstars** dagegen enttäuschten bislang.*^[~~DWDS~~: Die Zeit, 28.10.2016 (online).]
:::

Numerals can be used as attributive adjustor [@next a] and as referential head [@next b]. In both uses the numeral does not have any inflection. A numeral can be used as an adverbial adjustor with the suffix *-mal* [@next c]. Numerals can only be used as a predicative head with a copula in very specific contexts, namely to express a mathematical result [@next c], to express age [@next d] or in some proverbs [@next e].

::: ex
Syntactic uses of a *Numerale* in German

- Attributive adjustor: *Die **drei** Kandidaten traten gegeneinander an.*^[~~DWDS~~: Die Zeit, 22.11.2017 (online).]
- Referential head: *Die **drei** grummelten vor sich hin.*^[~~DWDS~~: Jentzsch, Kerstin: Seit die Götter ratlos sind, München: Heyne 1999 [1994], S. 257.]
- Adverbial adjustor: *Ich klopfe **dreimal**.*^[~~DWDS~~: Die Zeit, 08.01.2018, Nr. 02.]
- Mathematic result: *Eins plus eins ist **drei**.*^[~~DWDS~~: Der Tagesspiegel, 11.03.2004.]
- Age indication: *Maxi, die Jüngste, ist **drei**.*^[~~DWDS~~: Die Zeit, 07.11.2007, Nr. 46.]
- Proverb: *Aller guten Dinge sind **drei**.*
:::

Derived from numerals are *Ordinalzahlen* (ordinals) with the suffix *‑te* and *Bruchzahlen* (fractions) with the suffix *-tel*. Ordinals [@next] have a different syntax from numerals [@last]. Ordinals in attributive function have agreement [@next a] and ordinals in predicative function are only used for results of a competition [@next c]. Ordinals are not possible in adverbial function. To express such meanings a complete noun phrase has to be used, like *zum dritten Mal*.

::: ex
Syntactic uses of *Ordinalzahlen* in German

- Attributive adjustor: *Wir müssen uns mit dem **dritten** Geschlecht befassen.*^[~~DWDS~~: Die Zeit, 24.11.2017, Nr. 48.]
- Referential head: *Die **dritte** erzählt von Flucht und Immigration.*^[~~DWDS~~: Die Zeit, 27.04.2017 (online).]
- Rank in sports: *Die deutschen Fußballdamen wurden **dritte**.*^[~~DWDS~~: Die Zeit, 23.06.1995, Nr. 26.]
:::

In contrast, *Bruchzahlen* (fractions) have yet again different syntactic possibilities. They are neuter nouns in referential use [@next a] and can be used as verbs without copula [@next b]. Fractions cannot be used attributively nor adverbially and are consequently considered to be nouns in German, written with an initial capital.

::: ex
Syntactic uses of *Bruchzahlen* in German

- Referential head: *Ein **Drittel** aller verbliebenen Clubs kommen von der Insel.*^[~~DWDS~~: Die Zeit, 04.01.2018, Nr. 52.]
- Predicative head: *Seit Juli hat sich der Wert der Aktie fast **gedrittelt**.*^[~~DWDS~~: Berliner Zeitung, 07.09.2001.]
:::

There is a strange quirk in German orthography to write numerals with an initial lowercase even when they are used as a referential head, e.g. *diese drei flüchteten* 'those three fled', while writing *Million* (and other *‑llion* numerals) always with a capital, even when they are used as an attributive adjustor, e.g. *die Millionen Menschen* 'the million dollar'. The actual practice is a bit less stringent than these official prescriptive rules. A quick search in the DWDS corpus suggests a 10‑to‑1 preference for lower case with small numerals like *drei* or ordinals like *dritte* when used as a referential head ("noun").^[The search "die \@drei $p=VVFIN" gave 991 hits, while the Search "die \@Drei $p=VVFIN" gave 92 hits. Similarly, "die \@dritte $p=VVFIN" resulted in 1490 hits while "die \@Dritte $p=VVFIN" gave 228 hits. All searches were performed on <https://www.dwds.de/r/> on 1st December 2023 using the *Referenz- und Zeitungskorpora*.]

::: ex
German monomorphic numerals

- Numerals: *null, eins, zwei, drei, vier, fünf, sechs, sieb(en), acht, neun, zehn, hundert, tausend, Million*^[There exist more names for larger numerals, e.g. *Billion, Trillion*, that are backformations based on a folk etymology of *Million* having a suffix *‑llion* (the real etymology is from Italian *mille-on* 'thousand-large').]
- Suppletive numerals: *elf ("eins‑zehn"), zwölf ("zwei‑zehn"), zwanzig ("zwei‑zig")*
- Suppletive ordinals: *erste ("eins‑te")* 
- Suppletive fractions: *halb ("zwei‑tel"), drittel ("drei‑tel")*
:::

## Junctors

phrasal: both attributive and adverbial (and argument!)
clausal: only adverbial. Attributive clauses do not have junctor

head-specific roles (marked by case)! also: phrase: *Behälter* (genitive), clause *Mensuralergänzung* (accusative)

::: ex
Phrasal junctors 

- Prepositions governing dative: *ab, aus, außer, bei, entgegen, entsprechend, gegenüber, gemäß, mit, nach, nahe, seit, von, zu*
- Prepositions governing accusative: *bis, durch, entlang, für, gegen, ohne, um*
- Prepositions governing dative or accusative: *an, auf, hinter, in, neben, über, unter, vor, zwischen*
- Prepositions governing genitive: *abseits, abzüglich, angesichts, anfangs, anhand, anstatt, außerhalb, aufgrund, bar, bezüglich, dank, diesseits, eingangs, einschließlich, entlang, infolge, innerhalb, inmitten, jenseits, kraft, längs, laut, links, mittels, ob, oberhalb, rechts, seitens, statt, trotz, ungeachtet, unterhalb, unweit, während, wegen, zugunsten*
- Postpositions governing dative: *gegenüber, nach, voran, zufolge*
- Postpositions governing accusative: *durch, entlang, hoch, über*
- Postpositions governing genitive: *halber, wegen* 
:::

:::
Clausal junctors

- Temporal: *als, bevor, bis, ehe, nachdem, seit, seitdem, sobald, solange, während, wenn*
- Modal: *als ob, da, damit, falls, indem, insofern, insoweit, obgleich, obschon, obwohl, obzwar, sofern, sooft, sosehr, soviel, soweit, sowie, weil, wenngleich, wie, wo*
- Prepositional: *anstatt, außer, ohne, statt, um*
- Participial: *angenommen, ausgenommen, gegeben, gesetzt, ungeachtet, unterstellt, vorausgesetzt*
:::

some both conjunction and subjunction: doch, weil, vorausgesetzt
double: mal-mal, entweder/oder, sowohl/als-wie-auch, wenn/dann, weder/noch, nichtnur/sondernauch

::: ex
Conjunctions

*aber, denn, doch, noch, oder, sondern, sowie, und, und zwar*
:::

## Specifiers 

Limiters

Quantors, Abtönungspartikel, Konjunktionaladverben, Epithesis/Diathesis, etc.

multiple specifiers	
Rede von Wolfgang Clement, 14.01.2003
Manch einer sagt, es wehe ganz schön viel energiepolitischer Wind aus Brüssel,

Attributspezifikation ("Gradpartikel")

Gradadjektiv: absolut, annähernd, arg, ausgesprochen, außergewöhnlich, außerordentlich, äußerst, echt, eklatant, enorm, entsetzlich, erbärmlich, extrem, furchtbar, ganz, hochgradig, höchst, irre, komplett, recht, regelrecht, relativ, restlos, richtig, schrecklich, schön, tierisch, total, traumhaft, ungemein, ungeheuerlich, ungewöhnlich, unglaublich, unheimlich, unwahrscheinlich, übermäßig, verhältnismäßig, verschwindend, vollkommen, völlig, weit, weitgehend, wahnsinnig, ziemlich, maximal, minimal, mindestens, ungefähr
Gradadverb: beinahe, besonders, dermaßen, derart, durchaus, eher, einigermaßen, etwas, fast, kaum, so, spätestens, vergleichsweise, zumindest
Gradpartikel: nahezu, nur, schier, sehr, sogar, überaus, weitaus, zu, nicht

Referenzspezifikation ("Fokuspartikel")

FokusAdjektiv: ausgerechnet, einzig, erst
FokusAdverb: allein, allenfalls, bereits, besonders, bestenfalls, bloß, gerade, mindestens, lediglich, schon, spätestens, vor allem, wenigstens
Fokuspartikel: auch, sogar, nur, selbst, nicht

Adverbialspezifikation ("Grenzpartikel", "Adverbialpartikel")

Grenzpräposition = von, nach, seit, ab, bis, für

Präpositionsspezifikation = dicht, direkt, eng, genau, gerade, gleich, hoch, knapp, kurz, lang, leicht, nah, schräg, tief, weit, östlich, seitlich, ungefähr, unmittelbar, spätestens

AusmaßAdjektiv = direkt, genau, ganz, gleich, häufig, kurz, lange, unmittelbar, viel, völlig, weit, ziemlich
AusmaßAdverb = bald, beinahe, etwas, fast, gerade, immer, schon, spätestens
AusmaßPartikel: auch, eben, mal, nur, wohl, nicht, sogar

Ausmaß: allein, auch, ausgerechnet, bald, beinahe, bereits, besonders, bisher, bloß, da, deutlich, dort, eben, ebenfalls, eigens, einzig, erst, etwa, etwas, fast, ganz, gar, genau, gerade, gestern, gleich, heute, hier, hinten, immer, irgendwann, irgendwo, kaum, knapp, lange, lediglich, links, nahezu, nie, noch, nur, oben, rechts, schon, sehr, selbst, so, spätestens, überhaupt, ungefähr, unten, vorn, vorne, weiter, wenigstens, wieder, wohl, zeimlich, zumindest, zumindestens

Prädikationspezifikation ("Post-vorfeldpartikel", "Non-vorfeldpartikel")

Post-vorfeldAdverb = allerdings, also, andererseits, andernteils, beispielsweise, freilich, hingegen, hinwiederum, immerhin, indes, indessen, insbesondere, jedoch, mittlerweile, schließlich, schon, sonst, stattdessen, überhaupt, unterdessen, währenddessen, wiederum, wenigstens, zumindest, zwar
Post-vorfeldPartikel: auch, nur, nämlich

Adjektiv: bloß, eben, gar, rein
Adverb: auch, bloß, eben
Konjunktion: aber, denn, doch, noch
(Abtönungspartikel, Modalpartikel)

Non-Vorfeldpartikel: *aber, auch, bloß, denn, doch, eben, eh, etwa, gar, halt, ja, mal, nicht, noch, nur, rein, schon, wohl*

*eben, eh (~ehe!), etwa, gar, halt, ja, mal, nicht*

*nahezu, nämlich, schier, sehr, sogar, überaus, weitaus*

Second, the ingredients *nämlich* and *sogar* are similar to the non-modifiable adverbs as listed in [@adverbstype5]. When used adverbially, they can be placed rather freely in the sentence, depending on the intended meaning [@next a,b]. However, different from all adverbs discussed in this section, *nämlich* and *sogar* cannot occur as first element of the sentence, i.e. as *Vorfeld* [@next c,d]. This makes them somewhat similar to ingredients that are commonly called *Modalpartikel* in the German grammatical tradition. For this reason, the ingredients *nämlich* and *sogar* are not classified here as adverbs, but as "non-initial sentence operators" (see ???).

::: ex
- *Auf persönlicher Ebene ist **(nämlich)** in Deutschland **(nämlich)** von German Angst **nämlich** wenig zu spüren.*^[~~DWDS~~: Die Zeit, 31.12.2017 (online).]
- *Dänemark plant **(sogar)** feste Kontrollposten **sogar** im nächsten Haushalt ein.*^[~~DWDS~~: Die Zeit, 01.01.2018 (online).]
- ^* ***Nämlich** ist auf persönlicher Ebene in Deutschland von German Angst wenig zu spüren.*
- ^* ***Sogar** plant Dänemark feste Kontrollposten im nächsten Haushalt ein.*
:::

A few of these non-modifiable adverbs need special attention, namely *nahezu, schier, sehr, überaus* and *weitaus*.^[No attempt is made to propose English translations for these ingredients, because a faithful translation for them is extremely context-dependent.] They can indeed be used adverbially, but they are extremely restricted and not very common in adverbial usage. As will be discussed in (???), they have other uses in which they occur much more frequently. As sentence adverbials they only occur with a very small set of main verbs.

The adverbs *nahezu* and *schier* are mainly used with a gloomy connotation: *schier* is typically used in combination with verbs like *ersticken, verhungern, verzweifeln* or *erschlagen* [@next a], while *nahezu* typically is attested in collocations with verbs like *ausbremsen, erblinden, vernichten* or *ausschließen* [@next b]. In contrast, the adverbs *sehr, überaus* and *weitaus* are typically used with a much more positive connotation.

nahezu vernichten, erblinden, schaffen, ausschließen, ausrotten, ausschöpfen, positiv: verdoppeln
schier ersticken, verhungern, verzweifeln, positiv: 
sehr lieben, freuen, schätzen
überaus genießen, schätzen, verehren, lieben
weitaus übertreffen, überwiegen, überragen

::: ex
- *Und dass Florenz so viel zu bieten hat, dass einen die Masse **schier** erschlägt.*^[~~DWDS~~: Die Zeit, 21.11.2013 (online).]
- *"Über 50 Meter kann immer alles passieren", sagte Steffen, die ein zweites WM-Gold sogar **nahezu** ausschloss.^[~~DWDS~~: Die Zeit, 15.12.2012 (online).]
:::

*schier* also attributively: schiere Masse, schiere Überlastung, etc.

## Stems used in multiple classes

- Nomen/Verb (very many!)
- Nomen/Adjektiv (only ~10?): *das Deutsch/deutsch, das Doppel/doppelt, das Fett/fett, der Gram/gram, der Greis/greis, der Laut/laut, das Leck/leck, das Licht/licht, das Recht/recht, der Schmuch/schmuck, der Tot/tot, das Wild/wild*
- Verb/Adjektiv (219 out of 300 adjectives): 
- Numerale/Adjektiv: *hundert, tausend, Million* ('very many')
- Numeral/Nomen: *Million* ('one million in monetary value')
- Adverb/Nomen: *morgen/Morgen* ('tomorrow/morning')

Die Zeit, 23.02.2016 (online) 
Ab März dürfen die hunderte [tausende/Millionen] Jahre alten Bauwerke nicht mehr bestiegen werden.
Der Tagesspiegel, 28.05.1997 
Die Million kommt von diversen Sponsoren.

# Clause structure

# Phrase structure

# Context and indexing

do these really belong together?

# Old text

## Expressing the syntactic model

The syntactic model is turned into YAST-instructions as follows. Each base is a content lexeme that makes up a single instruction (i.e. a single line in the YAST-format as in the earlier example, repeated below). layering and embedding are specified by indenting of the instructions. The difference between redoubling and embedding is not explicitly specified. However, embedding typically can have further modifications and their relation to the superordinate base can be specified with a linkage (before the colon). Syntactically, each linkage is an operator. All other operators are added in brackets after the base lexeme.

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



'gestern' as noun?

Rückert, Friedrich: Die Weisheit des Brahmanen. Bd. 4. Leipzig, 1838. 
Das Gestern fraß der Fehl, soll fressen Reu das Heute?

Tieck, Ludwig: Phantasus. Bd. 1. Berlin, 1812. 
Der gestern glühte In aller Pracht, Denn er verblühte In dunkler Nacht.

Der Tagesspiegel, 01.12.2001 
Das Gestern harrt / auf ein Morgen / auf ein Morgen, das endlos weiterrückt.



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

The order of instructions in a recipe is to a large extend "free". The speaker is allowed to specify the instructions in any order in accordance with the intended message (within certain language-specific limits to be worked out later in detail). As an result, the rules will sometimes have to work around the instructions to mould the result in accordance to the structure of the language. A proficient speaker with much experience can take the expected output into account in building the instructions.


## Komplemente? Implizite Adverbialsätze ???

*wir haben viel zu besprechen*
*wir haben so viel zu besprechen, dass (???) wir noch länger bleiben müssen*
*wir haben so viel zu besprechen (und die Folge ist), dass wir ...*

reverse? *wir müssen länger bleiben, weil wir so viel zu besprechen haben*

*wir besprechen die neue Situation*
*wir besprechen, dass es schneller gehen muss*
*wir besprechen so viel, dass es mir schwindelt* => mir schwindelt weil wir so viel besprechen.