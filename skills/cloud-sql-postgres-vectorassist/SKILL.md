---
name: cloud-sql-postgres-vectorassist
description: Use these skills to set up and optimize production-ready vector workloads by simply expressing your intent and performance requirements.
metadata:
  version: v1
  publisher: google
license: Apache-2.0
---

## Usage

All scripts can be executed using Node.js. Replace `<param_name>` and
`<param_value>` with actual values.

**Bash:** `node <skill_dir>/scripts/<script_name>.js '{"<param_name>":
"<param_value>"}'`

**PowerShell:** `node <skill_dir>/scripts/<script_name>.js '{\"<param_name>\":
\"<param_value>\"}'`

Note: The scripts automatically load the environment variables from various .env
files. Do not ask the user to set vars unless skill executions fails due to env
var absence.

## Scripts

### apply_spec

This tool automatically executes all the SQL recommendations associated with a
specific vector specification (spec_id) or table. It runs the necessary commands
in the correct sequence to provision the workload, marking each step as applied
once successful. Use this tool when the user has reviewed the generated
recommendations from a defined (or modified) spec and is ready to apply the
changes directly to their database instance to finalize the vector search setup.
This tool can be used as a follow-up action after invoking the 'define_spec' or
'modify_spec' tool.

#### Parameters

| Name        | Type   | Description        | Required | Default |
| :---------- | :----- | :----------------- | :------- | :------ |
| spec_id     | string | The unique ID of   | No       |         |
:             :        : the vector         :          :         :
:             :        : specification to   :          :         :
:             :        : apply.             :          :         :
| table_name  | string | The name of the    | No       |         |
:             :        : table to apply the :          :         :
:             :        : vector             :          :         :
:             :        : specification to   :          :         :
:             :        : (in case of a      :          :         :
:             :        : single spec        :          :         :
:             :        : defined on the     :          :         :
:             :        : table).            :          :         :
| column_name | string | The                | No       |         |
:             :        : text_column_name   :          :         :
:             :        : or                 :          :         :
:             :        : vector_column_name :          :         :
:             :        : of the spec to     :          :         :
:             :        : identify the exact :          :         :
:             :        : spec in case there :          :         :
:             :        : are multiple specs :          :         :
:             :        : defined on a       :          :         :
:             :        : table.             :          :         :
| schema_name | string | The schema name    | No       |         |
:             :        : for the table.     :          :         :

--------------------------------------------------------------------------------

### define_spec

This tool defines a new vector specification by capturing the user's intent and
requirements for a vector search workload. This generates a complete, ordered
set of SQL recommendations required to set up the database, embeddings, and
vector indexes. While highly customizable, any optional parameters left
unspecified will use internally determined defaults optimized for the specific
workload. Use this tool at the very beginning of the vector setup process when a
user first wants to configure a table for vector search, generate embeddings, or
create a new vector index.

#### Parameters

| Name                   | Type    | Description      | Required | Default |
| :--------------------- | :------ | :--------------- | :------- | :------ |
| table_name             | string  | Table name on    | Yes      |         |
:                        :         : which vector     :          :         :
:                        :         : workload needs   :          :         :
:                        :         : to be set up.    :          :         :
| schema_name            | string  | Schema           | No       |         |
:                        :         : containing the   :          :         :
:                        :         : given table.     :          :         :
| spec_id                | string  | Unique ID for    | No       |         |
:                        :         : the vector spec. :          :         :
:                        :         : Auto-generated,  :          :         :
:                        :         : if not           :          :         :
:                        :         : specified.       :          :         :
| vector_column_name     | string  | Column name for  | No       |         |
:                        :         : the column with  :          :         :
:                        :         : vector           :          :         :
:                        :         : embeddings.      :          :         :
| text_column_name       | string  | Column name for  | No       |         |
:                        :         : the column with  :          :         :
:                        :         : text on which    :          :         :
:                        :         : vector search    :          :         :
:                        :         : needs to be set  :          :         :
:                        :         : up.              :          :         :
| vector_index_type      | string  | Type of the      | No       |         |
:                        :         : vector index to  :          :         :
:                        :         : be created       :          :         :
:                        :         : (Allowed         :          :         :
:                        :         : inputs\: 'hnsw', :          :         :
:                        :         : 'ivfflat',       :          :         :
:                        :         : 'scann').        :          :         :
| embeddings_available   | boolean | Boolean          | No       |         |
:                        :         : parameter to     :          :         :
:                        :         : know if vector   :          :         :
:                        :         : embeddings are   :          :         :
:                        :         : already          :          :         :
:                        :         : available in the :          :         :
:                        :         : table.           :          :         :
| num_vectors            | integer | Number of        | No       |         |
:                        :         : vectors expected :          :         :
:                        :         : in the dataset.  :          :         :
| dimensionality         | integer | If vectors are   | No       |         |
:                        :         : already          :          :         :
:                        :         : generated, set   :          :         :
:                        :         : to dimension of  :          :         :
:                        :         : vectors. If not, :          :         :
:                        :         : set to           :          :         :
:                        :         : dimensionality   :          :         :
:                        :         : of the           :          :         :
:                        :         : embedding_model. :          :         :
| embedding_model        | string  | Optional         | No       |         |
:                        :         : parameter\:      :          :         :
:                        :         : Model to be used :          :         :
:                        :         : for generating   :          :         :
:                        :         : embeddings. If   :          :         :
:                        :         : not provided, it :          :         :
:                        :         : has an           :          :         :
:                        :         : internally       :          :         :
:                        :         : selected default :          :         :
:                        :         : value.           :          :         :
| prefilter_column_names | array   | Columns based on | No       |         |
:                        :         : which            :          :         :
:                        :         : prefiltering     :          :         :
:                        :         : will happen in   :          :         :
:                        :         : vector search    :          :         :
:                        :         : queries.         :          :         :
| distance_func          | string  | Distance         | No       |         |
:                        :         : function to be   :          :         :
:                        :         : used for         :          :         :
:                        :         : comparing        :          :         :
:                        :         : vectors (Allowed :          :         :
:                        :         : inputs\:         :          :         :
:                        :         : 'cosine', 'ip',  :          :         :
:                        :         : 'l2', 'l1').     :          :         :
| quantization           | string  | Quantization to  | No       |         |
:                        :         : be used for      :          :         :
:                        :         : creating the     :          :         :
:                        :         : vector indexes   :          :         :
:                        :         : (Allowed         :          :         :
:                        :         : inputs\: 'none', :          :         :
:                        :         : 'halfvec',       :          :         :
:                        :         : 'bit').          :          :         :
| memory_budget_kb       | integer | Maximum size in  | No       |         |
:                        :         : KB that the      :          :         :
:                        :         : index can        :          :         :
:                        :         : consume in       :          :         :
:                        :         : memory while     :          :         :
:                        :         : building.        :          :         :
| target_recall          | float   | The recall that  | No       |         |
:                        :         : the user would   :          :         :
:                        :         : like to target   :          :         :
:                        :         : with the given   :          :         :
:                        :         : index for        :          :         :
:                        :         : standard vector  :          :         :
:                        :         : queries.         :          :         :
| target_top_k           | integer | The top-K values | No       |         |
:                        :         : that need to be  :          :         :
:                        :         : retrieved for    :          :         :
:                        :         : the given query. :          :         :
| tune_vector_index      | boolean | Boolean          | No       |         |
:                        :         : parameter to     :          :         :
:                        :         : specify if the   :          :         :
:                        :         : auto tuning is   :          :         :
:                        :         : required for the :          :         :
:                        :         : index.           :          :         :

--------------------------------------------------------------------------------

### execute_sql

Use this tool to execute a single SQL statement.

#### Parameters

Name | Type   | Description         | Required | Default
:--- | :----- | :------------------ | :------- | :------
sql  | string | The sql to execute. | Yes      |

--------------------------------------------------------------------------------

### generate_query

This tool generates optimized SQL queries for vector search by leveraging the
metadata and vector specifications defined in a specific spec_id. It may return
a single query or a sequence of multiple SQL queries that can be executed
sequentially. Use this tool when a user wants to perform semantic or similarity
searches on their data. It serves as the primary actionable tool to invoke for
generating the executable SQL required to retrieve relevant results based on
vector similarity. The 'execute_sql' tool can be used as a follow-up action
after invoking this tool.

#### Parameters

| Name                   | Type    | Description        | Required | Default |
| :--------------------- | :------ | :----------------- | :------- | :------ |
| spec_id                | string  | Generate the       | No       |         |
:                        :         : vector query       :          :         :
:                        :         : corresponding to   :          :         :
:                        :         : this vector spec.  :          :         :
| table_name             | string  | Generate the       | No       |         |
:                        :         : vector query       :          :         :
:                        :         : corresponding to   :          :         :
:                        :         : this table (in     :          :         :
:                        :         : case of a single   :          :         :
:                        :         : spec defined on    :          :         :
:                        :         : the table).        :          :         :
| schema_name            | string  | Schema name for    | No       |         |
:                        :         : the table related  :          :         :
:                        :         : to the vector      :          :         :
:                        :         : query generation.  :          :         :
| column_name            | string  | text_column_name   | No       |         |
:                        :         : or                 :          :         :
:                        :         : vector_column_name :          :         :
:                        :         : of the spec to     :          :         :
:                        :         : identify the exact :          :         :
:                        :         : spec in case there :          :         :
:                        :         : are multiple specs :          :         :
:                        :         : defined on a       :          :         :
:                        :         : table.             :          :         :
| search_text            | string  | Text search for    | No       |         |
:                        :         : which query needs  :          :         :
:                        :         : to be generated.   :          :         :
:                        :         : Embeddings are     :          :         :
:                        :         : generated using    :          :         :
:                        :         : the model defined  :          :         :
:                        :         : in the vector      :          :         :
:                        :         : spec.              :          :         :
| search_vector          | string  | Vector for which   | No       |         |
:                        :         : query needs to be  :          :         :
:                        :         : generated. Only    :          :         :
:                        :         : one of search_text :          :         :
:                        :         : or search_vector   :          :         :
:                        :         : must be populated. :          :         :
| output_column_names    | array   | Column names to    | No       |         |
:                        :         : retrieve in the    :          :         :
:                        :         : output search      :          :         :
:                        :         : query. Defaults to :          :         :
:                        :         : retrieving all     :          :         :
:                        :         : columns.           :          :         :
| top_k                  | integer | Number of nearest  | No       |         |
:                        :         : neighbors to be    :          :         :
:                        :         : returned in the    :          :         :
:                        :         : vector search      :          :         :
:                        :         : query. Defaults    :          :         :
:                        :         : to 10.             :          :         :
| filter_expressions     | array   | Any filter         | No       |         |
:                        :         : expressions to be  :          :         :
:                        :         : applied on the     :          :         :
:                        :         : vector search      :          :         :
:                        :         : query.             :          :         :
| target_recall          | float   | The recall that    | No       |         |
:                        :         : the user would     :          :         :
:                        :         : like to target     :          :         :
:                        :         : with the given     :          :         :
:                        :         : query. Overrides   :          :         :
:                        :         : the spec-level     :          :         :
:                        :         : target_recall.     :          :         :
| iterative_index_search | boolean | Perform iterative  | No       |         |
:                        :         : index search for   :          :         :
:                        :         : filtered queries   :          :         :
:                        :         : to ensure enough   :          :         :
:                        :         : results are        :          :         :
:                        :         : returned.          :          :         :

--------------------------------------------------------------------------------

### modify_spec

This tool modifies an existing vector specification (identified by a required
spec_id) with new parameters or overrides. Upon modification, it automatically
recalculates and refreshes the list of generated SQL recommendations to match
the updated requirements. This tool provides a way to modify column(s) in the
vector spec before applying and taking action on the recommendations. While
highly customizable, any optional parameters left unspecified will use
internally determined defaults optimized for the specific workload. Use this
tool to modify configurations established via 'define_spec' tool such as
adjusting target recall, embedding models, or quantization settings, etc.

#### Parameters

| Name                   | Type    | Description    | Required | Default |
| :--------------------- | :------ | :------------- | :------- | :------ |
| spec_id                | string  | Unique ID for  | Yes      |         |
:                        :         : the vector     :          :         :
:                        :         : spec you want  :          :         :
:                        :         : to modify.     :          :         :
| table_name             | string  | Modify the     | No       |         |
:                        :         : table name on  :          :         :
:                        :         : which vector   :          :         :
:                        :         : workload needs :          :         :
:                        :         : to be set up.  :          :         :
| schema_name            | string  | Modify the     | No       |         |
:                        :         : schema         :          :         :
:                        :         : containing the :          :         :
:                        :         : given table.   :          :         :
| vector_column_name     | string  | Modify the     | No       |         |
:                        :         : column name    :          :         :
:                        :         : for the column :          :         :
:                        :         : with vector    :          :         :
:                        :         : embeddings.    :          :         :
| text_column_name       | string  | Modify the     | No       |         |
:                        :         : column name    :          :         :
:                        :         : for the column :          :         :
:                        :         : with text on   :          :         :
:                        :         : which vector   :          :         :
:                        :         : search needs   :          :         :
:                        :         : to be set up.  :          :         :
| vector_index_type      | string  | Modify the     | No       |         |
:                        :         : type of the    :          :         :
:                        :         : vector index   :          :         :
:                        :         : to be created  :          :         :
:                        :         : (Allowed       :          :         :
:                        :         : inputs\:       :          :         :
:                        :         : 'hnsw',        :          :         :
:                        :         : 'ivfflat',     :          :         :
:                        :         : 'scann').      :          :         :
| embeddings_available   | boolean | Modify whether | No       |         |
:                        :         : vector         :          :         :
:                        :         : embeddings are :          :         :
:                        :         : already        :          :         :
:                        :         : available in   :          :         :
:                        :         : the table.     :          :         :
| num_vectors            | integer | Modify the     | No       |         |
:                        :         : number of      :          :         :
:                        :         : vectors        :          :         :
:                        :         : expected in    :          :         :
:                        :         : the dataset.   :          :         :
| dimensionality         | integer | Modify the     | No       |         |
:                        :         : dimensionality :          :         :
:                        :         : of the vectors :          :         :
:                        :         : or embedding   :          :         :
:                        :         : model.         :          :         :
| embedding_model        | string  | Modify the     | No       |         |
:                        :         : model used for :          :         :
:                        :         : generating     :          :         :
:                        :         : embeddings.    :          :         :
| prefilter_column_names | array   | Modify the     | No       |         |
:                        :         : column(s)      :          :         :
:                        :         : based on which :          :         :
:                        :         : prefiltering   :          :         :
:                        :         : will happen in :          :         :
:                        :         : vector search  :          :         :
:                        :         : queries.       :          :         :
| distance_func          | string  | Modify the     | No       |         |
:                        :         : distance       :          :         :
:                        :         : function to be :          :         :
:                        :         : used for       :          :         :
:                        :         : comparing      :          :         :
:                        :         : vectors        :          :         :
:                        :         : (Allowed       :          :         :
:                        :         : inputs\:       :          :         :
:                        :         : 'cosine',      :          :         :
:                        :         : 'ip', 'l2',    :          :         :
:                        :         : 'l1').         :          :         :
| quantization           | string  | Modify the     | No       |         |
:                        :         : quantization   :          :         :
:                        :         : to be used for :          :         :
:                        :         : creating the   :          :         :
:                        :         : vector indexes :          :         :
:                        :         : (Allowed       :          :         :
:                        :         : inputs\:       :          :         :
:                        :         : 'none',        :          :         :
:                        :         : 'halfvec',     :          :         :
:                        :         : 'bit').        :          :         :
| memory_budget_kb       | integer | Modify the     | No       |         |
:                        :         : maximum size   :          :         :
:                        :         : that the index :          :         :
:                        :         : can consume in :          :         :
:                        :         : memory while   :          :         :
:                        :         : building.      :          :         :
| target_recall          | float   | Modify the     | No       |         |
:                        :         : recall that    :          :         :
:                        :         : the user would :          :         :
:                        :         : like to target :          :         :
:                        :         : with the given :          :         :
:                        :         : index.         :          :         :
| target_top_k           | integer | Modify the     | No       |         |
:                        :         : Top-K matching :          :         :
:                        :         : values that    :          :         :
:                        :         : need to be     :          :         :
:                        :         : retrieved for  :          :         :
:                        :         : the given      :          :         :
:                        :         : query.         :          :         :
| tune_vector_index      | boolean | Modify whether | No       |         |
:                        :         : to tune vector :          :         :
:                        :         : index build    :          :         :
:                        :         : and search     :          :         :
:                        :         : parameters.    :          :         :

--------------------------------------------------------------------------------
