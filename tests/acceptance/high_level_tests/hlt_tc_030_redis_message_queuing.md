# HLT-TC-030: Redis Message Queuing and Processing

**Version:** 1.0
**Date:** May 17, 2025
**Author:** AI Assistant (Claude)

## 1. Test Overview
This HLT verifies that Township Connect's Redis message queuing system functions correctly, ensuring that messages sent to Redis streams by one part of the system are successfully picked up and processed by worker components, with proper handling of queue depth, message persistence, and processing reliability.

## 2. User Story / Scenario
* **Feature:** Redis message queuing for asynchronous processing and system integration.
* **Scenario (HLT Strategy 4.7):** Test Redis message queuing under load. Verification: Messages sent to Redis streams by one part of the system are successfully picked up and processed by worker components. Redis monitoring or application logs confirm queue depth changes and message processing.

## 3. Preconditions
* Township Connect is fully operational with Redis integration configured.
* Redis monitoring tools or access to Redis CLI is available.
* System logging is configured to capture message production, queuing, and consumption events.
* Test environment is representative of production conditions.
* Worker components that process messages from Redis are operational.

## 4. Test Steps

| Step | Test Action | Expected System Response & Verification |
|------|-------------|----------------------------------------|
| 1 | Identify all Redis streams/queues used in Township Connect | Complete inventory of Redis streams is created, including producer components, consumer components, and message types. |
| 2 | Configure monitoring for Redis queues to track message counts, processing rates, and queue depths | Monitoring is correctly configured to capture Redis queue metrics. |
| 3 | Configure system logging to track message production and consumption events | Logging is correctly configured to capture message lifecycle events with correlation IDs. |
| 4 | **Basic Message Flow:** Trigger an action that produces a message to Redis (e.g., user sends a command that requires asynchronous processing) | Message is successfully published to the appropriate Redis stream. Redis monitoring shows queue depth increase. Worker component picks up the message. System logs show message production and consumption events. The action completes successfully. |
| 5 | **Message Persistence:** Temporarily stop worker components, trigger actions that produce messages to Redis, then restart workers | Messages are persisted in Redis while workers are offline. Queue depth increases during worker downtime. Upon worker restart, all queued messages are processed. System logs confirm successful processing of all messages. |
| 6 | **High Volume Testing:** Generate a high volume of messages in a short period (e.g., simulate multiple users performing actions simultaneously) | All messages are successfully queued in Redis. Workers process messages at their maximum rate. No messages are lost. Queue depth eventually returns to normal as workers process the backlog. System logs confirm successful processing of all messages. |
| 7 | **Priority Handling:** If priority queues are implemented, test that high-priority messages are processed before lower-priority ones | High-priority messages are processed ahead of lower-priority messages regardless of queue order. System logs confirm priority-based processing. |
| 8 | **Error Handling:** Deliberately introduce errors in message processing (e.g., malformed message, simulated worker failure) | Error is detected and handled appropriately. Message is either retried, moved to a dead-letter queue, or logged for manual intervention. System does not crash or lose messages. System logs document the error and recovery actions. |
| 9 | **Long-Running Processing:** Test messages that trigger time-consuming operations | Long-running operations do not block other message processing. System maintains responsiveness. Operation completes successfully. System logs confirm successful processing. |
| 10 | **Monitoring and Metrics:** Review Redis monitoring data and system logs for the entire test period | Monitoring data shows expected patterns of queue depth changes. System logs provide clear visibility into message lifecycle. No anomalies or performance issues are detected. |

## 5. Acceptance Criteria (AI Verifiable)
* All messages published to Redis streams are successfully queued.
* Worker components reliably consume and process messages from Redis streams.
* Messages persist in Redis during temporary worker outages and are processed when workers return.
* The system handles high message volumes without message loss or significant performance degradation.
* If implemented, message priorities are correctly honored in processing order.
* Error handling mechanisms function correctly, preventing message loss and system crashes.
* Long-running message processing does not block or significantly delay other message processing.
* Redis queue depths remain within acceptable limits during normal operation.
* System logs and monitoring provide clear visibility into message production, queuing, and consumption.
* The Redis integration demonstrates reliability and robustness under various conditions, including high load and component failures.

## 6. References
* High-Level Test Strategy Report Section 4.7: API Integrations
* Master Acceptance Test Plan Section 3, Phase 7: API Integration Robustness
* Redis documentation
* Township Connect Redis integration documentation (if available)

## 7. Notes
* This test focuses specifically on Redis message queuing and processing, not on the detailed functionality of the features implemented via these messages.
* For AI verification purposes, Redis monitoring data, queue metrics, and system logs should be analyzed.
* The test should cover all major Redis streams/queues used in Township Connect.
* Special attention should be paid to:
  * Message persistence during component outages
  * System behavior under high message volumes
  * Error handling and recovery mechanisms
  * Performance characteristics (throughput, latency)
  * Resource utilization (memory, connections)
* This test is critical for ensuring the reliability of asynchronous processing in Township Connect.
* Consider testing Redis configuration parameters (e.g., stream length limits, consumer group settings) to ensure optimal performance.
* Document any queue optimization strategies implemented and verify they work as intended.
* Verify that message processing is properly logged for audit and troubleshooting purposes.
* If possible, test with Redis cluster configuration to verify behavior during Redis node failures.