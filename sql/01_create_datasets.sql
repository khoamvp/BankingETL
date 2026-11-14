CREATE SCHEMA IF NOT EXISTS `{project_id}.bronze`
OPTIONS(location='{location}');

CREATE SCHEMA IF NOT EXISTS `{project_id}.staging`
OPTIONS(location='{location}');