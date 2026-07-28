# Changelog

## [0.7.2](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/compare/0.7.2...0.7.2) (2026-07-28)


### Features

* Add AI.AGG function to Data Agent Kit ([9431ff2](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/commit/9431ff2d66468dcbe578499367699eba6cf03af3))
* Add codex-install.ps1 script for Windows installation ([#33](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/issues/33)) ([85de74d](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/commit/85de74d9d7f70b82964fbab88f58961d8e788b09))
* Add create_notebook and get_cell_outputs tools ([#27](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/issues/27)) ([06d5e67](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/commit/06d5e679479cd604a2cc98c1878064a55df9e24a))
* add notebook MCP configuration for Gemini, Codex, and Claude plugins ([#19](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/issues/19)) ([c3f2d4d](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/commit/c3f2d4d3d2cea1b3563f6dcc99e84e46e8456da8))
* Add Standalone Notebook MCP Server ([#4](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/issues/4)) ([0ec4307](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/commit/0ec4307d541195c10972ebec32de7764617d6bd3))
* Bigtable MCP support ([26f175e](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/commit/26f175e8e3f29a5e4103a05a102a522a5dcd7861)), refs [#146](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/issues/146)
* Bigtable MCP support ([c58f5e9](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/commit/c58f5e9d98d9cf94052d049712af8d27e03be5c8)), refs [#146](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/issues/146)
* bootstrap repository with data-cloud-ai-dev-kit structure and skills ([#1](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/issues/1)) ([6958559](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/commit/695855962702b2e33677f830dc1820b046f55071))
* Bundle IDE Proxy and Implement Resilience Fallback ([#16](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/issues/16)) ([6b160e5](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/commit/6b160e58cf16a7cf870436d88dafa9839509b2b0))
* Duplicate graph-schema component to bigquery skill ([b5bc330](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/commit/b5bc330f03758618e63cecd8e47c5f1ac87af2c1))
* Feature/codex install update ([#35](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/issues/35)) ([ac4d3b2](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/commit/ac4d3b20e35c776ee0c5a5aaffb71b06772b3df5))
* gcp-managed-airflow-migration - a new skill for Airflow code migration ([de2d876](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/commit/de2d876d6d3a8f555df2f833b3a2db5ef07d194e))
* Infer IDE from process tree ([#40](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/issues/40)) ([f3ccd0d](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/commit/f3ccd0dda4e5d97504e2f90b98376096301f9b01))
* Modularize BigQuery skills in data_agent_common ([b29c63a](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/commit/b29c63acb4e3d7f44b51bc8cb68785bb4d2a170f))
* prompt and configure GCP and BigQuery variables during installation ([#54](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/issues/54)) ([e12d327](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/commit/e12d3279b5bd97e88522427510d18dd7a43c1626))
* Remove DB skills, which are just wrappers on MCP toolbox from data agent common. Will add helpful skills once we come up with them. ([a9beba2](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/commit/a9beba24337cd4d9994ece7faab4adadd7e19bdb))
* rename plugin to dak and remove toolbox from mcp server names ([#99](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/issues/99)) ([cb3a6e8](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/commit/cb3a6e85b7b0607c09479216597a92f0dcf693ce))
* separate MCP configurations for Claude and Codex ([#49](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/issues/49)) ([33bbdd9](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/commit/33bbdd95b59610ee503e8ee3f63a761f9f214990))
* **skills:** Add AlloyDB Omni skills ([94b8582](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/commit/94b858250a5e099daa0ea9803077d0129d06cf14))
* **skills:** Add AlloyDB skills ([fb5bd8b](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/commit/fb5bd8b96bbdc5507a32df236efa50df9b5ef638))
* **skills:** Add Cloud SQL MySQL skills ([7f2442a](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/commit/7f2442abee545a2b75cdb3052be2482fb316cdbc))
* **skills:** Add Cloud SQL Postgres skills ([420e3ac](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/commit/420e3ac34deab005668e43a3507db160b760fb05))
* **skills:** Add Cloud SQL SQL Server skills ([7e887d0](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/commit/7e887d0836ab4d5e1bfc46307115b43ee2d9d7ec))
* **skills:** Add Firestore Native skills ([f6fa0df](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/commit/f6fa0df968b45f4760185135e88e26b76f9c35ca))
* **skills:** add github-release-skill and update Copybara reviewers ([ca05037](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/commit/ca050377cda6083ffa2be59785fb099150d6428e))
* **skills:** Add more IDE/environment values for resource attribution environment labels. ([3941694](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/commit/3941694cf37f326e81a74eeee514c2163d67c7f6))
* **skills:** Add Spanner skills ([c1dc599](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/commit/c1dc5990d698da3a9f82af390632d36b1880a2a7))
* **skills:** Clarify BQ label enforcement rules for resource attribution. ([c16b546](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/commit/c16b5465d6dba54f089e8ed8ac83d38ed5cc4aae))
* **skills:** Update bq label flag syntax in resource attribution skills. ([1ff44be](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/commit/1ff44bec65a1a7913e772892c9a2542006c584b2))
* split notebook and visualization MCP servers ([#51](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/issues/51)) ([3e4c2d1](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/commit/3e4c2d16f06c90c44b9c0df51ae8c91ef452d559))
* Sync data cloud skills ([#31](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/issues/31)) ([1ff456e](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/commit/1ff456eee57ddafcf03aa5ab8d600b221a3166c2))
* Sync data cloud skills ([#38](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/issues/38)) ([b3f3350](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/commit/b3f3350f112f29d0652336e8686764953239f5c4))
* Syncing data cloud skills ([#24](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/issues/24)) ([152832e](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/commit/152832ea769663884df7a43c090175e9134a1c9c))
* Update BQ ai_function_best_practices and constraints. ([f4394e1](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/commit/f4394e1e9de1d877af3238e9d332f0f259aa7bb9))
* Update DAK Skill to support Gemini CLI, Claude Code, and Codex attribution tags ([e1922d8](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/commit/e1922d8efb1770ed54d7a9758d3a5f7863b1f5a6))
* update skills from cloudtop ([#70](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/issues/70)) ([f094668](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/commit/f0946689ea9b5bd1f1a56225b24d5f5f4da95f87))
* viz mcp aggregator ([#21](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/issues/21)) ([400b33b](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/commit/400b33b968c839dccb0daa67c3737db73c5cf44b))


### Bug Fixes

* add missing notebook_guidance skill and fix data-autocleaning markdown formatting ([#6](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/issues/6)) ([3461cd9](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/commit/3461cd9f044e94cf89b5e90513ebf945e61f8863))
* Fix telemetry hook configurations for Codex, Claude Code, and Gemini CLI. ([b93ca2e](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/commit/b93ca2ea387872d2b7378b0e56671cedf3d32517))
* remove default hooks ([1171475](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/commit/1171475ffa60507cf06eaa5d9a1b459db467b670))
* restore repository dotfiles and workflows deleted by sync ([#114](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/issues/114)) ([beea04b](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/commit/beea04b27a778c95f92134f8140bf5c8b6eb8ab8))
* set correct plugin path in Codex installer script ([#5](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/issues/5)) ([64195b6](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/commit/64195b605d882cf7a1e634655bc61813b93e650a))
* Update codex commands version ([#56](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/issues/56)) ([f78aa61](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/commit/f78aa61e586f01b45581149bd5b9a2c3f9de70fd))
* Update skill references and bump version in dataform and dbt. ([879f134](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/commit/879f13499d5566ce2146050c2a8bce44abd69526))
* use tags for codex installation scripts ([#52](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/issues/52)) ([6cd5114](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/commit/6cd5114531dc807c9b8894b3511bb7b399afabad))
* use v4 tag for setup-node in workflow ([#14](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/issues/14)) ([2d72fff](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/commit/2d72fffed3a7f8c14cf2450d03f7895d1de4ab2d))


### Miscellaneous Chores

* force release 0.2.0 ([#72](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/issues/72)) ([90311ce](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/commit/90311cea40d6ebac8189fcced17e5b98d384e681))
* force release 0.4.0 ([#93](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/issues/93)) ([23aab90](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/commit/23aab90cf7a198e8481dce1475020e14014a7ebe))
* force release 0.6.1 ([e259079](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/commit/e259079e4f5a472d1c162063148da00fdf9b7599))
* force release 0.6.1 ([dbc59f7](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/commit/dbc59f7892b94e3672a526d3eb9d5c865c218a85))
* force release 0.7.0 ([3e89ba0](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/commit/3e89ba0527440893bcd085aa69fd1943c9e2c576))
* force release 0.7.2 ([62d2f9c](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/commit/62d2f9c5504297893251a32ca92ec34c5ae2eb67))
* release 0.1.0 ([#44](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/issues/44)) ([770de4e](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/commit/770de4ea7ee296bb1f69684eddfc9ed8b5bf76a4))

## [0.7.2](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/compare/0.7.1...0.7.2) (2026-07-28)


### Features

* **skills:** Clarify BQ label enforcement rules for resource attribution. ([c16b546](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/commit/c16b5465d6dba54f089e8ed8ac83d38ed5cc4aae))
* **skills:** Update bq label flag syntax in resource attribution skills. ([1ff44be](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/commit/1ff44bec65a1a7913e772892c9a2542006c584b2))


### Miscellaneous Chores

* force release 0.7.2 ([62d2f9c](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/commit/62d2f9c5504297893251a32ca92ec34c5ae2eb67))

## [0.7.1](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/compare/0.7.0...0.7.1) (2026-07-27)


### Bug Fixes

* remove default hooks ([1171475](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/commit/1171475ffa60507cf06eaa5d9a1b459db467b670))

## [0.7.0](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/compare/0.6.1...0.7.0) (2026-07-24)


### Features

* Add AI.AGG function to Data Agent Kit ([9431ff2](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/commit/9431ff2d66468dcbe578499367699eba6cf03af3))
* Bigtable MCP support ([26f175e](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/commit/26f175e8e3f29a5e4103a05a102a522a5dcd7861)), refs [#146](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/issues/146)
* Bigtable MCP support ([c58f5e9](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/commit/c58f5e9d98d9cf94052d049712af8d27e03be5c8)), refs [#146](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/issues/146)
* Modularize BigQuery skills in data_agent_common ([b29c63a](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/commit/b29c63acb4e3d7f44b51bc8cb68785bb4d2a170f))
* Remove DB skills, which are just wrappers on MCP toolbox from data agent common. Will add helpful skills once we come up with them. ([a9beba2](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/commit/a9beba24337cd4d9994ece7faab4adadd7e19bdb))
* **skills:** Add more IDE/environment values for resource attribution environment labels. ([3941694](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/commit/3941694cf37f326e81a74eeee514c2163d67c7f6))
* Update BQ ai_function_best_practices and constraints. ([f4394e1](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/commit/f4394e1e9de1d877af3238e9d332f0f259aa7bb9))


### Bug Fixes

* Fix telemetry hook configurations for Codex, Claude Code, and Gemini CLI. ([b93ca2e](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/commit/b93ca2ea387872d2b7378b0e56671cedf3d32517))
* Update skill references and bump version in dataform and dbt. ([879f134](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/commit/879f13499d5566ce2146050c2a8bce44abd69526))


### Miscellaneous Chores

* force release 0.7.0 ([3e89ba0](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/commit/3e89ba0527440893bcd085aa69fd1943c9e2c576))

## [0.6.1](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/compare/0.4.0...0.6.1) (2026-07-10)


### Features

* Duplicate graph-schema component to bigquery skill ([b5bc330](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/commit/b5bc330f03758618e63cecd8e47c5f1ac87af2c1))
* gcp-managed-airflow-migration - a new skill for Airflow code migration ([de2d876](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/commit/de2d876d6d3a8f555df2f833b3a2db5ef07d194e))
* rename plugin to dak and remove toolbox from mcp server names ([#99](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/issues/99)) ([cb3a6e8](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/commit/cb3a6e85b7b0607c09479216597a92f0dcf693ce))
* **skills:** Add AlloyDB Omni skills ([94b8582](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/commit/94b858250a5e099daa0ea9803077d0129d06cf14))
* **skills:** Add AlloyDB skills ([fb5bd8b](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/commit/fb5bd8b96bbdc5507a32df236efa50df9b5ef638))
* **skills:** Add Cloud SQL MySQL skills ([7f2442a](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/commit/7f2442abee545a2b75cdb3052be2482fb316cdbc))
* **skills:** Add Cloud SQL Postgres skills ([420e3ac](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/commit/420e3ac34deab005668e43a3507db160b760fb05))
* **skills:** Add Cloud SQL SQL Server skills ([7e887d0](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/commit/7e887d0836ab4d5e1bfc46307115b43ee2d9d7ec))
* **skills:** Add Firestore Native skills ([f6fa0df](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/commit/f6fa0df968b45f4760185135e88e26b76f9c35ca))
* **skills:** add github-release-skill and update Copybara reviewers ([ca05037](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/commit/ca050377cda6083ffa2be59785fb099150d6428e))
* **skills:** Add Spanner skills ([c1dc599](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/commit/c1dc5990d698da3a9f82af390632d36b1880a2a7))
* Update DAK Skill to support Gemini CLI, Claude Code, and Codex attribution tags ([e1922d8](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/commit/e1922d8efb1770ed54d7a9758d3a5f7863b1f5a6))


### Bug Fixes

* restore repository dotfiles and workflows deleted by sync ([#114](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/issues/114)) ([beea04b](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/commit/beea04b27a778c95f92134f8140bf5c8b6eb8ab8))


### Miscellaneous Chores

* force release 0.6.1 ([e259079](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/commit/e259079e4f5a472d1c162063148da00fdf9b7599))
* force release 0.6.1 ([dbc59f7](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/commit/dbc59f7892b94e3672a526d3eb9d5c865c218a85))

## [0.4.0](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/compare/0.2.0...0.4.0) (2026-06-11)


### Miscellaneous Chores

* force release 0.4.0 ([#93](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/issues/93)) ([23aab90](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/commit/23aab90cf7a198e8481dce1475020e14014a7ebe))

## [0.2.0](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/compare/0.1.4...0.2.0) (2026-05-15)


### Features

* update skills from cloudtop ([#70](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/issues/70)) ([f094668](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/commit/f0946689ea9b5bd1f1a56225b24d5f5f4da95f87))


### Miscellaneous Chores

* force release 0.2.0 ([#72](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/issues/72)) ([90311ce](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/commit/90311cea40d6ebac8189fcced17e5b98d384e681))

## [0.1.4](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/compare/0.1.3...0.1.4) (2026-05-07)


### Features

* prompt and configure GCP and BigQuery variables during installation ([#54](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/issues/54)) ([e12d327](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/commit/e12d3279b5bd97e88522427510d18dd7a43c1626))

## [0.1.3](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/compare/0.1.2...0.1.3) (2026-05-06)


### Bug Fixes

* Update codex commands version ([#56](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/issues/56)) ([f78aa61](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/commit/f78aa61e586f01b45581149bd5b9a2c3f9de70fd))

## [0.1.2](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/compare/0.1.1...0.1.2) (2026-05-04)


### Features

* split notebook and visualization MCP servers ([#51](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/issues/51)) ([3e4c2d1](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/commit/3e4c2d16f06c90c44b9c0df51ae8c91ef452d559))


### Bug Fixes

* use tags for codex installation scripts ([#52](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/issues/52)) ([6cd5114](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/commit/6cd5114531dc807c9b8894b3511bb7b399afabad))

## [0.1.1](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/compare/0.1.0...0.1.1) (2026-04-28)


### Features

* separate MCP configurations for Claude and Codex ([#49](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/issues/49)) ([33bbdd9](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/commit/33bbdd95b59610ee503e8ee3f63a761f9f214990))

## [0.1.0](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/compare/0.1.8...0.1.0) (2026-04-20)


### Features

* Feature/codex install update ([#35](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/issues/35)) ([ac4d3b2](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/commit/ac4d3b20e35c776ee0c5a5aaffb71b06772b3df5))
* Infer IDE from process tree ([#40](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/issues/40)) ([f3ccd0d](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/commit/f3ccd0dda4e5d97504e2f90b98376096301f9b01))
* Sync data cloud skills ([#38](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/issues/38)) ([b3f3350](https://github.com/gemini-cli-extensions/data-agent-kit-starter-pack/commit/b3f3350f112f29d0652336e8686764953239f5c4))
