DROP TABLE IF EXISTS episodes;
DROP TABLE IF EXISTS scores;

CREATE TABLE episodes (
       id SERIAL PRIMARY KEY,
       title TEXT UNIQUE NOT NULL,
       contents TEXT NOT NULL
);

CREATE TABLE scores (
        id SERIAL PRIMARY KEY,
        username TEXT NOT NULL,
        uuid TEXT NOT NULL,
        submitted TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        successes INTEGER NOT NULL,
        attempts INTEGER NOT NULL,
        laplace_estimator REAL NOT NULL,
        CHECK (attempts >= 0 AND attempts >= successes)
        -- TODO figure out how to make a constraint that the score estimator is right
);

-- CREATE INDEX score_estimate ON scores (laplace_estimator);
