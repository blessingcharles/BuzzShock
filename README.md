#### BuzzShock
![BuzzShock](https://static.wikia.nocookie.net/b-ua/images/1/12/Buzzshock.png)
An Text Based Protocol Fuzzer

##### Architecture Flow

```
ABNF Grammar ---(ABNF-Parser)---> ABNF-Objects ----(AST-BUILDER)[1..n]---> MESSAGES ----(MUTATOR)---> MUTATED-INPUT 
                                                                                                        |
                                                                                                        |
                                                        { YOUR LAB ENVIRONMENT  }<------ Fuzz Socket <---(FuZZer) 
```


