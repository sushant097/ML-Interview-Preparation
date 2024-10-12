

# End-to-End Realtime Data Streaming Project

## Table of Contents
- [Introduction](#introduction)
- [System Architecture](#system-architecture)
- [Technologies](#technologies)
- [Key Concepts](#key-concepts)
- [Getting Started](#getting-started)
- [Conclusion](#conclusion)
- [Watch the Video Tutorial](#watch-the-video-tutorial)

## Introduction

This project demonstrates how to build a robust, end-to-end real-time data engineering pipeline. The pipeline handles data ingestion, streaming, processing, and storage while ensuring scalability and high availability. Utilizing a combination of Apache Airflow for orchestration, Apache Kafka for streaming, Apache Spark for processing, and Cassandra for storage, this system architecture efficiently handles data flows. Docker is used for containerizing the entire setup to enable easy deployment and scalability.

## System Architecture

The system architecture consists of the following components:

![System Architecture](Data%20engineering%20architecture.png)

### Components Overview:
1. **Data Source**: 
   - `randomuser.me` API is used to generate random user data, which serves as the input for this pipeline.
   
2. **Apache Airflow**:
   - Manages and orchestrates the entire data pipeline. It pulls data from the API and stores it temporarily in **PostgreSQL** for staging.
   
3. **PostgreSQL**:
   - A relational database that temporarily holds the raw ingested data from the API. This helps in isolating the ingestion step before streaming.
   
4. **Apache Kafka**:
   - Facilitates real-time data streaming from PostgreSQL to other components. Kafka serves as the backbone of the streaming layer, ensuring smooth and fast data transfer.
   
5. **Apache Zookeeper**:
   - Coordinates distributed systems and helps manage Kafka brokers. Zookeeper ensures that the Kafka cluster runs smoothly with synchronization across brokers.
   
6. **Control Center and Schema Registry**:
   - **Control Center** provides a GUI for monitoring Kafka streams. **Schema Registry** ensures consistency in the data formats flowing through Kafka by managing the schemas used by Kafka producers and consumers.
   
7. **Apache Spark**:
   - Used for real-time data processing. In this setup, Spark is configured with a **master node** to coordinate, and **worker nodes** that perform distributed processing tasks such as data transformation and aggregation.
   
8. **Cassandra**:
   - A NoSQL distributed database that stores the processed data. Cassandra is known for its high availability, fault tolerance, and scalability, making it suitable for large-scale real-time applications.

9. **Docker**:
   - All components are containerized using Docker, allowing easy setup, consistent development environments, and scalable deployment.

## Technologies

This project uses the following technologies:

- **Apache Airflow**: Pipeline orchestration
- **Python**: Scripting and integration
- **Apache Kafka**: Data streaming
- **Apache Zookeeper**: Kafka management and coordination
- **Apache Spark**: Distributed data processing
- **Cassandra**: Scalable data storage
- **PostgreSQL**: Data staging
- **Docker**: Containerization and deployment

---

Here’s a detailed explanation of how data flows from the API to Cassandra:


### Data Flow from API to Cassandra

1. **Data Source (API) → Apache Airflow**:
   - The data flow begins with the **API**—in this case, the `randomuser.me` API, which generates random user data. This data serves as the raw input for the pipeline.
   - **Apache Airflow** kicks off the pipeline by making an HTTP request to the API and fetching the data. Airflow’s DAG (Directed Acyclic Graph) schedules this task, ensuring it happens periodically or based on a trigger, depending on how you’ve configured the workflow.
   - Once Airflow successfully retrieves the data from the API, it temporarily stores this raw data in **PostgreSQL**, acting as a staging area.

2. **PostgreSQL → Apache Kafka**:
   - After data lands in PostgreSQL, it needs to be streamed for further processing. This is where **Apache Kafka** comes in.
   - Kafka’s role is to stream data from the staging area (PostgreSQL) to downstream components for real-time processing. Think of Kafka as the "messenger" responsible for moving the data as fast as possible in real-time from point A to point B.
   - Kafka produces messages (in this case, batches of user data) from the PostgreSQL staging area and pushes these messages into **Kafka topics**. The topics act as queues where other components can consume the data in real-time.
   - **Apache Zookeeper** is responsible for maintaining and coordinating Kafka brokers (which handle data movement), ensuring synchronization, and managing the Kafka cluster so that data streams efficiently.

3. **Kafka → Apache Spark**:
   - **Apache Spark** plays a critical role in the real-time processing of the streamed data. Spark is designed to handle massive parallel data processing, transforming the raw data into a useful, refined form.
   - Spark consumes the data from Kafka topics. Here, the "worker nodes" in Spark process chunks of data in parallel. These workers apply transformations to the data—like filtering, aggregating, or cleaning—depending on the processing logic defined in your Spark jobs.
   - The **master node** in Spark orchestrates this distributed processing by assigning tasks to worker nodes, ensuring efficient processing of large-scale data.

4. **Apache Spark → Cassandra**:
   - After the data is processed by Spark, the clean and structured data is sent to **Cassandra** for storage.
   - **Cassandra** is a NoSQL distributed database known for its scalability and ability to handle large amounts of data. It’s optimized for high-throughput writes, making it perfect for real-time pipelines like yours.
   - The processed data is stored in a way that makes it easily accessible for further querying and analysis, ensuring that the pipeline outputs can be used by downstream systems, dashboards, or analytics platforms.

---

### Role of Each Component in the Data Flow:

1. **API (Data Source)**:
   - Generates the raw data for the pipeline, acting as the source of truth.
   - The API provides random user data, which is fetched regularly by Apache Airflow.

2. **Apache Airflow**:
   - Orchestrates the entire pipeline.
   - Fetches data from the API, storing it temporarily in PostgreSQL. It ensures each step of the pipeline happens in the correct order and at the right time.

3. **PostgreSQL**:
   - Acts as a staging area for raw data before it is streamed.
   - Temporarily holds the data, providing a clear separation between data ingestion and streaming.

4. **Apache Kafka**:
   - Streams data from PostgreSQL to other components.
   - Handles real-time data movement, ensuring low-latency streaming of data across the pipeline.
   - Kafka’s topics act as message queues where data is organized and consumed in real-time by downstream components.

5. **Apache Zookeeper**:
   - Coordinates and manages the Kafka brokers.
   - Ensures the Kafka cluster is synchronized and running smoothly, preventing bottlenecks and making sure that data streams continuously.

6. **Apache Spark**:
   - Processes data in real-time, transforming raw data into a more structured and useful form.
   - Uses distributed processing, breaking the data into smaller chunks to be processed in parallel across multiple worker nodes, making it fast and efficient.

7. **Cassandra**:
   - Stores the processed data, ensuring it’s highly available and scalable.
   - Cassandra’s distributed nature makes it ideal for handling the large volume of real-time data produced by the pipeline, ensuring that data can be quickly queried and retrieved.

---

This entire flow ensures that the pipeline can efficiently process and store data in real-time, from ingestion (API) to final storage (Cassandra). Each component plays a distinct role in maintaining the real-time nature of the pipeline, from orchestration and streaming to distributed processing and storage.


## Getting Started

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   ```

2. **Navigate to the project directory**:
   ```bash
   cd <project-directory>
   ```

3. **Run the Docker Compose to spin up all services**:
   ```bash
   docker-compose up
   ```

4. **Accessing Services**:
   - **Airflow UI**: [http://localhost:8080](http://localhost:8080) 
   - **Kafka Control Center**: [http://localhost:9021](http://localhost:9021)
   - **Spark UI**: [http://localhost:8081](http://localhost:8081)
   - **Cassandra**: Cassandra is running in the background, with data being stored as per the pipeline configuration.
