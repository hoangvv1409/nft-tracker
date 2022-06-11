# nft-tracker

A nft tracker hub, connect with multiple Web 3.0 API provider

Init environment

```bash
pipenv install --dev
```

Create .env from example and fill out the missing value. You need to get your own key and have a local postgres database (try docker)

```bash
cp .env.example .env
```

Test it out

```bash
pipenv run test
```

Migrate the database

```bash
pipenv run alembic upgrade head
```

Fetch top Collections (first 20 page of etherscan, sorting by transfer 24H)

```bash
pipenv run python fetch_collections.py
```
