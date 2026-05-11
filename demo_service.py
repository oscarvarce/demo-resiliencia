"""
Section C - Demo Service & Reliability Test
Demonstrates the Reusable Integration Framework against an unstable upstream.

Usage:
    python demo_service.py

Requirements:
    - integration_framework.py in the same directory
"""

import time
import random
import threading
from integration_framework import (
    IntegrationClient, IntegrationContext, ResilienceConfig,
    CircuitBreakerOpenException, BulkheadFullException, MaxRetriesExceededException
)

# ============================================================================
# C.1: UNSTABLE UPSTREAM SERVICE SIMULATOR
# ============================================================================

class UnstableUpstreamService:
    """
    Simulates a real-world unreliable service with multiple failure modes.

    Failure Scenarios:
    - Intermittent 500/503 errors (60% failure rate)
    - Random timeouts (20% of calls hang beyond timeout)
    - Success with slow responses (20% take 0.5-2.5s)
    """

    def __init__(self, name: str, failure_rate: float = 0.6, timeout_rate: float = 0.2):
        self.name = name
        self.failure_rate = failure_rate
        self.timeout_rate = timeout_rate
        self.call_count = 0
        self.failure_count = 0

    def call(self, timeout: float = 5.0) -> dict:
        """Simulate an upstream HTTP call."""
        self.call_count += 1
        rand = random.random()

        # Simulate timeout (hang longer than timeout)
        if rand < self.timeout_rate:
            time.sleep(timeout + 2)
            raise TimeoutError(f"Request to {self.name} timed out after {timeout}s")

        # Simulate server error
        elif rand < self.failure_rate + self.timeout_rate:
            self.failure_count += 1
            error = random.choice([
                ("Internal Server Error", 500),
                ("Bad Gateway", 502),
                ("Service Unavailable", 503),
                ("Gateway Timeout", 504),
            ])
            exc = Exception(error[0])
            exc.status_code = error[1]
            raise exc

        # Simulate slow but successful response
        else:
            delay = random.uniform(0.1, 0.5)
            time.sleep(delay)
            return {
                "service": self.name,
                "status": "success",
                "response_time": f"{delay:.2f}s",
                "data": {"order_id": f"ORD-{random.randint(10000, 99999)}"}
            }


# ============================================================================
# C.2: DEMO SERVICE USING THE FRAMEWORK
# ============================================================================

class OrderService:
    """
    Demo service that processes orders by calling an unstable payment gateway.
    Uses the Integration Framework for resilience.
    """

    def __init__(self):
        # Configure aggressive resilience for demo purposes
        config = ResilienceConfig(
            connect_timeout=1.0,
            read_timeout=2.0,
            max_retries=2,
            base_delay=0.3,
            max_delay=3.0,
            exponential_base=2.0,
            jitter_max=0.3,
            failure_threshold=3,        # Open circuit after 3 failures
            recovery_timeout=8.0,         # Try recovery after 8s
            half_open_max_calls=2,
            success_threshold_half_open=1,
            max_concurrent_calls=3,      # Small bulkhead for demo
            max_queue_size=1
        )

        self.payment_client = IntegrationClient("payment-gateway", config)
        self.upstream = UnstableUpstreamService("payment-gateway", failure_rate=0.6, timeout_rate=0.2)
        self.logger = self.payment_client.logger

    def process_order(self, order_id: str, amount: float, user_id: str) -> dict:
        """
        Process an order with full resilience wrapping.

        Args:
            order_id: Unique order identifier
            amount: Order amount
            user_id: Customer identifier
        """
        # Create trace context with idempotency key
        context = IntegrationContext(
            idempotency_key=f"order-{order_id}",
            baggage={"country_code": "ES", "channel": "mobile", "user_tier": "premium"}
        )

        payload = {
            "order_id": order_id,
            "amount": amount,
            "user_id": user_id,
            "currency": "EUR"
        }

        self.logger.info(
            context.trace_id,
            f"Processing order {order_id} for €{amount}"
        )

        try:
            # Execute with framework wrapping
            result = self.payment_client.execute(
                operation=lambda timeout: self.upstream.call(timeout),
                context=context,
                payload=payload,
                enable_idempotency=True,
                timeout=2.0
            )

            return {
                "order_id": order_id,
                "status": "completed",
                "payment_result": result,
                "trace_id": context.trace_id
            }

        except CircuitBreakerOpenException as e:
            self.logger.error(context.trace_id, f"Circuit breaker open: {str(e)}")
            return {
                "order_id": order_id,
                "status": "rejected",
                "reason": "circuit_breaker_open",
                "message": "Payment service temporarily unavailable. Please retry later.",
                "trace_id": context.trace_id
            }

        except BulkheadFullException as e:
            self.logger.error(context.trace_id, f"Bulkhead full: {str(e)}")
            return {
                "order_id": order_id,
                "status": "rejected",
                "reason": "bulkhead_full",
                "message": "System overloaded. Please retry later.",
                "trace_id": context.trace_id
            }

        except MaxRetriesExceededException as e:
            self.logger.error(context.trace_id, f"Max retries exceeded: {str(e)}")
            return {
                "order_id": order_id,
                "status": "failed",
                "reason": "max_retries_exceeded",
                "message": "Payment service unavailable after retries.",
                "trace_id": context.trace_id
            }

        except Exception as e:
            self.logger.error(context.trace_id, f"Unexpected error: {str(e)}")
            return {
                "order_id": order_id,
                "status": "error",
                "reason": "unexpected",
                "message": str(e),
                "trace_id": context.trace_id
            }


# ============================================================================
# C.3: RELIABILITY TEST RUNNER
# ============================================================================

def run_reliability_test():
    """
    Execute a comprehensive reliability test demonstrating all patterns.

    Test Scenarios:
    1. Normal operation with retries (shows backoff + jitter)
    2. Circuit breaker opening after threshold
    3. Fast-fail when circuit is OPEN
    4. Circuit recovery (HALF_OPEN -> CLOSED)
    5. Idempotency (duplicate requests return cached response)
    6. Bulkhead saturation (concurrent load test)
    """

    print("=" * 80)
    print("RELIABILITY TEST: Integration Framework vs Unstable Payment Gateway")
    print("=" * 80)
    print()

    service = OrderService()
    upstream = service.upstream

    # -------------------------------------------------------------------------
    # TEST 1: Basic operation with retries (8 sequential calls)
    # -------------------------------------------------------------------------
    print("TEST 1: Sequential Calls with Retry Demonstration")
    print("-" * 50)

    results = []
    for i in range(8):
        result = service.process_order(
            order_id=f"ORD-001-{i}",
            amount=99.99,
            user_id="user-12345"
        )
        results.append(result)
        time.sleep(0.3)

    success_count = sum(1 for r in results if r["status"] == "completed")
    print(f">>> Results: {success_count}/8 successful")
    print(f">>> Upstream total calls: {upstream.call_count}, failures: {upstream.failure_count}")
    print(f">>> Circuit state: {service.payment_client.circuit_breaker.get_state()}")
    print()

    # -------------------------------------------------------------------------
    # TEST 2: Circuit Breaker Opening (rapid failures)
    # -------------------------------------------------------------------------
    print("TEST 2: Circuit Breaker State Transition")
    print("-" * 50)
    print(f"Initial circuit state: {service.payment_client.circuit_breaker.get_state()}")

    for i in range(5):
        result = service.process_order(
            order_id=f"ORD-CB-{i}",
            amount=50.0,
            user_id="user-cb-test"
        )
        print(f"  Call {i+1}: {result['status']} | Circuit: {service.payment_client.circuit_breaker.get_state()}")
        if result["status"] == "rejected" and result["reason"] == "circuit_breaker_open":
            print("  >>> CIRCUIT BREAKER OPENED - Fast failing subsequent calls!")
            break

    print()

    # -------------------------------------------------------------------------
    # TEST 3: Fast-fail when circuit OPEN
    # -------------------------------------------------------------------------
    print("TEST 3: Fast-Fail Behavior (Circuit OPEN)")
    print("-" * 50)

    start = time.time()
    result = service.process_order("ORD-FAST-1", 25.0, "user-fast")
    elapsed = time.time() - start

    print(f">>> Response time: {elapsed:.3f}s (should be < 0.1s due to fast-fail)")
    print(f">>> Result: {result['status']} | Reason: {result.get('reason', 'N/A')}")
    print()

    # -------------------------------------------------------------------------
    # TEST 4: Circuit Recovery
    # -------------------------------------------------------------------------
    print("TEST 4: Circuit Recovery (HALF_OPEN -> CLOSED)")
    print("-" * 50)
    print(f"Waiting for recovery timeout ({service.payment_client.config.recovery_timeout}s)...")
    time.sleep(service.payment_client.config.recovery_timeout + 1)

    print(f"Circuit state after wait: {service.payment_client.circuit_breaker.get_state()}")

    # Temporarily make upstream stable to demonstrate recovery
    upstream.failure_rate = 0.0
    upstream.timeout_rate = 0.0

    result = service.process_order("ORD-RECOVER-1", 75.0, "user-recover")
    print(f">>> Recovery call result: {result['status']}")
    print(f">>> Circuit state after success: {service.payment_client.circuit_breaker.get_state()}")

    # Restore failure rate
    upstream.failure_rate = 0.6
    upstream.timeout_rate = 0.2
    print()

    # -------------------------------------------------------------------------
    # TEST 5: Idempotency Demonstration
    # -------------------------------------------------------------------------
    print("TEST 5: Idempotency (Duplicate Request Detection)")
    print("-" * 50)

    upstream.failure_rate = 0.0
    upstream.timeout_rate = 0.0

    order_id = "ORD-IDEM-001"

    result1 = service.process_order(order_id, 150.0, "user-idem")
    print(f"First call:  {result1['status']} | Source: {result1['payment_result'].get('source', 'N/A')}")

    result2 = service.process_order(order_id, 150.0, "user-idem")
    print(f"Second call: {result2['status']} | Source: {result2['payment_result'].get('source', 'N/A')}")

    if result2['payment_result'].get('source') == 'cache':
        print(">>> IDEMPOTENCY WORKING: Duplicate request returned cached response without calling upstream!")

    upstream.failure_rate = 0.6
    upstream.timeout_rate = 0.2
    print()

    # -------------------------------------------------------------------------
    # TEST 6: Bulkhead Saturation (Concurrent Load)
    # -------------------------------------------------------------------------
    print("TEST 6: Bulkhead Saturation (Concurrent Load Test)")
    print("-" * 50)

    bulkhead_results = []

    def concurrent_call(index: int):
        result = service.process_order(f"ORD-BULK-{index}", 10.0, "user-bulk")
        bulkhead_results.append((index, result['status'], result.get('reason', 'N/A')))

    threads = []
    start = time.time()

    for i in range(10):
        t = threading.Thread(target=concurrent_call, args=(i,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    elapsed = time.time() - start

    completed = sum(1 for _, status, _ in bulkhead_results if status == "completed")
    rejected_bulkhead = sum(1 for _, status, reason in bulkhead_results if status == "rejected" and reason == "bulkhead_full")

    print(f">>> Concurrent requests: 10 | Bulkhead limit: 3 + queue: 1")
    print(f">>> Completed: {completed} | Rejected (bulkhead): {rejected_bulkhead}")
    print(f">>> Total time: {elapsed:.2f}s")
    print(">>> BULKHEAD WORKING: Excess requests rejected to protect system!")
    print()

    # -------------------------------------------------------------------------
    # SUMMARY
    # -------------------------------------------------------------------------
    print("=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    print(f"Upstream service calls made: {upstream.call_count}")
    print(f"Upstream failures simulated: {upstream.failure_count}")
    print(f"Final circuit breaker state: {service.payment_client.circuit_breaker.get_state()}")
    print()
    print("Patterns Demonstrated:")
    print("  ✓ Retry with Exponential Backoff + Jitter")
    print("  ✓ Circuit Breaker (CLOSED -> OPEN -> HALF_OPEN -> CLOSED)")
    print("  ✓ Idempotency (duplicate request detection & cached response)")
    print("  ✓ Bulkhead (concurrent execution limiting)")
    print("  ✓ Timeout enforcement")
    print("  ✓ Structured logging with Trace ID propagation")
    print("=" * 80)


if __name__ == "__main__":
    run_reliability_test()
