# Skillable ADX schema deployment (no Blob / SAS)

## What to deploy

Use **`Deployment/azuredeploy-inline.json`** as the ARM template for each Skillable student environment. It contains the complete SQL-free KQL schema from [`Scripts/advanced_kql_v2.kql`](../Scripts/advanced_kql_v2.kql) as the ADX database script resource's `scriptContent`.

There are **no Azure Storage dependencies, SAS parameters, runtime GitHub downloads, or Life Cycle Actions for schema creation**. Skillable can deploy this single template to each student's Azure resource group as before. The environment still uses a separate ADX cluster and database per deployment.

**Do not deploy `azuredeploy.base.json`**: it has build-time placeholders.

## What was preserved

- ADX cluster SKU: `Standard_D11_v2`, tier Standard, capacity 2
- East US 2, engine V3, auto-stop, system-assigned identity, public network access
- Database: `advkql-db`, 365-day soft delete, 1-hour hot cache
- Skillable automation application: `AllDatabasesAdmin`
- Lab Users CSR lod group: `AllDatabasesViewer`
- Script level: Database; continue on errors: false; script permission retention: retained
- Original outputs: ResourceGroupName, ClusterName, DatabaseName

## Updating the KQL schema

1. Edit and commit `Scripts/advanced_kql_v2.kql` in GitHub.
2. From the repository root run `python Deployment/generate_inline_arm.py`.
3. Review and commit the regenerated `Deployment/azuredeploy-inline.json`.
4. Update Skillable's ARM template with the generated JSON (or point the provisioning process to the approved, pinned template revision).
5. Test a **new** student environment before rollout.

The generator derives `scriptForceUpdateTag` from the Git blob SHA of the source KQL instead of using `newGuid()`. This prevents unrelated updates from automatically rerunning the database script on existing deployments.

### Important considerations

- Your source KQL uses `.create table` commands. This package leaves those statements **unchanged**. Updating/re-running it on an existing database is not automatically a schema migration; test against a fresh student environment, or convert the commands to an appropriate idempotent strategy.
- `Scripts/advanced_kql_v2.kql` currently creates **22 tables** and does **not** ingest dataset records. Any existing ingestion Life Cycle Action or other data-loading process must stay in place.
- This repository is currently **public**; table schema contents are publicly readable. Do not embed secrets, credentials, SAS tokens, CTF answer keys, or restricted data in KQL or ARM.
- Do not reinsert the old SAS token. Revoke it if still active.
- If the KQL grows significantly toward 1 MB, revisit how to package it; ARM has a 1 MB resource-definition limit and 4 MB template limit.
- This artifact is syntactically generated from the reviewed KQL. Run a Skillable test deployment to verify live ADX service behavior and permissions.

## Direct deployment smoke test (optional)

Run `az deployment group validate --resource-group <test-rg> --template-file Deployment/azuredeploy-inline.json` with an authenticated Azure CLI session. This is a template validation, **not** a complete live Skillable end-to-end test.

For related docs see Microsoft Learn: https://learn.microsoft.com/en-us/azure/templates/microsoft.kusto/clusters/databases/scripts
