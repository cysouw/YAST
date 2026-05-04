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

**Language-specific model.** The majority of the rules and structures in YAST are language-specific. There are only very few principles proposed that hold for human language in general. By being language-specific, the current approach remains relatively close to traditional notions of grammatical description (although in this first chapter that might not look like that at all). Differently from traditional grammars, YAST includes a generative implementation (which traditional grammars typically lack). However, the "ingredients" that drive generation closely resemble the rules and regularities described in traditional grammars. Traditional grammatical descriptions require only minor adjustments to allow for this kind of computational implementation. This approach also ensures that the formalized model remains easily comprehensible to non-technically minded linguists.

**Minimal universal assumptions.** Because most grammatical structures arise from language-specific choices, YAST assumes only a very limited set of universal morphosyntactic principles. Observations of recurrent grammatical properties ("statistical universals") are better modeled through semantic-map approaches that describe cross-linguistic differences and similarities as language-specific discrete divisions of an underlying continuous semantic space, which itself is probably universal.

**Content-then-structure.** The generative process of YAST employs concrete morphemes from a specific language rather than abstract categories. This contrasts with the predominant approach in the syntactic literature of first generating an abstract structure and only later inserting lexical elements. In YAST, generation begins by selecting language-specific morphemes for insertion. Each such choice triggers structural repercussions that collectively establish the abstract morphosyntactic structure. Rather than "structure-then-content," YAST follows a "content-then-structure" generative process.

**Two-way generative model.** The current approach distinguishes two types of generative operations, namely (i) predominantly "free" lexical insertion, with only some grammatical restrictions resulting from the inserted lexemes, and (ii) completely automatic formal rules of language structure. This twofold distinction is useful for linguistic comparison and may benefit didactic approaches to language structure. The grammatical restrictions from (i) and the rules of (ii) typically appear in descriptive grammars, while the lexical inserations from (i) are better handled by probabilistic models like large language models.

**Dual structural representation.** lexical insertions and their repercussions (i.e. generation type (i) from above) generate a dependency-like "underlying" structure. Subsequently, mandatory rules (i.e. generation type (ii) from above) then "transform" this morphosyntactic structure into a linear utterance through an intermediate constituency-like representation. This might appear like a variant of an early "transformation generative grammar", but the details are quite different. In grammatical analysis (that is, when working backwards from actual utterances) the constituency structure thus represents a level of abstraction closer to the surface structure than the dependency structure. The dependency structure constitutes an underlyingly more abstract analytical representation of utterances.

**Immediate output.** An utterance does not have to be fully prepared before the actual production ("speaking") can begin. As soon as some parts of the underlying dependency structure are generated, the utterance can be started. Only in some limited situations will it be necessary to shortly delay the actual utterance of chosen content. YAST might thus be an interesting model for language production, although the details proposed here are simply a structuralist analysis, not the result of actual production research.

**Parsing by mirroring.** When confronted with a linguistic utterance, the parser ("hearer") does not "reverse engineer" the structure of an utterance, but attempts to mirror the underlying structure by guessing and constantly checking whether the assumed structure results in the observed utterance by mirroring the production process internally.

**Rule-defined word classes.** Classes of morphemes ("parts of speech") in YAST only exist as secondary phenomena based on their morphosyntactic characteristics. Each grammatical structure defines its own class of applicable morphemes. This approach has two key effects, namely (a) languages exhibit numerous overlapping word classes, with most morphemes belonging simultaneously to multiple classes, and (b) no singular atomic classification exists to which each morpheme can be uniquely assigned, that is, no set of mutually exclusive classes can serve as the basis for grammatical rules. Rather than "word classes determine the application of rules," YAST asserts that "rules define word classes."

[--
A generative potentially-probabilistic traditional-like templatic (GP^2^T^2^) model for human language
--]::

## Synopsis of the model

### Recipe-rule-result-receipt

In its most basic sense, YAST is a generative model for sentence structures. It starts from a set of ~~instructions~~ that, when fed into the morphosyntactic ~~rules~~, lead to an ~~result~~, i.e. a sequence of pronounceable linguistic elements. The instructions are language-specific, i.e. the instructions to make a German sentence consist of German elements. The basic guideline determining what should appear in the instructions is the notion of predictability: all parts of an actual utterance that can be predicted are added by the rules, only the non-predictable elements remain for the instructions. So, the research, that is needed to write morphosyntactic YAST-rules for a specific language, is to decide which parts of the utterance are predictable and which are non-predictable.

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
  There are three different types of instructions distinguished, which will be called ~~phrase~~, ~~clause~~ and ~~admodifier~~. The type of an instruction can mostly be inferred from the specification, but sometimes has to be explicitly indicated.
- **Junction** \
  Junctions express the relation of the instruction to earlier content. Such explicit relational ingredients are called ~~junctors~~. This part of the instruction can be empty for default ("unmarked") modification.
- **Nucleus** \
  The obligatory nucleaus of each instructions is a single base content lexeme. For phrases and clauses the nucleus is called a ~~head~~.
- **Specification** \
  Depending on the type of instruction, language-specific grammatical marking can be added. Such ingredients are called ~~specifiers~~. This part of the instruction can be empty for default ("unmarked") morphosyntax. 
:::

The information in an instruction purely consists of language-specific forms (except modification). The morphosyntactic structure of the eventual utterance is produced by the (automatic) rules from this information. The underlying principle used here is that the most precise and straightforward method to specify meaning in a recipe is to use language-specific elements. So, in YAST, a user of a specific language is juggling with the available language-specific elements to construct an utterance, instead of manipulating abstract linguistic concepts.

As an example, consider the German sentence in [@next] as an appetizer. This German sentence is generated by the instructions in [@nnext], using the grammatical rules as will be laid out in the rest of this book. The instructions in [@nnext] can be seen as the intention of the speaker, with indentation marking modification. These instructions seem suitable for a semantic analysis, though this aspect of the model will have to be worked out another time in more detail. Note that the specifications (in brackets) are intentionally formulated with language-specific morphosyntactic terminology, so their semantic interpretation will be language-specific as well. Any comprehensive cross-linguistic generalization over such language-specific elements is a separate (though highly important) endeavor, which will not be pursued here.

::: ex
Die Männer, deren kleinen Kinder schlecht schlafen, habe ich gestern in deinem schönen Garten gesehen.
:::

::: {.ex noFormat=true}
```
sehen (Perfekt)
  Gesehene: Mann (Plural + Definit)
    schlafen
      Schlafende: Kind (Plural)
        Behälter: Mann
        klein
      schlecht
  Sehende: 1
  gestern
  in: Garten (Definit)
    Behälter: 2
    schön
```
:::

Each line in [@last] is a single instruction with hierarchical indentation, possibly consisting of up to three different kinds of elements. Anything before the colon is an explicit ~~junctor~~ that marks the relation to the superordinate instruction. This is either a lexical role, an adposition or a subjunction/conjunction. When there is no colon, then the junction is assumed to be default modification. After the linkage follows the main lexical ~~nucleus~~. This is typically a German lexeme, though there are a few abstract abbreviations used, like '1' for the speaker. The actual lexemes are included in the instructions because the language-specific lexemes are the best summary of their meaning. 

After the nucleus follows a list with explicit grammatical ~~specifications~~ (between brackets). When there are no grammatical specifications the rules will infer a default ("unmarked") grammatical structure. Multiple grammatical specifications are separated with a plus-sign, and their order is relevant in some situations. Specifications are often grammatical terms like *Plural* because of their highly allomorphic formation, like in the case of the German plural. However, these specifications are always abbreviations for language-specific forms and do not describe universal grammatical categories.

The ~~type~~ of the instruction is not explicitly shown in the example of a recipe in [@last]. Technically speaking, each line should be marked as being a phrase, clause or admodifier. However, it turns out that for German the type of the large majority of instructions can be inferred from the specifications. In practice, the capitalisation of the nucleus is used as an indicator, which is useful for instructions without explicit specifiers.

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

The ephemeral role of the constituent-like receipt is also reflected in the workings of the ~~parser~~. The parser does not attempt to reconstruct the constituent tree from the receipt, but immediately (after observing each pronounced element) tries to reconstruct the underlying dependency-like instructions of the recipe. In the current implementation, various different instructions are attempted within the range of possibilities as constrained by the actual utterance. Each attempt is fed into the rules until the actually observed utterance is replicated. The YAST-parser is thus actually a predictor that constantly tries to reconstruct the instructions (as intended by the generator) by performing generation of a recipe in parallel and checking the results of these mirrored generation with the observed utterance. The parser mostly does not have to wait until an utterance is finished, but can already start predicting while the utterance is still ongoing. This aspect of YAST seems to be a very fruitful approach for modeling language processing. 

![Basic workflow of YAST](figures/basis){#fig:basis}

### Formal complexity

Before delving into the details of this syntactic model, a few words on the algorithmic complexity of this model are in order. This topic needs more in-depth investigation, but my initial impressions are as follows:

- Each instruction in the recipe can be generated with a simple regular language, i.e. a type-3 grammar.
- The recipe consists of a set of hierarchically ordered instructions, which can be modeled with a context-free language, i.e. a type-2 grammar.
- The rules differ in their complexity. Most operators are simple insertions with some reformatting, which are regular, i.e. captured by a type-3 grammar.
- Each insertion of a templatic constituent structure, with possibly multiple slots to be filled, are context-free, i.e. they form a type-2 grammar.
- Finally, the rules that are defined as "diathesis/valency alternation" in Cysouw (2023), including for example the passive, are exactly the rules that need multiple joint insertions and revisions of earlier insertions, so these are mildly-context-sensitive, i.e. they fall in between a type-2 and a type-1 grammar. It seems to be the case that it is this part, and only this part, of the morphosyntax that is more complex than context-free.
- The parsing needs more work, but it consist of reconstructing a dependency-like structure from an utterance, which does not appear to be highly complex, possibly just regular, i.e. a type-3 grammar.

## Postulates for morphosyntax {#sec:postulates}

A small set of concepts are proposed here as universal postulates for the structural analysis of morphosyntax. These postulates are no requisite for the morphosyntactic model proposed in this book. Rather, they represent an attempt to explicitly articulate the basic assumptions underlying YAST and to propose principles that may prove useful for investigating the nature of human language and its evolution. Even if these postulates ultimately might prove unconvincing, this does not affect the subsequent practical operations of the YAST morphosyntactic model.

These notions are termed "postulates" because they exhibit three key properties: they are (i) axiomatic, (ii) presumed, and (iii) cancelable. First, they are axiomatic in that they establish a foundation for morphosyntax from which other characteristics can be derived. Second, they are presumed, that is, they constitute "obvious" components of human language structure and are assumed to exist without extensive argumentation. Third, they are cancelable, meaning they need not necessarily form part of any communicational system. Human languages could conceivably exist without any of these characteristics. Thus, none of these postulates claim strict universality, if only because they must have emerged at some point during the evolution of human language. Nevertheless, the following characteristics appear widespread among human languages and are arguably present universally in contemporary human languages.

- (P1) **Morphemic division** \
  Utterances are separable into morphemes.
- (P2) **Hierarchical modification** \
  Morphemes modify other morphemes, and modifiers in turn can be modified.
- (P3) **Differential modification** \
  Morphemes have constraints on how they can be modified.
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

These postulates describe general principles that lead to very different grammatical structures in different languages. So, as general principles they appear to be universally present, but the concrete instantiation is widely variable. The capricious process of grammaticalisation (P8) and innovation (P9) is the root cause for the accumulation of differences in structure between languages.

The notion of differential modification (P3) has various immediate ramifications that all appear to be universally attested in human languages. This postulate thus might very well be further subdivided into more specific postulates describing special kinds of constraints on modification, including the following apparently universal phenomena.

- (P3a) **Non-modifiable operators** \
  Some morphemes cannot be further modified.
- (P3b) **Spawned roles** \
  Morphemes can induce morpheme-specific grammatical relations.
- (P3c) **Templatic structure** \
  Grammaticalisation can lead to a fixed linear structure with multiple "slots" that each only allow for a restricted set of "filler" morphemes.
- (P3d) **Probabilistic modifier choice** \
  Each morpheme has different preferences for what kind of modification typically follows. This kind of restrictions seems best modelled by large language models and will not be further pursued here.

As a basic null hypothesis, I assume that semantic space (P7) is a high-dimensional and continuous space, but also a compact, flat and simply connected space (borrowing terms from cosmology here). However, this is just a wild guess. It basically means that the underlying semantic space has no structure. Each individual language imposes a structure on semantic space by the distribution of its linguistic elements over the space. It could very well be the case that recurrent semantic similarities across languages are the result of some kind of structure in the underlying semantic space, thereby refuting this null hypothesis. However, other explanations for semantic universals are also possible, like frequency-of-use and shared historical coincidences. Any argument refuting the hypothesis of an unstructured semantic space will need major cross-linguistic research, far beyond the scope of the current book.

## Elements of a recipe

### Generating a recipe: ingredients

In the syntactic model pursued here, the production of an utterance consists of two stages: first a ~~recipe~~ is created, followed by the application of ~~rules~~. Planning an utterance means to create a recipe for it, and this formation of a recipe is a generative process. This generative process also has some "rules", that is, restrictions on which recipes can be constructed. However, these restrictions are relatively minor, even for a strongly flectional language like German. Other languages might exhibit even less constraints in this regard. The relative freedom to produce recipes reflects the wide leeway speakers have to produce a wide variety of utterances. In extremis, the automatic rules will sometimes have to "work around" the instructions in the recipe to mould the speaker's creative intention in accordance to the structure of the language.

The basic building blocks of a recipe will be called ~~ingredients~~ (in keeping with the cooking metaphor). The existance of ingredients follows from postulate P1 from [@sec:postulates]. Basically, ingredients are morphemes, but they also include fixed grammaticalized combinations of morphemes (like non-compositional idioms) and multi-part grammatical structures (like auxiliary constructions). Semantically, ingredients induce a state-of-mind at the addressee, probably consisting of a multitude of possible situations in accordance to the communally developed practice of using the ingredient (i.e. the ingredient's "meaning"). The act of using an ingredient intends to conjure up some of those possible situations in the mind of the addressee, narrowing down the interpretative possibilities with each further ingredient used.

Restrictions on building a recipe mainly consist of limits on which ingredients can be used in the generation. There will ultimately be two different kinds of restrictions, namely (i) restrictions on lexical insertion of ~~heads~~, which will be minimal, and (ii) restrictions on adding grammatical ~~operators~~, which are strongly determined by any chosen head. To fully describe these limits it will ultimately be necessary to specify individual possibilities separately for each ingredient of a language, because ultimately each ingredient has different distributional constraints and tendencies. In the end, something like a Large Language Model with millions of parameters is necessary to fully describe the distributional detail of a language. However, in this book I will only describe some general patterns with the understanding that these patterns are just a starting point for the subsequent specification of more detail. Ultimately, there is clearly a need for some kind of "grammatical lexicon" that includes the full syntactic detail for each ingredient in humanly readably form (as opposed to the unintelligible black box that is a Large Language Model).

### Combining ingredients: base & modifier

Language extends the usefulness of its ingredients by combining multiple of them into larger utterances. The underlying semantic effect of the combination of ingredients is probably something quite general like intersecting the two sets of possible situations. Uttering an ingredient-combination asks the addressee to search for possible situations that are in accordance with both ingredients. When, at first, the addressee might not be able to find any feasible intersection, this forces a reconsideration of possible interpretations of the ingredients, hopefully eventually leading to some kind of "understanding" on the part of the addressee.

Additionally, a central tenet of human language is that combinations of linguistic elements is in general asymmetrical. Ingredients are not simply combined as equals, but there is always a ~~base~~ that is modified by another linguistic element: the ~~modifier~~. Symmetrical connections with European-style *and*-coordination seem to be a relatively late addition to the grammatical spectrum (and mostly are not really completely symmetrical anyway). For the recipe, I will assume that all combinations of ingredients in human language are asymmetrical, including for grammatical coordination (i.e. in coordination there is always a primary and a secondary member with slightly asymmetric properties).

Bases can have multiple modifiers and each modifier can itself be a base that again can be modified. The existence of such hierarchical modification in human language is proposed as postulate P2 in [@sec:postulates]. So, a recipe is in essence just a complex hierarchical dependency structure. When a base has multiple modifiers, then the ordering of these modifiers is often meaningful, so the ordering will have to be encoded in the recipe. However, in many situations the actual ordering of modifiers is strongly restricted in a language, for example in morphologically bound constructions. Such templatic ordering restrictions are encoded in the rules, not in the recipe. Yet, there are also situation in which the ordering is not completely fixed, but there nevertheless are strong tendencies, for example in the ordering of attributive adjectives in many languages. It is currently unclear how to best encode such tendencies. For now the recipe will simply allow all possible orders, even when there is only minimal possible variation.

### Syntactic elements: head & operator

To streamline the raw intricacy of pure modification, it is helpful to distinguish two different kinds of elements in the hierarchical structure depending on to which extend they can be modified (cf. postulate P3 from [@sec:postulates]). First, when an ingredient cannot itself be modified again, or when it only can have a single modifier from a small set of possible ingredients, then it will be called an ~~operator~~. Second, when an ingredient potentially allows for more than one modifier in parallel, then it will be called a ~~head~~. It is important to note that these terms describe syntactic functions and not specific ingredients. One and the same ingredient might be both a head and an operator, depending on the context in which it is used.

Typically, operators are bound morphemes, but there are many other non-bound linguistic elements that are operators under the current definition (namely, that they cannot themselves be modified), for example intensifiers, quantifiers, adpositions, subjunctions and some ingredients traditionally called adverbs. Heads typically include nouns, verbs and adjectives, though there might also be some heads among the disparate group commonly known as adverbs.

::: ex
Syntactic elements in YAST

- **Operator** \
  An ingredient that itself cannot be modified, or can only have a single modifier chosen from a small class of possibilities.
- **Head** \
  An ingredient that can be modified by multiple other ingredients in parallel.
:::

The distinction between operator and head is largely independent from the distinction between base and modifier from the previous section. Heads and operators alike can be both modifiers and bases, leading to four different possibilities:

- The most typical situation is that a head-base is modified by an operator-modifier, like with bound morphology.
- The special situation in which an operator modifies another operator is called a ~~stack~~. Stacks are typically found in bound morphology in which the ordering is important, but not all stacks are bound and not all bound morphology forms stacks.
- When heads modify heads this is called ~~embedding~~. Note that this term is used here referring to both nominal and verbal embedding. The more traditional usage of the term "embedding" for clausal recursion will be explicitly called "clausal embedding".
- Finally, the modification of operators is quite restricted (by definition), so operators are only rarely used as the base of a modification. In German this occurs with highly restricted possibilities to modify adverbs, like in *seit gestern*.

### Modification: stacking & recursion

The hallmark of human language is the possibility to productively combine many different linguistic elements into large utterances. A central aspect of morphosyntactic structure is that linguistic elements can in turn consist of multiple linguistic elements, leading to a hierarchical internal structure of the utterance (cf. postulate P2 from [@sec:postulates]). This hierarchical structure is commonly modeled in syntactic theories by using the mechanism of recursion. However, not all hierarchical structures are equally in need of a recursive treatment. Crucially, only embedding will be modeled with recursion. Stacking is much simpler and does not need recursion. It can easily be modeled by iteration ("tail recursion"), i.e. stacked modifiers are simply applied one after the other without intricate branching.

### Heads: predicate & referendum {#sec:heads}

Heads, as defined in the previous section, are ingredients that can be modified freely, and they alone allow for embedding. For German (and possibly for all human languages), it only appears to be necessary to distinguish two different kinds of syntactic uses of heads, coinciding with two central functions of human language, namely ~~identification~~ (postulate P5) and ~~assertion~~ (postulate P6).

First, speakers attempt to convey which entities they are talking about and these entities (the referents) then have to be identified by the addressee (cf. postulate P5 from [@sec:postulates]). The primary ingredient that is used to encode the identity of a referent in an utterance is called a ~~referendum~~. This referendum is the head of a referential expression that includes all its modifiers (which might themselves again be modified). The whole referential expression is called a ~~phrase~~. A referent is typically encoded by what is traditionally called a noun, but many other parts of speech can also be used as referent. Note that, differently from most syntactic theories, there is only one kind of phrase in YAST, roughly equivalent to what is called "noun phrase" in most other approaches. For convenience, any head modifying a phrase is called an ~~attribute~~ (or maybe better an ~~adnominal~~).

Second, in a typical utterance some kind of assertion is made about these referents (cf. postulate P6 from [@sec:postulates]). The primary ingredient that is used to encode the assertion is called a ~~predicate~~. The predicate is the head of an assertion that also includes all its modifiers (which might themselves again be modified). This whole assertive expression is called a ~~clause~~. A predicate is typically encoded by what is traditionally called a verb, but other parts of speech can also be used predicatively. For convenience, any head modifying a clause is called an ~~adverbial~~.

::: ex
Heads in YAST

- **Referendum** \
  The head of a ~~phrase~~, used for ~~identification~~. Its modifiers are called ~~attributes~~ (or ~~adnominals~~).
- **Predicate** \
  The head of a ~~clause~~, used for ~~assertion~~. Its modifiers are called ~~adverbials~~.
:::

It is by no means necessary for identification and assertion to be encoded by syntactic heads and their encompassing expressions. Personal pronouns, demonstratives and content interrogatives can be interpreted as identifying expression, but they are operators (i.e. they mostly cannot be modified). Likewise, interjections and conversational particles can be seen as assertions without much internal structure. Still, it does not seem to be a coincidence that exactly the most elaborate syntactic structures (phrases and clauses) are precisely those structures that are used for two main communicative elements in a linguistic utterance.

[--
semi-clause, non-finite clause, restricted clause, deranked clause
--]::

### Operators: admodifiers, junctors & specifiers

Operators, as defined previously, are ingredients that cannot be modified, or can only have a single modifier out of a small set of possibilities. I will distinguish three different kinds of operators based on their morphosyntactic characteristics, called admodifiers, junctors and specifiers.

**Positionally-flexible admodifiers.** Most operators are positionally predictable–that is, when they are used to modify a base, their position relative to the base is morphosyntactically fixed. However, there is a group of operators that have more freedom in their positioning, so the speaker has to explicitly decide where to place them, mostly leading to slight differences in the intended meaning. Such positionally flexible operators will be called ~~admodifiers~~.^[This term is used differently here from Croft (2022:§2.2.2). Alternative terms for "admodifier" might be adorner, additor, adjustor or adaptor.] In German these admodifiers comprise various ingredients that are traditionally called adverbs. Also German numerals seem to belong to this class. Diachronically, admodifiers often seem to be an intermediate phase in the grammaticalisation of heads into positionally-fixed operators.

**Relation-marking junctors.** Among the positionally-fixed operators there is a special class of ingredients that specify the kind of modification, that is, they spell out more precisely what is the relation between a base and its modifier (cf. postulate P4 from [@sec:postulates]). Heads can be modified by multiple other heads, each with their own relation to the superordinate head. These relations between base-heads and modifier-heads are often explicitly marked in the linguistic structure by operators that are called ~~junctors~~ here. In German, examples of phrasal junctors are prepositions and case marking ("flagging"), while examples of clausal junctors are subjunctions and conjunctions. Default ("unmarked") relations also exist in the form of constructions like appositive phrases, relative clauses and non-finite "restricted" clauses.

**Positionally-fixed specifiers.** For clarity of exposition, all other positionally-fixed operators (i.e. all operators except for the admodifiers and junctors) are called ~~specifiers~~ here. These specifiers contain many traditional grammatical categories like tense-aspect-mood marking for clauses, or number and definiteness for phrases. Which specifiers can be added depends on the base being modified. The two largest groups of specifiers are the phrasal and clausal specifiers, but specifiers for other operators also exist (possibly leading to stacks of operators).

### Spawned junctors: roles

Heads typically spawn some language-specific junctors. This phenomenon is commonly known as a lexically-determined argument/roles, but it will be approaches from a slightly different angle here. The basic idea is that individual lexemes will have restrictions on how they can be modified (cf. postulate P3 from [@sec:postulates]). One such type of restriction is that a lexeme induces specific relations that are typically added to modify this lexeme. For example, the German verb *hoffen* 'to hope' has a relation *Hoffende* 'the hoping one', typically using the German *Nominativ* case as a junctor, and a relation *Hoffnung* 'the object of hope', typically using the German preposition *auf* as a junctor. 

Such lexically-determined junctors are called ~~roles~~. Although there are many widespread tendencies as to which roles exist and how they are expressed, for now I will simply specify the roles for each lexical ingredient seperately. German phrases and clauses almost always have a "principal" role, which for phrases will be called the ~~container~~ (German: *Behälter*, typically using a *Genitiv* junctor) and for clauses will be called the ~~protagonist~~ (German: *Protagonist*, typically using a *Nominativ* junctor).

These principal roles only very rarely appear to be absent, like the absence of a protagonist with weather verbs. In contrast, additional roles are spawned by many lexical items, like the well-known roles of (di)transitive verbs. However, adjectives and nouns can also spawn additional roles, in German typically using grammaticalised prepositions. For example, the adjective *froh* 'happy' uses the preposition *über* 'above, over' for the origin of the happiness, or the noun *Reaktion* 'reaction' using the preposition *auf* 'on top of' for the event causing the reaction.

### Building a recipe

Very simple utterances can consist of just an assertion (e.g. imperatives) or just an identification (i.e. answers to content questions). Recipes for such utterances consist of just a single predicate or just a single referendum. For more complex utterances various of the previously discussed ingredients are combined into larger recipes consisting of multiple instructions.

The generation of a recipe can be formalised as a very simple recursive procedure shown in [@next]. This procedure is completely context free as there are no restrictions on the generation at this level of abstraction. The notation used here is inspired by generative rewrite rules for constituency trees, but they work slightly differently to generate a dependency tree.

- The plus symbol stands for modification of the first element on the right side of the arrow.
- The arrow itself literally means replacement of the left side with the right side.
- The vertical bar stands for "or",
- The round brackets indicate optionality
- The superscripted (Kleene) star indicates that the enclosed elements can occur zero or more times. 

::: ex
Formalisation of the generation of a recipe:

1: base → instruction + (base)\* \
2: instruction → (junctor) + nucleus + (specifier)\* \
3: nucleus → predicate | referendum | admodifier
:::

The central elements of a recipe are the instructions. Using the first rule, instructions are inserted recursively modifying other instructions. For readability of the recipe I propose to write each instruction as a single line, using indentation for modification. Each instruction has an obligatory nucleus, with optionally a junctor in front, separated by a colon, and optionally specifiers in round brackets at the end of the line. The details of the formatting of a recipe are just a cosmetic convenience.

Randomly applying the above rules might result in a recipe like in [@next]. However, when building a real recipe in YAST, each instruction will immediately be constructed with actual linguistic content before moving to the generation of a subsequent instruction. A "skeleton" recipe like in [@next] will thus never be generated and it is just shown here to illustrate the formalisation in [@last]. This is rather different from most generative syntactic approaches in which first a skeleton is generated, which is only subsequently populated with lexical material ("spell-out").

::: {.ex noFormat=true}
```
predicate (specifier)
  junctor: referendum (specifier)
    admodifier
  admodifier
  junctor: predicate (specifier, specifier)
    junctor: referendum
      junctor: referendum
```
:::

To illustrate the dependency nature of such a recipe, the first three instructions from [@last] are shown as a dependency tree in [@fig:dependency]. The difference between such a dependency tree and a constituency tree is not really substantial. When the procedure in [@llast] is interpretated as a set of classic generative rewrite rules, then the first three instructions from [@last] result in a constituency tree as shown in [@fig:constituency]. Added to this figure is a notion of headedness, as indicated by the arrows. When these arrows are "collapsed" by inserting the arrow-origin into the arrow-goal, then the same dependency structure as shown in [@fig:dependency] is obtained. This demonstrates that a constituency structure (with an additional notion of headedness) is equivalent to a dependency structure. The only difference is that the constituent tree explicitly includes the history of application of the rewrite rules.

![Example of a dependency tree generated by the formalisation in [@llast], illustrated here for the first three lines of the example in [@last].](figures/dependency){#fig:dependency width=63%}

![Consituent tree for the same example as in [@fig:dependency]. This structure is the result of interpreting the formalisation in [@last] as generative rewrite rules. The arrows indicate the headedness of each constituent.](figures/constituency){#fig:constituency}

How to choose an appropriate linguistic content is to a large extent a matter of speaker choice, which seems most profitably to be handled by the kind of large language models developed recently. However, grammatical restrictions start to appear as soon as individual ingredients are chosen, specifically after any chosen nucleus. There are basically three kinds of syntactic restrictions: any chosen nuclues typically will restrict (i) the choice of junctor in the instruction, (ii) the choice of specifiers in the instruction, and possibly (iii) the choice of junctors in subsequent modifying instructions. 

Each instruction has an obligatory ~~nucleus~~ with optionally a ~~junctor~~ in front (separated by a colon) and optionally ~~specifiers~~ following (in round brackets). For example, the first instruction of the recipe in [@nnext] has a nucleus *hören* 'to hear' with a specifier indicating that it should be put in the *Perfekt* form. There is no junctor here, although a conjunction like *und* 'and' or *aber* 'but' could have been added, linking this utterance to the preceding discourse.

Each instruction has two further elements, which are less obviously present in the recipe. First, each instruction indicates which element it is modifying by indentation. In the example below, the first instruction is not indented, so there is no modification of an earlier instruction. Second, each instruction is either a clause, a phrase or an admodifier. In the example below, the first instruction is inferred to be a clause. This is the default inference for a verbal nucleus like *hören* 'to hear'. To simplify the recipes, such defaults are not explicitly written down, though capitalisation of the nucleus is in practice used to indicate phrases.

::: ex
Das kleine Kind hat gestern gehört, dass sein Vater Bürgermeister geworden ist.
:::

::: {.ex noFormat=true}
```
hören (perfekt)
  Hörende: Kind (definit)
    klein
  gestern
  Gehörte: Bürgermeister (werden + Zustandspassiv)
    Werdende: Vater
      Behälter: Kind
```
:::

The second instruction in [@last] indicates by indentation that it modifies the first instruction. The relation *Hörende* is just a German name for the protagonist role spawned by the verb *hören* of the modified instruction. The nucleus noun *Kind* 'child' is inferred to be the head of a phrase by the capitalisation. The third instruction *klein* 'small' only consist of a nucleus, modifying *Kind* from the second instruction with a default relationship (i.e. there is no junction).

The fourth instruction *gestern* 'yesterday' has only a single indentation, indicating that it modifies the clause *hören* of the first instruction. Crucially, this means that the possibility of the modification of the phrase *Kind* is now finished. This allows for the formulation of this phrase to be completed. In general, modification in the recipe is always immediate: it is not possible to resume modification later, once a hierarchically higher base is modified.

### Parts of speech

Ingredients can be categorized into classes on the basis of their syntactic characteristics. However, such ingredient classes ("parts of speech") are not an atomic feature of the morphosyntax in YAST, but a secondary consequence of the possible syntactic functions of the ingredients. In the end, when considering all morphosyntactic phenomena, I expect that each ingredient will have its own individual syntactic characteristics, so ultimately each ingredient will be its own class. When scrutinizing all linguistic details, ingredient classes will dissolve into an ever expanding pile of subclasses. Simply put, nouns and verbs are not primitive concepts in YAST. Instead there are syntactic functions like ~~referendum~~ and ~~predicate~~. A linguistic ingredient that is used as a referendum in a specific utterance can of course be called a "noun". However, this is not a property of the ingredient, but a reflection of the way the ingredient is used in a specific utterance.

In principle, all lexical elements can occur in all syntactic functions. However, in many languages, including in German, there are lexical elements that are strongly restricted to only occur in a subset of all possible syntactic functions. For example, the German word *Frieden* 'peace' is typically not used as an inflected verb. Yet, even in such a clear case of a "noun" it is definitively possible for any German speaker to say something like *du friedest mir zuviel*. The meaning of such an utterance is undefined, but there is nothing stopping speakers from actually uttering such a sentence. And it might even become a real possibility with a real meaning if enough people would start using it this way. Of course, for the description of German linguistic structure, it is highly relevant to note that there are derivations like *einfrieden* and *befriedigen* and that nouns can be used predicatively with a copula *werden/sein/bleiben*.

The crucial question in YAST then becomes: how are the syntactic functions defined? The basic proposal is that the operators of a language are a finite and often quite small set of elements. These can be exhaustively listed. The syntactic function of a head can then be established by the kind of operators that are used (or can be used) together with the head in a specific utterance. For example, a referendum (think "noun") in German typically has (or can have) a determiner, all forms of which can easily be listed (basically: articles, quantifiers and possessive pronouns). Additionally, a small set of *Fokuspartikel* (e.g. *nur, erst, spätestens*, ...) can be used with phrases, identifying their heads as a referendum. These kinds of lists and their distributional characteristics are part of the actual YAST grammar to be presented in the rest of this book.
