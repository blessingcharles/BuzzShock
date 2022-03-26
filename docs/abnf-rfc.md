#### ABNF RULES in RFC

[Reference](https://datatracker.ietf.org/doc/html/rfc5234)

-   Rule Names are case insensitive
-   Equal Sign Seperates the name from the definition of rule
-   Strings enclosed in a quotation marks[case insensitive] "abc" . For case sensitive , specify chars
    individually "a b c"
-   Terminals can also be specified with numeric charaters like %b , %x , %d
-   Alternatives / eg : foo / bar
-   Incremental Alternatives eg: Rule1 =/ Rule2
-   Value Range Alternatives[ - ]
-   Sequence Group (Rule1 Rule2)
-   Variable Repitation \<m>\*\<n> [default 0 and infinity]
-   Specific Repetion \<n>element == \<n>\*\<n>element
-   Optional Sequence [foo bar] = \*1(foo bar)
-   Comment - ; continues to EOL eg : ; I'm a comment , I will be ignored
