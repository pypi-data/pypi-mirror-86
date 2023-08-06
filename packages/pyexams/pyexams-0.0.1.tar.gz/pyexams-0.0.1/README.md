# pyexams

Generates variants of exam questions using [texsurgery](https://framagit.org/pang/texsurgery), keeps a question database, exports to pdf and moodle.

Much like [R exams](https://r-exams.org/), but with the following (main) differences:

 1. R-`exams` requires use of R for both creating exam variants and managing R-`exams` itself, while `pyexams` allows any language for exam creation and is called from a command which can be incorporated into your favourite LaTeX editor.
 2. R-`exams` keeps each question in a separate file, then use a simple R script to compose the whole exam, while `pyexams` use a single LaTeX file for the whole exam.
 3. Both R-`exams` and `pyexams` keep a record of past exam questions, but `pyexams` also keeps a database that can be queried in order to find, for instance, all questions with the tag `derivative` that appeared in exams at least two years ago. The question code is also saved in plain text and managed in a `git` repository, which simplifies the management of a shared question bank, whether group-private or totally open.
 4. Last but not least, R-`exams` is a mature and feature rich project, while `pyexams` is a very young project that still has to deliver.

Other important design decisions involved in `pyexams`:

 - The syntax for the questions is exactly that of [auto-multiple-choice](https://www.auto-multiple-choice.net/)
 - We will use [amc2moodle](https://github.com/nennigb/amc2moodle) (or a custom version of it) to generate the moodle question bank.
 - `pyexams` strives to feel as close to LaTeX as possible to its users, which paradoxically is better done through [texsurgery](https://framagit.org/pang/texsurgery) than through a LaTeX package.

## But where is the code??!

Please wait, we have built prototypes of all the advertised features, but the code is not polished yet, and some parts of the syntax may change as we discuss our prototypes with our colleagues.

## Installation

    python3 -m pip install pyexams
