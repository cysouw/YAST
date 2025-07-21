## Preface {.unnumbered}

The motivation to develop yet another syntactic model for an already well-described language like German grew out of a large research project on German diathesis (Cysouw 2023). That book claims to provide a complete list of all monoclausal syntactic derivations for German. This list is long (currently more than 300 clause derivations, and counting), but clearly finite. The impetus for the current syntactic model was the simple idea to investigate what remains to be done for the syntax once all these monoclausal derivations are put aside. In other words, what does a syntactic model look like when monoclausal derivations are reduced to just checkboxes to be ticked, alike to the treatment of other finite morphosyntactic categories like tense or number in a syntactic theory. The current proposal is the result of following that premise through. In essence, the current approach is an experiment build on a single fundamental question, namely what a syntax would look like when monoclausal derivation (called "stacking" in Cysouw 2023) is strictly separated from subordination.

Syntactic models need an acronym, so here I present to you YAST. This name started out in jest for 'Yet Another Syntax Theory', but I got enamored by the name, so it stuck. There is a slightly deeper meaning to this name, however. The acronym YAST is an obvious nod to YAML, which started out as meaning "Yet Another Markup Language". But then, as YAML was developed further, it turned out to be much more useful than originally anticipated, which led to a recursive backronym "YAML Ain't Markup Language". In the same vein, the YAST approach turned out to be much more useful than I had anticipated, so I now interpret the acronym YAST as a backronym meaning "YAST Ain't (just) Syntax Theory". But what's in a name? In the end it's just a sequence of letters to identify the approach to morphosyntactic analysis as outlined in this book.

The result is remarkable: with the hundreds of clause derivations from Cysouw (2023) out of the way, a reasonably fragment of a syntax for German can be formulated with just very few rules. I have implemented these rules in Python using XML-tree structures, and this part of the syntax takes just a few hundred lines of code. It can produce complete sentences with ordering, case marking, agreement and syntactic control for a wide range of complex syntactic structures. The remaining hundreds of clausal derivations (as listed in Cysouw 2023) also can be easily implemented in just a dozen or so lines of code each. Currently only a small exemplary subset of those has been implemented. There is also a basic parser, which is not very good yet, but there is ample room for improvement.

The syntactic rules presented here describe (standard) German. However, the general architecture of YAST seems transferable to other languages. The analysis of sentence structures in YAST is fully compatible with typological insights about the worldwide linguistic diversity as, for example, summarized in Croft (2022). I have tried to adapt my terminology to Croft's to make the parallels even more obvious. Still, linguistic diversity is vast, and I do not dare to predict how much work is necessary to adapt the current framework to other languages.

The first few chapters lay out YAST in rather abstract terms. This is not how YAST originated in my own personal thinking. I started out with some simple lines of code to produce German sentences and found various ways to generalize and simplify this algorithm. Once things worked quite well in practice I started formulating in more detail what kind of theoretical assumptions I was making. In so doing I followed the scientific procedure proposed by the Dutch cartoonists John Reid, Bastiaan Geleijnse and Jean-Marc von Tol: "very impressive, colleague ... but does it also work in theory?"

![The real scientific procedure (© Reid, Geleijnse & van Tol)](figures/fokkesukke.png){#fig:fokkesukke}

# Recipe-rule-result-receipt

## Introducing the YAST model

In its most basic sense, YAST is a generative model for sentence structures. It starts from a set of ~~instructions~~ that, when fed into the morphosyntactic ~~rules~~, lead to an ~~result~~, i.e. a sequence of pronounceable linguistic elements. The instructions are language-specific, i.e. the instructions to make a German sentence consist of German elements. The basic guideline determining what should appear in the instructions is the notion of predictability: all parts of an actual utterance that can be predicted are added by the rules, only the non-predictable elements remain for the instructions. So, the research that is needed to write morphosyntactic YAST-rules for a specific language is to decide which parts of the utterance are predictable and which are non-predictable. As it turns out for the current case of German, the set of instructions to produce a sentence is very similar to a dependency tree. This was not an a-priori decision, but a result of the research.

Pronunciation can often already start long before the instructions for even a single sentence are finished. So, YAST might also be a useful model for language processing, though note that the current model is based purely on syntactic analysis, without any actual research into real psychological processing. Still, to produce utterances in YAST there is only minimal memory required, in that just very few parts of the instructions cannot be immediately uttered, but have to be retained for later. Most instructions simply lead to linguistic elements that can be uttered immediately.

The complete process that leads to the utterance (i.e. the results of the evaluated instructions) can be recorded, and this ~~receipt~~ looks like a constituent tree. Crucially, the creation of such constituent trees are not necessary for the production of the utterance. The constituent tree is just the combined effect of all instructions. So, the constituent tree is really a receipt and not a recipe. In short, the syntactic approach of YAST can be summarized as a ~~recipe-rules-result-receipt~~ model. The (dependency-like) instructions are the recipe. The recipe is fed into the the rules to produce a resulting utterance. Additionally, a (constituent-like) receipt is a summary of all the procedures leading to the result.

This multi-step approach to syntactic analysis probably feels eerily similar to the familiar "deep structure being transformed to surface structure" approach developed by Harris and Chomsky starting in the late 1950s, and there are surely parallels to be found. However, in actual practice there is not much similarity in the inner working of the algorithms. The difference is most obvious in the "rules" of YAST, which do not transform the recipe, but start from scratch building a syntactic structure on the basis of the recipe.

## A generative probabilistic templatic language model for humans

goals: 

- allow human analysis of linguistic structure
- use parameters that can be grasped by human understanding (but can be further fine-tuned towards LLM-like models)
- level of abstraction that is helpful for language learning
- compare structure across languages

universal postulates for morphosyntax 

None of these characteristics are necessary universal, because at some point in the evolution of morphosyntax they did not exist. However, they seem to be very widespread among human languages, currently basically universally present:

Major principles:

- morphemic division (-> morpheme)
- hierarchical modification (-> modifier)
- reference vs. assertion (-> phrase, clause)

Major effects of grammaticalisation:

- combinatorical restrictions (-> head, specifier, stack)
- explicit relations (-> junctor, flag = phrasal junctor)
- templatic structures (-> template)

Operators, specifiers and junctors are typically deficient heads (grammaticalisation). However, they might also develop *into* heads ?! leftover non-head (mostly non-modifyable?!) morphemes with variable position (-> operator, only some 'adverbs' left here?)

morpheme classes are language specific

Morphemes can be classified into classes based on the 'construction' in which they can appear. Such a class should clearly be implemented as a gradual class, e.g. by adding frequencies. Speaker's ingenuity can always add a specific morpheme into a class.

- templates and specifiers define classes
- morphemes can be (and typically are) multi-functional, i.e. they appear in multiple classes
- classes cross-sect each other ()

Adverbs are a non-coherent group:

- typically they are operators

## The recipe

The recipe consists of a collection of one-line instructions that use indentation to indicate hierarchical modifications. Instructions consist of three different kinds of information, namely ~~junction~~, ~~content~~ and ~~specification~~. All information in an instruction ideally will be of a functional/semantic nature. The formal linguistic structure is not something that should be of concern in the planning of the instructions. The formal syntactic structure of the eventual utterance is produced by the (automatic) rules. 

The most precise and straightforward method to specify meaning in a recipe is to use language-specific elements. In YAST, a user of a specific language is necessarily juggling with the available language-specific tools to construct an utterance and is not manipulating some abstract non-linguistic concepts.

::: ex
Parts of an instruction in YAST

- ~~junction~~: explicit relation to earlier content (can be empty for default modification)
- ~~content~~: a single base lexeme
- ~~specification~~: language-specific grammatical marking (can be empty for unmarked morphosyntax)
:::

As an example, consider the German sentence in [@next] as an appetizer. This German sentence is generated by the instructions in [@nnext] using the grammatical rules as will be laid out in the rest of this book. The instructions in [@nnext] can be seen as the intention of the speaker, with indentation marking modification. These instructions seem suitable for a semantic analysis, though this side of the model will has to be worked out in more detail. Note that the specifications (in brackets) are intentionally formulated with language-specific morphosyntactic categories, so their semantic interpretation will have to be language-specific as well. Any cross-linguistic generalization over language-specific elements is a separate, though highly important, endeavor.

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

Each line in [@last] is a single instruction, possibly consisting of up to three different kinds of elements. Anything before the colon is an explicit ~~junctor~~ that marks the relation to the superordinate instruction. This is either a lexical role, an adposition or a subjunction/conjunction. When there is no colon, then the junction is assumed to be default modification. After the linkage follows the main lexical ~~nucleus~~. This is typically a German lexeme, though there are a few abstract abbreviations used, like '1' for the speaker. The actual lexemes are included in the instructions because the language-specific lexemes are the best summary of their meaning. After the content lexeme (between brackets) follows a list with explicit grammatical ~~specifications~~. When there are no grammatical specifications the rules will infer a default ('unmarked') grammatical structure. Multiple grammatical specifications are separated with a plus-sign, and their order is relevant in some situations.

## The rules

The rules use the instructions to produce an actual utterance. They specify how to put the elements from an instruction in their proper place and give them their proper grammatical form. The basic action induced by an instruction is the insertion of linguistic material into the structure prepared by the superordinate instructions, followed by various morphosyntactic edits to produce the right inflection, allomorphy, agreement and government.

## The result

In the current implementation, the result of applying the rules to a recipe is an utterance in orthographic form. Each part of the utterance is prepared as soon as possible, i.e. the first words of an utterance can mostly already be uttered long before all instructions for a complete sentence are even finished. This is illustrated in [@tbl:example] for the recipe from [@last]. This intuitively seems similar to actual language production in that it is often possible to start speaking without even knowing what will be said in the rest of the sentence.

There are a few syntactic restrictions that result in a slight delay in the result. Basically, finite verbs have to wait for the subject to be planned, so the verb agreement can be added. Also nouns have to be in the waiting queue to be sure that there are no further pre-nominal attributes that have to placed before the noun is uttered. Still, the production of the resulting utterance stays really close to the generation of the instructions.

Instructions                                    | Results
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

Table: Production of the utterance (right), shown parallel to the instructions (left). There is only a minimal delay between the generation of an instruction and the production of the utterance. {#tbl:example}

## The receipt

The receipt summarizes the process of building an output from the recipe. I use a constituent-like structure for the receipt, but this is not necessarily the best or ideal approach. In general, the details of the receipt are rather ephemeral in that it is mostly a question of taste which aspects of the recipe+rules process is shown in the receipt. That is to say, most details of how the receipt currently looks are easily changed to other preferences. For example, in the current implementation, I have added a "cleanup" stage, in which various details are removed to present a simpler receipt. 

![Constituent structure in YAST](figures/example){#fig:example}

Still, I have retained various "traces" of the process leading to the end result, which might look somewhat like transformational movements from early proposals in transformational grammar. This happens because some elements of the instructions have to be temporarily kept "in memory" as they cannot immediately be cleared for pronunciation. This happens, for example, with verbs that are waiting for their subject specification to get subject agreement. Such ingredients "in waiting" are stored internally somewhere and are only uttered at the requisite moment/position. At the moment when such ingredients are being processed for pronunciation, they are taken from their internal storage and "moved" to their eventual position in the constituent structure. Crucially though, the location of the internal storage in the structure is really arbitrary, so the movement is actually more like a process of "preparing for pronunciation". I tend to temporarily store elements in such a position that it only needs minimal movement, but the internal storage could just as well be a unordered named list.

## The parser

The ephemeral role of the constituent-like receipt is also reflected in the workings of the ~~parser~~. The parser does not attempt to reconstruct the constituent tree, but immediately (after observing each pronounced element) tries to reconstruct the underlying dependency-like instructions. In the current implementation, various different instructions are attempted within the range of possibilities as constrained by the actual utterance. Each attempt is fed into the rules until the actually observed utterance is replicated. The YAST-parser is thus actually a predictor that constantly tries to reconstruct the instructions (as intended by the generator) by performing generation in parallel and checking the results of these mirrored generation with the observed utterance. The parser mostly does not have to wait until an utterance is finished, but can already start predicting while the utterance is still ongoing. This aspect of YAST seems to be a very fruitful approach for modeling language processing. 

![Basic workflow of YAST](figures/basis){#fig:basis}

## Formal complexity

Before delving into the details of this syntactic model, a few words on the algorithmic complexity of this model are in order. This topic needs more in-depth investigation, but my initial impressions are as follows:

- Each instruction in the recipe can be generated with a simple regular language, i.e. a type-3 grammar.
- The recipe consists of a set of hierarchically ordered instructions, which can be modeled with a context-free language, i.e. a type-2 grammar.
- The rules differ in their complexity. Most operators are simple insertions with some reformatting, which are regular, i.e. captured by a type-3 grammar.
- Each insertion of a constituent structures, with possibly multiple slots to be filled, are context-free, i.e. they form a type-2 grammar.
- Finally, the rules that are defined as "diathesis" in Cysouw (2023) are exactly the rules that need multiple joint insertions, so these are mildly-context-sensitive, i.e. they fall in between a type-2 and a type-1 grammar. It seems to be the case that it is this part, and only this part, of the morphosyntax that is more complex than context-free.
- The parsing needs more work, but it consist reconstructing a dependency-like structure from an utterance, which is considered not highly complex.

# The recipe

## Generating a recipe: ingredients

In the syntactic model pursued here, the production of an utterance consists of two stages: first a ~~recipe~~ is created, followed by the application of ~~rules~~. Planning an utterance means to create a recipe for it, and this formation of a recipe is a generative process. This generative process also has some "rules", i.e. restrictions on which recipes can be constructed. However, these restrictions are relatively minor, even for a strongly flectional language like German. Other languages might exhibit even less constraints in this regard. The relative freedom to produce recipes reflects the wide leeway speakers have to produce a wide variety of utterances. In extremis, the automatic rules will sometimes have to "work around" the instructions in the recipe to mould the speaker's intention in accordance to the structure of the language.

The basic building blocks of a recipe will be called ~~ingredients~~ (in keeping with the cooking metaphor). Basically, ingredients are morphemes, but they also include fixed grammaticalized combinations of morphemes (like non-compositional idioms) and multi-part grammatical structures (like auxiliary constructions). Semantically, ingredients induce a state-of-mind at the addressee, probably consisting of a multitude of situations in accordance to the communally developed practice of using the ingredient (i.e. the ingredient's "meaning"). The act of uttering an ingredient intends to conjure up some of those possible situations in the mind of the addressee.

Restrictions on building a recipe mainly consist of limits on which ingredients can be used in specific positions in the generation. To fully describe these limits it will eventually be necessary to specify individual possibilities for each ingredient of a language, because ultimately each ingredient has different distributional constraints and tendencies. In the end, something like a Large Language Model with millions of parameters is necessary to fully describe the full distributional detail of a language. However, in this book I will only describe some general patterns with the understanding that these patterns are just a starting point for the subsequent specification of more detail. Ultimately, there is clearly a need for some kind of "grammatical lexicon" that includes the full syntactic detail for each ingredient in humanly readably form (as opposed to the unintelligible black box that is a Large Language Model).

## Combining ingredients: base & modifier

Language extends the usefulness of its ingredients by combining multiple of them into larger utterances. The underlying semantic effect of the combination of ingredients is probably something quite general like intersecting the two sets of possible situations. Uttering an ingredient-combination asks the addressee to search for possible situations that are in accordance with both ingredients. When, at first, the addressee might not be able to find any feasible intersection, this forces a reconsideration of possible interpretations of the ingredients, hopefully eventually leading to some kind of "understanding" on the part of the addressee.

Additionally, a central tenet of human language is that combinations of linguistic elements is in general asymmetrical. Ingredients are not simply combined as equals, but there is always a ~~base~~ that is modified by another linguistic element, the ~~modifier~~. Symmetrical connections with European-style *and*-coordination seem to be a relatively late addition to the grammatical spectrum. For the recipe, I will assume that all combinations of ingredients in human language are asymmetrical.

Bases can have multiple modifiers and each modifier can itself be a base that again can be modified. In this way, a recipe is in essence just a complex hierarchical dependency structure. When a base has multiple modifiers, then the ordering of these modifiers is often meaningful, so the ordering will have to be encoded in the recipe. However, in many situations the actual ordering of modifiers is strongly restricted in a language, for example in morphologically bound constructions. Such restrictions are encoded in the rules, not in the recipe. Yet, there are also situation in which the ordering is not completely fixed, but there nevertheless are strong tendencies, for example in the ordering of attributive adjectives in German. It is currently unclear how to best encode such tendencies. For now the recipe will simply allow all possible orders, also the unusual variants. 

## Syntactic elements: operator, adjustor & head

The raw intricacy of pure modification can be further streamlined by distinguishing three different kinds of elements in the hierarchical structure. First, when an ingredient cannot itself be modified again, it will here be called an ~~operator~~. Second, when a base can only be modified by unmodifiable operators, it will be called an ~~adjustor~~. Finally, when a base can freely be modified by operators, adjustors and other bases, it will be called a ~~head~~. It is important to note that these terms describe syntactic functions and not specific ingredients. One and the same ingredient will often be able to occur in different functions depending on the context in which it is used.

all three can modify other ingredients, so all can function as modifier. Only adjustors and heads can be modified, so they can function as base.

::: ex
Syntactic elements in YAST

- ~~operator~~: an ingredient that itself cannot be modified.
- ~~adjustor~~: an ingredient that can only be modified by operators or other adjustors.
- ~~head~~: an ingredient that can be modified by operators, adjustors or other heads.
:::

[comment]: # (Other terms instead of "adjustor" might be: adorner, additor, admodifier, adaptor)

The current definitions of the terms "operator" and "head" might not always coincide with what one might otherwise conceive of as an operator or head. However, the effect of these definitions seems close enough to most other applications of these terms that it seemed worthwhile to retain these terms, notwithstanding possible confusion. The term "adjustor" is newly conceived here to be reminiscent of the traditional terms "adjective" and "adverb", while indicating that its function is to "adjust" or "alter" another ingredient.

Typical operators are bound morphemes, but there are many other non-bound linguistic elements that are operators under the current definition (namely, that they cannot themselves be modified), for example intensifiers, quantifiers, adpositions or subjunctions. Typical adjustors are adverbs and attributive adjectives, which only allow for limited modification like gradation and intensification. Finally, heads typically comprise verbs and nouns, but they also includes most adjectives, and even some adverbs. 

## Hierarchical structure: stacking, layering & embedding

The hallmark of human language is the possibility to productively combine many different linguistic elements into large utterances. One important aspect of morphosyntactic structure is that linguistic elements can in turn consist of multiple linguistic elements, leading to a hierarchical internal structure of the utterance. This hierarchical structure is commonly modeled in syntactic theories by using the mechanism of recursion. However, not all hierarchical structures are equally in need of a recursive treatment.

Roughly coinciding with the three kinds of syntactic elements introduced above, I propose to break down the hierarchical structure of a recipe into three different levels of modification, which I will refer to as ~~stacking~~, ~~layering~~ and ~~embedding~~. These three levels of hierarchical structure are conceptually constructed as variations of each other, all three being different kinds of modification. Specifically, layering is a special case of stacking, and embedding is a special case of layering. In practice, however, I will use the term "stacking" only for modification that is not layering nor embedding. Likewise, "embedding" is only used for layers that that themselves include further layers.

Crucially, only embedding will be modeled with recursion. Stacking and layering are much simpler and do not need recursion. They can easily be modeled by iteration, i.e. stacked and layered modifiers are simply applied one after the other without intricate branching.

::: ex
Hierarchical structures in YAST

- ~~stacking~~ is modification by operators.
- ~~layering~~ is modification by an adjustor or head, possibly including stacking itself (i.e. they might have their own operators).
- ~~embedding~~ is modification by a head that itself exhibits layering (not just stacking).
:::

The term ~~stack~~ is proposed for a base with all its operators. Multiple operators modify the base iteratively, as the order of the operators is sometimes important. A typical example of a stack is a fully inflected wordform, consisting of a base root with its modifying bound morphemes. However, also non-bound operators are part of the stack, like nominal focus particles. A stack will be written as a single line in the recipe.

A typical ~~layer~~ is an attributive adjective, an argument or an adverbial adjunct. Each layer is a new line in the recipe, with indentation showing the dependency. The ordering of the layers in the recipe is often crucial for the ordering in the resulting utterance. 

Only when such a layer itself again has layers of its own then the point is reached of real recursion in language. Such recursive layers are then called ~~embeddings~~. Note that the term embedding is used here both for nominal and verbal recursive structures.

[comment]: # There is an unfortunate inconsistency in the structure of this terminology. First, ideally the phenomenon would be a term ending in *-ing*, while the concrete instantiation would not have this suffix (i.e. *a stack* vs. *stacking* and *a layer* vs. *layering*). However, this regularity breaks down with the term *embedding*, which is used for both meanings (i.e. *an embedding* as instantiation and *embedding* as the phenomenon. Alternatively *an embed* might be used for the instantiation, but that sounds weird). Second, a stack is the complete set of all modifiers added by stacking, while a layer and an embedding are single modifications added by layering or embedding.

These three levels of modification suggest an evolutionary development in that human language first developed stacking, then layering and then embedding. However, that is purely speculation because all human languages currently appear to employ all three kinds of hierarchical structure. Also note that contemporaneous language change does not follow the path from stacking to layering to embedding. In contrast, grammaticalization typically develops in the reverse direction, from embedding to layering to stacking.

## Heads: referent & predicate

Heads, as defined previously, are ingredients that can be modified freely, and they alone allow for embedding. For German (and possibly for all human languages), it only appears to be necessary to distinguish two different kinds of heads, coinciding with two central functions of human language, namely identification and assertion. 

First, speakers attempt to convey which entities they are talking about and these entities then have to be identified by the addressee. The primary ingredient that is used to encode the identity of an entity in an utterance is called a ~~referent~~. This referent is the head of a referential expression that includes all its modifiers (which might themselves again be modified). The whole referential expression is called a ~~phrase~~. A referent is typically encoded by a noun, but many other parts of speech can also be used as referent. Note that, differently from most syntactic theories, there is only one kind of phrase in YAST, roughly equivalent to what is called "noun phrase" in other approaches.

Second, in a typical utterance some kind of assertion is made about these entities. The primary ingredient that is used to encode the assertion is called a ~~predicate~~. The predicate is the head of an assertion that also includes all its modifiers (which might themselves again be modified). This whole assertive expression is called a ~~clause~~. A predicate is typically encoded by a verb, but other parts of speech can also be used predicatively.

::: ex
Heads in YAST

- ~~referent~~, the head of a ~~phrase~~, used for ~~identification~~
- ~~predicate~~, the head of a ~~clause~~, used for ~~assertion~~
:::

It is by no means necessary for identification and assertion to be encoded by syntactic heads and their encompassing expressions. Personal pronouns, demonstratives and content interrogatives can be interpreted as identificational expression that are operators (i.e. they cannot be modified). Likewise, interjections and conversational particles can be seen as assertions without much internal structure. Still, it does not seem to be a coincidence that exactly the most elaborate syntactic structures are precisely those structures that are used for two main communicative elements in a linguistic utterance.

Heads can be modified by multiple other heads, each with their own complex internal structure and each with their own relation to their superordinate head. These relations between heads and modifier-heads are often explicitly marked in the linguistic structure by operators that are called ~~junctors~~ here. In German, phrasal junctors are prepositions or case marking ("flagging"), while clausal junctors are subjunctions, conjunctions and a few preposition-like operators. Default "unmarked" relations between heads only occur in the form of appositive phrases and relative clauses.

## Modification: attribute, adverbial & argument


## Building a recipe

very simple utterances can consist of just an assertion (e.g. imperatives) or just an identification (i.e. answers to content questions). Recipes for such utterances would then consist of just a predicate or just a referent.

Sentences consist of an assertion about some referent(s) with various additional modification.


# Ingredient classes

## Parts of speech

Ingredients can be categorized into classes on the basis of their syntactic possibilities. When considering all linguistic evidence, I expect that – in the end – each ingredient will have its own special distributional characteristics, so ultimately each ingredient will be its own class. Yet, a few large classes can profitably be formulated, although these classes should not be expected to be perfectly homogeneous. When scrutinizing the details, these classes will dissolve into an ever expanding pile of subclasses.

Ingredients will be classified on the basis how they are used in the the four syntactic functions, namely in (i) referential phrases, (ii) predicative clauses, (iii) phrasal attributes, and (iv) clausal adverbials. The classification of bases will be first discussed. This will be followed by a discussion of the classification of operators. Recall that bases are ingredients that can be modified, while operators are ingredients that cannot be modified.

Note: classes in German are mostly necessary for the generation of a recipe. There are only very few phenomena in the rules that need to know additional classes (e.g. postpositions). Also: attribute genitives: pre-nominal with proper names, otherwise postnominal. Also: order of adjectives

Note: compounding is extremely frequent to make new bases

## Base classes

Base-classes are established by the possibility of a base being the center of any of the four major syntactic functions, namely whether they can be used as (i) referential head, (ii) predicative head, (iii) attributive adjustor, or as (iv) adverbial adjustor. Five German base classes can then be defined by the distribution as shown in [@tbl:baseclasses]. These classes largely correspond to the traditional categories as used in German grammar, except for adverbs, which turn out to be a rather incoherent hybrid class. The first three classes (*Nomen, Verb, Adjektiv*) are very large, while the latter two (*Adverb, Numerale*) are strongly restricted in size. Additionally, as indicated by the "plus-minus" symbol, the classes of adverbs and numerals actually consist of various syntactic subclasses.

Syntactic function   | *Nomen* | *Verb* | *Adjektiv* | *Adverb* | *Numerale*
:---------           | :-: | :-: | :-: | :-: | :-:
Referential head     |  ✓  |  ✓  |  ✓  |  ±  |  ✓  
Predicative head     |  ✓  |  ✓  |  ✓  |  ±  |  ±  
Attributive adjustor |  –  |  ✓  |  ✓  |  ±  |  ✓  
Adverbial adjustor   |  –  |  –  |  ✓  |  ✓  |  ±  

Table: Syntactic possibilities of German base-classes. {#tbl:baseclasses}

### *Nomen*

The class of *Nomen* corresponds to the traditional concept of nouns as it is used in German grammar, and it is arguably the largest of the base classes. Nouns in German have a lexically determined inherent gender when used as a referential head [@next a] and they can all be used as predicative head with the help of a copula, either *werden* 'to become', *sein* 'to be', or *bleiben* 'to remain' [@next b]. Note that such a "real" predicative use of a noun does not have an article. Many nouns can only be used as "real" predicative head (i.e. without article) in the plural to indicate the generic meaning [@next c]. With an article the predicative use of a noun turns into an identificational construction to be discussed later (see ???).

::: ex
Syntactic uses of a *Nomen* in German

- Referential head: *Der **Vater** ist noch jung.*
- Predicative head: *Er wird bald **Vater**.*
- Predicative head (Generic plural): *Dryaden und Hamadryaden sind **Bäume**.*^[~~DWDS~~: Spengler, Oswald: Der Untergang des Abendlandes, München: Beck 1929 [1918], S. 516.]
- Identification: *Er ist der **Vater**.*
:::

German nouns can only be used as an attributive adjustor and as an adverbial adjustor using lexically-specific morphological derivations with suffixes like *‑haft, ‑ig, ‑isch, ‑lich, ‑gemäß, ‑mäßig* or *‑artig*. The availability of these derivations are strongly lexically dependent. Many nouns allow for multiple such derivations (e.g. *kindhaft, kindisch, kindlich, kindgemäß*), while others do not seem to allow any of these derivational suffixes (e.g. *Stuhl* or *Schuh*). Such uses of nouns as adjustors are not included here as syntactic possibilities because these suffixes are not productively available to all nouns.

### *Verb*

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

### *Adjektiv*

The class of *Adjektiv* consists of ingredients that can be used in all four syntactic functions from [@tbl:baseclasses], as illustrated with the adjective *groß* 'large' in [@next]. Grammatically, there are few special characteristics of the different uses of adjectives. First, when used as a referential head [@next a] the gender can be freely assigned. Second, both as a referential head [@next a] and as an attributive adjustor [@next c], adjectives in German have case-number-gender agreement suffixes, so-called *KNG-Kongruenz* in the German grammatical tradition. Third, an adjective needs a copula when used as a predicative head [@next b], either *werden* 'to become', *sein* 'to be', or *bleiben* 'to remain'. When used as an adverbial adjustor it is used without any further morphological change [@next d]. Note that it is also possible to use adjectives as "fake" adverbials, i.e. to use them depictively [@next e], similar to the use of participles in [@last d]. This is treated as an attributive adjustor, though with a different syntactic appearance in the sentence.

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

### *Adverb*

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

### *Numerale*

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

### Stems used in multiple base classes

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

## Operator classes

Junctors, Limiters

Quantors, Abtönungspartikel, Konjunktionaladverben, Epithesis/Diathesis, etc.

### Junctors

phrasal: both attributive and adverbial (and argument!)
clausal: only adverbial. Attributive clauses do not have junctor

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


### Specifiers 

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


### Komplemente? Implizite Adverbialsätze ???

*wir haben viel zu besprechen*
*wir haben so viel zu besprechen, dass (???) wir noch länger bleiben müssen*
*wir haben so viel zu besprechen (und die Folge ist), dass wir ...*

reverse? *wir müssen länger bleiben, weil wir so viel zu besprechen haben*

*wir besprechen die neue Situation*
*wir besprechen, dass es schneller gehen muss*
*wir besprechen so viel, dass es mir schwindelt* => mir schwindelt weil wir so viel besprechen.