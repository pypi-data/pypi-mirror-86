-- Auto-constructed DDL file from version 4e056ca



-- roles/admin.sql

DO
$query$
BEGIN
  IF NOT EXISTS (SELECT * FROM pg_catalog.pg_roles WHERE rolname = 'admin')
  THEN
    CREATE ROLE admin NOSUPERUSER NOCREATEDB NOCREATEROLE NOINHERIT NOLOGIN NOREPLICATION NOBYPASSRLS;
  END IF;
END
$query$;


-- roles/reader.sql

DO
$query$
BEGIN
  IF NOT EXISTS (SELECT * FROM pg_catalog.pg_roles WHERE rolname = 'reader')
  THEN
    CREATE ROLE reader NOSUPERUSER NOCREATEDB NOCREATEROLE NOINHERIT NOLOGIN NOREPLICATION NOBYPASSRLS;
  END IF;
END
$query$;


-- roles/writer.sql

DO
$query$
BEGIN
  IF NOT EXISTS (SELECT * FROM pg_catalog.pg_roles WHERE rolname = 'writer')
  THEN
    CREATE ROLE writer INHERIT NOSUPERUSER NOCREATEDB NOCREATEROLE NOLOGIN NOREPLICATION NOBYPASSRLS;
  END IF;
END
$query$;

SET client_min_messages TO WARNING;

GRANT reader TO writer;

SET client_min_messages TO INFO;


-- roles/imbi.sql

DO
$query$
BEGIN
  IF NOT EXISTS (SELECT * FROM pg_catalog.pg_roles WHERE rolname = 'imbi')
  THEN
    CREATE ROLE imbi INHERIT NOCREATEROLE NOCREATEDB LOGIN PASSWORD 'imbi';
  END IF;
END
$query$;

ALTER USER imbi SET statement_timeout = 60000;  -- Maximum duration for a query
ALTER USER imbi SET idle_in_transaction_session_timeout = 60000; -- Maximum idle in transaction

SET client_min_messages TO WARNING;

GRANT reader TO imbi;
GRANT writer TO imbi;

SET client_min_messages TO INFO;


-- extensions/uuid.sql

CREATE EXTENSION "uuid-ossp";


-- schemata/v1.sql

CREATE SCHEMA v1;

GRANT USAGE ON SCHEMA v1 TO PUBLIC;


-- types/v1/cookie_cutter_type.sql

SET search_path=v1;

CREATE TYPE cookie_cutter_type AS ENUM ('project', 'dashboard');

COMMENT ON TYPE cookie_cutter_type IS 'Used to specify the type of cookie cutter in v1.cookie_cutters';


-- types/v1/entity_type.sql

SET search_path=v1;

CREATE TYPE entity_type AS ENUM ('internal', 'ldap');

COMMENT ON TYPE entity_type IS 'Used to track the type of authentication entity is record';


-- tables/v1/configuration_systems.sql

SET search_path=v1;

CREATE TABLE IF NOT EXISTS configuration_systems (
  "name"      TEXT NOT NULL PRIMARY KEY,
  created_at  TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
  modified_at TIMESTAMP WITH TIME ZONE,
  description TEXT,
  icon_class  TEXT NOT NULL DEFAULT 'fas fa-slider-h'
);

COMMENT ON TABLE configuration_systems IS 'Systems used for project configuration';
COMMENT ON COLUMN configuration_systems.name IS 'Configuration system name';
COMMENT ON COLUMN configuration_systems.created_at IS 'When the record was created at';
COMMENT ON COLUMN configuration_systems.modified_at IS 'When the record was last modified';
COMMENT ON COLUMN configuration_systems.description IS 'Description of the configuration system';
COMMENT ON COLUMN configuration_systems.icon_class IS 'Font Awesome UI icon class';

GRANT SELECT ON configuration_systems TO reader;
GRANT SELECT, INSERT, UPDATE, DELETE ON configuration_systems TO admin;


-- tables/v1/data_centers.sql

SET search_path=v1;

CREATE TABLE IF NOT EXISTS data_centers (
  "name"       TEXT NOT NULL PRIMARY KEY,
  created_at   TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
  modified_at  TIMESTAMP WITH TIME ZONE,
  description  TEXT,
  icon_class   TEXT NOT NULL DEFAULT 'fas fa-globe'
);

COMMENT ON TABLE data_centers IS 'Data Centers';
COMMENT ON COLUMN data_centers.name IS 'Data Center name';
COMMENT ON COLUMN data_centers.created_at IS 'When the record was created at';
COMMENT ON COLUMN data_centers.modified_at IS 'When the record was last modified';
COMMENT ON COLUMN data_centers.description IS 'Description of the data center';
COMMENT ON COLUMN data_centers.icon_class IS 'Font Awesome UI icon class';

GRANT SELECT ON data_centers TO reader;
GRANT SELECT, INSERT, UPDATE, DELETE ON data_centers TO admin;


-- tables/v1/deployment_types.sql

SET search_path=v1;

CREATE TABLE IF NOT EXISTS deployment_types (
  "name"      TEXT NOT NULL PRIMARY KEY,
  created_at  TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
  modified_at TIMESTAMP WITH TIME ZONE,
  description TEXT,
  icon_class  TEXT NOT NULL DEFAULT 'fas fa-box'
);

COMMENT ON TABLE deployment_types IS 'Types of project deployment systems';
COMMENT ON COLUMN deployment_types.name IS 'Deployment Type name';
COMMENT ON COLUMN deployment_types.created_at IS 'When the record was created at';
COMMENT ON COLUMN deployment_types.modified_at IS 'When the record was last modified';
COMMENT ON COLUMN deployment_types.description IS 'Description of the deployment type';
COMMENT ON COLUMN deployment_types.icon_class IS 'Font Awesome UI icon class';

GRANT SELECT ON deployment_types TO reader;
GRANT SELECT, INSERT, UPDATE, DELETE ON deployment_types TO admin;


-- tables/v1/environments.sql

SET search_path=v1;

CREATE TABLE IF NOT EXISTS environments (
  "name"      TEXT NOT NULL PRIMARY KEY,
  created_at  TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
  modified_at TIMESTAMP WITH TIME ZONE,
  description TEXT,
  icon_class  TEXT DEFAULT 'fas fa-mountain'
);

COMMENT ON TABLE environments IS 'Operational Environments';
COMMENT ON COLUMN environments.name IS 'Environment name';
COMMENT ON COLUMN environments.created_at IS 'When the record was created at';
COMMENT ON COLUMN environments.modified_at IS 'When the record was last modified';
COMMENT ON COLUMN environments.icon_class IS 'Font Awesome UI icon class';

GRANT SELECT ON environments TO reader;
GRANT SELECT, INSERT, UPDATE, DELETE ON environments TO admin;


-- tables/v1/groups.sql

SET search_path=v1;

CREATE TABLE IF NOT EXISTS groups (
  "name"      TEXT                     NOT NULL PRIMARY KEY,
  created_at  TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
  modified_at TIMESTAMP WITH TIME ZONE,
  group_type  entity_type              NOT NULL DEFAULT 'internal',
  external_id TEXT                     CONSTRAINT nullable_external_id
                                                  CHECK ((external_id IS NOT NULL AND group_type <> 'internal') OR
                                                         (external_id IS NULL and group_type = 'internal')),
  permissions TEXT[]
);

CREATE UNIQUE INDEX groups_external_id ON groups (external_id) WHERE external_id IS NOT NULL;

COMMENT ON TABLE groups IS 'User Groups';

COMMENT ON COLUMN groups.name IS 'The name used to reference the group in Imbi';
COMMENT ON COLUMN groups.created_at IS 'When the record was created at';
COMMENT ON COLUMN groups.modified_at IS 'When the record was was last modified at';
COMMENT ON COLUMN groups.group_type IS 'Indicates if the group is managed by Imbi or externally via LDAP (or other system)';
COMMENT ON COLUMN groups.external_id IS 'If the group is externally managed, the ID in the external system';
COMMENT ON COLUMN groups.permissions IS 'Array of permissions to grant members of the group';

GRANT SELECT ON groups TO reader;
GRANT SELECT, INSERT, UPDATE, DELETE ON groups TO admin;




-- tables/v1/orchestration_systems.sql

SET search_path=v1;

CREATE TABLE IF NOT EXISTS orchestration_systems (
  "name"      TEXT NOT NULL PRIMARY KEY,
  created_at  TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
  modified_at TIMESTAMP WITH TIME ZONE,
  description TEXT,
  icon_class  TEXT NOT NULL DEFAULT 'fas fa-hand-point-right'
);

COMMENT ON TABLE orchestration_systems IS 'Systems used for project orchestration';
COMMENT ON COLUMN orchestration_systems.name IS 'Orchestration system name';
COMMENT ON COLUMN orchestration_systems.created_at IS 'When the record was created at';
COMMENT ON COLUMN orchestration_systems.modified_at IS 'When the record was last modified';
COMMENT ON COLUMN orchestration_systems.description IS 'Description of the orchestration system';
COMMENT ON COLUMN orchestration_systems.icon_class IS 'Font Awesome UI icon class';

GRANT SELECT ON orchestration_systems TO reader;
GRANT SELECT, INSERT, UPDATE, DELETE ON orchestration_systems TO admin;


-- tables/v1/teams.sql

SET search_path=v1, public, pg_catalog;

CREATE TABLE IF NOT EXISTS teams (
  "name"      TEXT NOT NULL PRIMARY KEY,
  created_at  TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
  modified_at TIMESTAMP WITH TIME ZONE,
  slug        TEXT NOT NULL UNIQUE,
  icon_class  TEXT NOT NULL,
  "group"     TEXT,
  FOREIGN KEY ("group") REFERENCES v1.groups (name) ON DELETE CASCADE ON UPDATE CASCADE
);

COMMENT ON TABLE teams IS 'Organizational Teams';
COMMENT ON COLUMN teams.name IS 'Team name';
COMMENT ON COLUMN teams.created_at IS 'When the record was created at';
COMMENT ON COLUMN teams.modified_at IS 'When the record was last modified';
COMMENT ON COLUMN teams.slug IS 'Team path slug / abbreviation';
COMMENT ON COLUMN teams.icon_class IS 'Font Awesome UI icon class';
COMMENT ON COLUMN teams.group IS 'Optional group that is associated with the team';

GRANT SELECT ON teams TO reader;
GRANT SELECT, INSERT, UPDATE, DELETE ON teams TO admin;


-- tables/v1/project_link_types.sql

SET search_path=v1;

CREATE TABLE IF NOT EXISTS project_link_types (
  link_type    TEXT NOT NULL PRIMARY KEY,
  created_at   TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
  modified_at  TIMESTAMP WITH TIME ZONE,
  icon_class   TEXT DEFAULT 'fas fa-link'
);

COMMENT ON TABLE project_link_types IS 'Table of the types of links allowed for a project';
COMMENT ON COLUMN project_link_types.link_type IS 'The project link type';
COMMENT ON COLUMN project_link_types.created_at IS 'When the record was created at';
COMMENT ON COLUMN project_link_types.modified_at IS 'When the record was last modified';
COMMENT ON COLUMN project_link_types.icon_class IS 'Font Awesome UI icon class';

GRANT SELECT ON project_link_types TO reader;
GRANT SELECT, INSERT, UPDATE, DELETE ON project_link_types TO admin;


-- tables/v1/project_types.sql

SET search_path=v1;

CREATE TABLE IF NOT EXISTS project_types (
   "name"       TEXT NOT NULL PRIMARY KEY,
   created_at   TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
   modified_at  TIMESTAMP WITH TIME ZONE,
   description  TEXT,
   slug         TEXT,
   icon_class   TEXT DEFAULT 'fas fa-box'
);

COMMENT ON TABLE project_types IS 'Service Types';
COMMENT ON COLUMN project_types.name IS 'The project type (API, Consumer, Database, etc)';
COMMENT ON COLUMN project_types.created_at IS 'When the record was created at';
COMMENT ON COLUMN project_types.modified_at IS 'When the record was last modified';
COMMENT ON COLUMN project_types.description IS 'Service Type Description';
COMMENT ON COLUMN project_types.slug IS 'Namespace Slug';
COMMENT ON COLUMN project_types.icon_class IS 'Font Awesome UI icon class';

GRANT SELECT ON project_types TO reader;
GRANT SELECT, INSERT, UPDATE, DELETE ON project_types TO admin;


-- tables/v1/projects.sql

SET search_path=v1, public, pg_catalog;

CREATE TABLE IF NOT EXISTS projects (
  id                   UUID NOT NULL PRIMARY KEY DEFAULT uuid_generate_v4(),
  created_at           TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
  modified_at          TIMESTAMP WITH TIME ZONE,
  "name"               TEXT NOT NULL,
  slug                 TEXT NOT NULL,
  description          TEXT,
  owned_by             TEXT NOT NULL,
  data_center          TEXT NOT NULL,
  project_type         TEXT NOT NULL,
  configuration_system TEXT,
  deployment_type      TEXT,
  orchestration_system TEXT,
  FOREIGN KEY (owned_by) REFERENCES teams ("name") ON UPDATE CASCADE ON DELETE RESTRICT,
  FOREIGN KEY (data_center) REFERENCES data_centers ("name") ON UPDATE CASCADE ON DELETE RESTRICT,
  FOREIGN KEY (project_type) REFERENCES project_types ("name") ON UPDATE CASCADE ON DELETE RESTRICT,
  FOREIGN KEY (configuration_system) REFERENCES configuration_systems ("name") ON UPDATE CASCADE ON DELETE RESTRICT,
  FOREIGN KEY (deployment_type) REFERENCES deployment_types ("name") ON UPDATE CASCADE ON DELETE RESTRICT,
  FOREIGN KEY (orchestration_system) REFERENCES orchestration_systems ("name") ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE UNIQUE INDEX unique_team_project_name ON projects (owned_by, "name");
CREATE UNIQUE INDEX unique_team_project_slug ON projects (owned_by, slug);

COMMENT ON TABLE projects IS 'Services';

COMMENT ON COLUMN projects.id IS 'Unique ID for the project';
COMMENT ON COLUMN projects.created_at IS 'When the record was created at';
COMMENT ON COLUMN projects.modified_at IS 'When the record was last modified';
COMMENT ON COLUMN projects.slug IS 'Service path slug / abbreviation';
COMMENT ON COLUMN projects.owned_by IS 'The name of the team that is responsible for the project';
COMMENT ON COLUMN projects.data_center IS 'The data center that the project is run in';
COMMENT ON COLUMN projects.project_type IS 'The type of project (API, Consumer, Database, etc)';
COMMENT ON COLUMN projects.configuration_system IS 'The system used to configure the project (Ansible, Consul, etc)';
COMMENT ON COLUMN projects.deployment_type IS 'How the project is deployed (Jenkins, GitLab-CI, etc)';
COMMENT ON COLUMN projects.orchestration_system IS 'The system used to manage the runtime state of the project (Kubernetes, Nomad, etc)';

GRANT SELECT ON projects TO reader;
GRANT SELECT, INSERT, UPDATE, DELETE ON projects TO writer;


-- tables/v1/project_dependencies.sql

SET search_path=v1, public, pg_catalog;

CREATE TABLE IF NOT EXISTS project_dependencies (
  project_id    UUID NOT NULL,
  dependency_id UUID NOT NULL,
  created_at    TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (project_id, dependency_id),
  FOREIGN KEY (project_id) REFERENCES projects (id) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (dependency_id) REFERENCES projects (id) ON DELETE CASCADE ON UPDATE CASCADE
);

COMMENT ON TABLE project_dependencies IS 'Relationships between a project and the projects that it depends upon';
COMMENT ON COLUMN project_dependencies.project_id IS 'The dependent project';
COMMENT ON COLUMN project_dependencies.dependency_id IS 'The project that is depended upon';
COMMENT ON COLUMN project_dependencies.created_at IS 'When the record was created at';

GRANT SELECT ON project_dependencies TO reader;
GRANT SELECT, INSERT, UPDATE, DELETE ON project_dependencies TO writer;


-- tables/v1/project_links.sql

SET search_path=v1, public, pg_catalog;

CREATE TABLE IF NOT EXISTS project_links (
  project_id    UUID NOT NULL,
  link_type     TEXT NOT NULL,
  url           TEXT NOT NULL,
  created_at    TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
  modified_at   TIMESTAMP WITH TIME ZONE,
  PRIMARY KEY   (project_id, url),
  FOREIGN KEY   (project_id) REFERENCES projects (id) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY   (link_type) REFERENCES project_link_types (link_type) ON DELETE RESTRICT ON UPDATE CASCADE
);

COMMENT ON TABLE project_links IS 'Service specific links';
COMMENT ON COLUMN project_links.project_id IS 'The project the link is for';
COMMENT ON COLUMN project_links.link_type IS 'The type of link';
COMMENT ON COLUMN project_links.url IS 'The URL of the link';
COMMENT ON COLUMN project_links.created_at IS 'When the record was created at';
COMMENT ON COLUMN project_links.modified_at IS 'When the record was last modified at';

GRANT SELECT ON project_links TO reader;
GRANT SELECT, INSERT, UPDATE, DELETE ON project_links TO writer;


-- tables/v1/users.sql

SET search_path=v1;

CREATE TABLE IF NOT EXISTS users (
  username      TEXT                     NOT NULL PRIMARY KEY,
  created_at    TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
  last_seen_at  TIMESTAMP WITH TIME ZONE,
  user_type     entity_type              NOT NULL DEFAULT 'internal',
  external_id   TEXT                     CONSTRAINT nullable_external_id
                                              CHECK ((external_id IS NOT NULL AND user_type <> 'internal') OR
                                                     (external_id IS NULL and user_type = 'internal')),
  email_address TEXT                     NOT NULL UNIQUE,
  display_name  TEXT                     NOT NULL,
  password      TEXT                     CONSTRAINT nullable_password
                                              CHECK ((password IS NOT NULL AND user_type = 'internal') OR
                                                     (password IS NULL and user_type <> 'internal'))
);

CREATE UNIQUE INDEX users_external_id ON users (external_id) WHERE external_id IS NOT NULL;

COMMENT ON COLUMN users.username IS 'The username used to login to Imbi';
COMMENT ON COLUMN users.created_at IS 'When the record was created at';
COMMENT ON COLUMN users.last_seen_at IS 'When the most recent request occurred at';
COMMENT ON COLUMN users.user_type IS 'Indicates if the user is managed by Imbi or externally via LDAP (or other system)';
COMMENT ON COLUMN users.external_id IS 'If the user is externally managed, the ID in the external system';
COMMENT ON COLUMN users.email_address IS 'The email address for the user';
COMMENT ON COLUMN users.display_name IS 'The value to display when referencing the user';
COMMENT ON COLUMN users.password IS 'The password for the user when the user is internally managed';

GRANT SELECT ON users TO reader;
GRANT SELECT, INSERT, UPDATE, DELETE ON users TO writer;




-- tables/v1/authentication_tokens.sql

SET search_path=v1, public;

CREATE TABLE IF NOT EXISTS authentication_tokens (
  token      UUID NOT NULL PRIMARY KEY DEFAULT uuid_generate_v4(),
  username   TEXT NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
  expires_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP + interval '1 year',
  FOREIGN KEY (username) REFERENCES users (username) ON DELETE CASCADE ON UPDATE CASCADE);

COMMENT ON TABLE authentication_tokens IS 'User created authentication tokens for interacting with the API';
COMMENT ON COLUMN authentication_tokens.token IS 'The authentication token value';
COMMENT ON COLUMN authentication_tokens.username IS 'The username used to login to Imbi referencing v1.users.username';
COMMENT ON COLUMN authentication_tokens.created_at IS 'When the token was created';
COMMENT ON COLUMN authentication_tokens.expires_at IS 'When the token expires';

GRANT SELECT ON authentication_tokens TO reader;
GRANT SELECT, INSERT, UPDATE, DELETE ON authentication_tokens TO writer;


-- tables/v1/cookie_cutters.sql

SET search_path=v1;

CREATE TABLE IF NOT EXISTS cookie_cutters (
  "name"       TEXT NOT NULL PRIMARY KEY,
  created_at   TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
  modified_at  TIMESTAMP WITH TIME ZONE,
  description  TEXT,
  "type"       cookie_cutter_type NOT NULL DEFAULT 'project',
  project_type TEXT NOT NULL,
  url          TEXT NOT NULL,
  FOREIGN KEY (project_type) REFERENCES v1.project_types ("name") ON DELETE CASCADE ON UPDATE CASCADE
);

COMMENT ON TABLE cookie_cutters IS 'Cookie Cutters';
COMMENT ON COLUMN cookie_cutters.name IS 'Cookie Cutter name';
COMMENT ON COLUMN cookie_cutters.created_at IS 'When the record was created at';
COMMENT ON COLUMN cookie_cutters.modified_at IS 'When the record was last modified';
COMMENT ON COLUMN cookie_cutters.description IS 'The description of the cookie cutter';
COMMENT ON COLUMN cookie_cutters.type IS 'The type of cookie cutter (project or dashboard)';
COMMENT ON COLUMN cookie_cutters.project_type IS 'The project type associated with the cookie cutter';
COMMENT ON COLUMN cookie_cutters.url IS 'The git URL to the cookie cutter';

GRANT SELECT ON cookie_cutters TO reader;
GRANT SELECT, INSERT, UPDATE, DELETE ON cookie_cutters TO admin;


-- tables/v1/group_members.sql

SET search_path=v1;

CREATE TABLE IF NOT EXISTS group_members (
  "group"   TEXT  NOT NULL,
  username TEXT  NOT NULL,
  PRIMARY KEY ("group", username),
  FOREIGN KEY ("group") REFERENCES v1.groups (name) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (username) REFERENCES v1.users (username) ON DELETE CASCADE ON UPDATE CASCADE);

COMMENT ON TABLE group_members IS 'Group Memberships';

COMMENT ON COLUMN group_members.group IS 'The group name the user is a member to';
COMMENT ON COLUMN group_members.username IS 'The user that is a member of the group';


-- functions/v1/group_name_from_ldap_dn.sql

SET search_path=v1, pg_catalog;

CREATE OR REPLACE FUNCTION group_name_from_ldap_dn(IN in_name TEXT, OUT name TEXT) AS $$
  SELECT substring(in_name FROM E'^[A-Za-z]+=([A-Za-z0-9\ _-]+),.*') AS name
$$ LANGUAGE sql SECURITY DEFINER;

COMMENT ON FUNCTION group_name_from_ldap_dn(IN in_name TEXT, OUT name TEXT) IS 'Extracts the name of a group from a LDAP DN';


-- functions/v1/maintain_group_membership_from_ldap_groups.sql

SET search_path=v1, pg_catalog;

CREATE OR REPLACE FUNCTION maintain_group_membership_from_ldap_groups(IN in_username TEXT, IN in_groups TEXT[])
RETURNS TEXT[] AS $$
DECLARE
  dn          TEXT;
  group_name  TEXT;
  group_names TEXT[];
BEGIN
  FOREACH dn IN ARRAY in_groups
  LOOP
    group_name := v1.group_name_from_ldap_dn(dn);

    -- Ensure the group exist in the v1.groups table
    INSERT INTO v1.groups (name, group_type, external_id)
         VALUES (group_name, 'ldap', dn)
             ON CONFLICT ("name") DO NOTHING;

    -- Insure thr group and user combo exists
    INSERT INTO v1.group_members ("group", username)
         VALUES (group_name, in_username)
             ON CONFLICT DO NOTHING;
  END LOOP;

    WITH groups AS (SELECT unnest(in_groups) AS "name")
  SELECT array_agg(v1.group_name_from_ldap_dn(groups.name))
    INTO group_names
    FROM groups
   ORDER BY group_name;

  -- Delete any LDAP group memberships not passed in
  DELETE FROM v1.group_members
        WHERE username = username
          AND "group" IN (SELECT "name"
                            FROM v1.groups
                           WHERE group_type = 'ldap'
                             AND "name" NOT IN (SELECT unnest(group_names)));

  -- Return the group names
  RETURN group_names;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;
