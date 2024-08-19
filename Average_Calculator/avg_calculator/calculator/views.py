from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import requests

WINDOW_SIZE = 10
numbers_window = []

API_BASE_URLS = {
    'p': 'http://20.244.56.144/test/primes',
    'f': 'http://20.244.56.144/test/fibo',
    'e': 'http://20.244.56.144/test/even',
    'r': 'http://20.244.56.144/test/rand'
}

def fetch_numbers(number_id):
    url = API_BASE_URLS.get(number_id)
    if not url:
        return {"numbers": []}

    try:
        response = requests.get(url, timeout=0.5)
        response.raise_for_status()
        return response.json()
    except (requests.RequestException, ValueError):
        return {"numbers": []}

@require_http_methods(["GET"])
def get_numbers(request, numberid):
    global numbers_window

    new_numbers = fetch_numbers(numberid).get('numbers', [])
    if not new_numbers:
        return JsonResponse({"error": "Failed to fetch numbers"}, status=500)

    numbers_window = (numbers_window + new_numbers)[-WINDOW_SIZE:]
    
    window_prev_state = numbers_window[:-len(new_numbers)]
    window_curr_state = numbers_window
    
    avg = sum(numbers_window) / len(numbers_window) if numbers_window else 0

    return JsonResponse({
        "numbers": new_numbers,
        "windowPrevState": window_prev_state,
        "windowCurrState": window_curr_state,
        "avg": avg
    })
