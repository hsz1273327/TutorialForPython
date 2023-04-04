# 设计模式

如果把学python比作学习一门外语,那python语言本身只是相当于学了这门语言中的单词语法,语法糖类似于俚语俗语,学会这些充其量不过是可以写一写词语句子,离可以写一篇文章还有很长的路要走.设计模式就类似一些写作技巧,比如什么起承转合,什么插叙倒叙这些,很多时候不用它并不影响表达(实现功能),但能熟练使用这些技巧则可以大大提高表达的效果.

设计模式是关于[抽象](https://en.wikipedia.org/wiki/Abstraction_(computer_science))的技巧.而抽象是编程的关键,它关系到代码间如何[解耦](https://en.wikipedia.org/wiki/Coupling_(computer_programming)),这又进一步涉及到系统复杂性,而软件设计的根本问题就是要降低软件系统的复杂性.


从某种意义上说设计模式无关语言,但它又必须依托于语言来实现,而由于不同语言有不同的特性,所以其实现往往差别很大.狭义上的设计模式是伴随面向对象编程范式而兴起的.最具代表性的著作是由GOF(知名的四人帮)基于静态语言java的 *'Design Patterns: Elements of Reusable Object-Oriented Software'* 一书.`Peter Norvig `在题为[Design Patterns in Dynamic Languages](http://norvig.com/designpatterns/)
的演讲中指出 *'Design Patterns: Elements of Reusable Object-Oriented Software'* 一书中的23种模式中有16种在以lisp为代表的动态语言中'不见了或者简化了',而简化的方法只是简单的将样板代码使用一些函数式编程的技巧进行替代.而python正是一种动态语言.

GOF也在引言中承认所用的语言决定了那些模式可用:

```text
程序设计语言的选择非常重要，它将影响人们理解问题的出发点。我们的设计模式采用了Smalltalk 和C++ 层的语言特性，
这个选择实际上决定了哪些机制可以方便地实现，而哪些则不能。若我们采用过程式语言，可能就要包括诸如“集成”“封装”和“多态”的设计模式。
相应地，一些特殊的面向对象语言可以直接支持我们的某些模式，例如CLOS 支持多方法概念，这就减少了访问者模式的必要性.
```


