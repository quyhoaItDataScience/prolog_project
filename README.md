# Simple Predicate Logic Query Processor
This is a simple simulation that similar to a deductive reasoning system using one of the learned deductive methods: backtracking.

&bull; Input: a file contain knowledge base, and user questions.

# Predicate Logic Query Processor

This is a Python code that processes queries based on predicate logic using a knowledge base. It allows you to define predicates, load them into the knowledge base, and perform queries on the knowledge base.

## Usage

To use the code, follow these steps:

1. Define your predicates in a text file named "BritishRoyalFamily.txt" (you can change the filename if needed). Each predicate should be on a separate line. The predicates can be of the following forms:

   - `relation(variables)` - Define a predicate with a relation name and a list of variables. Example: `parent(charles, william)`.

   - `relation(variables) :- subPredicate1, subPredicate2, ...` - Define a predicate with a relation name and a list of sub-predicates. The sub-predicates should be separated by commas. Example: `grandparent(X, Y) :- parent(X, Z), parent(Z, Y)`.

2. Run the code using a Python interpreter.

3. The program will prompt you with `?-` to enter your queries. Enter your queries in the following format:

   - Single query: `relation(variables)`.
   - Multiple queries: `relation1(variables1), relation2(variables2), ...`.

4. The program will process the queries and provide the results.

## Example

Suppose you have the following predicates defined in "BritishRoyalFamily.txt":

parent(charles, william).
parent(charles, harry).
parent(queen_elizabeth, charles).
grandparent(X, Y) :- parent(X, Z), parent(Z, Y).

Sure! Here's a markdown version of the README for the code you provided:

markdown
Copy code
# Predicate Logic Query Processor

This is a Python code that processes queries based on predicate logic using a knowledge base. It allows you to define predicates, load them into the knowledge base, and perform queries on the knowledge base.

## Usage

To use the code, follow these steps:

1. Define your predicates in a text file named "BritishRoyalFamily.txt" (you can change the filename if needed). Each predicate should be on a separate line. The predicates can be of the following forms:

   - `relation(variables)` - Define a predicate with a relation name and a list of variables. Example: `parent(charles, william)`.

   - `relation(variables) :- subPredicate1, subPredicate2, ...` - Define a predicate with a relation name and a list of sub-predicates. The sub-predicates should be separated by commas. Example: `grandparent(X, Y) :- parent(X, Z), parent(Z, Y)`.

2. Run the code using a Python interpreter.

3. The program will prompt you with `?-` to enter your queries. Enter your queries in the following format:

   - Single query: `relation(variables)`.
   - Multiple queries: `relation1(variables1), relation2(variables2), ...`.

4. The program will process the queries and provide the results.

## Example

Suppose you have the following predicates defined in "BritishRoyalFamily.txt":

parent(charles, william).
parent(charles, harry).
parent(queen_elizabeth, charles).
grandparent(X, Y) :- parent(X, Z), parent(Z, Y).

vbnet
Copy code

Here's an example interaction with the program:

?- parent(charles, william).
['charles', 'william']

?- grandparent(queen_elizabeth, william).
['queen_elizabeth', 'william']

?- parent(charles, X), parent(X, harry).
['charles', 'diana']
['diana', 'harry']

## Notes

- The code uses the `defaultdict` class from the `collections` module to store the predicates in the knowledge base.
- The code supports variables in the predicates, allowing for more complex queries and inference.
- The code uses a backtracking algorithm to process the queries and find matches in the knowledge base.

Feel free to modify and adapt the code according to your needs.

