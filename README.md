# Simple Deductive Reasoning Processor

This is a simple simulation that similar to a deductive reasoning system using one of the learned deductive methods: backtracking.

&bull; Input: a file contain knowledge base and user questions.

&bull; Output: a system's answer, inferred from the question on the basis of existing knowledge.

## Usage

To use the code, follow these steps:

1. Define your knowledge base in a text file named "input.txt" (you can change the filename if needed). Each predicate should be on a separate line. The predicates can be of the following forms:

   - `relation(variables)` - Define a predicate with a relation name and a list of variables. Example: `wife(shizuka,nobita)`.

   - `relation(variables):-subPredicate1, subPredicate2, ...` - Define a predicate with a relation name and a list of sub-predicates. The sub-predicates should be separated by commas. And there are no spaces between each predicates. Example: `strong(X):-workingout(X),eating(X),sleep(X)`.

2. Run the code using a Python interpreter.

3. The program will prompt you with `?-` to enter your queries. Enter your queries in the following format:

   - Single query: `relation(variables)`.
   - Multiple queries: `relation1(variables1), relation2(variables2), ...`.
   - Example: `mother(tamako, nobita)` or with multiple queries `mother(tamako, nobita),father(nobisuke, nobita)`

4. The program will process the queries and provide the results.

## Example

Suppose you have the following predicates defined in "input.txt":

&bull; parent(nobisuke, nobita).
&bull; parent(tamako, nobita).

## Example

Suppose you have the following predicates defined in "input.txt":

friend(nobita, shizuka).
wife(shizuka, nobita).
wife(X,Y):-loves(X,Y),friend(X,Y)

Here's an example interaction with the program:

?- friend(nobita,shizuka).

The system will response with: true.

?- wife(X,Y).

The system will response with: [shizuka, nobita]

?-friend(X, shizuka).
The system will reponse with: [nobita, shizuka]

## Notes
- The code utilizes the defaultdict class from the collections module to store the predicates in the knowledge base.
- The code supports variables in the predicates, enabling more complex queries and inference.
The code employs a backtracking algorithm to process the queries and identify matches in the knowledge base.
- There are two versions of this system. I recommend using the main2.py version because it supports complex and multiple queries. Moreover, the `main2.py` version executes significantly faster than the `main.py` version.

Feel free to modify and adapt the code according to your needs.
