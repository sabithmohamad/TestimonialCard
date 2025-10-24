# get_token_with_proxies.py
import requests
import json
import time
from concurrent.futures import ThreadPoolExecutor

# UAE and Middle East focused proxies
UAE_PROXIES = [
         # US-UAE
    'http://40.172.232.213:8088',        # US-UAE
    'http://40.172.232.213:29214',     # US-UAE
]

def test_proxy_with_token(proxy):
    """Test if proxy can access the token API"""
    url = "https://geapps.germanexperts.ae:7007/api/crmservicegetaccesstokenByStatus/Active/1"
    
    headers = {
        'accept': '*/*',
        'accept-language': 'en-GB,en;q=0.9,en-US;q=0.8',
        'content-type': 'application/json',
        'origin': 'https://geapps.germanexperts.ae',
        'referer': 'https://geapps.germanexperts.ae/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        session = requests.Session()
        session.proxies = {'http': proxy, 'https': proxy}
        
        start_time = time.time()
        response = session.get(url, headers=headers, timeout=10)
        response_time = round((time.time() - start_time) * 1000)
        
        if response.status_code == 200:
            data = response.json()
            has_tokens = isinstance(data, list) and len(data) > 0
            
            if has_tokens:
                token_data = data[0]
                return {
                    'proxy': proxy,
                    'status': '✅ WORKING',
                    'response_time': f'{response_time}ms',
                    'has_token': True,
                    'token_preview': token_data.get('crm_accesstoken', '')[:30] + '...' if token_data.get('crm_accesstoken') else 'No token',
                    'country': 'UAE' if 'uae' in proxy.lower() else 'International'
                }
            else:
                return {
                    'proxy': proxy,
                    'status': '⚠️  NO TOKEN',
                    'response_time': f'{response_time}ms',
                    'has_token': False,
                    'country': 'UAE' if 'uae' in proxy.lower() else 'International'
                }
        else:
            return {
                'proxy': proxy,
                'status': '❌ FAILED',
                'error': f'HTTP {response.status_code}',
                'country': 'UAE' if 'uae' in proxy.lower() else 'International'
            }
            
    except Exception as e:
        return {
            'proxy': proxy,
            'status': '❌ ERROR',
            'error': str(e),
            'country': 'UAE' if 'uae' in proxy.lower() else 'International'
        }

def get_access_token(proxy=None):
    """Get active access token from the API with optional proxy"""
    
    url = "https://geapps.germanexperts.ae:7007/api/crmservicegetaccesstokenByStatus/Active/1"
    
    headers = {
        'accept': '*/*',
        'accept-language': 'en-GB,en;q=0.9,en-US;q=0.8',
        'content-type': 'application/json',
        'origin': 'https://geapps.germanexperts.ae',
        'priority': 'u=1, i',
        'referer': 'https://geapps.germanexperts.ae/',
        'sec-ch-ua': '"Microsoft Edge";v="141", "Not?A_Brand";v="8", "Chromium";v="141"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36 Edg/141.0.0.0'
    }
    
    try:
        print(f"🔐 Fetching access token{' with proxy: ' + proxy if proxy else ''}...")
        
        session = requests.Session()
        if proxy:
            session.proxies = {'http': proxy, 'https': proxy}
        
        response = session.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        print("✅ Token API call successful!")
        
        if isinstance(data, list) and len(data) > 0:
            token_data = data[0]
            print(f"\n🎯 ACTIVE TOKEN FOUND:")
            print("=" * 50)
            print(f"Access Token: {token_data.get('crm_accesstoken', 'N/A')}")
            print(f"Refresh Token: {token_data.get('crm_refreshtoken', 'N/A')}")
            print(f"Status: {token_data.get('status', 'N/A')}")
            print(f"App ID: {token_data.get('app_id', 'N/A')}")
            
            # Save token to file for later use
            with open('token.json', 'w') as f:
                json.dump(token_data, f, indent=2)
            print(f"\n💾 Token saved to 'token.json'")
            
            return token_data
        else:
            print("❌ No active tokens found in response")
            return None
            
    except Exception as e:
        print(f"❌ Request failed: {e}")
        return None

def test_all_proxies():
    """Test all proxies against the token API"""
    print("🚀 Testing UAE Proxies Against Token API...")
    print("=" * 60)
    
    # Test all proxies
    with ThreadPoolExecutor(max_workers=5) as executor:
        results = list(executor.map(test_proxy_with_token, UAE_PROXIES))
    
    # Display results
    working_count = 0
    uae_working = 0
    working_proxies = []
    
    print("\n📊 PROXY TEST RESULTS FOR TOKEN API:")
    print("-" * 60)
    
    for result in results:
        print(f"{result['status']} | {result['proxy']:30} | {result['country']:15} | ", end="")
        
        if result['status'] == '✅ WORKING':
            working_count += 1
            working_proxies.append(result['proxy'])
            if 'UAE' in result['country']:
                uae_working += 1
            print(f"Time: {result['response_time']} | Token: {result['token_preview']}")
        elif result['status'] == '⚠️  NO TOKEN':
            print(f"Time: {result['response_time']} | No active tokens")
        else:
            print(f"Error: {result.get('error', 'Unknown')[:30]}...")
    
    print("=" * 60)
    print(f"🎯 SUMMARY: {working_count}/{len(UAE_PROXIES)} proxies working")
    print(f"🇦🇪 UAE Proxies Working: {uae_working}")
    
    return working_proxies

def main():
    print("🚀 German Experts Token Fetcher with Proxy Testing")
    print("=" * 50)
    
    # First test all proxies
    working_proxies = test_all_proxies()
    
    if working_proxies:
        print(f"\n🎁 WORKING PROXIES:")
        for i, proxy in enumerate(working_proxies, 1):
            print(f"  {i}. {proxy}")
        
        # Ask user which proxy to use
        try:
            choice = input(f"\n🔢 Choose proxy (1-{len(working_proxies)}) or Enter for direct: ").strip()
            if choice and choice.isdigit():
                proxy_index = int(choice) - 1
                if 0 <= proxy_index < len(working_proxies):
                    selected_proxy = working_proxies[proxy_index]
                    print(f"🎯 Using proxy: {selected_proxy}")
                else:
                    selected_proxy = None
                    print("🎯 Using direct connection")
            else:
                selected_proxy = None
                print("🎯 Using direct connection")
        except:
            selected_proxy = None
            print("🎯 Using direct connection")
    else:
        selected_proxy = None
        print("🎯 No working proxies found, using direct connection")
    
    # Get token with selected proxy
    print("\n" + "=" * 50)
    token_data = get_access_token(selected_proxy)
    
    if token_data:
        access_token = token_data.get('crm_accesstoken')
        print(f"\n🎉 Ready to use token:")
        print(f"   {access_token[:50]}...")
        
        # Save working proxies for future use
        if working_proxies:
            with open('working_proxies.json', 'w') as f:
                json.dump(working_proxies, f, indent=2)
            print(f"💾 Working proxies saved to 'working_proxies.json'")
            
    else:
        print("\n💥 Failed to get access token")

if __name__ == "__main__":
    main()