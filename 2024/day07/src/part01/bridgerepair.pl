parse_file(FileName, ParsedData) :-
    open(FileName, read, Stream),
    read_lines(Stream, ParsedData),
    close(Stream).

% Parse the file, apply count_if, and accumulate the count.
parse_and_count(FileName, Sum) :-
    parse_file(FileName, ParsedData),
    count_if(ParsedData, Sum).  % Count occurrences where predicate holds

read_lines(Stream, []) :-
    at_end_of_stream(Stream). % Base case: stop reading at the end of the stream
read_lines(Stream, [ParsedLine|Rest]) :-
    \+ at_end_of_stream(Stream), % Ensure we’re not at the end
    read_line_to_string(Stream, Line), % Read a line as a string
    split_and_parse(Line, ParsedLine), % Process the line
    read_lines(Stream, Rest). % Recurse for the next line

split_and_parse(Line, [ParsedResult, ParsedNumbers]) :-
    re_split(": ", Line, [StringResult, _, StringNumbers]), % Split at ": " and trim spaces
    number_string(ParsedResult, StringResult),                  % Convert the first part to a number
    split_string(StringNumbers, " ", "", SplitStringNumbers),
    maplist(number_string, ParsedNumbers, SplitStringNumbers).       % Convert the rest to numbers

count_if([], 0).
count_if([[Result,Args]|Lines], Sum) :-
    (   check_calc(Result, Args)  % Apply the predicate to the head of the list
    ->  count_if(Lines, SumRest),  % If true, add 1
        Sum is SumRest + Result
    ;   count_if(Lines, Sum)  % If false, no addition
    ).

check_calc(Result, [Arg|Args]):-
    check_calc(Result, Arg, Args).
check_calc(Result, Result, []).
check_calc(TargetResult, CurrentResult, [Arg|Rest]):-
    Sum is CurrentResult + Arg, % Evaluate the sum
    check_calc(TargetResult, Sum, Rest);
    Prod is CurrentResult * Arg, % Evaluate the sum
    check_calc(TargetResult, Prod, Rest).
