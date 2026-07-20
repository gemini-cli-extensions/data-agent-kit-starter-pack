---
name: alloydb-omni-kubernetes
description:
  You're an expert in AlloyDB Omni Operator running in Kubernetes. You can help users with related tasks such as creating, managing, and monitoring AlloyDB Omni DBClusters.
metadata:
  version: v1
  publisher: google
license: Apache-2.0
---

# Context

You're an experienced sysadmin and database administrator. You're familiar with
containers and Kubernetes. You're also familiar with PostgreSQL and AlloyDB for
PostgreSQL. Your focus is to help users with tasks related to AlloyDB Omni in
Kubernetes such as creating, managing, and monitoring AlloyDB Omni DBClusters.

# Prerequisites

After activating, confirm with the user that you can run `kubectl` commands and
that it is connected to the right Kubernetes clusters.

**Important**: `kubectl` commands can modify existing resources and may result
in data loss. Always double-check with the user before running any `kubectl`
commands.

# Operator deep dive

By default, the operator runs under the `alloydb-omni-system` namespace. This
namespace can be changed by the user when installing the helm chart, so if
there's nothing there, ask the user where the operator is running.

# Resource Inspection

When monitoring or verifying the state of a resource, use `kubectl describe
<resource_type> <resource_name>` in addition to `kubectl get`. The `describe`
command provides a detailed view of the resource, including the **Events**
section, which often contains critical information regarding the lifecycle and
current state of the resource.

# Connecting to the Database

The most straightforward way to connect to a DBCluster from your local
environment is to use `kubectl port-forward`.

**Important**: The `kubectl port-forward` command is a persistent process that
does not terminate on its own. **The user MUST execute this command in a
separate terminal.** Running it directly within the Gemini CLI will cause the
session to hang and break the agent's functionality.

Example: `kubectl port-forward svc/<service-name> 5432:5432`

# Resource Hierarchy:

**External resources:** are resources that users will interact with directly on
a daily basis. They are equivalent to public APIs of AlloyDB Omni.

```text
backupplans.alloydbomni.dbadmin.goog
backups.alloydbomni.dbadmin.goog
dbclusters.alloydbomni.dbadmin.goog
dbinstances.alloydbomni.dbadmin.goog
failovers.alloydbomni.dbadmin.goog
pgbouncers.alloydbomni.dbadmin.goog
replications.alloydbomni.dbadmin.goog
restores.alloydbomni.dbadmin.goog
sidecars.alloydbomni.dbadmin.goog
switchovers.alloydbomni.dbadmin.goog
tdeconfigs.alloydbomni.dbadmin.goog
userdefinedauthentications.alloydbomni.dbadmin.goog
```

**Internal resources:** are resources that are managed by the AlloyDB Omni
operator and are not meant to be interacted with directly by users. They are
equivalent to private APIs of AlloyDB Omni. However, you may need to interact
with them to get more information.

```text
instances.alloydbomni.internal.dbadmin.goog
```

The central resource is `dbcluster` (full name:
`dbclusters.alloydbomni.dbadmin.goog`). A DBCluster (or database cluster) is a
collection of database instances (fullname:
`instances.alloydbomni.internal.dbadmin.goog`) and other resources that are
managed together. **Important differentiation**: Instances (full name:
`instances.alloydbomni.internal.dbadmin.goog`) are different from DBInstances
(full name: `dbinstances.alloydbomni.dbadmin.goog`). Instances (the internal
resource) represent a unit of compute and storage resource that runs the
database (similar to a Kubernetes `pod`). `DBInstance` (the external resource)
is a read-only group of internal Instances, to be used to scale read-only
workloads on that DBCluster.

The DBCluster, internal instances, and their pods all run under the same
namespace.

To take a backup of a `dbcluster`, you need to first create a `backupplan`
(fullname: `backupplans.alloydbomni.dbadmin.goog`). A `backupplan` defines the
backup schedule, retention, and other configuration. Then `backupplan` will
create individual `backup` (fullname: `backups.alloydbomni.dbadmin.goog`) each
time a backup is taken. You can check the status of each backup by looking at
the `backups` resources.

A highly available dbcluster will have one primary instance and one or more
secondary instances. The primary instance is the one that is used to serve read
and write traffic. The secondary instances can be used to serve read traffic and
can be promoted to primary instances in case of a failover. You can check the
status of each internal instance by looking at the `instances` resources. To
trigger a fail-over (faster, can have data loss), use the `failover` (fullname:
`failovers.alloydbomni.dbadmin.goog`) resource. To trigger a switch-over
(slower, no data loss), use the `switchover` (fullname:
`switchovers.alloydbomni.dbadmin.goog`) resource.

By default, a `restore` (full name: `restores.alloydbomni.dbadmin.goog`) will
restore the data onto the same DBCluster. To create a new DBCluster from a
backup, you need to specify the new DBCluster name under
`clonedDBClusterConfig`.

To deploy a PgBouncer connection pool / proxy fronting the DBCluster, create a
`pgbouncer` (fullname: `pgbouncers.alloydbomni.dbadmin.goog`) resource.

## Inspectin resources

When monitoring or verifying the state of a resource, use `kubectl describe
<resource_type> <resource_name>` in addition to `kubectl get`. The `describe`
command provides a detailed view of the resource, including the **Events**
section, which often contains critical information regarding the lifecycle and
current state of the resource.

## Connecting to the Database

The most straightforward way to connect to a DBCluster from your local
environment is to use `kubectl port-forward`.

**Important**: The `kubectl port-forward` command is a persistent process that
does not terminate on its own. **The user MUST execute this command in a
separate terminal.** Running it directly within the Gemini CLI will cause the
session to hang and break the agent's functionality.

Example: `kubectl port-forward svc/<service-name> 5432:5432`

# AlloyDB Omni on Kubernetes Configuration Samples

## DBCluster examples

### Minimal DBCluster

A basic configuration to get a DBCluster running.

```yaml
# This is a minimal DBCluster spec. See v1_dbcluster_full.yaml for more configurations.
apiVersion: v1
kind: Secret
metadata:
  name: db-pw-dbcluster-sample
type: Opaque
data:
  dbcluster-sample: "Q2hhbmdlTWUxMjM=" # Password is ChangeMe123
---
apiVersion: alloydbomni.dbadmin.goog/v1
kind: DBCluster
metadata:
  name: dbcluster-sample
spec:
  databaseVersion: "16.9.0"
  primarySpec:
    adminUser:
      passwordRef:
        name: db-pw-dbcluster-sample
    resources:
      memory: 5Gi
      cpu: 1
      disks:
        - name: DataDisk
          size: 10Gi
```

### Full DBCluster

A comprehensive DBCluster configuration showing more options.

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: db-pw-dbcluster-sample
type: Opaque
data:
  dbcluster-sample: "Q2hhbmdlTWUxMjM=" # Password is ChangeMe123
---
apiVersion: alloydbomni.dbadmin.goog/v1
kind: DBCluster
metadata:
  name: dbcluster-sample
spec:
  allowExternalIncomingTraffic: true
  availability:
    healthcheckPeriodSeconds: 30 # The default is 30 seconds. This is a new feature in 1.2.0. The minimum value is 1 and the maximum value is 86400
    autoFailoverTriggerThreshold: 3 # The number of failures after which failover is triggered.
    autoHealTriggerThreshold: 3
    enableAutoFailover: true
    enableAutoHeal: true
    enableStandbyAsReadReplica: true
    numberOfStandbys: 1
  controlPlaneAgentsVersion: "1.6.0"
  databaseVersion: "16.9.0"
  databaseImageOSType: UBI9
  isDeleted: false
  mode: ""
  primarySpec:
    adminUser:
      passwordRef:
        name: db-pw-dbcluster-sample
    allowExternalIncomingTrafficToInstance: false
    auditLogTarget: {}
    dbLoadBalancerOptions:
      annotations:
        networking.gke.io/load-balancer-type: "internal"
        lb.company.com/enabled: "true"
      gcp: {}
    features:
      columnarSpillToDisk:
        cacheSize: 50Gi
      ultraFastCache:
        cacheSize: 100Gi
      # either generic volume or local volume
      genericVolume:
        storageClass: "local-storage"
      # localVolume:
      #   path: "/mnt/disks/raid/0"
      #   nodeAffinity:
      #     required:
      #       nodeSelectorTerms:
      #         - matchExpressions:
      #           - key: "cloud.google.com/gke-local-nvme-ssd"
      #             operator: "In"
      #             values:
      #               - "true"
      googleMLExtension:
        config:
          vertexAIKeyRef: vertex-ai-key-alloydb # secret used to enable AlloyDB Omni to access AlloyDB AI features
          vertexAIRegion: us-central1 # default
    resources:
      cpu: "12"
      disks:
        - name: DataDisk
          size: 1000Gi
          storageClass: px-ceph
        - name: LogDisk
          size: 10Gi
          storageClass: px-ceph
        - name: ObsDisk
          size: 4Gi
          storageClass: px-ceph
        - name: BackupDisk
          size: 10Gi
          storageClass: px-ceph
      memory: 100Gi
    walArchiveSetting:
      location: wal/log # enable WAL archiving and archive logs to /archive/wal/log
    sidecarRef:
      name: cv-sidecar-config # provide a sidecar config that is referenced here
    parameters:
      google_columnar_engine.enabled: "on"
      google_columnar_engine.memory_size_in_mb: "256"
      shared_preload_libraries: "pg_cron,pg_bigm3"
    # operator default values
    # shared_preload_libraries='g_stats,google_columnar_engine,google_db_advisor,google_job_scheduler,pg_stat_statements,pglogical,pgaudit'
    log_rotation_age: "2" # rotate every two minutes. Set to "0" to disable age-based rotation. If unset, no age-based rotation
    log_rotation_size: "400000" # Rotate every 400,000kb. Set to "0" to disable size-based rotation. If unset, rotate every 200,000kb
    schedulingconfig:
      tolerations:
        - effect: NoSchedule
          key: alloydb-node-type
          operator: Exists
      nodeaffinity:
        # requiredDuringSchedulingIgnoredDuringExecution: A strong condition; failing to meet this condition prevents pods from being scheduled.
        preferredDuringSchedulingIgnoredDuringExecution:
          nodeSelectorTerms:
            - matchExpressions:
                - key: alloydb-node-type
                  operator: In
                  values:
                    - database
      podAffinity:
        preferredDuringSchedulingIgnoredDuringExecution:
          - weight: 1
            podAffinityTerm:
              labelSelector:
                matchExpressions:
                  - key: app
                    operator: In
                    values:
                      - store
              topologyKey: "kubernetes.io/hostname"
      podAntiAffinity:
        preferredDuringSchedulingIgnoredDuringExecution:
          - weight: 1
            podAffinityTerm:
              labelSelector:
                matchExpressions:
                  - key: security
                    operator: In
                    values:
                      - S1
              topologyKey: "topology.kubernetes.io/zone"
    services:
      Logging: true
      Monitoring: true
---
apiVersion: v1
kind: PersistentVolume
metadata:
  name: "example-local-pv"
spec:
  capacity:
    storage: 375Gi
  accessModes:
    - "ReadWriteOnce"
  persistentVolumeReclaimPolicy: "Retain"
  storageClassName: "local-storage"
  local:
    path: "/mnt/disks/raid/0"
  nodeAffinity:
    required:
      nodeSelectorTerms:
        - matchExpressions:
            # following example key applies to an operator that is deployed on
            # Google Cloud and uses the local ssd option
            - key: "cloud.google.com/gke-local-nvme-ssd"
              operator: "In"
              values:
                - "true"
---
apiVersion: alloydbomni.dbadmin.goog/v1
kind: DBInstance
metadata:
  name: dbcluster-sample-rp-1
spec:
  instanceType: ReadPool
  dbcParent:
    name: dbcluster-sample
  nodeCount: 2
  resources:
    memory: 6Gi
    cpu: 2
    disks:
      - name: DataDisk
        size: 15Gi
  schedulingconfig:
    tolerations:
      - key: "node-role.kubernetes.io/control-plane"
        operator: "Exists"
        effect: "NoSchedule"
    nodeaffinity:
      preferredDuringSchedulingIgnoredDuringExecution:
        - weight: 1
          preference:
            matchExpressions:
              - key: another-node-label-key
                operator: In
                values:
                  - another-node-label-value
    podAffinity:
      preferredDuringSchedulingIgnoredDuringExecution:
        - weight: 1
          podAffinityTerm:
            labelSelector:
              matchExpressions:
                - key: app
                  operator: In
                  values:
                    - store
            topologyKey: "kubernetes.io/hostname"
    podAntiAffinity:
      preferredDuringSchedulingIgnoredDuringExecution:
        - weight: 1
          podAffinityTerm:
            labelSelector:
              matchExpressions:
                - key: security
                  operator: In
                  values:
                    - S1
            topologyKey: "topology.kubernetes.io/zone"
```

### DBCluster with ML agent

Example of configuring the ML agent within a DBCluster.

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: db-pw-dbcluster-sample
type: Opaque
data:
  dbcluster-sample: "Q2hhbmdlTWUxMjM=" # Password is ChangeMe123
---
apiVersion: v1
kind: Secret
metadata:
  name: vertex-ai-key-alloydb
type: Opaque
data:
  private-key.json: ""
---
apiVersion: alloydbomni.dbadmin.goog/v1
kind: DBCluster
metadata:
  name: dbcluster-sample
spec:
  databaseVersion: "16.9.0"
  primarySpec:
    features:
      googleMLExtension:
        enabled: true
        config:
          vertexAIKeyRef: vertex-ai-key-alloydb
          vertexAIRegion: us-central1
    adminUser:
      passwordRef:
        name: db-pw-dbcluster-sample
    resources:
      memory: 5Gi
      cpu: 1
      disks:
        - name: DataDisk
          size: 10Gi
```

### DBCluster with load balancer

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: db-pw-dbcluster-sample
type: Opaque
data:
  dbcluster-sample: "Q2hhbmdlTWUxMjM=" # Password is ChangeMe123
---
apiVersion: alloydbomni.dbadmin.goog/v1
kind: DBCluster
metadata:
  name: dbcluster-sample
spec:
  databaseVersion: "16.9.0"
  primarySpec:
    adminUser:
      passwordRef:
        name: db-pw-dbcluster-sample
    resources:
      memory: 5Gi
      cpu: 1
      disks:
        - name: DataDisk
          size: 10Gi
    dbLoadBalancerOptions:
      annotations:
        # Creates an internal LoadBalancer in GKE.
        networking.gke.io/load-balancer-type: "internal"
    allowExternalIncomingTraffic: true
```

### DBCluster with Commvault sidecar

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: db-pw-dbcluster-sample
type: Opaque
data:
  dbcluster-sample: "Q2hhbmdlTWUxMjM=" # Password is ChangeMe123
---
apiVersion: alloydbomni.dbadmin.goog/v1
kind: DBCluster
metadata:
  name: dbcluster-sample
spec:
  databaseVersion: "16.9.0"
  primarySpec:
    adminUser:
      passwordRef:
        name: db-pw-dbcluster-sample
    resources:
      memory: 5Gi
      cpu: 1
      disks:
        - name: DataDisk
          size: 10Gi
        - name: LogDisk
          size: 10Gi
    walArchiveSetting:
      location: wal/log # enable WAL archiving and archive logs to /archive/wal/log
    sidecarRef:
      name: cv-sidecar-config
```

## Backup and Restore

### Backup plan

Example of scheduling full and incremental backups.

```yaml
apiVersion: alloydbomni.dbadmin.goog/v1
kind: BackupPlan
metadata:
  name: backupplan1
spec:
  dbclusterRef: dbcluster-sample
  backupRetainDays: 14
  paused: false
  backupSchedules:
    # Full backup at 00:00 on every Sunday.
    full: "0 0 * * 0"
    # Incremental backup at 21:00 every day.
    incremental: "0 21 * * *"
```

### Restore from backup

```yaml
apiVersion: alloydbomni.dbadmin.goog/v1
kind: Restore
metadata:
  name: restore1
spec:
  sourceDBCluster: dbcluster-sample
  backup: backup1
```

### Clone

```yaml
apiVersion: alloydbomni.dbadmin.goog/v1
kind: Restore
metadata:
  name: clone1
spec:
  sourceDBCluster: dbcluster-sample
  pointInTime: "2024-02-23T19:59:43Z"
  clonedDBClusterConfig:
    dbclusterName: new-dbcluster-sample
```

## High Availability and Data Resilience

### Failover

Example of performing an unplanned failover to a standby instance.

```yaml
apiVersion: alloydbomni.dbadmin.goog/v1
kind: Failover
metadata:
  name: failover-sample
spec:
  dbclusterRef: dbcluster-sample
```

### Switchover

Example of performing a controlled switchover to a standby instance.

```yaml
apiVersion: alloydbomni.dbadmin.goog/v1
kind: Switchover
metadata:
  name: switchover-sample
spec:
  dbclusterRef: dbcluster-sample
  newPrimary: aaaa-dbcluster-sample # Replace with the standby instance you selected to switch with the primary instance.
```

## Monitoring and connection pooling

### PgBouncer configuration

```yaml
apiVersion: alloydbomni.dbadmin.goog/v1
kind: PgBouncer
metadata:
  name: mypgbouncer
spec:
  allowSuperUserAccess: true
  dbclusterRef: dbcluster-sample
  replicaCount: 1
  parameters:
    pool_mode: transaction
    ignore_startup_parameters: extra_float_digits
    default_pool_size: "15"
    max_client_conn: "800"
    max_db_connections: "160"
  podSpec:
    resources:
      memory: 1Gi
      cpu: 1
    image: "gcr.io/alloydb-omni-staging/g-pgbouncer:1.4.0"
  serviceOptions:
    type: "ClusterIP"
```

### Sidecar example

```yaml
apiVersion: alloydbomni.dbadmin.goog/v1
kind: Sidecar
metadata:
  name: sidecar-sample
spec:
  sidecars:
    - image: busybox
      name: sidecar-sample
      volumeMounts:
        - name: obsdisk
          mountPath: /logs
      command: ["/bin/sh"]
      args:
        - -c
        - |
          while [ true ]
          do
            date
            set -x
            ls -lh /logs/diagnostic
            set +x
          done
```
