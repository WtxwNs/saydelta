# Contributing

Start with a reproducible recording/script mismatch or a concrete review difficulty. Remove private speech before sharing a sample and state your rights to distribute it. Include the Python/package version, model, operating system, command, expected result and what you heard. Do not paste credentials or private model paths.

```sh
python -m pip install -e ".[asr,dev]"
python -m pytest
ruff check saydelta tests
ruff format --check saydelta tests
python -m build
```

Changes to alignment or rechecks must retain their counterexamples and replay the disclosed validation inputs. Never feed the expected script to recognition to improve apparent accuracy. Keep uncertain findings inspectable. Changes to the report should be exercised in a real browser, including playback, decision export/import, narrow layout and input containing HTML characters.

The project deliberately has no server, account system, analytics or paid API dependency. Propose a concrete user need before adding another major component. Maintain the English README and Chinese quickstart when behavior changes.
