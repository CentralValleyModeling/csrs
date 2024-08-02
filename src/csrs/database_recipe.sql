CREATE TABLE assumptions (
	id INTEGER NOT NULL, 
	name VARCHAR NOT NULL, 
	kind VARCHAR NOT NULL, 
	detail VARCHAR NOT NULL, 
	PRIMARY KEY (id), 
	CONSTRAINT unique_name UNIQUE (name, kind), 
	CONSTRAINT unique_detail UNIQUE (detail, kind)
);

CREATE TABLE scenario_assumptions (
	id INTEGER NOT NULL, 
	scenario_id INTEGER NOT NULL, 
	assumption_kind VARCHAR NOT NULL, 
	assumption_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(scenario_id) REFERENCES scenarios (id), 
	FOREIGN KEY(assumption_id) REFERENCES assumptions (id)
);

CREATE TABLE scenarios (
	id INTEGER NOT NULL, 
	name VARCHAR NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (name)
);

CREATE TABLE runs (
	id INTEGER NOT NULL, 
	scenario_id INTEGER NOT NULL, 
	parent_id INTEGER, 
	contact VARCHAR NOT NULL, 
	confidential BOOLEAN NOT NULL, 
	published BOOLEAN NOT NULL, 
	code_version VARCHAR NOT NULL, 
	detail VARCHAR NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(scenario_id) REFERENCES scenarios (id), 
	FOREIGN KEY(parent_id) REFERENCES runs (id)
);

CREATE TABLE preferred_versions (
	scenario_id INTEGER NOT NULL, 
	run_id INTEGER NOT NULL, 
	PRIMARY KEY (scenario_id), 
	CONSTRAINT unique_preference UNIQUE (scenario_id, run_id), 
	FOREIGN KEY(scenario_id) REFERENCES scenarios (id), 
	FOREIGN KEY(run_id) REFERENCES runs (id)
);

CREATE TABLE run_history (
	id INTEGER NOT NULL, 
	run_id INTEGER NOT NULL, 
	scenario_id INTEGER NOT NULL, 
	version VARCHAR NOT NULL, 
	PRIMARY KEY (id), 
	CONSTRAINT unique_run UNIQUE (scenario_id, run_id), 
	CONSTRAINT unique_version UNIQUE (scenario_id, version), 
	FOREIGN KEY(run_id) REFERENCES runs (id), 
	FOREIGN KEY(scenario_id) REFERENCES scenarios (id)
);

CREATE TABLE common_catalog (
	id INTEGER NOT NULL, 
	run_id INTEGER NOT NULL, 
	path_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(run_id) REFERENCES runs (id), 
	FOREIGN KEY(path_id) REFERENCES named_paths (id)
);

CREATE TABLE named_paths (
	id INTEGER NOT NULL, 
	name VARCHAR NOT NULL, 
	path VARCHAR NOT NULL, 
	category VARCHAR NOT NULL, 
	period_type VARCHAR(8) NOT NULL, 
	interval VARCHAR(6) NOT NULL, 
	detail VARCHAR NOT NULL, 
	units VARCHAR NOT NULL, 
	PRIMARY KEY (id), 
	CONSTRAINT unique_purpose UNIQUE (name, category)
);

CREATE TABLE timeseries_ledger (
	id INTEGER NOT NULL, 
	run_id INTEGER NOT NULL, 
	path_id INTEGER NOT NULL, 
	datetime FLOAT NOT NULL, 
	value FLOAT NOT NULL, 
	PRIMARY KEY (id), 
	CONSTRAINT unique_datapoint UNIQUE (run_id, path_id, datetime), 
	FOREIGN KEY(run_id) REFERENCES runs (id), 
	FOREIGN KEY(path_id) REFERENCES named_paths (id)
);

CREATE TABLE metrics (
	id INTEGER NOT NULL, 
	name VARCHAR NOT NULL, 
	x_detail VARCHAR NOT NULL, 
	detail VARCHAR NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (name)
);

CREATE TABLE metric_values (
	path_id INTEGER NOT NULL, 
	run_id INTEGER NOT NULL, 
	metric_id INTEGER NOT NULL, 
	x INTEGER NOT NULL, 
	units VARCHAR NOT NULL, 
	value FLOAT NOT NULL, 
	PRIMARY KEY (path_id, run_id, metric_id), 
	FOREIGN KEY(path_id) REFERENCES named_paths (id), 
	FOREIGN KEY(run_id) REFERENCES runs (id), 
	FOREIGN KEY(metric_id) REFERENCES metrics (id)
);

