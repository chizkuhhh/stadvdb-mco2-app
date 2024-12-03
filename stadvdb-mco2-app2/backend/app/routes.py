from flask import jsonify, request
from app import app
from app.db_config import get_db_connection
from concurrent.futures import ThreadPoolExecutor

@app.route('/simulate', methods=['POST'])
def simulate_transactions():
    data = request.json
    transactions = data.get('transactions', [])

    results = []
    errors = []

    # Create a ThreadPoolExecutor for concurrent execution
    with ThreadPoolExecutor() as executor:
        futures = []
        for t in transactions:
            futures.append(executor.submit(process_transaction, t))  # Submit each transaction for processing

        for future in futures:
            result = future.result()  # Wait for each future to complete
            if 'error' in result:
                errors.append(result)
            else:
                results.append(result)

    # Combine results and errors in the response
    return jsonify({
        "status": "success" if not errors else "partial_success",
        "results": results,
        "errors": errors
    })


def process_transaction(t):
    node = t['node']
    query = t['query']
    isolation_level = t.get('isolation', 'READ COMMITTED')

    connection = None
    cursor = None

    try:
        # Connect to the database for this transaction
        connection = get_db_connection(node)
        cursor = connection.cursor(dictionary=True)

        # Set the isolation level and start the transaction
        cursor.execute(f"SET TRANSACTION ISOLATION LEVEL {isolation_level};")
        cursor.execute("START TRANSACTION;")

        # Execute the query
        cursor.execute(query)
        result = None
        if query.strip().upper().startswith("SELECT"):
            result = cursor.fetchall()

        connection.commit()

        return {
            "transaction_id": t['id'],
            "node": node,
            "query": query,
            "result": result
        }

    except Exception as e:
        # Rollback transaction on error
        if connection:
            connection.rollback()
        return {
            "transaction_id": t['id'],
            "node": node,
            "query": query,
            "error": str(e)
        }

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
