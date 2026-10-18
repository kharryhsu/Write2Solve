# Write2Solve

Write2Solve is an interactive math game where players solve equations by writing digits with their own handwriting.

---

## How It Works

A random equation appears on screen. Draw your answer on the canvas and press Submit. A CNN trained on MNIST reads your digit and checks it against the solution.

---

## Setup

Requires [uv](https://docs.astral.sh/uv/).

    git clone https://github.com/kharryhsu/Write2Solve.git
    cd Write2Solve
    uv sync

`uv sync` installs Python 3.12 and all dependencies from `pyproject.toml`.

---

## Run

    uv run python -m write2solve

---

## Project Structure

    write2solve/    game code and equation generator
    notebooks/      model training notebook
    models/         trained digit classifier
    data/           MNIST CSVs for training (not tracked)

To retrain the model, put `train.csv` and `test.csv` in `data/`, install the notebook dependencies with `uv sync --group notebook`, and run `notebooks/train.ipynb`.

---

## Contributions

Thank you for your interest in this project! 🙌  
At the moment, we are not accepting contributions as the project is still under active development.  

Stay tuned for updates!