# Redis clustering 

Redis Cluster provides a way to run a Redis installation where data is  **automatically sharded across multiple Redis nodes**.

### What is Redis?

1.  Redis is an  **in-memory,**  **key-value**  **store**.
-   **In-memory store**: Redis keeps the data in the cache and it does not write to the disk. This makes reading/writing data very fast. (However, Redis has an option to write data to the disk)
-   **Key-value store**: Redis can store data as key-value pairs.
2. It is a  [No-SQL](https://en.wikipedia.org/wiki/NoSQL)  database.
3. Uses  [data structures](https://redis.io/topics/data-types-intro)  to store data.
4. Interaction with data is command-based.
 
 for example
```bash
SET $KEY $VALUE
#eg:
SET name Aryan

#if your key or value has spaces, wrap them with quotes
SET $KEY "$VALUE" 
SET 'full-name' 'Aryan Ahmed Anik'
```

**We can put the requests that need to be serviced very fast into the Redis memory and service from there while keeping the rest of the data in the main database as it is a in-memeory database.**

### Redis cluster
![source: https://redislabs.com/redis-features/redis-cluster  ](https://i.ibb.co/KWgJBMF/redis-cluster-diagram.png)

A Redis cluster is simply a **data sharding strategy**. 
#### What is sharding?
  
The word “**Shard**” means “**a small part of a whole**“. Hence Sharding means dividing a larger part into smaller parts.
Sharding is a type of partitioning in which a large *data store* is divided or partitioned into smaller data, also known as shards.
Redis cluster  automatically partitions data across multiple Redis nodes. It is an advanced version of Redis that achieves distributed storage and prevents a single point of failure.
 
 -   Horizontally scalable: We can continue to add more nodes as the capacity requirement increases.
-   Auto data sharding: can automatically partition and split data among the nodes.
-   Fault tolerant: even though we lose a node, we can still continue to operate without losing any data and no downtime.
-   Decentralized cluster management: no single node acts as an orchestrator of the entire cluster, every node participates in the cluster configuration ([via gossip protocol](https://en.wikipedia.org/wiki/Gossip_protocol)).

So in summary, 
- The ability to  **automatically split your dataset among multiple nodes**.
- The ability to  **continue operations when a subset of the nodes are experiencing failures**  or are unable to communicate with the rest of the cluster.
-  *It also provides **some degree of availability during partitions**, that is in practical terms the ability to continue the operations when some nodes fail or are not able to communicate.*

 
### Redis Cluster goals

Redis Cluster is a distributed implementation of Redis with the following goals, in order of importance in the design:

-   High performance and linear scalability up to 1000 nodes. There are no proxies, asynchronous replication is used, and no merge operations are performed on values.
-   Acceptable degree of write safety: the system tries (in a best-effort way) to retain all the writes originating from clients connected with the majority of the master nodes. Usually there are small windows where acknowledged writes can be lost. Windows to lose acknowledged writes are larger when clients are in a minority partition.
-   Availability: Redis Cluster is able to survive partitions where the majority of the master nodes are reachable and there is at least one reachable slave for every master node that is no longer reachable. Moreover using  _replicas migration_, masters no longer replicated by any slave will receive one from a master which is covered by multiple slaves.

  
Every Redis Cluster node requires two TCP connections open. The normal Redis TCP port used to serve clients, for example 6379, plus the port obtained by adding 10000 to the data port, so 16379 in the example.
**The offset is always 10000**.

### Prerequisites

The minimal cluster that works as expected requires;
-   Minimum 3 Redis master nodes
-   Minimum 3 Redis slaves, 1 slave per master (to allow minimal fail-over mechanism)

### Distributed storage of the cluster

Every key that you save into a Redis cluster is associated with a hash slot. There are 0–16383 slots in a Redis cluster. Thus, a Redis cluster can have a maximum of 16384 master nodes (with the first 0) and each master node in a cluster handles a subset of the 16384 hash slots.

### Cyclic Redundency Check

A **cyclic redundancy check** (**CRC**) is an [error-detecting code](https://en.wikipedia.org/wiki/Error_detection_and_correction "Error detection and correction") commonly used in digital [networks](https://en.wikipedia.org/wiki/Telecommunications_network "Telecommunications network") and storage devices to detect accidental changes to raw data. Blocks of data entering these systems get a short _check value_ attached, based on the remainder of a [polynomial division](https://en.wikipedia.org/wiki/Polynomial_long_division "Polynomial long division") of their contents. On retrieval, the calculation is repeated and, in the event the check values do not match, corrective action can be taken against data corruption. CRCs can be used for [error correction](https://en.wikipedia.org/wiki/Error_correcting_code "Error correcting code") (see [bitfilters](https://en.wikipedia.org/wiki/Mathematics_of_cyclic_redundancy_checks#Bitfilters "Mathematics of cyclic redundancy checks")).[[1]](https://en.wikipedia.org/wiki/Cyclic_redundancy_check#cite_note-1)
-wikipedia

```
HASH_SLOT = CRC16(key) mod HASH_SLOTS_NUMBER
```


For example, let’s assume the key space is divided into 10 slots (0–9). Each node will hold a subset of the hash slots.
![enter image description here](https://miro.medium.com/max/1400/1*g_uPH1TnC40Nqiqx4X0ifQ.png)

### Detective failures

Every node has a unique ID in the cluster. This ID is used to identify each and every node across the entire cluster using the gossip protocol.

So, a node keeps the following information within itself;

-   Node ID, IP, and port
-   A set of flags
-   What is the Master of the node if it is flagged as “slave”
-   Last time a node was pinged
-   Last time the pong was received

Nodes in a cluster always keep gossiping with each other, enabling them to auto-discover other nodes.

e.g. If A knows B, and B knows C, eventually B will send gossip messages to A about C. Then A will register C as part of the network and will try to connect with C.

When node A talks to the cluster by the gossip protocol, If a/any node fails, the cluster's reply will be node X,Y responded okay but P,Q,R didn't response.

 
 ### Notes to self
 
#### Replication Or Clustering?
If you have more data than RAM in a single machine, use a Redis cluster to shard the data across multiple databases.

If you have less data than RAM in a machine, set up a master/slave replication with a sentinel in front to handle the failover.

#### Why Do you need a minimum of 3 masters?

During the failure detection, the majority of the master nodes are required to come to an agreement. If there are only 2 masters, say A and B and B failed, then the A master node cannot reach to a decision according to the protocol. The A node needs another third node, say C, to tell A that it also cannot reach B.

Special thanks to [Varuni Punchihewa](https://blog.usejournal.com/@varunipunchihewa)
