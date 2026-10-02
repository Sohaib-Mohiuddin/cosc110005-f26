# COSC1100-05 · Python classroom

Professor-led Python demonstrations and classroom materials for Fall 2026.

**[Open the student course site →](https://sohaib-mohiuddin.github.io/cosc110005-f26/)**

Browse by week, search topics and code, read highlighted Python examples, download source files, and open exercise handouts. New to Python? Start with the site's [getting started guide](https://sohaib-mohiuddin.github.io/cosc110005-f26/getting-started.html).

## Available materials

| Folder | Topics |
| --- | --- |
| [Week 2](week-2-demos/) | Algorithms and problem solving |
| [Week 3](week-3-demos/README.md) | Variables, data types, arithmetic, and strings |
| [Week 4](week-4-demos/README.md) | Selection, Boolean expressions, and validation |
| [Week 5](week-5-demos/README.md) | Loops, accumulators, sentinels, and menus |
| [Exercise 2](in-class-exercise-2/) | Numeric and string data |
| [Exercise 3](in-class-exercise-3/) | Selection |
| [Classroom utilities](utilities/README.md) | Demo launcher, trace tables, and user-testing worksheet |

The website discovers the available course folders automatically. Future weeks appear when their materials are added.

## Run a Python example

Download and extract this repository using **Code → Download ZIP**, or clone it. Open a terminal in the repository folder, then use Python 3:

```sh
python3 week-3-demos/01_explore_data_types.py
```

On Windows, use `py` in place of `python3`. No pip packages are required for the current classroom demos. Some examples ask for keyboard input. Read the comments and predict the output before running, then change one input and try again.

Numbered weekly demonstrations include pseudocode, desk checks, and classroom variations. Some weeks have an optional sixth demonstration; additional `in-class-example.py` files reflect live classroom work. Example prices, score bands, and other rules are illustrative, not course policies.

## Add new course content

Upload or commit Python files, notes, or handouts to `week-N-demos/`, `in-class-exercise-N/`, `utilities/`, or `materials/`. Keep companion files with the demos that use them. Push to `main` or merge a pull request; GitHub Actions checks, rebuilds, and publishes the site automatically.

See the [instructor guide on the site](https://sohaib-mohiuddin.github.io/cosc110005-f26/instructor.html) or the [website maintenance guide](site/README.md) for publishing, supported formats, and local previews.

The original [classroom utilities guide](utilities/README.md) describes the optional launcher and saved demo checks. Some utility scenarios reference later weeks that have not been uploaded yet; select an available week when using those tools.
