read_file_lines(File, Lines) :-
    open(File, read, Stream),
    read_lines(Stream, Lines),
    close(Stream).

read_lines(Stream, []) :-
    at_end_of_stream(Stream).
read_lines(Stream, [Point|Rest]) :-
    \+ at_end_of_stream(Stream),
    read_line_to_string(Stream, Line),
    parse_line(Line, Point),
    read_lines(Stream, Rest).


parse_line(Line, [X, Y]) :-
    re_split(",", Line, [StrX, _, StrY]),
    number_string(X, StrX),
    number_string(Y, StrY).

squares([X1, Y1], [], []).
squares([X1, Y1], [[X2, Y2] | Points], [Square | Squares]) :-
    Square is abs((X1 - X2 + 1) * (Y1 - Y2 + 1)),
    squares([X1, Y1], Points, Squares).

all_squares([], []).
all_squares([Pt | Pts], AllSquares) :-
    squares(Pt, Pts, PtSquares),
    all_squares(Pts, Squares),
    append(PtSquares, Squares, AllSquares).

part1(Max, File) :-
    format(string(FullPath), "../resources/~w.txt", [File]),
    read_file_lines(FullPath, Points),
    all_squares(Points, AllSquares),
    max_list(AllSquares, Max).