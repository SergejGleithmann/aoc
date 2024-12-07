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
    re_split(": ", Line, [StringResult, _, StringNumbers]),
    number_string(ParsedResult, StringResult),  % Convert result to a number
    split_string(StringNumbers, " ", "", SplitStringNumbers),
    maplist(number_string, ParsedNumbers, SplitStringNumbers).  % Convert the rest to numbers

count_if([], 0).
count_if([[Result,Args]|Lines], Sum) :-
    (   check_calc(Result, Args)  % Apply the predicate to the head of the list
    ->  count_if(Lines, SumRest),  % If true, add 1
        Sum is SumRest + Result
    ;   count_if(Lines, Sum)  % If false, no addition
    ).

concat_numbers(N1, N2, Result) :-
    number_string(N1, S1),        % Convert the first number to a string
    number_string(N2, S2),        % Convert the second number to a string
    string_concat(S1, S2, SResult), % Concatenate the strings
    number_string(Result, SResult). % Convert the concatenated string back to a number

% use the first Arg as startvalue for accumulator
check_calc(Result, [Arg|Args]):-
    check_calc(Result, Arg, Args).
% terminate check
check_calc(Result, Result, []).
check_calc(TargetResult, CurrentResult, [Arg|Rest]):-
    Sum is CurrentResult + Arg, % Evaluate the sum
    check_calc(TargetResult, Sum, Rest);
    Prod is CurrentResult * Arg, % Evaluate the sum
    check_calc(TargetResult, Prod, Rest);
    concat_numbers(CurrentResult,Arg,Conc),
    check_calc(TargetResult, Conc, Rest).
