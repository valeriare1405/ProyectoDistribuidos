
### My-Uber (Distributed Taxi Simulation)


A distributed system inspired by ride-hailing apps, simulating taxis and users in a city grid. Built with **Python** and **ZeroMQ**, the project leverages **Request-Reply** and **Publish-Subscribe** communication patterns to manage real-time interactions between taxis, users, and a central server.

The system includes:

* **Fault tolerance** with replica servers and health-checks for automatic failover.
* **Distributed execution** across multiple machines to simulate real-world scalability.
* **Efficient communication** between components for assigning nearest taxis to users.
* **Data persistence** for tracking positions, assignments, and system performance.


**Quick facts:**

* Runs across at least **3 machines** (taxis, users, server).
* Implements **synchronous and asynchronous patterns**.
* Designed for **resilience and scalability**.
* Measures **response times and service success rates**.
