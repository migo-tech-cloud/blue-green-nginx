# DECISION.md
## Why Nginx upstreams
Nginx’s built-in backup upstream allows automatic failover from Blue to Green when primary fails.
## Why envsubst
It lets us dynamically substitute ACTIVE_POOL and other env variables during runtime without rebuilding.
